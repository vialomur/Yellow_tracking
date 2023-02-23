import cv2
import numpy as np
import keyboard

H_lower: int = 15
H_upper: int = 35
S_lower: int = 150
S_upper: int = 255
V_lower: int = 20
V_upper: int = 255

lower = np.array([H_lower, S_lower, V_lower])
upper = np.array([H_upper, S_upper, V_upper])

# Capturing webcam footage
webcam_video = cv2.VideoCapture(0)

while True:
    success, video = webcam_video.read() # Reading webcam footage

    img = cv2.cvtColor(video, cv2.COLOR_BGR2HSV) # Converting BGR image to HSV format

    mask = cv2.inRange(img, lower, upper) # Masking the image to find our color

    mask_contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) # Finding contours in mask image

    # Finding position of all contours
    if len(mask_contours) != 0:
        for mask_contour in mask_contours:
            if cv2.contourArea(mask_contour) > 500:
                x, y, w, h = cv2.boundingRect(mask_contour)
                cv2.rectangle(video, (x, y), (x + w, y + h), (0, 0, 255), 3) #drawing rectangle

    cv2.imshow("mask image", mask) # Displaying mask image

    cv2.imshow("window", video) # Displaying webcam image

    cv2.waitKey(1)

    if keyboard.is_pressed('q'):
        cv2.destroyAllWindows()
        webcam_video.release()
        break


