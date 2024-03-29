import os
import csv

def sim_groups(new_path,folder_path="./fastdup_files"):
    new_path
    # Open the connected_components.csv file
    with open(os.path.join(folder_path,'connected_components.csv'), 'r') as cc_file:
        cc_reader = csv.DictReader(cc_file)
        folder_count = 0
        for row in cc_reader:
            component_id = row['component_id']
            component_index = int(row['__id'])
            
            # Create a folder with the component_id name
            if not os.path.exists(os.path.join(new_path,component_id)):
                os.makedirs(os.path.join(new_path,component_id))
                folder_count += 1
            
            # Open the atrain_stats.csv file
            with open(os.path.join(folder_path,'atrain_stats.csv'), 'r') as ts_file:
                ts_reader = csv.DictReader(ts_file)
                for ts_row in ts_reader:
                    if int(ts_row['index']) == component_index:
                        file_path = ts_row['filename']
                        try:
                            # Move the file to the component_id folder
                            os.rename(file_path, os.path.join(os.path.join(new_path,component_id), os.path.basename(file_path)))
                        except:
                            print(f'Error moving {file_path} to {os.path.join(new_path,component_id)}')
        print(f"\nCreated {folder_count} folders based on similarity!")
