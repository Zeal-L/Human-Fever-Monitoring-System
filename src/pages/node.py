from abc import ABC, abstractmethod
from typing import Optional
from src.pages import page

class Node(page.Page):
    @abstractmethod
    def onButton(self):
        # return "did not implement onButton()"
        print("did not implement onButton()")
    
    @abstractmethod
    def onRotary(self, rotaryValue: int):
        # return "did not implement onRotary()"
        print("did not implement onRotary()")