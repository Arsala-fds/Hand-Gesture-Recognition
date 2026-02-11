import cv2
import math
import subprocess
import mediapipe as mp

# ------------------ BRIGHTNESS CONTROL (MAC - REAL) ------------------
def set_brightness(level):
    level = max(0.1, min(1.0, level))  # brightness tool range
    subprocess.run(["brightness", f"{level}"])


# ------------------ MEDIAPIPE SETUP ------------------
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

# ------------------ DISTANCE ------------------
def distance(p1, p2):
    return math.hypot(p2.x - p1.x, p2.y - p1.y)


# ------------------ MAIN ------------------
def main():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("❌ Camera not opened")
        return

    while True:
        success, frame = cap.read()
        if not success:
            break

        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(rgb)

        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:
                mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                thumb = hand_landmarks.landmark[4]
                index = hand_landmarks.landmark[8]

                d = distance(thumb, index)

                # Map distance → brightness (0.1 to 1.0)
                brightness = (d - 0.02) * 3
                brightness = max(0.1, min(1.0, brightness))

                set_brightness(brightness)

                cv2.putText(
                    frame,
                    f"Brightness: {int(brightness * 100)}%",
                    (20, 50),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 255, 255),
                    2
                )

        cv2.imshow("Gesture Brightness Control (Mac)", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
