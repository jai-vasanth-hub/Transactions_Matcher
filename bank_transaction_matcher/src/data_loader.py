import pandas as pd
import os

def load_master_data(file_path):
    """
    Load master data CSV/Excel with columns: OwnerName, PlotNumber
    """
    if file_path.endswith('.csv'):
        df = pd.read_csv(file_path)
    elif file_path.endswith(('.xlsx', '.xls')):
        df = pd.read_excel(file_path)
    else:
        raise ValueError("Unsupported file format. Use CSV or Excel.")
    
    # Normalize columns
    df.columns = df.columns.str.strip().str.lower()
    if 'ownername' not in df.columns or 'plotnumber' not in df.columns:
        raise ValueError("Master data must have 'OwnerName' and 'PlotNumber' columns.")
    
    # Normalize data
    df['ownername'] = df['ownername'].astype(str).str.upper().str.strip()
    df['plotnumber'] = df['plotnumber'].astype(str).str.strip()
    
    return df

def load_bank_statement(file_path):
    """
    Load bank statement CSV/Excel with transaction descriptions.
    First tries to read with header and find 'transactiondescription' column.
    If not found, reads without header and uses the second column.
    """
    if file_path.endswith('.csv'):
        # Try with header
        df = pd.read_csv(file_path, header=0)
        df.columns = df.columns.str.strip().str.lower()
        if 'transactiondescription' in df.columns:
            df['transactiondescription'] = df['transactiondescription'].astype(str)
        else:
            # Read without header, use second column
            df = pd.read_csv(file_path, header=None)
            if df.shape[1] >= 2:
                df['transactiondescription'] = df.iloc[:, 1].astype(str)
            else:
                df['transactiondescription'] = df.iloc[:, 0].astype(str)
    
    elif file_path.endswith(('.xlsx', '.xls')):
        # Try with header
        df = pd.read_excel(file_path)
        df.columns = df.columns.str.strip().str.lower()
        if 'transactiondescription' in df.columns:
            df['transactiondescription'] = df['transactiondescription'].astype(str)
        else:
            # Read without header, use second column
            df = pd.read_excel(file_path, header=None)
            if df.shape[1] >= 2:
                df['transactiondescription'] = df.iloc[:, 1].astype(str)
            else:
                df['transactiondescription'] = df.iloc[:, 0].astype(str)
    
    else:
        raise ValueError("Unsupported file format. Use CSV or Excel.")
    
    # Filter out invalid descriptions
    df = df[df['transactiondescription'].notna() & (df['transactiondescription'] != '') & (df['transactiondescription'].str.lower() != 'nan')]
    
    return df