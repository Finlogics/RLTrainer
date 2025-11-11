# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

RLTrainer is a Reinforcement Learning training framework. The repository is currently in its initial setup phase.

## Project Structure

This is a Python-based project as indicated by the .gitignore file which includes Python-specific patterns for:
- Virtual environments (.venv, venv/)
- Python bytecode (__pycache__, *.pyc)
- Package distribution (dist/, *.egg-info/)
- Testing artifacts (.pytest_cache/, .coverage)

## Development Setup

Project structure and commands to be documented as the codebase develops.
- Always write minimal code that does the job. do not excessively put if statements or check edge cases. your docstring for methods and classes should not exceed 1 line. do not use chopping format to break method calls and definitions to multiple line. do not use module methods unless necessary. prefer to use classes and OO paradigm when appropriate.
if you have questions about an issue, ask me to clarify. do not make big assumptions.
for each class, methods are ordered in sections. sections are separated by hyphen comment lines. order is: LifeCycle, Business Logic, IO, Misc.
method parameters should have type: eg. def unnormalize_value(self, ticker: str, granularity: str, values: list[dict]) -> float:
- Always write minimal code that does the job. do not excessively put if statements or check edge cases. your docstring for methods and classes should not exceed 1 line. do not 
use chopping format to break method calls and definitions to multiple line. do not use module methods unless necessary. prefer to use classes and OO paradigm when appropriate.
if you have questions about an issue, ask me to clarify. do not make big assumptions.
for each class, methods are ordered in sections. sections are separated by hyphen comment lines. order is: LifeCycle, Business Logic, IO, Misc.
method parameters should have type: eg. def unnormalize_value(self, ticker: str, granularity: str, values: list[dict]) -> float:
- this project trains DRL algorithms that will trade in stock markets. it is preferred to use FinRL available from https://github.com/AI4Finance-Foundation/FinRL if the requested functionality is there.
- we have gathered many examples from various repos related to finrl in finrl-examples folder. these can be used as examples to gather insight on how to use finRL.
- temporary codes for diagnostics and other one-off matters should be created in ad-hoc folder.