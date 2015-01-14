
import pygame, sys
from pygame.locals import *
from threading import Lock

# Differing from curses, w and x comes first, not h or y

class pygameTerminal():
    def __init__(self, size=None, fullscreen=False):
        pygame.init()
        info = pygame.display.Info()
        w, h = info.current_w, info.current_h
        fontname = ""
        if w <= 800 or h <= 600:
            fontname = "font8x8.bmp"
        elif w <= 1200 or h <= 900:
            fontname = "font12x12.bmp"
        else:
            fontname = "font16x16.bmp"
        self.font = pygame.image.load(fontname)
        self.letter_w = self.font.get_width() // 16
        self.letter_h = self.font.get_height() // 16
        if fullscreen:
            self.display = pygame.display.set_mode((w,h), HWSURFACE|DOUBLEBUF|FULLSCREEN)
            self.w = size[0] if size else w // self.letter_w
            self.h = size[1] if size else h // self.letter_h
            self.offset = ((w - self.w * self.letter_w)/2, (h - self.h * self.letter_h)/2)
        else:
            self.w = min(size[0] if size else w // self.letter_w, 80)
            self.h = min(size[1] if size else h // self.letter_h, 50)
            if self.w == w // self.letter_w or self.h == h // self.letter_h:
                self.display = pygame.display.set_mode((w,h), HWSURFACE|DOUBLEBUF|FULLSCREEN)
                self.offset = ((w - self.w * self.letter_w)/2, (h - self.h * self.letter_h)/2)
            else:
                self.display = pygame.display.set_mode((self.w * self.letter_w, self.h * self.letter_h), HWSURFACE|DOUBLEBUF)
                self.offset = (0,0)
        self.buff = []
        for y in range(self.h):
            self.buff.append([])
            for x in range(self.w):
                self.buff[y].append([32, 0, 0xaaaaaa])
        self.modified = [pygame.Rect(0,0,self.w, self.h)]
        self.cursor = 0
        self.cursorloc = (0,0) # x,y
        self.cursorback = self.buff[0][0][:]
        self.charbuffer = pygame.Surface((self.letter_w, self.letter_h), HWSURFACE)
        self.charbuffer.set_colorkey(0)
        self.cursortimer = 0
        self.cursortoggle = True
        self.fps = 20
        self.inputlock = Lock()
        self.drawlock = Lock()
        self.waiting = False
        self.inkey = None
        self.waitclock = pygame.time.Clock()

    def uninit(self):
        pygame.display.quit()

    def draw(self):
        self.drawlock.acquire()
        self.cursorback = self.buff[self.cursorloc[1]][self.cursorloc[0]][:]
        for area in self.modified:
            for y in range(area.y, area.y+area.h):
                for x in range(area.x, area.x+area.w):
                    self._drawchar(self.buff[y][x], x, y)
        self.modified = []
        pygame.display.flip()
        self.drawlock.release()

    def drawcursor(self, d):
        self.drawlock.acquire()
        if d:
            if self.cursor == 1:
                self.charbuffer.fill(self.cursorback[2])
                sx = 95 % 16 * self.letter_w
                sy = 95 // 16 * self.letter_h
                self.charbuffer.blit(self.font, (-sx,-sy), BLEND_MULT)
                self.display.blit(self.charbuffer, (self.cursorloc[0]*self.letter_w, self.cursorloc[1]*self.letter_h))
                pygame.display.flip()
            elif self.cursor == 2:
                self._drawchar([self.cursorback[0], self.cursorback[1], self.cursorback[2]],
                    self.cursorloc[0], self.cursorloc[1])
                pygame.display.flip()
        else:
            self._drawchar(self.cursorback, self.cursorloc[0], self.cursorloc[1])
            pygame.display.flip()
        self.drawlock.release()

    def _drawchar(self, c, x, y):
        self.charbuffer.fill(c[2])
        sx = c[0] % 16 * self.letter_w
        sy = c[0] // 16 * self.letter_h
        self.charbuffer.blit(self.font,(-sx,-sy), special_flags=BLEND_MULT)
        self.display.fill(c[1], (x*self.letter_w, y*self.letter_h, self.letter_w, self.letter_h))
        self.display.blit(self.charbuffer, (x*self.letter_w, y*self.letter_h))

    def run(self):
        self.running = True
        clock = pygame.time.Clock()
        while self.running:
            dt = clock.tick(self.fps)
            self.cursortimer -= dt
            if self.cursortimer <= 0:
                self.drawcursor(self.cursortoggle)
                self.cursortoggle = not self.cursortoggle
                self.cursortimer = 600
            for evt in pygame.event.get():
                if evt.type == QUIT or evt.type == KEYDOWN and evt.dict["key"] == K_ESCAPE:
                    self.running = False
                    break
                elif evt.type == KEYDOWN and self.waiting:
                    self.inkey = evt.dict["key"]
                    self.inputlock.release()

    def resize(self, w, h):
        oldw = self.w
        oldh = self.h
        self.w = w
        self.h = h
        self.display = pygame.display.set_mode((w*self.letter_w, h*self.letter_h), HWSURFACE|DOUBLEBUF)
        if h < oldh:
            self.buff = self.buff[:h]
        else:
            black = pygame.Color("black")
            white = pygame.Color(0xdddddd)
            for i in range(h - oldh):
                self.buff.append([])
                for j in range(w):
                    self.buff.append([32, 0, 0xdddddd])
        if w < oldw:
            for y in range(min(oldh, h)):
                self.buff[y] = self.buff[y][:w]
        else:
            for y in range(min(oldh, h)):
                for x in range(w - oldw):
                    self.buff[y].append([32, 0, 0xdddddd])
        self.modified = [pygame.Rect(0,0,w,h)]
        self.draw()

    def setCursor(self, c):
        self.cursor = c
        self.cursortimer = 0
        self.cursortoggle = True if c != 0 else False

    def setCursorPosition(self, x, y):
        self.cursorloc = (x,y)
        self.cursortimer = 0
        self.cursortoggle = True

    def setBackground(self, x, y, w, h, color):
        for i in range(y, y+h):
            for j in range(x, x+w):
                self.buff[i][j][1] = color
        self.modified.append(pygame.Rect(x,y,w,h))

    def setForeground(self, x, y, w, h, color):
        for i in range(y, y+h):
            for j in range(x, x+h):
                self.buff[i][j][2] = color
        self.modified.append(pygame.Rect(x,y,w,h))

    def addString(self, message, color=None):
        self.addString(self.cursorloc[0], self.cursorloc[1], message, color)

    def addString(self, x, y, message, color=None):
        if type(message) is str:
            message = message.encode("cp437")
        for i in range(min(len(message), self.w - x)):
            self.buff[y][x+i][0] = message[i]
            if color:
                self.buff[y][x+i][2] = color
        self.modified.append(pygame.Rect(x, y, len(message), 1))

    def scroll(self, x, y, w, h, n=1):
        if n > 0:
            for i in range(y, y+h-n):
                self.buff[i] = self.buff[i+n]
            for i in range(y+h-n, y+h):
                for j in range(x, x+w):
                    self.buff[i][j][0] = 0
        elif n < 0:
            for i in reversed(range(y-n, y+h)):
                self.buff[i] = self.buff[i+n]
            for i in range(y, y-n):
                for j in range(x, x+w):
                    self.buff[i][j][0] = 0
        self.modified.append(pygame.Rect(x,y,w,h))

    def hscroll(self, x, y, w, h, n=1):
        if n > 0:
            for i in range(y, y+h):
                self.buff[i][x:x+h-n] = self.buff[i][x+n:x+h]
                for j in range(x+w-n, x+w):
                    self.buff[i][j][0] = 0
        elif n < 0:
            for i in range(y, y+h):
                self.buff[i][x-n:x+h] = self.buff[i][x:x+h+n]
                for j in range(x, x-n):
                    self.buff[i][j][0] = 0
        self.modified.append(pygame.Rect(x,y,w,h))

    def getChar(self):
        self.inputlock.acquire()
        self.waiting = True
        self.inputlock.acquire()
        key = self.inkey
        self.inputlock.release()
        return key

if __name__ == "__main__":
    term = pygameTerminal()
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        term.setCursorPosition(0,0)
        term.setCursor(0)
        term.addString(0, 0, [5, 16, 28, 13, 4])
        term.addString(1, 1, "Shiny!")
        term.addString(3, 1, "This is a test")
        term.draw()
    term.run()
    term.uninit()
