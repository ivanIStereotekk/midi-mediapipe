import cv2
import mediapipe as mp
import numpy as np
import time

# drawings poses and lines
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
hands = mp.solutions.hands.Hands(static_image_mode=False,
                                 max_num_hands=2,
                                 min_tracking_confidence=0.5,
                                 min_detection_confidence=0.5)

mpDraw = mp.solutions.drawing_utils
# video stream capturing

cap = cv2.VideoCapture(0) # or 1 while two cameras connected

with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        ret, frame = cap.read()
        # Recolor image to RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        # Make detection
        results = pose.process(image)
        result_hands = hands.process(image)
        # Recolor back to BGR
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        # Extract landmarks
        try:
            landmarks = results.pose_landmarks.landmark
            for one in landmarks:
                print('landmark X: ',str(one.x)[::-1][0])
                print('landmark Y: ',str(one.y)[::-1][0])
                print('landmark Z: ',str(one.z)[::-1][0])

                
        except:
            pass
        # Render detections
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                  mp_drawing.DrawingSpec(color=(223, 65, 67), thickness=3, circle_radius=4),
                                  mp_drawing.DrawingSpec(color=(245, 66, 67), thickness=2, circle_radius=1)
                                  )
        print("Pose Connections: >>",mp_pose.POSE_CONNECTIONS)
        # print(mp_pose.PoseLandmark.LEFT_HIP,"LENGTH of Array Pose Connections Lines")
        if result_hands.multi_hand_landmarks:
            for one in result_hands.multi_hand_landmarks:
                mpDraw.draw_landmarks(image, one, mp.solutions.hands.HAND_CONNECTIONS)
        cv2.imshow('Pose and Hand Detection by: - Ivan Goncharov', image)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

#https://github.com/google/mediapipe/tree/master/docs/solutions

#https://github.com/google/mediapipe/blob/master/docs/solutions/pose_classification.md