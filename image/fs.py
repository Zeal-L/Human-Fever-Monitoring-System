import cv2
import sys
def get_resolution(camera_index):
    cap = cv2.VideoCapture(int(camera_index))

    # 检查摄像头是否成功打开
    if not cap.isOpened():
        print(f"无法打开摄像头 {camera_index}")
        return

    # 获取分辨率
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # 释放资源
    cap.release()

    return width, height

# 示例用法
# camera_index = sys.argv[1]
for i in range(10):
    resolution = get_resolution(i)

    if resolution is not None:
        print(f"摄像头 {i} 的分辨率为：{resolution[0]} x {resolution[1]}")
