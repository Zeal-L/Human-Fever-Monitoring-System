from src.hardware import hardware, grove_rgb_lcd, OledScreen
from src.pages import node, page
from src.pages.setting import passwordPage
from src.storage import readAndWrite
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import time

class PasswordNode(node.Node):

    def __init__(self, prevNode: node.Node):
        super().__init__()
        self.pages = [prevNode]
        self.passwordPage = passwordPage.PasswordPage()
        self.oldPassword = readAndWrite.ReadAndWrite.getValue("password")
        self.newPassword = ""
        self.enterStatus = "old"
        self.curretEnter = ""
        self.passWordLength = 4
        pass

    def showText(self, offset: int = 0):
        
        node.NodeScreen("/home/pi/project/Resource/password.png", "Password", offset)
        OledScreen.disp.image(OledScreen.image)
        OledScreen.disp.display()
        
    def onButton(self) -> None:
        self.curretEnter += str(self.passwordPage.curretSelect)
        self.passwordPage.enteredPassword = len(self.curretEnter)
        if self.enterStatus == "old":
            self.passwordPage.status = 'old'
            if len(self.curretEnter) == len(self.oldPassword):
                self.passwordPage.enteredPassword = 0
                if self.curretEnter == self.oldPassword:
                    self.enterStatus = "new"
                    self.enterEdit = 0
                    self.curretEnter = ""
                else:
                    self.enterEdit = 0
                    self.curretEnter = ""
                    self.passwordPage.status = 'old'
                    node.showErrorScreen("password does not match")
            self.passwordPage.showText()
        if self.enterStatus == "new":
            self.passwordPage.status = 'new'
            if len(self.curretEnter) == self.passWordLength:
                self.newPassword = self.curretEnter
                self.enterStatus = "cfm"
                self.enterEdit = 0
                self.curretEnter = ""
            self.passwordPage.showText()
        if self.enterStatus == "cfm":
            self.passwordPage.status = 'cfm'
            if len(self.curretEnter) == self.passWordLength:
                if self.curretEnter == self.newPassword:
                    self.oldPassword = self.newPassword
                    self.enterStatus = "old"
                    readAndWrite.ReadAndWrite.setValue("password", self.oldPassword)
                    self.enterEdit = 0
                    self.curretEnter = ""
                    page.currentPage = self.pages[0]
                else:
                    self.enterEdit = 0
                    self.curretEnter = ""
                    node.showErrorScreen("password does not match")
                    self.passwordPage.showText()
            else:
                self.passwordPage.showText()
                    
        # OledScreen.clear()
        # page.currentPage = self.pages[0]
        # page.currentPage.currentPage = -1

    def onRotary(self, rotaryValue: int):
        OledScreen.clear()
        subAngle = 1024 / 10
        index = int(rotaryValue / subAngle)
        index = 9 - index
        self.passwordPage.curretSelect = index
        self.passwordPage.showText()
    
    
        
