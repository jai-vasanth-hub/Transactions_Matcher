import streamlit as st
import pandas as pd
from src.data_loader import load_master_data, load_bank_statement
from src.matcher import match_transactions
import os
__import__('pysqlite3')

import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

st.title("Bank Transaction Matcher")

st.sidebar.header("Upload Files")
master_file = st.sidebar.file_uploader("Master Data (CSV/Excel)", type=['csv', 'xlsx', 'xls'])
bank_file = st.sidebar.file_uploader("Bank Statement (CSV/Excel)", type=['csv', 'xlsx', 'xls'])
threshold = st.sidebar.slider("Fuzzy Match Threshold", 0, 100, 80)

if st.sidebar.button("Match Transactions"):
    if master_file and bank_file:
        try:
            # Save uploaded files temporarily
            master_path = f"temp_master.{master_file.name.split('.')[-1]}"
            bank_path = f"temp_bank.{bank_file.name.split('.')[-1]}"
            
            with open(master_path, 'wb') as f:
                f.write(master_file.getbuffer())
            with open(bank_path, 'wb') as f:
                f.write(bank_file.getbuffer())
            
            master_df = load_master_data(master_path)
            bank_df = load_bank_statement(bank_path)
            
            results_df = match_transactions(master_df, bank_df, threshold)
            
            st.success("Matching completed!")
            st.dataframe(results_df)
            
            # Download button
            csv = results_df.to_csv(index=False)
            st.download_button("Download Results as CSV", csv, "matched_results.csv", "text/csv")
            
            # Clean up
            os.remove(master_path)
            os.remove(bank_path)
            
        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.error("Please upload both files.")