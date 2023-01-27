import os

path = '/Users/liorrozin/Desktop/2.0' 


for root, dirs, files in os.walk(path):
    for dir in dirs:
        dir_path = os.path.join(root, dir)
        if os.listdir(dir_path): # check if directory is non-empty
            for file in os.listdir(dir_path):
                file_path = os.path.join(dir_path, file)
                os.rename(file_path, os.path.join(path, file)) # move files to root directory
        os.rmdir(dir_path) # remove the non-empty directory
