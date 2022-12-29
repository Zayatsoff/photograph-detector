import os

from facenet_pytorch import MTCNN
import torch
import numpy as np
import cv2
from PIL import Image, ImageDraw


def face_extraction(path, destination_path, device):
    print("Running on device: {}".format(device))

    # Define MTCNN module
    mtcnn = MTCNN(keep_all=True, device=device)

    # Get a sample image
    images = [f for f in os.listdir(path) if f.endswith(".JPEG")]

    for i, im in enumerate(images):
        im = Image.open(path + im)
        # Detect faces
        boxes, probs = mtcnn.detect(im)

        # Make folder for images
        os.mkdir(destination_path + f"{i}")
        # Loop through each face and save it if the confidence percentage is above 90%
        for j, box in enumerate(boxes):
            # Get the confidence percentage for the detected face
            confidence = int(probs[j] * 100)

            # Extract the face only if the confidence is above 90%
            if confidence > 80:
                # Crop face from the original image
                face_im = im.crop(box.tolist())
                # Construct the full path for the image
                file_path = destination_path + f"{i}/face_{j}_{confidence/100}.jpg"

                # Save the face
                face_im.save(file_path)

    print("\nFaces extracted successfully!")
