
from threading import Lock

class Graphics:
    def init(self,size=None):
        pass

    def uninit(self):
        pass

    def update(self):
        pass

    def draw(self):
        pass

    def resize(self, size=None):
        pass

    def getInput(x, y, width=0, linebreak=False):
        pass

    def getKeyPress():
        pass

    def showCursor():
        pass

    def setCursorPosition():
        pass

    def showCursor(highlight):
        pass

    def hideCursor():
        pass

    def moveCursor(x,y):
        pass

    def setColor(col):
        pass

    def setBackground(x, y, w, h, color):
        pass

    def setForeground(x, y, w, h, color):
        pass

    def addString(message, color=None):
        pass

    def addString(x, y, message, color=None):
        pass

    def scroll(x, y, w, h, n=1):
        pass

