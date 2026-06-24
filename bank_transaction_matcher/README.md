# Bank Transaction Matcher

A safe, offline application to match bank transactions with plot owners using a master dataset.

## Features

- Loads master data (OwnerName, PlotNumber) and bank statements (TransactionDescription)
- Normalizes and cleans text
- Extracts potential names and plot numbers from transaction descriptions
- Matches using exact and fuzzy string matching
- Assigns confidence levels (High/Medium/Low)
- Flags unmatched or ambiguous transactions
- Exports results to CSV/Excel

## Installation

1. Install Python 3.8+
2. Install dependencies: `pip install -r requirements.txt`
3. Run the application locally: `streamlit run bank_transaction_matcher/app.py`
4. For Streamlit Cloud, the repository root entry point is `streamlit_app.py`

## Usage

- Place master_data.csv and bank_statement.csv in the data/ folder
- Run the app and select files or use CLI

## Architecture

- `src/data_loader.py`: Loads CSV/Excel files
- `src/text_processor.py`: Text normalization and extraction
- `src/matcher.py`: Matching logic
- `src/main.py`: CLI entry point
- `app.py`: Streamlit UI