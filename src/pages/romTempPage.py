from src.hardware import hardware, grove_rgb_lcd, OledScreen
from src.pages import page
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

class RomTempPage(page.Page):
    def __init__(self):
        print(hardware.tempValue)
        pass

    def showText(self):
        grove_rgb_lcd.setText_norefresh("temp = %.02f C  humidity = %.02f%%"%(hardware.getTempValue(), hardware.getHumidityValue()))
        OledScreen.clear()
        icon = Image.open("/home/pi/project/Resource/temp.png")
        icon.thumbnail((OledScreen.width, 20))  # Resize the icon to fit within the screen height
        icon_width, icon_height = icon.size
        icon_x = 13
        icon_y = (OledScreen.height - icon_height) // 2 - 15  # Adjust the value as needed
        OledScreen.image.paste(icon, (icon_x, icon_y))

        # Draw an icon
        icon = Image.open("/home/pi/project/Resource/humid.png")
        icon.thumbnail((OledScreen.width, 20))  # Resize the icon to fit within the screen height
        icon_width, icon_height = icon.size
        icon_x = 10
        icon_y = (OledScreen.height - icon_height) // 2 + 15  # Adjust the value as needed
        OledScreen.image.paste(icon, (icon_x, icon_y))

        # Load a default font
        font = ImageFont.load_default()
        # change font size
        font = ImageFont.truetype("/home/pi/project/Resource/Arial.ttf", 15)

        # Display temperature
        temperature = str(hardware.getTempValue())
        temperature_width, temperature_height = font.getsize(temperature)
        temperature_x = OledScreen.width - temperature_width - 48
        temperature_y = (OledScreen.height - temperature_height) // 2 - 15  # Adjust the value as needed
        OledScreen.draw.text((temperature_x, temperature_y), temperature, font=font, fill=255)

        # Display humidity
        humidity = str(hardware.getHumidityValue())
        humidity_width, humidity_height = font.getsize(humidity)
        humidity_x = OledScreen.width - humidity_width - 50
        humidity_y = (OledScreen.height - humidity_height) // 2 + 15  # Adjust the value as needed
        OledScreen.draw.text((humidity_x, humidity_y), humidity, font=font, fill=255)
        
        
        OledScreen.disp.image(OledScreen.image)
        OledScreen.disp.display()

    def showTextChangable(self):
        return True
    