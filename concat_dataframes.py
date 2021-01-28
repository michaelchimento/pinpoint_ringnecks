from os.path import join, isdir
import fileinput
import sys
import re
import pandas as pd
from os import listdir

directory_path = "/home/michael/pinpoint_ringnecks/data"
new_directory_path = "/home/michael/pinpoint_ringnecks/coallated_data"

target_pops = ["P1","P2","P3","P4"]

types = ["Social","Feeder"]

folder_list = [join(directory_path,f) for f in listdir(directory_path) if "readme" not in f]
print(folder_list)

for camera_type in types:
    for target_pop in target_pops:
        print(camera_type + target_pop)
        
        df_list = [pd.read_csv(join(folder,f)) for folder in folder_list for f in listdir(folder) if re.search("P\d+", f).group(0)==target_pop and camera_type in folder]
        
        if len(df_list) > 0:
            df_concat = pd.concat(df_list)
            df_concat = df_concat.drop_duplicates(subset = ["population","time","id"],keep='first')
            df_concat.to_csv(join(new_directory_path,"{}_{}_full.csv".format(target_pop, camera_type)), index = False)
