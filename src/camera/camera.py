import time
import cv2
import numpy as np
from src.camera.thermal import Thermal
from src.camera.faceMesh import FaceMeshDetector
from src.camera.rgb_depth import RGB_Depth
from src.hardware import hardware
# from thermal import Thermal
# from faceMesh import FaceMeshDetector
# from rgb_depth import RGB_Depth


class Camera:
    thermal = Thermal()
    faceMesh = FaceMeshDetector()
    rgb_depth = RGB_Depth()
    
    face_T = 0
    
    isStart = True
    
    M = np.array(
        [
            [1.28426396e00, 5.51150439e-17, 1.11131980e02],
            [-1.17976291e-17, 1.36426117e00, -1.07969072e02],
            [-5.45110718e-19, 9.65109729e-20, 1.00000000e00],
        ]
    ).astype(np.float32)
        
    @staticmethod
    def run():
        while True:
            print("1", end=" ")
            thermal_data = Camera.thermal.grab()
            print("2", end=" ")
            color_image, depth_data = Camera.rgb_depth.grab()
            print("3", end=" ")
            face_landmarks_list = Camera.faceMesh.grab(color_image)
            print("4", end=" ")
            aligned_thermal_data = cv2.warpPerspective(
                thermal_data, Camera.M, (color_image.shape[1], color_image.shape[0])
            )
            if face_landmarks_list.__len__() != 0:
                print("5")
                print(get_angle_offset(face_landmarks_list))
                Camera.face_T = Camera.thermal.get_temperature_depth(aligned_thermal_data, face_landmarks_list, depth_data)
                print("{:.2f} C".format(Camera.face_T))
                
        
    

def get_angle_offset(face_landmarks_list):
    currentAngle = 0
    
    # 获取face_landmarks_list里最大和最小的x
    x_max = max(face_landmarks_list, key=lambda x: x[0])[0]
    x_min = min(face_landmarks_list, key=lambda x: x[0])[0]
    
    x_center = (x_max + x_min) / 2
    
    width = 640
    
    # 计算需要移动的角度
    angle_offset = (x_center - width / 2) / width * 60
    
    return angle_offset


if __name__ == "__main__":
    Camera.run()