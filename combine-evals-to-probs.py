import pandas as pd

probs_path = "D:/Users/E1005556/Downloads/D20210430T091157_IFCB114.prob.csv"

probs = pd.read_csv(probs_path)
evals = pd.read_csv('D:/Users/E1005556/Downloads/D20210430T091157_IFCB114.select.csv', header = None)
evals.columns = ['roi', 'prediction']
evals = evals.sort_values(by = "roi")

for index, row in evals.iterrows():
    roi = row['roi']
    prediction = row['prediction']
    
    if prediction in probs.columns:
        probs.loc[probs['roi'] == roi, prediction] = 1
    else:
        probs.loc[probs['roi'] == roi, probs.columns[1:]] = 0

probs.to_csv("D:/IFCB/data/test/D20210430T091157_IFCB114.prob.csv", index=False, float_format='%.6f')