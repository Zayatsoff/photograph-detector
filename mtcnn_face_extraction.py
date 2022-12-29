import os

from facenet_pytorch import MTCNN
import torch
import numpy as np
import cv2
from PIL import Image, ImageDraw


def face_extraction(path, image, device):
    print("Running on device: {}".format(device))

    # Define MTCNN module
    mtcnn = MTCNN(keep_all=True, device=device)

    # Define the desired width and height of the cropped faces
    face_width = 200
    face_height = 200
    # Create an empty 3-dimensional NumPy array with shape (0, height, width) and the default data type (float64)
    faces = np.empty((face_width, face_height, 0))
    num_faces = 0

    im = Image.open(path + f"/{image}")
    # Detect faces
    boxes, probs = mtcnn.detect(im)

    # Loop through each face and save it if the confidence percentage is above 90%
    for j, box in enumerate(boxes):
        # Get the confidence percentage for the detected face
        confidence = int(probs[j] * 100)
        num_faces += 1
        # Extract the face only if the confidence is above 90%
        if confidence > 80:
            # Crop face from the original image
            face_im = im.crop(
                (box[0], box[1], box[0] + face_width, box[1] + face_height)
            )

            # Convert the image to a numpy array
            face_np = np.array(face_im)
            face_np = face_np.reshape(
                face_np.shape[2], face_np.shape[0], face_np.shape[1]
            )
            # If the faces array is empty, create it using the shape and data type of the face_np array
            if faces.size == 0:
                faces = np.empty(
                    (face_np.shape[0], face_np.shape[1], face_np.shape[2]),
                    dtype=face_np.dtype,
                )

            # Stack the face numpy array vertically to the existing faces array using vstack()
            faces = np.vstack((faces, face_np))

    print(
        f"\nFaces extracted successfully!\n faces:{num_faces}"
    )  # \n faces: \n {faces} \n {total_faces}\n DONE \n
    # Return the list of detected faces
    return num_faces, faces
