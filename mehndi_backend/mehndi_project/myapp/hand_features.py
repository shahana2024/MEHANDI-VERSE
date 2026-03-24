import cv2
import mediapipe as mp
import math

mp_hands = mp.solutions.hands

def distance(p1, p2):
    return math.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)

def extract_hand_features(image_path):

    image = cv2.imread(image_path)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    with mp_hands.Hands(static_image_mode=True) as hands:
        results = hands.process(image_rgb)

        if not results.multi_hand_landmarks:
            return None

        landmarks = results.multi_hand_landmarks[0].landmark

        palm_width = distance(landmarks[5], landmarks[17])
        finger_length = distance(landmarks[0], landmarks[12])

        return {
            "palm_width_ratio": palm_width,
            "finger_length_ratio": finger_length
        }