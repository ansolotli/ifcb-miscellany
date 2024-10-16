from pathlib import Path
import pandas as pd
import os

# root directory of IFCB raw data
root = "D:/IFCB/data/2024-data/raw/summer/"
maintenance_log = "D:/IFCB/data/maintenance_log_combined.csv"
log = [] 

ifcbFlowrate = 0.25
sampleRuntime = 0.0
sample_ml_analyzed = 0 
sampleRuntype = ""
sampleADCFileFormat = []

TH_runTime = 800 #[seconds]
TH_images2triggers_low = 0.6 #[images/trigger]
TH_images2triggers_high = 1.1
TH_roiSize = 1e8

roiPaths = (roi for roi in Path(root).glob("**/*.roi"))

def load_hdr_data(hdr_file):
    with open(hdr_file) as fh:
        for line in fh:
            if line.startswith("runTime"):
                global sampleRuntime
                sampleRuntime= float(line.split()[1])
            elif line.startswith("inhibitTime"):
                sampleInhibitTime = float(line.split()[1])
            elif line.startswith("runType"):
                global sampleRuntype 
                sampleRuntype = line.split()[1]
            elif line.startswith("ADCFileFormat"):
                global sampleADCFileFormat 
                sampleADCFileFormat = line.strip().split(",")
        
    looktime = sampleRuntime - sampleInhibitTime
    global sample_ml_analyzed 
    sample_ml_analyzed= ifcbFlowrate * (looktime / 60.0)


def count_images(adc_file):
    df = pd.read_csv(adc_file, names = sampleADCFileFormat, sep = ",")
    adcLength = len(df)
    imageCount = (df[' ROIy'] != 0).sum()

    global images2triggers
    if adcLength:
        images2triggers = imageCount/adcLength
    else:
        images2triggers = 0


def maintenance_breaks():
    mb = pd.read_csv(maintenance_log, sep = ";", encoding = 'latin-1')
    mb["start"] = mb["start"].str.replace("-|:| ", "", regex=True)
    mb["end"] = mb["end"].str.replace("-|:| ", "", regex=True)
    return mb


def process_samples():

    breaks = maintenance_breaks()
    for path in roiPaths:

        head, tail = os.path.split(path)
        sampleName = tail.split("_")[0]
        sampleTime = sampleName[1:16]
        sampleTime = sampleTime.replace("T", "")
        
        flags = {"Sample": sampleName, "No data": 0, "ROI is too big": 0, "Volume is 0": 0, "Incomplete sample": 0, "Beads": 0, "Images2triggers": 0, "Maintenance": 0}

        adc = path.with_suffix(".adc")
        hdr = path.with_suffix(".hdr")

        load_hdr_data(hdr)
        count_images(adc)

        for index, row in breaks.iterrows():
            if row["start"] < sampleTime and row["end"] > sampleTime:
                flags["Maintenance"] = 1
                continue

        if path.stat().st_size == 0:
            flags["No data"] = 1
        if path.stat().st_size >= TH_roiSize: 
            flags["ROI is too big"] = 1
        if sample_ml_analyzed == 0:
            flags["Volume is 0"] = 1
        if sampleRuntype == "BEADS":
            flags["Beads"] = 1
        if sampleRuntime < TH_runTime:
            flags["Incomplete sample"] = 1
        if images2triggers < TH_images2triggers_low or images2triggers > TH_images2triggers_high:
            flags["Images2triggers"] = 1
    
        df = pd.Series(flags, dtype=object).to_frame()
        df_transposed = df.transpose()
        log.append(df_transposed)

process_samples()
final_df = pd.concat(log)
final_df.to_csv('D:/IFCB/data/qc-2024-summer-flag-data.csv', index=False)

flagged = final_df.apply(lambda row: (row == 1).any(), axis=1)
flagged_samples = final_df[flagged]
exclusion_list = flagged_samples.iloc[:, 0].to_list()

with open(r'D:/IFCB/data/sample-exclusion-list-2024-summer.txt', 'w') as fp:
    for item in exclusion_list:
        fp.write("%s\n" % item)

print("Done!")