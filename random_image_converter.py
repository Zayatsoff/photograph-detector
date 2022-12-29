import os
import random
import shutil
import rawpy
from PIL import Image
import cv2


def random_image_convert(path, destination_path):
    # Create a list of all the .ARW and .JPG files in the folder
    img_files = [
        f
        for f in os.listdir(path)
        if f.endswith(".ARW") or f.endswith(".JPG") or f.endswith(".JPEG")
    ]

    # Select 20 random .ARW and .JPG files from the list
    selected_files = random.sample(img_files, 20)

    # Loop through the selected files
    for file in selected_files:
        if file.endswith(".ARW"):
            # Open the .ARW file using rawpy
            with rawpy.imread(path + "/" + file) as raw:
                # Convert the raw image to a RGB image
                rgb_image = raw.postprocess()
        elif file.endswith(".JPG"):
            # Open the .JPG file using cv2
            rgb_image = cv2.imread(path + "/" + file)
            # Convert the image from BGR to RGB
            rgb_image = cv2.cvtColor(rgb_image, cv2.COLOR_BGR2RGB)
        else:
            rgb_image = cv2.imread(path + "/" + file)

        # Convert the RGB image to a PIL image
        pil_image = Image.fromarray(rgb_image)
        # Save the image as a JPEG to the destination folder
        pil_image.save(destination_path + "/" + file[:-4] + ".JPEG", "JPEG")

    print("\nImages converted!")
