from barcode_tracker_photos_modified import *
from os.path import isfile, isdir, join, splitext, ismount
import re
from datetime import datetime
from os import rename, mkdir
import TagList
import time
from sys import argv
from shutil import rmtree


target_pop = argv[1]
server_path = "/mnt/ringnecks/summer_2021/"
data_dir_csv = "data/"
data_dir_video_frame = "video_frame_data/"
already_processed_filename = "already_processed/processed_photos_{}.txt".format(target_pop)

with open(already_processed_filename, "a+") as processed_file:
    processed_file.seek(0)
    already_processed = [line.strip() for line in processed_file]
    print("Already processed {}".format(len(already_processed)))

def create_csv(data_filepath):
    with open(data_filepath, "a+") as savefile: # open data file in append mode
        # write column names to file
        header = "population,room,camera_name,time,id,id_prob,x,y,orientation,area\n"
        savefile.write(header)

def create_csv_vframe(video_frame_filepath):
    with open(video_frame_filepath, "w") as savefile: # open data file in append mode
        # write column names to file
        header = "time,frame\n"
        savefile.write(header)

if __name__=="__main__":

    tags = TagList.TagList()
    tags.load("master_list_outdoor.pkl")

    parent_directories = [join(server_path, d) for d in os.listdir(server_path)
                            if (isdir(join(server_path, d)) and
                            re.search("P\d+", d).group(0)==target_pop) and
                            join(server_path,d) not in already_processed]
    parent_directories = sorted(parent_directories, key=str.lower, reverse=False)

    for directory in parent_directories:
        #make directory structure if not already done
        if not isdir(join(data_dir_csv,os.path.basename(directory))):
            mkdir(join(data_dir_csv,os.path.basename(directory)))
        if not isdir(join(data_dir_video_frame,os.path.basename(directory))):
            mkdir(join(data_dir_video_frame,os.path.basename(directory)))
        #rawtime = re.search("\d\d\d\d-\d\d-\d\d_\d\d", directory).group(0)
        population = re.search("P\d+", directory).group(0)
        room = re.search("B\d+|C\d+|D\d+", directory).group(0)
        camera_name = re.search("Social(\d+)?|Feeder(\d+)?", directory).group(0)
        #these child directories are filled with photos from 5 min intervals
        child_directories = [join(server_path, directory, child) for child in os.listdir(directory)
                                if (isdir(join(server_path, directory, child)) and
                                join(server_path,directory,child) not in already_processed)]
        child_directories = sorted(child_directories, key=str.lower, reverse=False)

        for folder in child_directories:
            if folder not in already_processed:
                print("now processing {}".format(folder))
                #create filepaths for pp data, the video conversion, and it's accompanying csv with frame and time information
                data_filepath = join(data_dir_csv,os.path.basename(directory),"{}_pinpoint.csv".format(os.path.basename(folder)))
                video_filepath = "{}.mp4".format(folder)
                video_frame_filepath = join(data_dir_video_frame,os.path.basename(directory),"{}.csv".format(os.path.basename(folder)))

                if not isfile(data_filepath):
                    create_csv(data_filepath)

                create_csv_vframe(video_frame_filepath)

                t0= time.time()

                #run pinpoint on the folder
                try:
                    decode(folder, data_filepath, video_filepath, video_frame_filepath, tags, population, room, camera_name)
                except Exception as e:
                    print("Error processing folder: {}".format(e))
                   
                else:
                    
                    #delete the folder
                    try:
                        rmtree(folder)
                    except OSError as e:
                        print("Error: %s : %s" % (folder, e.strerror))

                    #check how much time it took
                    t1= time.time()
                    print("Processing took {} seconds".format(t1-t0))

                    #add to already processed list
                    with open(already_processed_filename, "a+") as processed_file:
                        processed_file.write("{}\n".format(folder))

        print("finished processing {}".format(directory))
