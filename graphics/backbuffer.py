
from pygame import Color
from threading import Lock

class Backbuffer:
    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.letters = []
        self.background = []
        self.foreground = []
        for y in range(h):
            self.letters.append([])
            self.background.apend([])
            self.foreground.append([])
            for x in range(w):
                self.letters[y].append(" ")
                self.background[y].append(Color(0))
                self.foreground[y].append(Color(0xdddddd))
        self.lock = Lock()

    def lock():
        self.lock.acquire()

    def release():
        self.lock.release()

    def getForeground(x,y):
        if x >= self.w or x < 0:
            raise IndexError(x)
        if y >= self.h or y < 0:
            raise IndexError(y)
        return self.foreground[y][x]

    def getBackground(x,y):
        if x >= self.w or x < 0:
            raise IndexError(x)
        if y >= self.h or y < 0:
            raise IndexError(y)
        return self.background[y][x]

    def getCharacter(x,y):
        if x >= self.w or x < 0:
            raise IndexError(x)
        if y >= self.h or y < 0:
            raise IndexError(y)
        return self.letters[y][x]

    def setForeground(x,y, color):
        self.lock()
        if x >= self.w or x < 0:
            raise IndexError(x)
        if y >= self.h or y < 0:
            raise IndexError(y)
       self.foreground[y][x] = color
       self.release()

    def setBackground(x,y, color):
        self.lock()
        if x >= self.w or x < 0:
            raise IndexError(x)
        if y >= self.h or y < 0:
            raise IndexError(y)
        self.background[y][x] = color
        self.release()

    def setChar(x,y, c):
        if x >= self.w or x < 0:
            raise IndexError(x)
        if y >= self.h or y < 0:
            raise IndexError(y)
        self.letters[y][x] = c

    def set(x,y, fg, bg, c):
        if x >= self.w or x < 0:
            raise IndexError(x)
        if y >= self.h or y < 0:
            raise IndexError(y)
        self.letters[y][x] = c
        self.foreground[y][x]=fg
        self.background[y][x]=bg

    def get(x,y):
        if x >= self.w or x < 0:
            raise IndexError(x)
        if y >= self.h or y < 0:
            raise IndexError(y)
        c = self.letters[y][x]
        fg = self.foreground[y][x]
        bg = self.background[y][x]
        return (c, fg, bg)

