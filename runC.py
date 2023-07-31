import subprocess
import json
# 1. 使用subprocess运行lsblk -J命令并获取输出
lsblk_output = subprocess.check_output(['lsblk', '-p', '-J'])

# 2. 将输出转换为Python对象 
lsblk = json.loads(lsblk_output)
for device in lsblk['blockdevices']:
    print(device['name'], device['size'], device['mountpoint'], device['type'])