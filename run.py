import os
import shutil
import torch
import argparse

from random_image_converter import random_image_convert
from mtcnn_face_extraction import face_extraction
from variance_of_laplacian import blur_detection

## --- Arg Parse ---
# Create a parser object
parser = argparse.ArgumentParser()

# Add the "convert_im" argument and set its default value to False
parser.add_argument(
    "--convert_im",
    default=True,
    action="store_true",
    help="Convert images from .ARW to .JPEG format [boolean]",
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


# Get images
images = [f for f in os.listdir(args.new_path) if f.endswith(".JPEG")]

for i, image in enumerate(images):
    # Extract all the faces from each image
    total_faces, pil_faces = face_extraction(args.new_path, image, device)
    if total_faces == 0:
        # Create the "No Faces" folder if it does not exist
        if not os.path.exists(os.path.join(args.extracted_path, "No Faces")):
            os.mkdir(os.path.join(args.extracted_path, "No Faces"))
        # Move the image to the "No Faces" folder
        shutil.move(
            os.path.join(args.new_path, image),
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

        # Loop through the ratings dictionary
        for rating, (min_val, max_val) in ratings.items():
            # Check if the blurriness value falls within the range for the current rating
            if min_val <= blurriness <= max_val:
                # Check if the directory for the extracted folder
                if not os.path.exists(args.extracted_path):
                    # Create the directory for extracted folder
                    os.mkdir(args.extracted_path)
                if not os.path.exists(os.path.join(args.extracted_path, rating)):
                    # Create the directory for the rating
                    os.mkdir(os.path.join(args.extracted_path, rating))
                # Move the image to the appropriate folder
                shutil.move(
                    os.path.join(args.new_path, image),
                    os.path.join(args.extracted_path, rating),
                )
    print(f"{i+1} image(s) processed successfully!")

    # Raise an error if the blurriness value is outside the valid range
    if blurriness < 0 or blurriness > 1:
        raise ValueError("Blurriness value is outside the valid range (0 to 1)")
print("\n---All images have been organized!---")
