import cv2
import face_recognition
import numpy as np
import os

known_user_encodings = []
known_user_names = []

def load_known_faces(directory):
    for file in os.listdir(directory):
        if file.endswith(('.jpg', '.png')):
            image = face_recognition.load_image_file(f"Users/{file}")
            encoding = face_recognition.face_encodings(image)
            if encoding:  # Make sure encoding list isn't empty
                known_user_encodings.append(encoding[0])
                known_user_names.append(os.path.splitext(file)[0])
    return known_user_encodings, known_user_names

def stream_identify(directory, input, output):
    load_known_faces(directory)
    print("[ID] Ready to identify Users")
    while True:
        print("[ID] Waiting for footage")
        footage = input.recv()
        print("[ID] Received footage")
        identified_users = facial_recognition(footage)
        print("[ID] Identified users")
        output.send([footage, identified_users])

def facial_recognition(frame):
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    identified_users = []

    face_locations = face_recognition.face_locations(small_frame)
    face_encodings = face_recognition.face_encodings(small_frame, face_locations)

    for (top, right, bottom, left), encoding in zip(face_locations, face_encodings):
        name = "Unknown"
        known_user = False

        matches = face_recognition.compare_faces(known_user_encodings, encoding)
        print(f"  Matches: {matches}")
        
        if len(matches) > 0:
            face_distances = face_recognition.face_distance(known_user_encodings, encoding)
            best_match_index = np.argmin(face_distances)

            if matches[best_match_index]:
                name = known_user_names[best_match_index]
                known_user = True

            identified_users.append({
                "name": name,
                "known_user": known_user,
                "top": top * 4,
                "right": right * 4,
                "bottom": bottom * 4,
                "left": left * 4,
            })

    return identified_users



