import pandas as pd
import os

probs_dir = f"D:/IFCB/data/test/probs-to-read"
evals_dir = f"D:/IFCB/data/test/evals-to-read"

# Create dictionaries to hold DataFrames
probs_dfs = {}
evals_dfs = {}

# Function to read CSV files and store them in a dictionary
def get_dataframes(directory, dataframes_dict, suffix, header = None):
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename.endswith(suffix):
                key = filename[:-len(suffix)]  # Remove suffix to create key
                filepath = os.path.join(root, filename)
                df = pd.read_csv(filepath, header=header)  # Read CSV into DataFrame
                dataframes_dict[key] = df  # Store DataFrame with key

# Read DataFrames from both directories
get_dataframes(probs_dir, probs_dfs, '.prob.csv', header = 0)
get_dataframes(evals_dir, evals_dfs, '.select.csv', header = None)

for key in probs_dfs.keys():
    if key in evals_dfs:

        probs = probs_dfs[key]
        evals = evals_dfs[key]

        evals.columns = ['roi', 'prediction']
        evals = evals.sort_values(by = "roi")

        for index, row in evals.iterrows():
            roi = row['roi']
            prediction = row['prediction']
            
            if prediction in probs.columns:
                probs.loc[probs['roi'] == roi, prediction] = 1
            else:
                probs.loc[probs['roi'] == roi, probs.columns[1:]] = 0
        
        outdir = f"D:/IFCB/data/test"
        output_filepath = os.path.join(outdir, f"{key}.prob.csv")

        probs.to_csv(output_filepath, index=False, float_format='%.6f')