from abc import ABC, abstractmethod
from typing import Optional

currentPage = None

class Page(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def showText(self, offset: int = 0):
        return "did not implement showText()"
    
    def showTextChangable(self):
        return False