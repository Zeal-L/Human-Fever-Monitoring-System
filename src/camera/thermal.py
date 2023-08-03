import time
import cv2
import numpy as np
from flirpy.camera.lepton import Lepton

class Thermal:
    def __init__(self):
        self.camera = Lepton()
        self.timer = time.time()

    def grab(self):
        thermal_data = self.camera.grab().astype(np.float32)
        thermal_data = np.rot90(thermal_data, 1)

        # 原始是160x120
        # 将图像放大3倍, 变成 480x360
        thermal_data = cv2.resize(
            thermal_data, (0, 0), fx=3, fy=3, interpolation=cv2.INTER_NEAREST
        )

        # 重新缩放至8位图像
        thermal_img = (
            255
            * (thermal_data - thermal_data.min())
            / (thermal_data.max() - thermal_data.min())
        )

        # 将热敏图像转换为伪彩色图像
        thermal_img = cv2.applyColorMap(
            thermal_img.astype(np.uint8), cv2.FONT_HERSHEY_SIMPLEX
        )

        self.timer = time.time()

        return thermal_img, thermal_data

    def get_temperature_depth(self, thermal_data, face_coordinates, depth_data, Rtemp):
        
        # # 去除face_coordinates里的所有超过图像大小的坐标
        # face_coordinates = [ cor for cor in face_coordinates if cor[0] < thermal_data.shape[0] and cor[1] < thermal_data.shape[1] and cor[0] >= 0 and cor[1] >= 0]
        

        if not face_coordinates:
            return 0

        # 获取face_coordinates里最高的5个温度的值和坐标
        temperatures = [(thermal_data[cor[0], cor[1]], cor) for cor in face_coordinates]
        temperatures = sorted(temperatures, key=lambda x: x[0], reverse=True)[:5]
        temperatures, temperatures_coordinates = zip(*temperatures)

        # print(temperatures / 100 - 273.15)

        avg_temperature = sum(temperatures) / len(temperatures)
        avg_temperature = self.to_celsius(avg_temperature)

        # 统计脸部的平均深度
        face_depth = [depth_data[cor[0], cor[1]] for cor in temperatures_coordinates]

        avg_depth = sum(face_depth) / len(face_depth)

        # mm -> cm
        avg_depth = avg_depth / 10
        # print(f"Depth: {avg_depth} cm")
        
        # data = str(round(avg_temperature, 2)) + ' ' + str(round(avg_depth, 2))
        # with open('data.txt', 'a') as f:
        #     f.write(str(data) + '\n')

        # # 根据脸的距离修正温度 (经验值)
        # k = 0.01
        # avg_temperature = avg_temperature + avg_depth * (0.02 + k * (Rtemp - 22))
        
        print(f"Temperature: {avg_temperature}, Rtemp: {Rtemp}, Depth: {avg_depth}")
        
        stand_temp = self.standardize_temperature(avg_temperature, avg_depth)
        # fitted_temperature = 3.55779053925635e-05 * distance1**2 + -0.01761694145549804 * distance1 + 33.63784631681277
                # processed_temperature = 38 - ( temperature - fitted_temperature) 
                
        k = 0.563 if Rtemp < 22 else -0.5
        env_temp_offset =  k * (Rtemp - 22)
        final_temp = stand_temp + env_temp_offset
        
        return (round(final_temp, 2), avg_depth)
    
    def standardize_temperature(self, temperature, distance):
        # 计算拟合线的值
        x = distance
        fitted_temperature = 3.603211147506769e-05 * x**2 + -0.01777649340384927 * x + 33.651835737110936
        # 计算标准温度
        return (37 - fitted_temperature) + temperature

    def to_celsius(self, data):
        return data / 100 - 273.15

    def __del__(self):
        print("Closing camera")
        self.camera.close()

