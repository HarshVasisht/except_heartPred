from deepface import DeepFace as df
import matplotlib.pyplot as plt
import numpy as np
import cv2
import config
import datacapture
import heartpred as hp

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
    data = obj[0]
    # print("Age: ", obj["age"])
    # print("Emotion: ", obj["dominant_emotion"])
    # print("Gender: ", obj["gender"])
    # print("Race: ", obj["dominant_race"])
    # print('─' * 10)
    # emotion, age, gender= obj["dominant_emotion"], obj["age"], obj["gender"]
    return data

def face_detector(img_path):
  backends = ['opencv', 'ssd', 'dlib', 'mtcnn', 'retinaface', 'mediapipe']
  face = df.detectFace(img_path = img_path, target_size = (224, 224), detector_backend = backends[4])

def display_img(img):
  img = plt.imread(img)
  plt.imshow(img)
  plt.show()


def extract_data(data):
    emt, gen, age, race, dmt = data['emotion'], data['gender'], data['age'], data['race'],  data['dominant_race']
    pred_emt = max(zip(emt.values(), emt.keys()))
    pred_gen = max(zip(gen.values(), gen.keys()))
    pred_race = max(zip(race.values(), race.keys()))
    data_list = [pred_emt,pred_gen,pred_race, age, dmt]
    # return pred_emt,pred_gen,pred_race, age, dmt
    return data_list

# def predict(img_path ,file_path = file, emotion = pred_emt, gender = pred_gen, race = pred_race, age = age, demt = dmt):
def predict(img_path,   username = 'Default' ,file_path = file):
    esti_HR, username = hp.heart_pred()

    # extract_face_from_video(username = username, video_path = "videos/cam{username}.avi", output_folder_path = oft, hrc = hrc)

    obj = actions(img_path=img_path)
    dl = extract_data(obj)
    display_img(img=img_path)
    db = { 'User Name': username , 'Emotion': dl[0], 'Age': dl[3], 'Gender': dl[1], 'Race': dl[2], 'Dominant Emotion': dl[4], 'Estimated HeartRate': esti_HR}
    datacapture.write_data(db, file_path)




if __name__ == '__main__':
    predict('face_image/face0.jpg')
