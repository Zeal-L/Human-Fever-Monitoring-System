from abc import ABC, abstractmethod
from typing import Optional

currentPage = None

class Page(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def showText(self):
        return "did not implement showText()"