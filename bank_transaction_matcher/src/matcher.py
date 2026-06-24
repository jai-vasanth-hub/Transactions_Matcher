import pandas as pd
from .text_processor import extract_candidates

def match_transactions(master_df, bank_df, fuzzy_threshold=80):
    """
    Match bank transactions to master data.
    Only match if USV plot number is found and exists in master.
    Returns DataFrame with matched results.
    """
    results = []
    
    for idx, row in bank_df.iterrows():
        desc = row['transactiondescription']
        candidates = extract_candidates(desc)
        
        matched_owner = None
        matched_plot = None
        match_type = 'No Match'
        confidence = 'Low'
        score = None
        
        # Check for USV plot match
        if candidates['usv_numbers']:
            usv_plot = candidates['usv_numbers'][0]
            if usv_plot in master_df['plotnumber'].values:
                owner = master_df[master_df['plotnumber'] == usv_plot]['ownername'].iloc[0]
                matched_owner = owner
                matched_plot = usv_plot
                match_type = 'Exact'
                confidence = 'High'
                score = 100
        
        # If not matched, check for exact name match
        if not matched_owner:
            normalized_desc = desc.upper()
            for _, master_row in master_df.iterrows():
                master_name = master_row['ownername']
                if master_name in normalized_desc:
                    matched_owner = master_name
                    matched_plot = master_row['plotnumber']
                    match_type = 'Exact'
                    confidence = 'High'
                    score = 100
                    break
        
        results.append({
            'TransactionDescription': desc,
            'MatchedOwnerName': matched_owner,
            'MatchedPlotNumber': matched_plot,
            'MatchType': match_type,
            'ConfidenceScore': score
        })
    
    return pd.DataFrame(results)