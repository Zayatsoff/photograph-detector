import cv2
import imutils
import argparse
import numpy as np

from keras.models import load_model
from tensorflow.keras.utils import img_to_array


def main():
    # Get arguments
    # args = getArguments()
    img = f"C:/Users/Orange/Desktop/test/sad.jpg"
    model = "models/lenet_smiles.hdf5"

    print("[INFO] loading face detector...")
    cascade = "cascade/haarcascade_frontalface_default.xml"
    detector = cv2.CascadeClassifier(cascade)

    print("[INFO] loading model...")
    model = load_model(model)

    print("[INFO] getting image...")
    frame = cv2.imread(img)

    print("[INFO] starting image loop...")
    imageLoop(frame, detector, model)

    print("[INFO] cleaning streaming and closing windows")
    cv2.destroyAllWindows()


def getArguments():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument(
        "-m", "--model", default="models/lenet_smiles.hdf5", help="path to custom model"
    )
    # arg_parser.add_argument("-v", "--video", help="path to video file")
    arg_parser.add_argument("-i", "--image", help="path to video file")
    return vars(arg_parser.parse_args())


def imageLoop(frame, detector, model):
    while True:
        frame_copy, gray = processImage(frame, width=600)
        faces = detectFaces(gray, detector, scale=1.1, neighbors=5, size=30)

        frame_copy = detectSmile(frame_copy, faces, gray, model)

        cv2.imshow("Face", frame_copy)

        # ESC to quit
        key = cv2.waitKey(1)
        if key == 27:
            break



def processImage(frame, width):
    frame = imutils.resize(frame, width=width)
    grayscale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    return frame.copy(), grayscale


def detectFaces(gray, detector, scale, neighbors, size):
    return detector.detectMultiScale(
        gray,
        scaleFactor=scale,
        minNeighbors=neighbors,
        minSize=(size, size),
        flags=cv2.CASCADE_SCALE_IMAGE,
    )


def detectSmile(frame, faces, grayscale, model):
    for (x, y, width, height) in faces:
        roi = extractROI(grayscale, x, y, width, height, size=28)
        label = predictLabel(roi, model)
        writeLabelToVideo(
            frame,
            label,
            origin=(x, y - 10),
            font=cv2.FONT_HERSHEY_SIMPLEX,
            font_scale=0.75,
            color=(0, 0, 255),
            thickness=1,
            x=x,
            y=y,
            w=width,
            h=height,
        )
    return frame


def extractROI(frame, x, y, w, h, size):
    roi = frame[y : y + h, x : x + w]
    roi = cv2.resize(roi, (size, size))
    roi = roi.astype("float") / 255.0
    roi = img_to_array(roi)
    return np.expand_dims(roi, axis=0)


def predictLabel(face, model):
    (no_smile, smile) = model.predict(face)[0]
    return "Smile" if smile >= no_smile else "No Smile"


def writeLabelToVideo(
    frame, label, origin, font, font_scale, color, thickness, x, y, w, h
):
    cv2.putText(frame, label, origin, font, font_scale, color, thickness)
    cv2.rectangle(frame, (x, y), (x + w, y + h), color, thickness)


if __name__ == "__main__":
    main()
