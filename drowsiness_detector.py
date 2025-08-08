import cv2
import time
import pygame
import mediapipe as mp
import math
import os
import numpy as np

# Initialize pygame mixer
pygame.mixer.init()
pygame.mixer.music.load(r"C:\Users\dravi\OneDrive\Desktop\opencv_project\script\alarm3.mp3")

# Thresholds
EAR_THRESHOLD = 0.25
CLOSE_DURATION = 3

# Eye landmarks
LEFT_EYE = [33, 160, 158, 133, 153, 144]
RIGHT_EYE = [362, 385, 387, 263, 373, 380]

# Mediapipe setup
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True)
mp_drawing = mp.solutions.drawing_utils

# Distance calculation
def euclidean_distance(p1, p2):
    return math.hypot(p1[0] - p2[0], p1[1] - p2[1])

# EAR calculation
def get_ear(landmarks, eye_points, img_w, img_h):
    coords = [(int(landmarks[p].x * img_w), int(landmarks[p].y * img_h)) for p in eye_points]
    vertical1 = euclidean_distance(coords[1], coords[5])
    vertical2 = euclidean_distance(coords[2], coords[4])
    horizontal = euclidean_distance(coords[0], coords[3])
    ear = (vertical1 + vertical2) / (2.0 * horizontal)
    return ear

# Load refreshment images from folder
def load_refreshment_images(folder_path):
    images = []
    for file in os.listdir(folder_path):
        img_path = os.path.join(folder_path, file)
        img = cv2.imread(img_path)
        if img is not None:
            img = cv2.resize(img, (200, 200))
            images.append(img)
    return images

# Display stacked image window
def show_refreshment_window(images):
    if not images:
        return
    stacked = cv2.vconcat(images)
    cv2.imshow("Refreshments", stacked)

# Set path to your image folder
refreshment_folder = r"C:\Users\dravi\OneDrive\Desktop\opencv_project\script\refreshments"
refreshments = load_refreshment_images(refreshment_folder)

# Camera setup
cap = cv2.VideoCapture(0)

eyes_closed_start = None
alarm_playing = False

print("Deep Eye Drowsiness Detection started...")

while True:
    success, frame = cap.read()
    if not success:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img_h, img_w = frame.shape[:2]

    results = face_mesh.process(rgb)

    if results.multi_face_landmarks:
        landmarks = results.multi_face_landmarks[0].landmark

        left_ear = get_ear(landmarks, LEFT_EYE, img_w, img_h)
        right_ear = get_ear(landmarks, RIGHT_EYE, img_w, img_h)
        avg_ear = (left_ear + right_ear) / 2

        mp_drawing.draw_landmarks(
            frame, results.multi_face_landmarks[0], mp_face_mesh.FACEMESH_CONTOURS,
            landmark_drawing_spec=None,
            connection_drawing_spec=mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=1, circle_radius=1)
        )

        if avg_ear < EAR_THRESHOLD:
            if eyes_closed_start is None:
                eyes_closed_start = time.time()
            elif time.time() - eyes_closed_start > CLOSE_DURATION:
                if not alarm_playing:
                    print("Eyes closed too long. Alarm ON.")
                    pygame.mixer.music.play(-1)
                    alarm_playing = True
                    show_refreshment_window(refreshments)
        else:
            eyes_closed_start = None
            if alarm_playing:
                print("Eyes open. Alarm OFF.")
                pygame.mixer.music.stop()
                alarm_playing = False
                cv2.destroyWindow("Refreshments")

    cv2.imshow("Deep Drowsiness Detector", frame)

    if cv2.waitKey(1) & 0xFF == 27:  # ESC to quit
        break

cap.release()
cv2.destroyAllWindows()
pygame.mixer.music.stop()
