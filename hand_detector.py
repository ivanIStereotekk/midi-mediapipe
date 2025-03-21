import base64
import json
import sys
import cv2
import mediapipe as mp
import os
import time
from cv2.typing import Scalar
from dotenv import dotenv_values
import socket

# S O C K E T   C L I E N T


def socket_send_data(data_object):
    HOST = '127.0.0.1'
    PORT = 65432 
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(data_object)




config = dotenv_values(".env")

# Getting the webcam
web_cam = cv2.VideoCapture(0) # or 1 durring second camera connected



#hands

hands = mp.solutions.hands.Hands(static_image_mode=False,
                                 max_num_hands=2,
                                 min_tracking_confidence=0.1,
                                 min_detection_confidence=0.1)

mpDraw = mp.solutions.drawing_utils

HOST = '127.0.0.1'
PORT = 65432
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket_connection:
        socket_connection.connect((HOST, PORT))
        while True:
            _, image = web_cam.read()
            result = hands.process(image)
            print(result)
            if result.multi_hand_landmarks:
                for one in result.multi_hand_landmarks:
                    for id, lm in enumerate(one.landmark):
                        print("ID=  ", id)
                        print("Landmark=   ", lm)
                        h, w, _ = image.shape
                        c_x, c_y = int(lm.x * w), int(lm.y * h)
                        cv2.circle(image, (c_x, c_y), 5, (240, 160, 80))
                        pointers = [4, 8, 12, 16, 20, 0]
                        if id in pointers:
                            """ Importing here two instance of players"""
                            cv2.circle(image, (c_x, c_y), 18, (60, 107, 225), cv2.FILLED)
                            a, b = c_x / 4, c_y / 2
                            print(f"ID={id}    LM={lm}   A={a} B={b}")
                            # cv2.rectangle(image, (c_x, c_y), (40, 40), (82, 28, 210), thickness=2)
                            X_H, Y_W = abs(h - c_x), abs(w - c_y)
                            dict_data = {'id_port': id,'c_x': c_x,'c_y': c_y,'height': X_H,'width': Y_W}
                            # check size
                            string_data = str(dict_data) + "\n"
                            bytes_data = string_data.encode('utf-8')
                            print(sys.getsizeof(bytes_data) , " = Bytes")
                            # bytes_data = [id,c_x,c_y,X_H,Y_W]
                            socket_connection.sendall(bytes_data)
                    mpDraw.draw_landmarks(image, one, mp.solutions.hands.HAND_CONNECTIONS)
            cv2.imshow('Camera Capturing', image)
            cv2.waitKey(1)
            if cv2.waitKey(1) == ord('q'):
                break





