from src.hardware import hardware, grove_rgb_lcd, OledScreen
from src.pages import page
from src.storage import readAndWrite
# from src.camera import camera
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

class FaceTempPage(page.Page):
    def __init__(self):
        print(hardware.Temp_humidity.tempValue)
        self.prevTemp = 39
        self.frame = 5
        pass

    def showText(self, offset: int = 0):
        # if self.prevTemp == hardware.Temp_humidity.tempValue and self.prevHumid == hardware.Temp_humidity.humidityValue:
        #     return
        self.prevTemp = 0
        self.frame = hardware.Temp_humidity.humidityValue
        yoffset = -9
        offset = -10
        OledScreen.clear()
        icon = Image.open("/home/pi/project/Resource/face.png")
        icon.thumbnail((OledScreen.width, 20))  # Resize the icon to fit within the screen height
        _, icon_height = icon.size
        icon_x = 13
        icon_y = (OledScreen.height - icon_height) // 2 - 15  # Adjust the value as needed
        OledScreen.image.paste(icon, (icon_x-offset, icon_y-yoffset))

        # Draw an icon
        icon = Image.open("/home/pi/project/Resource/frame.png")
        icon.thumbnail((OledScreen.width, 20))  # Resize the icon to fit within the screen height
        _, icon_height = icon.size
        icon_x = 10
        icon_y = (OledScreen.height - icon_height) // 2 + 13  # Adjust the value as needed
        OledScreen.image.paste(icon, (icon_x-offset, icon_y-yoffset))

        # Load a default font
        # font = ImageFont.load_default()
        # change font size
        font = ImageFont.truetype("/home/pi/project/Resource/Arial.ttf", 15)

        # Display temperature
        temperature = "{:.2f} C".format(self.prevTemp) if self.prevTemp != 0 else "N/A"
        temperature_width, temperature_height = font.getsize(temperature)
        temperature_x = OledScreen.width - temperature_width - 35
        temperature_y = (OledScreen.height - temperature_height) // 2 - 15  # Adjust the value as needed
        OledScreen.draw.text((temperature_x-offset, temperature_y-yoffset), temperature, font=font, fill=255)

        # Display humidity
        humidity =  str(self.frame)
        humidity_width, humidity_height = font.getsize(humidity)
        humidity_x = OledScreen.width - humidity_width - 35
        humidity_y = (OledScreen.height - humidity_height) // 2 + 13  # Adjust the value as needed
        OledScreen.draw.text((humidity_x-offset, humidity_y-yoffset), humidity, font=font, fill=255)
        

        font = ImageFont.load_default()
        text = "body temperature"
        text_width, text_height = OledScreen.draw.textsize(text, font=font)
        text_x = (OledScreen.width - text_width) // 2
        text_y = 0
        OledScreen.draw.text((text_x, text_y), text, font=font, fill=255)
        
        OledScreen.disp.image(OledScreen.image)
        OledScreen.disp.display()


    def showTextChangable(self):
        return True
        
        