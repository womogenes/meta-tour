from multiprocessing.sharedctypes import Value
import cv2 as cv
import os
import time
import json
import numpy as np
import sys


def stitch_images():
    """NOT IN USE. Iterates through and stiches images from the images folder, storing them in Stitches/"""
    imageFolder = 'Images'
    folders = os.listdir(imageFolder)

    # Goes through all folders in images folder (rooms) and takes images
    for room in folders:
        start_time = time.time()
        path = imageFolder + "/" + room
        images = []
        myList = os.listdir(path)
        # Reads images from folder and adds them to images list, resizing them
        for imgName in myList:
            curImg = cv.imread(f'{path}/{imgName}')
            curImg = cv.resize(curImg, (0, 0), None, .5, .5)
            images.append(curImg)
            # cv.imshow(imgName, curImg)

        print("[INFO] Images Parsed")

        stitcher = cv.Stitcher_create()
        (status, result) = stitcher.stitch(images)
        if (status == 0):
            print(f"[SUCCESS]: Image Sphere Generated for {room}")
            cv.imwrite(f"Stitches/stitch-{room}.jpg", result)
            print(
                f"[INFO]: Time elapsed to stitch {room} was {round(time.time()-start_time, 3)} seconds.")
            cv.imshow(room, result)
            cv.waitKey(0)
        elif status == 1:
            print(f"[ERROR] Not enough keypoints in images of {room}")
        else:
            print(f"[ERROR]: {room} Status {status}")


def convert_milli_to_frames(milli: int, totalMilli: int, totalFrames: int):
    """Returns the frame in a video given a specific timestamp in milliseconds"""
    ratio = milli / totalMilli
    return np.floor(ratio * totalFrames)


def select_timestamps(rotations, distance: float):
    """Creates a list of all the desired timestamps for a given rotation distance between frames. Selects the frame closest to the next step. It will return a list of length: 360/distance full of timestamps in milliseconds."""
    if distance <= 0:
        print("[ERROR]: Distance must be > 0")
        exit(1)
    # Timestamps stores our relevant timestamps
    timestamps = []
    # Need to store where we start
    startRotation = rotations[0][0]
    timestamps.append(rotations[0][1])
    # We want a point every distance degrees, so 360/distance points + 1 for the start
    length = 360 // distance + 1
    for i in range(1, length):
        # Finding our desired rotation
        desRot = startRotation + i * distance
        # Gets the index of where desired rotation would fit in our array, checks to make sure we don't go out of bounds
        index = max(np.searchsorted(rotations[:, 0], desRot) - 1, 0)
        timestamps.append(rotations[index][1])
    return timestamps


def load_video_frames(vidcap, frameList: list, resizeCoeff: float, flip: bool):
    """Returns a list of all the images of frames of the video given a frame list. Each image is resized by the resizeCoeff (1 being normal scale), and rotated 180 degrees based on if flip is True or not."""
    frames = []
    # Read in image and success status
    for frame in frameList:
        vidcap.set(1, frame)
        success, image = vidcap.read()
        if success:
            image = cv.resize(image, (0, 0), None, resizeCoeff, resizeCoeff)
            if flip:
                image = cv.rotate(image, cv.ROTATE_180)
            frames.append(image)
            # cv.imshow(f"{frame}", image)
            # cv.waitKey(2)

    return frames


def load_json(filename: str):
    """Returns a dictionary from a json file"""
    with open(filename, "r") as file:
        return json.load(file)


# Check if there is an images and stitches folder
def check_folder(folderName: str):
    """Checks if a folder exists and returns True if it does or creates the folder and returns False if it doesn't"""
    currentPath = os.getcwd()
    folderPath = os.path.join(currentPath, folderName)
    if not os.path.isdir(folderPath):
        print(
            f"[INFO]: '{folderName}' not found, automatically created new folder")
        os.mkdir(folderPath)
        exit(1)
        return False
    return True


def videoToPanorama(tourData: list, videoName: str, scaleCoeff: int):
    """Takes in the name of a json file with odometry data and the name of a video file and stitches a panorama stored in stitches/. Files whose names are inputted should exist in the most outside directory (same directory as imageStitch.py)"""
    vidcap = cv.VideoCapture(videoName)
    totalFrames = vidcap.get(7)
    # Creates a list of tuples with all timestamps and y absolute rotations (relevant rotation).
    rotations = np.array([(row[9] * 180 / np.pi, row[0])
                         for row in tourData[::]])
    totalMilli = rotations[-1][1]

    # Sorts the array by orientation ascending (starts around 0, ends around 360)
    rotations = rotations[rotations[:, 0].argsort()]
    print("[INFO]: Rotations Sorted")

    # Printing scatter plot of index against rotation
    # plt.scatter(range(len(rotations)), rotations[:,0])
    # plt.show(block=True)

    # Want an image every 6 or so degrees
    timestamps = np.array(select_timestamps(rotations, 6))
    frames = convert_milli_to_frames(timestamps, totalMilli, totalFrames)
    images = load_video_frames(vidcap, frames, scaleCoeff, True)
    print(f"[INFO]: {len(images)} images gathered")
    print("[INFO]: Stitching images...")

    start_time = time.time()
    stitcher = cv.Stitcher_create()
    (status, result) = stitcher.stitch(images)
    if (status == 0):
        print(f"[SUCCESS]: Image Sphere Generated for {videoName}")
        cv.imwrite(f"Stitches/{videoName[:-5]}_stitch.jpg", result)
        print(
            f"[INFO]: Time elapsed to stitch {videoName} was {round(time.time()-start_time, 3)} seconds.")
        cv.imshow(videoName, result)
        cv.waitKey(0)
        return result
    elif status == 1:
        print(f"[ERROR] Not enough keypoints in images of {videoName}")
        return 1
    else:
        print(f"[ERROR]: {videoName} Status {status}")
        return 1


if __name__ == "__main__":
    # check for valid num of arguments
    if len(sys.argv) != 4:
        print("[ERROR]: usage: python imageStitch.py 'datafile.json' 'videofile.webm' float: scaleCoefficient")
        exit(1)

    jsonFile = sys.argv[1]
    videoFile = sys.argv[2]
    # Test if scalecoefficient is inputted as an integer
    try:
        scaleCoeff = float(sys.argv[3])
    except ValueError:
        print("[ERROR] scale coefficient not float")
        exit(1)

    if not jsonFile.endswith(".json"):
        print("First argument must be name of JSON file")
        exit(1)

    if not videoFile.endswith(".webm"):
        # Technically we can accept a bunch of video file types I think, but since this
        # is what we've been getting from the website this is what we have for now
        print("First argument must be name of a webm file")
        exit(1)

    if (check_folder("Data") and check_folder("Stitches")):
        print("[INFO]: All necessary folders exist")

    videoToPanorama(jsonFile, videoFile, scaleCoeff=1)
