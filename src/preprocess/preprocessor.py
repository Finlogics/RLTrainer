import json
import pandas as pd
from datetime import datetime, timedelta
from pathlib import Path


class Preprocessor:
    """Preprocesses raw CFD data by filling missing timestamps and formatting output."""

    # LifeCycle ----------------------------------------------------------------

    def __init__(self):
        """Load symbol configurations from symbols.json."""
        config_path = Path(__file__).parent.parent.parent / "configs" / "symbols.json"
        with open(config_path, "r") as f:
            self.symbols = json.load(f)
        self.raw_data_dir = Path(__file__).parent.parent.parent / "raw-data"
        self.processed_data_dir = Path(__file__).parent.parent.parent / "processed-data"
        self.processed_data_dir.mkdir(exist_ok=True)

    # Business Logic -----------------------------------------------------------

    def process_all_symbols(self):
        """Process all symbols defined in symbols.json."""
        for symbol_config in self.symbols:
            print(f"Processing {symbol_config['symbol']}...")
            self.process_symbol(symbol_config)

    def process_symbol(self, symbol_config: dict):
        """Process a single symbol's raw data."""
        df = self._load_raw_data(symbol_config)
        self._validate_data(df, symbol_config)
        df = self._fill_missing_data(df, symbol_config)
        df = self._split_time_column(df)
        first_date = df['Date'].iloc[0].replace('-', '')
        last_date = df['Date'].iloc[-1].replace('-', '')
        self._save_processed_data(df, symbol_config['symbol'], first_date, last_date)

    def _validate_data(self, df: pd.DataFrame, symbol_config: dict):
        """Validate that all data is within allowed TOD range."""
        df['Time'] = pd.to_datetime(df['Time']).dt.tz_localize(None)
        start_time = pd.to_datetime(symbol_config['data_start_time'], format='%H:%M').time()
        end_time = pd.to_datetime(symbol_config['data_end_time'], format='%H:%M').time()
        invalid_tod = df[~df['Time'].dt.time.between(start_time, end_time)]
        if not invalid_tod.empty:
            raise ValueError(f"Data found outside TOD range {symbol_config['data_start_time']}-{symbol_config['data_end_time']}: {invalid_tod['Time'].iloc[0]}")

    def _fill_missing_data(self, df: pd.DataFrame, symbol_config: dict) -> pd.DataFrame:
        """Fill missing minute-level timestamps according to intraday and cross-day rules."""
        df = df.copy()
        df['Time'] = pd.to_datetime(df['Time']).dt.tz_localize(None)
        df = df.sort_values('Time').reset_index(drop=True)
        start_time = pd.to_datetime(symbol_config['data_start_time'], format='%H:%M').time()
        end_time = pd.to_datetime(symbol_config['data_end_time'], format='%H:%M').time()
        valid_dates = df['Time'].dt.date.unique()
        full_range = []
        for date in valid_dates:
            current_datetime = datetime.combine(date, start_time)
            end_datetime = datetime.combine(date, end_time)
            while current_datetime <= end_datetime:
                full_range.append(current_datetime)
                current_datetime += timedelta(minutes=1)
        full_df = pd.DataFrame({'Time': full_range})
        merged = full_df.merge(df, on='Time', how='left')
        price_cols = ['OpenBid', 'OpenAsk', 'HighBid', 'HighAsk', 'LowBid', 'LowAsk', 'CloseBid', 'CloseAsk']
        for i in range(len(merged)):
            if pd.isna(merged.loc[i, 'CloseBid']):
                prev_idx = i - 1
                while prev_idx >= 0 and pd.isna(merged.loc[prev_idx, 'CloseBid']):
                    prev_idx -= 1
                if prev_idx >= 0:
                    close_bid = merged.loc[prev_idx, 'CloseBid']
                    close_ask = merged.loc[prev_idx, 'CloseAsk']
                    for col in price_cols:
                        if 'Bid' in col:
                            merged.loc[i, col] = close_bid
                        else:
                            merged.loc[i, col] = close_ask
        return merged

    # IO -----------------------------------------------------------------------

    def _load_raw_data(self, symbol_config: dict) -> pd.DataFrame:
        """Load raw CSV data for a symbol."""
        filepath = self.raw_data_dir / symbol_config['raw_file']
        return pd.read_csv(filepath)

    def _split_time_column(self, df: pd.DataFrame) -> pd.DataFrame:
        """Split Time column into Date (YYYY-MM-DD) and TOD (HH:MM)."""
        df = df.copy()
        df['Date'] = df['Time'].dt.strftime('%Y-%m-%d')
        df['TOD'] = df['Time'].dt.strftime('%H:%M')
        df = df[['Date', 'TOD', 'OpenBid', 'OpenAsk', 'HighBid', 'HighAsk', 'LowBid', 'LowAsk', 'CloseBid', 'CloseAsk']]
        return df

    def _save_processed_data(self, df: pd.DataFrame, symbol: str, first_date: str, last_date: str):
        """Save processed data to CSV file."""
        filename = f"{symbol}-M1-{first_date}-{last_date}-processed.csv"
        filepath = self.processed_data_dir / filename
        df.to_csv(filepath, index=False)
        print(f"Saved {len(df)} rows to {filename}")
