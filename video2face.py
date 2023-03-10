from deepface import DeepFace as df
import matplotlib.pyplot as plt
import numpy as np
import cv2
import config
import datacapture

artifact_config_file = config.read_yaml('config.yaml')
hrc = artifact_config_file['Artifacts_path']['haarcascade']
oft = artifact_config_file['Artifacts_path']['output_folder_path']
file = 'database.json'

def extract_face_from_video(username, video_path, output_folder_path = oft, hrc = hrc):
    try:
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + hrc)
        if face_cascade.empty():
            raise Exception("Failed to load face cascade classifier file")
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise Exception("Failed to open video file")
        
        count = 0
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
            
            for (x, y, w, h) in faces:
                face_image = frame[y:y+h, x:x+w]
                cv2.imwrite(f"{output_folder_path}/{username}{count}.jpg" )
                count += 1
    
    except Exception as e:
        raise e

    finally:
        cap.release()





def actions(img_path):
    actions=('emotion', 'age', 'gender', 'race')
    img = plt.imread(img_path)
    obj  = df.analyze(img)
    # print("Age: ", obj["age"])
    # print("Emotion: ", obj["dominant_emotion"])
    # print("Gender: ", obj["gender"])
    # print("Race: ", obj["dominant_race"])
    # print('─' * 10)
    emotion, age, gender= obj["emotion"], obj["age"], obj["gender"]
    return emotion, age, gender

def face_detector(img_path):
  backends = ['opencv', 'ssd', 'dlib', 'mtcnn', 'retinaface', 'mediapipe']
  face = df.detectFace(img_path = img_path, target_size = (224, 224), detector_backend = backends[4])

def display_img(img):
  img = plt.imread(img)
  plt.imshow(img)
  plt.show()


## >> Our Calling Functions >>


def predict(img_path, user_name , file_path = file):
    emotion, age, gender = actions(img_path=img_path)
    display_img(img=img_path)
    db = {'Name':user_name, 'Emotion': emotion, 'Age': age, 'Gender': gender}
    datacapture.write_data(db, file_path)




if __name__ == '__main__':
    predict('face_image/face0.jpg', user_name= 'harsh_face2video')
