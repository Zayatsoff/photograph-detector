import fastdup
import os
import time 

folder_path = "/Users/liorrozin/Documents/GitHub/photograph-detector/fd"

fastdup.run("/Users/liorrozin/Desktop/2.0",folder_path,threshold=0.70)
# time.sleep(2)
for file_name in os.listdir(folder_path):
    if file_name != 'similarity.csv' and file_name != 'tmp':
        file_path = os.path.join(folder_path, file_name)
        os.remove(file_path)
       

print("DONE")