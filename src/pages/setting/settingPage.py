from src.hardware import hardware, grove_rgb_lcd
from src.pages import node

class SettingNode(node.Node):
    def __init__(self, prevNode: node.Node):
        print(hardware.tempValue)
        pass

    def showText(self):
        grove_rgb_lcd.setText_norefresh("Setting Page   \n               \x00")
    
    def onButton(self):
        # return "did not implement onButton()"
        print("did not implement onButton()")
    
    def onRotary(self, rotaryValue: int):
        grove_rgb_lcd.setText_norefresh(f"Setting Page   \nrotaryValue = {rotaryValue}")
