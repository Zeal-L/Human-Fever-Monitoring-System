import cv2

cv2.namedWindow("vid", cv2.WINDOW_NORMAL)
# 0 th
cap = cv2.VideoCapture(6)
while True:
    ret, frame = cap.read()
    cv2.imshow("vid", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
