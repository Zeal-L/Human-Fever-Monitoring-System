from src.hardware import hardware, grove_rgb_lcd, OledScreen
from src.pages import page
# from src.camera import camera
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

class FaceTempPage(page.Page):
    def __init__(self):
        print(hardware.Temp_humidity.tempValue)
        self.prevTemp = 0
        self.prevHumid = hardware.Temp_humidity.humidityValue
        pass

    def showText(self, offset: int = 0):
        # if self.prevTemp == hardware.Temp_humidity.tempValue and self.prevHumid == hardware.Temp_humidity.humidityValue:
        #     return
        self.prevTemp = 0
        self.prevHumid = hardware.Temp_humidity.humidityValue
        grove_rgb_lcd.setText_norefresh("temp = %.02f C  Nframe = %.02f%%"%(self.prevTemp, hardware.Temp_humidity.humidityValue))
        OledScreen.clear()
        icon = Image.open("/home/pi/project/Resource/face.png")
        icon.thumbnail((OledScreen.width, 20))  # Resize the icon to fit within the screen height
        icon_width, icon_height = icon.size
        icon_x = 11
        icon_y = (OledScreen.height - icon_height) // 2 - 15  # Adjust the value as needed
        OledScreen.image.paste(icon, (icon_x-offset, icon_y))

        # Draw an icon
        icon = Image.open("/home/pi/project/Resource/frame.png")
        icon.thumbnail((OledScreen.width, 20))  # Resize the icon to fit within the screen height
        icon_width, icon_height = icon.size
        icon_x = 10
        icon_y = (OledScreen.height - icon_height) // 2 + 15 
        OledScreen.image.paste(icon, (icon_x-offset, icon_y))

        # Load a default font
        font = ImageFont.load_default()
        # change font size
        font = ImageFont.truetype("/home/pi/project/Resource/Arial.ttf", 15)

        
        temperature = "{:.2f} C".format(self.prevTemp) if self.prevTemp != 0 else "N/A"
        temperature_width, temperature_height = font.getsize(temperature)
        temperature_x = OledScreen.width - temperature_width - 38
        temperature_y = (OledScreen.height - temperature_height) // 2 - 15
        OledScreen.draw.text((temperature_x-offset, temperature_y), temperature, font=font, fill=255)

        # Display humidity
        Nframe = "0"
        Nframe_width, Nframe_height = font.getsize(Nframe)
        Nframe_x = OledScreen.width - Nframe_width - 50
        Nframe_y = (OledScreen.height - Nframe_height) // 2 + 15  # Adjust the value as needed
        OledScreen.draw.text((Nframe_x-offset, Nframe_y), Nframe, font=font, fill=255)
        
        OledScreen.disp.image(OledScreen.image)
        OledScreen.disp.display()

    def showTextChangable(self):
        return True
    