# Face Blur Detector and Organiser
A program that reads a list of files with the extension .ARW or .JPG from a specified directory, selects a random sample of 20 files, and converts them to JPEG images (unless they are already .JPEG). These images are then passed through MTCNN to extract all of the faces in the image. Using the variance of Laplacian method, the program labels each face as either "blurry" or "not blurry" based on a user-specified threshold value (less than 10.00 is considered blurry by default). For each photograph, the program calculates the percentage of blurry faces by dividing the total number of blurry faces by the total number of faces. Based on this percentage, the program categorizes each image into one of five folders, ranging from 1 to 5 stars. Finally, the program moves each converted JPEG image into the appropriate folder based on its blurriness rating.

## Installation
1. Clone this repository
2. Install the required dependencies:
```
pip install -r requirements.txt

```

## Usage
To run the program, use the following command:

```
python run.py --convert_im --old_path [path] --new_path [path] --extracted_path [path] --thresh [threshold in float]
```

For a full list of available arguments and their descriptions, run the following command:
```
python run.py --help

```

## Output
The program will create six folders named "1 star", "2 stars", "3 stars", "4 stars",  "5 stars", and "No Faces" in the specified directory. It will then move the processed images into the appropriate folder based on their blurriness rating.

## TODO
- [x] Create `extracted` folder unless already created
- [x] Add universal OS support
- [x] Account for no faces in images
- [ ] Check for similar looking images
- [ ] Turn into a standalone
- [ ] Detect weird faces in images
- [ ] Improve Facial recognition


## Additional Notes
- The MTCNN model provided by [Tim Esler](https://github.com/timesler/facenet-pytorch). 
- The MTCNN model may not accurately detect all faces in the images.
- The variance of Laplacian method may not accurately detect blurriness in all cases. Use caution when interpreting the results.
