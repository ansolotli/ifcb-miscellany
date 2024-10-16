import os
import pandas as pd

directoryPath = f"D:/IFCB/data/finnmaid/unzipped/feats-old-conversion-factor"

for path, subdirs, files in os.walk(directoryPath):
    for fn in files:
        f = open(os.path.join(path, fn), "r")

        commentlines = [f.readline() for x in range(2)]
        volume = [value.strip().split('=') for value in commentlines][1][1]

        df = pd.read_csv(f, sep = ",", header = 0)
        df["biovolume_um3"] = df["biovolume_px"] / 2.8**3
        df["biomass_ugl"] = df["biovolume_um3"] / float(volume) / 1000
        df = df.astype({"roi": str})

        #format csv file with commented lines
        csv_content = f"# version={[value.strip().split('=') for value in commentlines][0][1]}\n"
        csv_content += f"# volume_ml={volume}\n"
        csv_content += (
        "roi,biovolume_px,biovolume_um3,biomass_ugl,"
        "area,major_axis_length,minor_axis_length\n"
        )
        for index, row in df.iterrows():
            csv_content += ",".join(map(str, row)) + "\n"

        outdir = f"D:/IFCB/data/finnmaid/unzipped/feats"

        with open(os.path.join(outdir, fn), "w") as fh:
            fh.write(csv_content)

print("Done!")