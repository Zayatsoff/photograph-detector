import os
from imutils import paths

# import argparse
import cv2


def variance_of_laplacian(image):
    # compute the Laplacian of the image and then return the focus
    # measure, which is simply the variance of the Laplacian
    return cv2.Laplacian(image, cv2.CV_64F).var()


# Define threshhold
thresh = 10.00

# Set the destination path for the JPEG files
destination_path = r"D:/Petr/2.0/extracted_faces/"

# Create a list of all the .ARW files in the folder
folders = [f for f in os.listdir(destination_path)]

# Loop over folders
for i, fld in enumerate(folders):
    images = [f for f in os.listdir(destination_path + fld)]
    # loop over the input images
    count = 0
    for j, imagePath in enumerate(images):
        # load the image, convert it to grayscale, and compute the
        # focus measure of the image using the Variance of Laplacian
        # method
        image = cv2.imread(destination_path + f"{fld}" + "/" + imagePath)

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        fm = variance_of_laplacian(gray)
        # if the focus measure is less than the supplied threshold,
        # then the image should be considered "blurry"

        if fm >= thresh:
            count += 1
            print(f"thresh: {fm} fld: {fld} name: {imagePath} count: {count}")
    file_path = destination_path + f"{count}_{fld}"
    # Save the face
    os.rename(destination_path + f"{fld}", file_path)
