import cv2
import numpy as np
import face_recognition
import joblib

import os
import random



def read_list_from_file(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file]

# Example usage
label_file_path = "C:\\Users\\Lagan\\OneDrive\\Desktop\\celebrity_recogniton\\labels.txt"
labels = read_list_from_file(label_file_path)

known_labels = np.unique(labels)
def recognize_faces_in_video(video_path, model_path, output_path):
    # Load the trained model
    clf = joblib.load(model_path)
    def recognize_faces(frame):
      #print('entered recognize faces')
      try:
        # Convert BGR to RGB format (expected by face_recognition)
        
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        

       
        face_locations = face_recognition.face_locations(rgb_frame)
       
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
        #128- dimensional face_encodings
        

        face_names = []
        for face_encoding in face_encodings:
          # Use the trained SVM model for recognition
          probabilities = clf.predict_proba([face_encoding])[0]
          best_match_index = np.argmax(probabilities)
          name = known_labels[best_match_index] if probabilities[best_match_index] > 0.5 else "Unknown"
          face_names.append(name)

        return face_locations, face_names
      except Exception as e:
        print("Error during face recognition:", e)


    # Load the video
    video_path = video_path 
    video_capture = cv2.VideoCapture(video_path)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(output_path, fourcc, 10.0, (int(video_capture.get(3)), int(video_capture.get(4))))

    while video_capture.isOpened():
      ret, frame = video_capture.read()
      if not ret:
        break
      #print('entered while loop')

      face_locations, face_names = recognize_faces(frame)
        
      for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Draw rectangle around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (255, 0, 0), 2)
            # Draw label
            cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)
        
      out.write(frame)
      cv2.imshow('Video', frame)
        
      if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # ... rest of your recognize_faces function ...

def select_random_video(folder_path):
    print('entred')
    # List all video files in the folder
    video_files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f)) and f.lower().endswith(('.mp4', '.avi', '.mov'))]

    if not video_files:
        print("No video files found in the folder.")
        return None

    # Select a random video file
    selected_video = random.choice(video_files)
    return os.path.join(folder_path, selected_video)



# Example usage:
#model_path = 'C:/Users/Lenovo/Desktop/majorProject/clf.pkl'
model_path = "C:\\Users\\Lagan\\OneDrive\\Desktop\\celebrity_recogniton\\clf.pkl"
#video_path = "C:/Users/Lenovo/Desktop/celebrity_recogniton/downloded_videos/I'm not a Perfectionist! ｜ Aamir Khan #shorts #aamirkhan #bollywood #perfection.mp4"
folder_path = 'C:\\Users\\Lagan\\OneDrive\\Desktop\\celebrity_recogniton\\downloded_videos'  # Replace with your folder path
video_path = select_random_video(folder_path)
output_path = "output_video.avi"
recognize_faces_in_video(video_path, model_path, output_path)
