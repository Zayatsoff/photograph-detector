import os
import random
import shutil
import rawpy
from PIL import Image


def random_image_convert(path, destination_path):
    # Create a list of all the .ARW files in the folder
    arw_files = [f for f in os.listdir(path) if f.endswith(".ARW")]

    # Select 20 random .ARW files from the list
    selected_files = random.sample(arw_files, 20)

    # Loop through the selected files
    for file in selected_files:
        # Open the .ARW file using rawpy
        with rawpy.imread(path + "/" + file) as raw:
            # Convert the raw image to a RGB image
            rgb_image = raw.postprocess()
        # Convert the RGB image to a PIL image
        pil_image = Image.fromarray(rgb_image)
        # Save the image as a JPEG to the destination folder
        pil_image.save(destination_path + "/" + file[:-4] + ".JPEG", "JPEG")

    print("\nImages converted!")
