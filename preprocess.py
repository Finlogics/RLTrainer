from src.preprocess import Preprocessor

if __name__ == "__main__":
    preprocessor = Preprocessor()
    preprocessor.process_all_symbols()
    print("Preprocessing completed successfully!")
