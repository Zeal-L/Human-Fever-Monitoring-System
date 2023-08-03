import os
import time
import cv2

class saveImage:

    @staticmethod 
    def saveImg(image, temperature):
        # fever detection threshold
        if temperature > 37.2:
            dir = "/home/pi/project/src/storage/fever"
            # get unix timestamp
            if not os.path.exists(dir):
                os.makedirs(dir)
            
            currTimeStamp = str(time.time())
            print(currTimeStamp)
            # filename format
            filename = currTimeStamp + "-{:.2f}.jpg".format(temperature)
            # 2 ds of temperature
            path = os.path.join(dir, filename)
            
            # save image
            cv2.imwrite(path, image)
