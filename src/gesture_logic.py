import math

def distance(a, b):
    return math.hypot(a.x - b.x, a.y - b.y)


def count_fingers(landmarks):
    fingers = 0
    wrist = landmarks[0]

    finger_tips = [8, 12, 16, 20]
    finger_pips = [6, 10, 14, 18]

    for tip, pip in zip(finger_tips, finger_pips):
        if landmarks[tip].y < landmarks[pip].y:
            fingers += 1

    return fingers

def is_thumbs_up(landmarks):
    thumb_up = landmarks[4].y < landmarks[3].y

    other_fingers_closed = all([
        landmarks[8].y > landmarks[6].y,
        landmarks[12].y > landmarks[10].y,
        landmarks[16].y > landmarks[14].y,
        landmarks[20].y > landmarks[18].y
    ])

    return thumb_up and other_fingers_closed

    # ---------- OTHER FINGERS ----------
    finger_sets = [
        (8, 6, 5),   # Index
        (12, 10, 9), # Middle
        (16, 14, 13),# Ring
        (20, 18, 17) # Pinky
    ]

    for tip, pip, mcp in finger_sets:
        if (
            landmarks[tip].y < landmarks[pip].y and
            landmarks[tip].y < landmarks[mcp].y and
            distance(landmarks[tip], wrist) > distance(landmarks[pip], wrist)
        ):
            fingers += 1

    return fingers


def is_thumbs_up(landmarks):
    thumb_up = landmarks[4].y < landmarks[3].y

    other_fingers_closed = all([
        landmarks[8].y > landmarks[6].y,
        landmarks[12].y > landmarks[10].y,
        landmarks[16].y > landmarks[14].y,
        landmarks[20].y > landmarks[18].y
    ])

    return thumb_up and other_fingers_closed


def recognize_gesture(hand_landmarks):
    landmarks = hand_landmarks.landmark

    if is_thumbs_up(landmarks):
        return "THUMBS UP 👍"

    fingers = count_fingers(landmarks)

    if fingers == 0:
        return "FIST ✊"
    elif fingers == 1:
        return "ONE ☝️"
    elif fingers == 2:
        return "TWO ✌️"
    elif fingers == 3:
        return "THREE 🤟"
    elif fingers == 4:
        return "FOUR ✋"
    elif fingers == 5:
        return "OPEN PALM 🖐️"
    else:
        return "UNKNOWN"
