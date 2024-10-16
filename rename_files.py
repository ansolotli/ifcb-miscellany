import os

path_to_folder = f"D:/IFCB/data/2018_data/feat-2018"

for files in os.listdir(path_to_folder):
    os.rename(os.path.join(path_to_folder, files), os.path.join(path_to_folder, files.replace('.feat', '_IFCB114.feat')))