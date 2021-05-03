from os.path import join
import fileinput
import sys
import re
import os
from datetime import date, timedelta
from os.path import isfile, isdir, join, splitext, ismount
import subprocess

def terminal(command):
    try:
        term_output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
    except subprocess.CalledProcessError as e:
        #uncomment line below for more detailed debugging
        #print("{}: {}".format(e.cmd,e.output.decode()))
        raise e
    else:
        return term_output.decode()


server_path = "/mnt/ringnecks/winter_2021/"

if __name__=="__main__":
    
    today = date.today()
    print("today is {}".format(today))

    parent_directories = [join(server_path, d) for d in os.listdir(server_path) if isdir(join(server_path, d)) and re.search("P\d+", d).group(0)!="P3"]
    parent_directories = sorted(parent_directories, key=str.lower, reverse=False)
    print(parent_directories)
    for directory in parent_directories:
        #these child directories are filled with photos from 5 min intervals
        child_directories = [join(server_path, directory, child) for child in os.listdir(directory)]
        child_directories = sorted(child_directories, key=str.lower, reverse=False)

        for folder in child_directories:
            print(folder)
            rawtime = re.search("\d\d\d\d-\d\d-\d\d", folder).group(0)
            folder_date = date.fromisoformat(rawtime)
            if folder_date <= (today+timedelta(days=-1)):
                try:
                    command = "rm -rf {}".format(folder)                            
                    response = terminal(command)
                    print(response)
                except Exception as e:
                    print("problem deleting folder: {}".format(e))
                else:
                    print("folder deleted")


