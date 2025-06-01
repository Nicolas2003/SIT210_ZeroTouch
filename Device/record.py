from picamzero import Camera
import cv2
import time

camera = Camera()

def get_footage():
    # frame = "pseudo-frame"
    frame = cv2.cvtColor(camera.capture_array(), cv2.COLOR_RGB2BGR)
    return frame

def end_record():
    # === Cleanup ===
    camera.stop_preview()
    cv2.destroyAllWindows()

def stream_record(send_frames):
    print("[Record] Streaming started...")
    while True:
        live_footage = get_footage()
        print("[Record] Another frame...")
        send_frames.send(live_footage)
