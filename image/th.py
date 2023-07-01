from flirpy.camera.lepton import Lepton
import cv2
import numpy as np

camera = Lepton()

while True:
    frame = camera.grab()
    
    # 图像翻转
    frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
    frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
    frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
    
    img = frame.astype(np.float32)
    img = 255 * (img - img.min()) / (img.max() - img.min())
    img_col = cv2.applyColorMap(img.astype(np.uint8), cv2.COLORMAP_JET)

    # 获取图像尺寸
    height, width = img.shape[:2]

    # 计算中心像素点坐标
    center_x = int(width / 2)
    center_y = int(height / 2)

    # 获取中心像素点的温度（以摄氏度为单位）
    temperature_kelvin = frame[center_y, center_x]
    temperature_celsius = temperature_kelvin/100 - 273.15

    # 在图像上显示温度
    cv2.putText(img_col, f"{temperature_celsius:.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    # 绘制中心十字
    cv2.drawMarker(img_col, (center_x, center_y), (255, 255, 255), cv2.MARKER_CROSS, 10, 2)

    cv2.imshow("Lepton", img_col)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

camera.close()
cv2.destroyAllWindows()
