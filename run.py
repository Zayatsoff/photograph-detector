from random_image_converter import random_image_convert
from mtcnn_face_extraction import face_extraction
from variance_of_laplacian import blur_detection

import shutil
import torch
import os


## --- Paths ---
# Set the path to the folder containing the .ARW files
path_ARW = r"D:/Petr/OG"
# Set the destination path for the JPEG files
new_path = r"D:/Petr/2.0"
# Set the destination path for the images
extracted_path = r"D:/Petr/2.0/extracted_faces"

## --- Misc ---
# Determine if an nvidia GPU is available
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
# Define threshhold of blurriness
thresh = 10.00
# Define a dictionary with the directory names and range of blurriness values for each rating
ratings = {
    "1 Star": (0.0, 0.20),
    "2 Stars": (0.21, 0.40),
    "3 Stars": (0.41, 0.60),
    "4 Stars": (0.61, 0.80),
    "5 Stars": (0.81, 1.00),
}


## --- Functions ---
# Converts 20 random images from .ARW to .JPEG
# random_image_convert(path_ARW, new_path)


# Get images
images = [f for f in os.listdir(new_path) if f.endswith(".JPEG")]

for i, image in enumerate(images):
    # Extract all the faces from each image
    total_faces, pil_faces = face_extraction(new_path, image, device)
    # Detect all the blurred faces
    count = blur_detection(pil_faces, thresh)

    blurriness = 0 if total_faces == 0 else count / total_faces
    print(f"\nBlurriness: {blurriness}\n")

    # Loop through the ratings dictionary
    for rating, (min_val, max_val) in ratings.items():
        # Check if the blurriness value falls within the range for the current rating
        if min_val <= blurriness <= max_val:
            # Check if the directory for the current rating already exists
            if not os.path.exists(extracted_path + f"/{rating}"):
                # Create the directory for the rating
                os.mkdir(extracted_path + f"/{rating}")
            # Copy the image to the directory
            shutil.copyfile(
                new_path + "/" + image, extracted_path + f"/{rating}/" + image
            )
            # Break the loop once the image has been copied to the appropriate directory
            break

    # Raise an error if the blurriness value is outside the valid range
    # if blurriness < 0 or blurriness > 1:
    #     raise ValueError
