import qrcode as qr
from PIL import Image

class qrgenerator:
    
    @staticmethod   
    def qrgen(temperature):
        data = 'Your temperature is {}'.format(temperature)
        img = qr.make(data)

        img = img.resize((64, 64))

        # show the image
        img.show()

'''
qrg = qrgenerator()
qrg.qrgen(36.5)
'''
