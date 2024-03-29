import os
import shutil
import torch
import argparse

from random_image_converter import random_image_convert
from mtcnn_face_extraction import face_extraction
from variance_of_laplacian import blur_detection
from fastdup_analysis import fastdup_analyze
from group_similar_images import sim_groups

## --- Arg Parse ---
# Create a parser object
parser = argparse.ArgumentParser()

# Add the "convert_im" argument and set its default value to True
parser.add_argument(
    "--convert_im",
    default=False,
    action="store_true",
    help="Convert images from .ARW to .JPEG format [boolean]",
)
# Add the "sim" argument and set its default value to True
parser.add_argument(
    "--sim",
    default=True,
    action="store_true",
    help="Categories images by similarity",
)
# Add the "old_path" argument and set its default value to an empty string
parser.add_argument(
    "--old_path",
    default="/Users/liorrozin/Desktop/OG",
    help="Path to the folder containing the .ARW files",
)
# Add the "new_path" argument and set its default value to an empty string
parser.add_argument(
    "--new_path",
    default="/Users/liorrozin/Desktop/2.0",
    help="Destination path for the JPEG files",
)
# Add the "extracted_path" argument and set its default value to an empty string
parser.add_argument(
    "--extracted_path",
    default="/Users/liorrozin/Desktop/2.0/extracted_faces",
    help="Destination path for the images",
)
# Add the "extracted_path" argument and set its default value to an empty string
parser.add_argument(
    "--thresh", type=float, default="10.00", help="Threshold of blurriness [float]"
)

# Parse the arguments
args = parser.parse_args()

## --- Misc ---
# Determine if an MPS or CUDA is available
device = torch.device(
    "cuda:" + str(torch.cuda.current_device()) if torch.cuda.is_available() else "cpu"
)
# Define a dictionary with the directory names and range of blurriness values for each rating
ratings = {
    "1 Star": (0.0, 0.20),
    "2 Stars": (0.21, 0.40),
    "3 Stars": (0.41, 0.60),
    "4 Stars": (0.61, 0.80),
    "5 Stars": (0.81, 1.00),
}
print("\n---Beginning process---\n")
## --- Functions ---
# Converts 20 random images from .ARW to .JPEG
if args.convert_im:
    random_image_convert(args.old_path, args.new_path)

# Organize images by similarity
if args.sim:
    fastdup_analyze(args.new_path)
    sim_groups(args.new_path)


# Get all the folders in the path
folders = [f for f in os.listdir(args.new_path) if os.path.isdir(os.path.join(args.new_path, f))]

for folder in folders:
    highest_blurriness = 0
    highest_blurriness_image = None

    # Get all the images in the folder
    images = [f for f in os.listdir(os.path.join(args.new_path, folder)) if f.endswith(".JPEG")]
    for i, image in enumerate(images):
        # Extract all the faces from each image
        total_faces, pil_faces = face_extraction(os.path.join(args.new_path, folder), image, device)
        if total_faces == 0:
            # Create the "No Faces" folder if it does not exist
            if not os.path.exists(os.path.join(args.extracted_path, "No Faces")):
                os.mkdir(os.path.join(args.extracted_path, "No Faces"))
            # Move the image to the "No Faces" folder
            shutil.move(
                os.path.join(args.new_path, folder, image),
                os.path.join(args.extracted_path, "No Faces"),
            )
        else:
            if pil_faces == None:
                blurriness = 1
            else:
                # Detect all the blurred faces
                count = blur_detection(pil_faces, args.thresh)
                # Calculate the blurriness factor of each photograph
                blurriness = count / total_faces

            # Check if the current image has the highest blurriness
            if blurriness > highest_blurriness:
                highest_blurriness = blurriness
                highest_blurriness_image = os.path.join(args.new_path, folder, image)
    # Only move the image with the highest blurriness
    if os.path.isfile(args.extracted_path):
        os.remove(args.extracted_path)
    if not os.path.exists(args.extracted_path):
        os.mkdir(args.extracted_path)
    if highest_blurriness_image:
        shutil.move(highest_blurriness_image, os.path.join(args.extracted_path, folder + '_' + highest_blurriness_image.split("/")[-1]))
    print(f"{i+1} image(s) processed successfully!")





    # Raise an error if the blurriness value is outside the valid range
    if blurriness < 0 or blurriness > 1:
        raise ValueError("Blurriness value is outside the valid range (0 to 1)")
print("\n---All images have been organized!---")

