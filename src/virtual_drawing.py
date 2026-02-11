import cv2
import numpy as np
import mediapipe as mp

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

# Canvas
canvas = None

# Default settings
draw_color = (255, 0, 255)  # Purple
brush_thickness = 5
eraser_thickness = 40
mode = "DRAW"

xp, yp = 0, 0

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)

    if canvas is None:
        canvas = np.zeros_like(img)

    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            lmList = []

            for id, lm in enumerate(handLms.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append((cx, cy))

            mp_draw.draw_landmarks(img, handLms, mp_hands.HAND_CONNECTIONS)

            if len(lmList) != 0:

                x1, y1 = lmList[8]   # Index finger
                x2, y2 = lmList[12]  # Middle finger

                # Detect which fingers are up
                fingers = []

                # Thumb
                if lmList[4][0] > lmList[3][0]:
                    fingers.append(1)
                else:
                    fingers.append(0)

                # Other fingers
                tips = [8, 12, 16, 20]
                pip = [6, 10, 14, 18]

                for tip, p in zip(tips, pip):
                    if lmList[tip][1] < lmList[p][1]:
                        fingers.append(1)
                    else:
                        fingers.append(0)

                # ✏ DRAW MODE (Only index finger up)
                if fingers[1] == 1 and fingers[2] == 0:
                    mode = "DRAW"

                    cv2.circle(img, (x1, y1), 10, draw_color, cv2.FILLED)

                    if xp == 0 and yp == 0:
                        xp, yp = x1, y1

                    thickness = eraser_thickness if draw_color == (0, 0, 0) else brush_thickness

                    cv2.line(img, (xp, yp), (x1, y1), draw_color, thickness)
                    cv2.line(canvas, (xp, yp), (x1, y1), draw_color, thickness)

                    xp, yp = x1, y1

                # 🎛 SELECT MODE (Index + Middle up)
                elif fingers[1] == 1 and fingers[2] == 1:
                    xp, yp = 0, 0
                    mode = "SELECT"

                    # Color selection area (top bar)
                    if y1 < 100:

                        if 0 < x1 < 100:
                            draw_color = (255, 0, 255)  # Purple

                        elif 100 < x1 < 200:
                            draw_color = (255, 0, 0)  # Blue

                        elif 200 < x1 < 300:
                            draw_color = (0, 255, 0)  # Green

                        elif 300 < x1 < 400:
                            draw_color = (0, 0, 255)  # Red

                        elif 400 < x1 < 500:
                            draw_color = (0, 0, 0)  # BLACK (Real black)

                        elif 500 < x1 < 600:
                            canvas = np.zeros_like(img)  # Clear

                        elif 600 < x1 < 700:
                            cv2.imwrite("drawing.png", canvas)
                            print("Image Saved ✅")

    # Merge canvas
    gray = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY)
    _, inv = cv2.threshold(gray, 20, 255, cv2.THRESH_BINARY_INV)
    inv = cv2.cvtColor(inv, cv2.COLOR_GRAY2BGR)
    img = cv2.bitwise_and(img, inv)
    img = cv2.bitwise_or(img, canvas)

    # UI Top Bar
    cv2.rectangle(img, (0, 0), (100, 100), (255, 0, 255), cv2.FILLED)
    cv2.rectangle(img, (100, 0), (200, 100), (255, 0, 0), cv2.FILLED)
    cv2.rectangle(img, (200, 0), (300, 100), (0, 255, 0), cv2.FILLED)
    cv2.rectangle(img, (300, 0), (400, 100), (0, 0, 255), cv2.FILLED)
    cv2.rectangle(img, (400, 0), (500, 100), (0, 0, 0), cv2.FILLED)
    cv2.rectangle(img, (500, 0), (600, 100), (50, 50, 50), cv2.FILLED)
    cv2.putText(img, "CLEAR", (510, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 2)
    cv2.rectangle(img, (600, 0), (700, 100), (100, 100, 100), cv2.FILLED)
    cv2.putText(img, "SAVE", (620, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 2)

    # Mode indicator
    cv2.putText(img, f"MODE: {mode}", (20, 460),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 3)

    cv2.imshow("AI Drawing App - Arsala Edition 🎨", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
