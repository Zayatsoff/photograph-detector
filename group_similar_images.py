import csv
import os

# Create a dictionary to store the groups
groups = {}

# Open the CSV file
with open('/Users/liorrozin/Documents/GitHub/photograph-detector/fd/similarity.csv', 'r') as f:
    reader = csv.DictReader(f)

    # Iterate over the rows in the CSV file
    for row in reader:
        # Get the file paths and distance
        img1 = row['from']
        img2 = row['to']
        distance = float(row['distance'])

        # Check if the distance is above 0.85
        if distance >= 0.82:
            # Check if the files are already in a group
            group_name1 = None
            group_name2 = None
            for g in groups:
                if img1 in groups[g]['files']:
                    group_name1 = g
                if img2 in groups[g]['files']:
                    group_name2 = g

            # If the files are not already in a group, add the new group to the dictionary
            if group_name1 is None and group_name2 is None:
                folder_name = os.path.commonprefix([img1, img2])
                groups[folder_name] = {'files': [img1, img2]}
            # If one of the files is already in a group, add the other file to that group
            elif group_name1 is not None:
                groups[group_name1]['files'].append(img2)
            elif group_name2 is not None:
                groups[group_name2]['files'].append(img1)
            

# Move the files to the corresponding folders
    for group_name in groups:
        if not os.path.exists(group_name):
            os.makedirs(group_name)
        for img in groups[group_name]['files']:
            if os.path.exists(img):
                if not os.path.isfile(os.path.join(group_name, os.path.basename(img))):
                    try:
                        os.rename(img, os.path.join(group_name, os.path.basename(img)))
                    except:
                        print(f'Error moving {img} to {group_name}')

print(f'Number of groups created: {len(groups)}')
print(f'Number of files moved to folders: {sum([len(g["files"]) for g in groups.values()])}')
