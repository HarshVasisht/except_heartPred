import heartpred
from video2face import *
from datacapture import *
import datacapture
import config
import video2face


artifact_config_file = config.read_yaml('config.yaml')
hrc = artifact_config_file['Artifacts_path']['haarcascade']
oft = artifact_config_file['Artifacts_path']['output_folder_path']
file = 'database.json'

hr, Uname = heartpred.heart_pred()
video_path = f'./videos/cam{Uname}.avi'
extract_face_from_video(username = Uname, video_path = video_path, output_folder_path = oft, hrc = hrc)