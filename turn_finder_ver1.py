import math

import cv2


# 1 == LEFT
# 2 == RIGHT
# 3 == PASS
def get_line_side(img, line) -> int:
    height, width, _ = img.shape
    x1, y1, x2, y2 = line[0]
    if x1 == x2:
        return 0

    slope = (y2 - y1) / (x2 - x1)

    if slope == 0:
        return 0

    y_intercept = y1 - slope * x1
    x_intercept_left = -y_intercept / slope
    x_intercept_right = (height - y_intercept) / slope
    if x_intercept_left < width / 2 and x_intercept_right < width / 2:
        return 1
    elif x_intercept_left > width / 2 and x_intercept_right > width / 2:
        return 2
    else:
        return 0



cap = cv2.VideoCapture(0)

# Video parametrs
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

while True:
    # Video
    ret, frame = cap.read()

    # Video capture success
    if not ret:
        break

    # Converting image to scaling gray
    # Перетворюємо зображення в градації сірого.
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Using Gauss filter to reduce noise
    # Використовуємо фільтр Гаусса для зменшення шуму на зображенні.
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    # Using Canny algorithm to find edges in image
    # Використовуємо алгоритм Canny для виявлення границь на зображенні.
    edges = cv2.Canny(blur, 50, 150)


    # Використовуємо алгоритм Хафа для знаходження ліній на зображенні.
    lines = cv2.HoughLinesP(edges, 1, math.pi / 180, 50, minLineLength=50, maxLineGap=50)

    # Filtering finded lines
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
            line_side = get_line_side(frame, line)
            if line_side == 1:
                cv2.putText(frame, 'LEFT', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
            elif line_side == 2:
                cv2.putText(frame, 'RIGHT', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

    # Showing image
    cv2.imshow('frame', frame)

    #Escape end program
    if cv2.waitKey(1) == 27:
        break
