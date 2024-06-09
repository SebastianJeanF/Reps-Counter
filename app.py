import base64
import os
import cv2
import numpy as np
from flask import Flask, render_template, send_from_directory
from flask_socketio import SocketIO, emit


import mediapipe as mp
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
counter = 0
stage = "up"
create = None
opname = "output.avi"
pose = mp_pose.Pose(
min_detection_confidence=0.7,
min_tracking_confidence=0.7)



app = Flask(__name__, static_folder="./templates/static")
app.config["SECRET_KEY"] = "secret!"
socketio = SocketIO(app)
@app.route("/")
def index():
    return render_template("index.html")

def base64_to_image(base64_string):
    # Extract the base64 encoded binary data from the input string
    base64_data = base64_string.split(",")[1]
    # Decode the base64 data to bytes
    image_bytes = base64.b64decode(base64_data)
    # Convert the bytes to numpy array
    image_array = np.frombuffer(image_bytes, dtype=np.uint8)
    # Decode the numpy array as an image using OpenCV
    image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
    return image

def findPosition(image, results, draw=True):
  lmList = []
  if results.pose_landmarks:
      mp_drawing.draw_landmarks(
         image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
      for id, lm in enumerate(results.pose_landmarks.landmark):
          h, w, c = image.shape
          cx, cy = int(lm.x * w), int(lm.y * h)
          lmList.append([id, cx, cy])
          #cv2.circle(image, (cx, cy), 5, (255, 0, 0), cv2.FILLED)
  return lmList



# @socketio.on("connect")
# def test_connect():
#     print("Connected")
#     emit("my response", {"data": "Connected"})

@socketio.on("image")
def receive_image(image):
    global stage
    global counter
    
    # Decode the base64-encoded image data
    image = base64_to_image(image)

    # Perform image processing using OpenCV
    # gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # frame_resized = cv2.resize(gray, (640, 360))
    

    image = cv2.resize(image, (640,480))
    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
    # To improve performance, optionally mark the image as not writeable to
    # pass by reference.
    results = pose.process(image)
    # Draw the pose annotation on the image.
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    lmList = findPosition(image, results, draw=True)
    if len(lmList) != 0:
      cv2.circle(image, (lmList[12][1], lmList[12][2]), 20, (0, 0, 255), cv2.FILLED)
      cv2.circle(image, (lmList[11][1], lmList[11][2]), 20, (0, 0, 255), cv2.FILLED)
      cv2.circle(image, (lmList[12][1], lmList[12][2]), 20, (0, 0, 255), cv2.FILLED)
      cv2.circle(image, (lmList[11][1], lmList[11][2]), 20, (0, 0, 255), cv2.FILLED)
      if ((lmList[12][2] + 100) and (lmList[11][2] + 100) >= lmList[14][2] and lmList[13][2]):
        cv2.circle(image, (lmList[12][1], lmList[12][2]), 20, (0, 255, 0), cv2.FILLED)
        cv2.circle(image, (lmList[11][1], lmList[11][2]), 20, (0, 255, 0), cv2.FILLED)
        stage = "down"
      if ((lmList[12][2] + 100) and (lmList[11][2] + 100) <= lmList[14][2] and lmList[13][2]) and stage == "down":
        stage = "up"
        counter += 1
        counter2 = str(int(counter))
        print(counter)
        os.system("echo '" + counter2 + "' | festival --tts")
    text = "{}:{}".format("Push Ups", counter)
    cv2.putText(image, text, (10, 40), cv2.FONT_HERSHEY_SIMPLEX,
                1, (255, 0, 0), 2)




    # Encode the processed image as a JPEG-encoded base64 string
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
    result, frame_encoded = cv2.imencode(".jpg", image, encode_param)
    processed_img_data = base64.b64encode(frame_encoded).decode()

    # Prepend the base64-encoded string with the data URL prefix
    b64_src = "data:image/jpg;base64,"
    processed_img_data = b64_src + processed_img_data

    # Send the processed image back to the client
    emit("processed_image", processed_img_data)

if __name__ == "__main__":
    socketio.run(app, debug=True, port=5000, host='0.0.0.0')