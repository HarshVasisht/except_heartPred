import cv2
import numpy as np
from cv2 import VideoWriter
from cv2 import VideoWriter_fourcc
# import timer
faceCascade = cv2.CascadeClassifier("haarcascades/haarcascade_frontalface_alt0.xml")


# Read in and simultaneously preprocess video
def read_video(path):
    cap = cv2.VideoCapture(path)
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    video_frames = []
    face_rects = ()

    while cap.isOpened():
        ret, img = cap.read()
        if not ret:
            break
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        roi_frame = img

        # Detect face
        if len(video_frames) == 0:
            face_rects = faceCascade.detectMultiScale(gray, 1.3, 5)

        # Select ROI
        if len(face_rects) > 0:
            for (x, y, w, h) in face_rects:
                roi_frame = img[y:y + h, x:x + w]
            if roi_frame.size != img.size:
                roi_frame = cv2.resize(roi_frame, (500, 500))
                frame = np.ndarray(shape=roi_frame.shape, dtype="float")
                frame[:] = roi_frame * (1. / 255)
                video_frames.append(frame)

    frame_ct = len(video_frames)
    cap.release()

    return video_frames, frame_ct, fps
def capture_video(user_name,ip=False,port='4747'):
    if ip == True:
        """Capturing the video for an external IP network
        >> Camera use is Droid Cam---Must have an Client connection
        """
        ip_value=input("Enter your IP address for establishing connection")
        #file_path=os.path.join('videos','cam')
        cap = cv2.VideoCapture(f'{ip_value}:{port}/video')
        # from datetime import datetime
        # start_time = timer(None)
        # timer(start_time)
        video = VideoWriter(f'videos/{user_name}.avi', VideoWriter_fourcc(*'MP42'), 25.0, (640,480))
        while True:
                ret, frame = cap.read()
                cv2.imshow('Capturing HeartRate.....',frame)
                video.write(frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        cap.release()
        video.release()
        cv2.destroyAllWindows()
    else:
        """Capturing the video from the local Camera"""
        #file_path=os.path.join('videos','cam')
        cap = cv2.VideoCapture(0)
        # from datetime import datetime
        # start_time = timer(None)
        # timer(start_time)
        video = VideoWriter(f'videos/{user_name}.avi', VideoWriter_fourcc(*'MP42'), 25.0, (640,480))
        while True:
                ret, frame = cap.read()
                cv2.imshow('Capturing HeartRate.....',frame)
                video.write(frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        cap.release()
        video.release()
        cv2.destroyAllWindows()
