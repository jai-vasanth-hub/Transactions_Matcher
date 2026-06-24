import re
from rapidfuzz import fuzz

def normalize_text(text):
    """
    Normalize text: uppercase, remove extra spaces, keep alphanumeric and spaces.
    """
    text = text.upper()
    text = re.sub(r'[^A-Z0-9\s]', '', text)  # Remove non-alphanumeric except spaces
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def extract_candidates(description):
    """
    Extract potential owner names and plot numbers from transaction description.
    Returns dict with 'names': list of possible names, 'numbers': list of possible plot numbers, 'usv_numbers': prioritized plot numbers from USV pattern
    """
    normalized = normalize_text(description)
    words = normalized.split()
    
    names = []
    numbers = []
    usv_numbers = []
    
    for word in words:
        if word.isdigit():
            # Assume numbers 1-999 are plot numbers
            if 1 <= int(word) <= 999:
                numbers.append(word)
        elif len(word) > 2 and word.isalpha():
            # Potential names: alphabetic words longer than 2 chars
            names.append(word)
    
    # Also, look for patterns like MAINTENANCE FOR 51
    match = re.search(r'MAINTENANCE\s+FOR\s+(\d+)', normalized)
    if match:
        numbers.append(match.group(1))
    
    # New rule: USV followed by digits, then month
    months = 'JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOV|DEC'
    usv_match = re.search(r'USV(\d+)(' + months + r')', normalized)
    if usv_match:
        plot_num = usv_match.group(1)
        usv_numbers.append(plot_num)
        numbers.append(plot_num)  # Also add to general numbers
    
    return {'names': names, 'numbers': numbers, 'usv_numbers': usv_numbers}

def fuzzy_match(candidate, master_list, threshold=80):
    """
    Fuzzy match candidate against master list.
    Returns best match and score if above threshold, else None
    """
    best_match = None
    best_score = 0
    for item in master_list:
        score = fuzz.ratio(candidate, item)
        if score > best_score:
            best_score = score
            best_match = item
    if best_score >= threshold:
        return best_match, best_score
    return None, 0

def stepwise_name_match(candidate, master_list):
    """
    Check if any master name is a substring of the candidate.
    Returns the matching master name and score 100.
    """
    for master in master_list:
        if master in candidate:
            return master, 100
    return None, 0