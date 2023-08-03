import os
import shutil
import pyudev

def detect_usb_device():
    context = pyudev.Context()
    for device in context.list_devices(subsystem='block', DEVTYPE='disk'):
        print(device)
        if 'usb' in device.get('ID_BUS'):
            return device.device_node
    return None

def write_file_to_usb(usb_path, file_path):
    try:
        shutil.copy(file_path, usb_path)
        print("文件写入成功！")
    except Exception as e:
        print("文件写入失败：", e)

if __name__ == "__main__":
    usb_path = detect_usb_device()
    if usb_path:
        file_to_write = "/home/pi/project/qrcode.png"  # 替换为您想写入的文件路径
        write_file_to_usb(usb_path, file_to_write)
    else:
        print("未检测到U盘。")
