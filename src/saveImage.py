import os

class saveImage:

    @staticmethod 
    def saveImg(image, temperature):
        # fever detection threshold
        if temperature > 37.2:
            dir = "/home/pi/project/src/storage/fever"
        else:
            dir = "/home/pi/project/src/storage/fever"
        
        if not os.path.exists(dir):
            os.makedirs(dir)
        
        # filename format
        filename = "{}˚C.jpg".format(temperature)
        path = os.path.join(dir, filename)

        # check for filename duplications
        if os.path.isfile(path):
            i = 2
            while True:
                filename = "{}˚C-{}.jpg".format(temperature, i)
                path = os.path.join(dir, filename)
                if not os.path.isfile(path):
                    break
                i += 1
        
        image.save(path)
