import os
from imutils import paths
import numpy as np

# import argparse
import cv2


def blur_detection(pil_faces, thresh=10.00):
    # Convert PIL images into cv2 images

    faces = convert_pil_to_cv2(pil_faces)
    count = 0
    # print(f"P FACES: {faces}")
    # Loop over the input faces
    for face in faces:
        # Load the image, convert to grayscale, and compute the focus measure of the image using the Variance of Laplacian method

        image = face
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        fm = variance_of_laplacian(gray)
        # If the focus measure is less than the supplied threshold, then the image should be considered "blurry" and is added to the count
        if fm >= thresh:
            count += 1
            cv2.imwrite(f"D:/Petr/2.0/extracted_faces/why/test_{count}.jpg", image)
            # print(f"thresh: {fm} fld: {fld} name: {imagePath} count: {count}")

    print("\nBlurriness calculated!")
    return count


def convert_pil_to_cv2(faces):
    # Initialize an empty list to store the cv2 images
    cv2_images = []

    # Loop through each face in the faces array
    for face in faces:
        # Convert the face from BGR (PIL format) to RGB (cv2 format)
        face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)

        # Append the face to the cv2_images list
        cv2_images.append(face)

    # Return the list of cv2 images
    return cv2_images


def variance_of_laplacian(image):
    # Compute the Laplacian of the image and then return the focus measure, which is simply the variance of the Laplacian
    return cv2.Laplacian(image, cv2.CV_64F).var()
