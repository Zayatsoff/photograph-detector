import fastdup
import os
import time 

def fastdup_analyze(new_path,folder_path="./fastdup_files"):
    path = folder_path
    if not os.path.exists(folder_path):
                os.makedirs(folder_path)

    fastdup.run(new_path,folder_path,turi_param='nnmodel=0,ccthreshold=0.85',threshold=0.70)

    for file_name in os.listdir(folder_path):
        if file_name != 'atrain_stats.csv' and file_name != 'tmp' and file_name != "connected_components.csv":
            file_path = os.path.join(folder_path, file_name)
            os.remove(file_path)
    print("\nFastDup Analysis complete!")
        
