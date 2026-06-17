import sys
import pandas as pd
import re

def validate(csv_path):
    try:
        df = pd.read_csv(csv_path)
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return False
        
    errors = []
    
    # Check headers
    expected_headers = ['candidate_id', 'rank', 'score', 'reasoning']
    if list(df.columns) != expected_headers:
        errors.append(f"Headers must be {expected_headers}, got {list(df.columns)}")
        
    # Check exactly 100 rows
    if len(df) != 100:
        errors.append(f"Expected exactly 100 rows, got {len(df)}")
        
    # Check ranks 1-100
    if not (df['rank'].values == list(range(1, 101))).all():
        errors.append("Ranks must be exactly 1 to 100 in order")
        
    # Check scores non-increasing
    scores = df['score'].values
    for i in range(len(scores) - 1):
        if scores[i] < scores[i+1]:
            errors.append(f"Scores must be non-increasing. Found violation at rank {i+1} and {i+2}")
            break
            
    # Check tie breaks
    for i in range(len(scores) - 1):
        if scores[i] == scores[i+1]:
            id1 = str(df.iloc[i]['candidate_id'])
            id2 = str(df.iloc[i+1]['candidate_id'])
            if id1 > id2:
                errors.append(f"Tie-break violation at rank {i+1} and {i+2}. {id1} should be after {id2}")
                break
                
    # Check ID format
    id_pattern = re.compile(r'^CAND_\d{7}$')
    for i, cid in enumerate(df['candidate_id']):
        if not id_pattern.match(str(cid)):
            errors.append(f"Invalid candidate_id format at row {i+1}: {cid}")
            break
            
    if errors:
        for e in errors:
            print(f"ERROR: {e}")
        return False
        
    print("Submission is valid.")
    return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python validate_submission.py <path_to_csv>")
        sys.exit(1)
        
    validate(sys.argv[1])
