import cv2
import mediapipe as mp
import numpy as np
import math

class HandTracking:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands()
        self.mp_draw = mp.solutions.drawing_utils
        self.cap = cv2.VideoCapture(0)
        self.left_hand_position = {'x':0, 'y':0}
        self.right_hand_position = {'x':0, 'y':0}
        self.left_hand_gesture = "unknown"
        self.right_hand_gesture = "unknown"
    
    def calculate_distance(self, hand_landmarks):
        palm_width = math.sqrt(
            (hand_landmarks.landmark[5].x - hand_landmarks.landmark[17].x)**2 +
            (hand_landmarks.landmark[5].y - hand_landmarks.landmark[17].y)**2
        )
        estimated_distance = 0.1 / palm_width
        return estimated_distance

    def get_position(self, x, y, width, height):
        ret_x: float = round((x / width)* 100, 2)
        ret_y: float = round((y / height) * 100, 2)
        return {"x": ret_x, "y": ret_y}

    def get_hand_center(self, hand_landmarks, width, height):
        landmarks = np.array([(lm.x * width, lm.y * height) for lm in hand_landmarks.landmark])
        return np.mean(landmarks, axis=0)

    def update(self):
        success, image = self.cap.read()
        if not success:
            return

        image = cv2.flip(image, 1)
        height, width, _ = image.shape

        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = self.hands.process(image_rgb)

        self.left_hand_position = self.right_hand_position = None

        if results.multi_hand_landmarks:
            for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
                distance = self.calculate_distance(hand_landmarks)

                if distance <= 3.0:  # 3m以内の手のみを処理
                    self.mp_draw.draw_landmarks(image, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)

                    center_x, center_y = self.get_hand_center(hand_landmarks, width, height)
                    cv2.circle(image, (int(center_x), int(center_y)), 5, (0, 0, 255), -1)

                    hand_pos = self.get_position(center_x, center_y, width, height)
                    gesture = self.get_gesture(hand_landmarks)

                    if handedness.classification[0].label == "Left":
                        self.left_hand_position = hand_pos
                        self.left_hand_gesture = gesture
                    else:
                        self.right_hand_position = hand_pos
                        self.right_hand_gesture = gesture

    def get_hand_pos(self):
        return {"left": self.left_hand_position, "right": self.right_hand_position}

    def is_rock(self):
        return {
            "left": self.left_hand_gesture == "rock",
            "right": self.right_hand_gesture == "rock"
        }

    def finish(self):
        self.cap.release()
        self.cv2.destroyAllWindows()

    def get_gesture(self, hand_landmarks):
        finger_tips = [4, 8, 12, 16, 20]
        finger_bases = [2, 5, 9, 13, 17]

        def is_finger_extended(tip, base):
            return hand_landmarks.landmark[tip].y < hand_landmarks.landmark[base].y

        extended_fingers = []
        for i in range(5):
            if i == 0:  # Thumb
                if hand_landmarks.landmark[finger_tips[i]].x < hand_landmarks.landmark[finger_bases[i]].x:
                    extended_fingers.append(True)
                else:
                    extended_fingers.append(False)
            else:
                if is_finger_extended(finger_tips[i], finger_bases[i]):
                    extended_fingers.append(True)
                else:
                    extended_fingers.append(False)

        extended_count = sum(extended_fingers)

        if extended_count <= 1:
            return "rock"
        else:
            return "unknown"
