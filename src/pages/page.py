from abc import ABC, abstractmethod
from typing import Optional

class Page(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def showText(self) -> str:
        return "did not implement showText()"
    
    @abstractmethod
    def onButton(self) -> None:
        # return "did not implement onButton()"
        print("did not implement onButton()")
    
    @abstractmethod
    def onRotary(self, value: int) -> None:
        # return "did not implement onRotary()"
        print("did not implement onRotary()")
    