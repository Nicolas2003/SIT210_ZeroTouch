import cv2

from identify import load_known_faces, facial_recognition
from record import get_footage, end_record
from display import add_users

def main():
    load_known_faces("./Users")
    while True:
        frame = get_footage()
        users = facial_recognition(frame)
        frame_with_users = add_users(footage, users)
        cv2.imshow("User Identification", frame_with_users)
        
        if cv2.waitKey(1000) & 0xFF == ord('q'):
            break
    
    end_record()

if __name__ == '__main__':
    main()
