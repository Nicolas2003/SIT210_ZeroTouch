import cv2
import base64
from websocket_server import WebsocketServer
from threading import Thread

livestream_server = None
authentication_server = None

def add_users(frame, users):
    print(f"[Display] Received frame with{len(users)} users.")
    for user in users:
        name, top, right, bottom, left = user["name"], user["top"], user["right"], user["bottom"], user["left"]
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)
    return frame

def video_transmission(frame, server):
    _, buffer = cv2.imencode('.jpg', frame)
    jpg_as_text = base64.b64encode(buffer).decode('utf-8')
    print("[Display] sending frame")
    server.send_message_to_all(jpg_as_text)

def user_authentication(username, server):
    print(f"  [Display] User has authenticated with {username}")
    server.send_message_to_all(username)

def new_client(handler, server):
    print(f"  [Display]: New client connected arg1: {handler} and arg2: {server}!")

def start_video_server():
    global livestream_server
    livestream_server = WebsocketServer(host='0.0.0.0', port=8765)
    livestream_server.set_fn_new_client(new_client)
    livestream_server.run_forever()

def start_authentication_server():
    global authentication_server
    authentication_server = WebsocketServer(host='0.0.0.0', port=8766)
    authentication_server.set_fn_new_client(new_client)
    authentication_server.run_forever()

def stream_display_users(received_identity):
    global livestream_server
    print("[Display]: Starting Livestream Server...")
    Thread(target=start_video_server, daemon=True).start()
    Thread(target=start_authentication_server, daemon=True).start()

    while True:
        print("[Display] waiting footage and users")
        try:
            footage, users = received_identity.recv()
        except Exception as e:
            print(f"[Display] Pipe closed. Exiting display loop.\nError: {e}")
            break

        frame = add_users(footage, users)
        video_transmission(frame, livestream_server)
        if len(users) > 0:
            user_authentication(users[0]["name"], authentication_server)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()
