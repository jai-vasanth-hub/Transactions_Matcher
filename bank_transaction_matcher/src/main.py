import argparse
import os
from .data_loader import load_master_data, load_bank_statement
from .matcher import match_transactions
import pandas as pd

def main():
    parser = argparse.ArgumentParser(description='Match bank transactions to plot owners.')
    parser.add_argument('--master', required=True, help='Path to master data CSV/Excel')
    parser.add_argument('--bank', required=True, help='Path to bank statement CSV/Excel')
    parser.add_argument('--output', default='matched_results.csv', help='Output file path')
    parser.add_argument('--threshold', type=int, default=80, help='Fuzzy match threshold (0-100)')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.master):
        print(f"Master file {args.master} not found.")
        return
    if not os.path.exists(args.bank):
        print(f"Bank file {args.bank} not found.")
        return
    
    try:
        master_df = load_master_data(args.master)
        bank_df = load_bank_statement(args.bank)
        
        results_df = match_transactions(master_df, bank_df, args.threshold)
        
        results_df.to_csv(args.output, index=False)
        print(f"Results saved to {args.output}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    main()