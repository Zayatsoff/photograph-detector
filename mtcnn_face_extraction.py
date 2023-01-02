import os

from facenet_pytorch import MTCNN
import torch
import numpy as np
import cv2
from PIL import Image, ImageDraw

def face_extraction(path, image, device):
    # Define MTCNN module
    mtcnn = MTCNN(keep_all=True, device=device)

    # Define the desired width and height of the cropped faces
    face_width = 200
    face_height = 200
    # Create an empty list to store the extracted faces
    faces_list = []
    num_faces = 0

    # Open the image using PIL
    im = Image.open(os.path.join(path, image))
    # Detect faces
    boxes, probs = mtcnn.detect(im)
    if boxes is None:
        # Return num_faces as 0 and faces_cv2 as None if boxes is None
        return 0, None
    else:
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
                # Add the face numpy array to the list of faces
                faces_list.append(face_np)

        # Convert the list of faces to a numpy array
        faces = np.array(faces_list)
        # Convert the numpy array of faces to a list of cv2 images
        faces_cv2 = [cv2.cvtColor(face, cv2.COLOR_BGR2RGB) for face in faces]

        # print(f"\nFaces extracted successfully!\n")
        # Return the list of detected faces
        return num_faces, faces_cv2
