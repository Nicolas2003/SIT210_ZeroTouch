import asyncio
import websockets
import cv2
import base64

async def video_feed(websocket, path):
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        # Do face recognition and draw here
        _, buffer = cv2.imencode('.jpg', frame)
        jpg_as_text = base64.b64encode(buffer).decode('utf-8')
        await websocket.send(jpg_as_text)
        await asyncio.sleep(0.03)  # ~30 fps

start_server = websockets.serve(video_feed, "0.0.0.0", 8765)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
