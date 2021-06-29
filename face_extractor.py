import argparse
import face_recognition
import os
import cv2
import time
import platform
from etaprogress.progress import ProgressBar

parser = argparse.ArgumentParser(
    description='Extract faces from video to specified dir'
)
parser.add_argument("-v", "--video", required=True, help="Path to video file")
parser.add_argument("-o", "--output", required=True, help="Path to output directory")
parser.add_argument("-m", "--model", required=False, type=str, choices=['hog', ' small', 'cnn'], default='hog',
                    help="Name of selected recognition model. CUDA accelerated (if available) deep-learning pretrained model")
parser.add_argument("-q", "--quiet", required=False, type=bool, choices=[True, False], default=False,
                    help="Hide progress bar")
parser.add_argument("-e", "--expand", required=False, type=float, nargs=4, default=[0.25, 0.25, 0.25, 0.25],
                    help="Expand face face detection borders [UP, DOWN, LEFT, RIGHT]")
args = parser.parse_args()

VIDEO_PATH = args.video
OUTPUT_DIR_PATH = args.output
RECOGNITION_MODEL = args.model
QUIET_MODE = args.quiet
EXTEND_CROPPED_VALUES = args.expand

PROGRESS_BAR_REFRESH_INTERVAL = 3
PROGRESS_BAR_LAST_REFRESH = 0

video = cv2.VideoCapture(os.path.abspath(VIDEO_PATH))
bar = ProgressBar(int(video.get(cv2.CAP_PROP_FRAME_COUNT)), max_width=40)

print('Processing video')
while True:
    ret, frame = video.read()
    if int(video.get(cv2.CAP_PROP_POS_FRAMES)) % 60 == 0:
        # This time we first grab face locations - we'll need them to draw boxes
        locations = face_recognition.face_locations(frame, model=RECOGNITION_MODEL)
        locations = sorted(locations, key=lambda face: face[3])
        for nb, face_location in enumerate(locations):
            croped = frame[
                     int(face_location[0] - ((face_location[2] - face_location[0]) * EXTEND_CROPPED_VALUES[0])):int(
                         face_location[2] + ((face_location[2] - face_location[0]) * EXTEND_CROPPED_VALUES[1])),
                     int(face_location[3] - ((face_location[1] - face_location[3]) * EXTEND_CROPPED_VALUES[2])):int(
                         face_location[1] + ((face_location[1] - face_location[3]) * EXTEND_CROPPED_VALUES[3]))]
            try:
                cv2.imwrite(
                    os.path.abspath(f'{OUTPUT_DIR_PATH}/{str(nb)}-{int(video.get(cv2.CAP_PROP_POS_FRAMES))}.jpg'),
                    croped)
            except:
                print("Not working")

    if not QUIET_MODE and time.time_ns() > (PROGRESS_BAR_LAST_REFRESH + PROGRESS_BAR_REFRESH_INTERVAL * 1000000000):
        bar.numerator = int(video.get(cv2.CAP_PROP_POS_FRAMES))
        if platform.system() == 'Linux':
            os.system('clear')
        elif platform.system() == 'Windows':
            os.system('cls')
        print(bar)
        PROGRESS_BAR_LAST_REFRESH = time.time_ns()
