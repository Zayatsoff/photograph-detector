import os
from imutils import paths
import numpy as np
import cv2


def blur_detection(pil_faces, thresh=10.00):
    faces = pil_faces
    face_count = 0

    # Loop over the input faces
    for face in faces:
        # Load the image, convert to grayscale, and compute the focus measure of the image using the Variance of Laplacian method
        image = face
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        fm = variance_of_laplacian(gray)
        # If the focus measure is less than the supplied threshold, then the image should be considered "blurry" and is added to the count
        if fm >= thresh:
            face_count += 1

    # print("\nBlurriness calculated!")
    return face_count


def variance_of_laplacian(image):
    # Compute the Laplacian of the image and then return the focus measure, which is simply the variance of the Laplacian
    return cv2.Laplacian(image, cv2.CV_64F).var()
