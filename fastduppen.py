import fastdup
import os
import time 

folder_path = "./fastdup_files"
if not os.path.exists(folder_path):
            os.makedirs(folder_path)

# fastdup.run("/Users/liorrozin/Desktop/2.0",folder_path,turi_param='nnmodel=0,ccthreshold=0.85',threshold=0.70)
# # time.sleep(2)

for file_name in os.listdir(folder_path):
    if file_name != 'atrain_stats.csv' and file_name != 'tmp' and file_name != "connected_components.csv":
        file_path = os.path.join(folder_path, file_name)
        os.remove(file_path)
       

print("DONE")