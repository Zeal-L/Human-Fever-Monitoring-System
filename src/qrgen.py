import qrcode as qr
from PIL import Image

class qrgen:
    
    @staticmethod   
    def generateQR(temperature):
        data = 'Your temperature is {}'.format(temperature)
        img = qr.make(data)

        img = img.resize((64, 64))

        # show the image
        # change to display on screen
        img.show()

'''
test code 

qrg = qrgen()
qrg.generateQR(36.5)
'''
