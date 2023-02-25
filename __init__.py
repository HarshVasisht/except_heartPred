from rich import traceback
from rich.console import Console
import cv2
from pathlib import Path
import os
from src.eulerian import fft_filter
from src.evalutation import error
from src.heartrate import find_heart_rate
from src.preprocessing import read_video, capture_video
from datetime import datetime

# current dateTime
now = datetime.now()

# convert to string
date_time_str = now.strftime("%Y-%m-%d %H:%M:%S")
print('DateTime String:', date_time_str)
# from pyramids import build_gaussian_pyramid, build_laplacian_pyramid, build_video_pyramid, collapse_laplacian_video_pyramid
from src.pyramids import *

# vpath = Path("src/videos/cam2_best_83(84).avi")
# print(vpath)
print(os.getcwd())

faceCascade = cv2.CascadeClassifier("haarcascades/haarcascade_frontalface_alt0.xml")

traceback.install()
console = Console()

freq_min = 1
freq_max = 1.8

# input_camera=int(input())
# user_name=input("Enter your name:")
# console.print("Entering capturing mode......\n", style="blink bold red underline on white")

def heart_pred():
    # user_name = input("Enter Name:") # can be taken from the user also
    user_name = input("Please enter your name: ") # can be taken from the user also
    capture_video(user_name)
    console.print("Capturing of video Done......!!\n", style="blink bold red underline on white")
    video_frames, frame_ct, fps = read_video(f"videos/cam{user_name}.avi")

    # if vpath.exists():
    #     video_frames, frame_ct, fps = read_video("src/videos/cam2_best_83(84).avi") #direct video
    #     console.print("read successfully!")
    #     lap_video = build_video_pyramid(video_frames)
    # else:
    #     print("No vpath")
    # print(video_frames)
    lap_video = build_video_pyramid(video_frames)
    # print(lap_video)
    amplified_video_pyramid = []

    heart_rate = 0

    for i, video in enumerate(lap_video):
        if i == 0 or i == len(lap_video)-1:
            continue
            # Eulerian magnification with temporal FFT filtering
        result, fft, frequencies = fft_filter(video, freq_min, freq_max, fps)
        lap_video[i] += result

        # Calculate heart rate
        
        heart_rate = find_heart_rate(fft, frequencies, freq_min, freq_max) #line to update HR



    # Collapse laplacian pyramid to generate final video
    amplified_frames = collapse_laplacian_video_pyramid(lap_video, frame_ct)

    heart_rate = heart_rate + 20  #20 for Indian tone

    # Output heart rate and final video

    console.print("Heart rate: ", heart_rate , "bpm", style="blink bold red underline on white")
    console.print("Displaying final video...", style="blink bold red underline on white")

    # for frame in amplified_frames:
    #     cv2.imshow("frame", frame)
    #     cv2.waitKey(20)

    console.print("+++++++++++++++++++++++++++++++", style="blink bold red underline on Green")
    error(heart_rate)
    file1 = open("CamTrialhr.txt", "w")  # write mode
    file1.write('Hello,'+ user_name + ' your\n')
    file1.write('Predicted Heart Rate: '+ str(heart_rate) + " @ " + date_time_str )
    file1.close()
    console.print("+++++++++++++++++++++++++++++++", style="blink bold red underline on Green")
    return heart_rate, user_name

heart_pred()
