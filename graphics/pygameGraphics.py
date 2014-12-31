
import pygame
from pygame.locals import *
from threading import Lock

class pygameGraphics():
    def init(self, size=None):
        self.font = pygame.image.load("font.bmp")
        self.letter_w = self.font.get_width() // 16
        self.letter_h = self.font.get_height() // 16
        if not size:
            info = pygame.display.Info()
            w = info.current_w
            h = info.current_h
            if w < self.letter_w * 80 or h < self.letter_h * 50:
                self.display = pygame.display.set_mode((w,h), HWSURFACE|DOUBLEBUF|FULLSCREEN)
                self.w = w // self.letter_w
                self.h = h // self.letter_h
            else:
                self.display = pygame.display.set_mode((80*self.letter_w, 50*self.letter_h), HWSURFACE|DOUBLEBUF|RESIZABLE)
                self.w = 80
                self.h = 50
        else:
            self.display = pygame.display.set_mode((size[0]*self.letter_w, size[1]*self.letter_h), HWSURFACE|DOUBLEBUF|RESIZABLE)
            self.w = size[0]
            self.h = size[1]

#        self.displaybuff = pygame.Surface((self.display.get_width(), self.display.get_height()), HWSURFACE)
        self.lock = Lock()
        self.buff = []
        black = pygame.Color("black")
        white = pygame.Color(0xdddddd)
        for y in range(self.h):
            self.buff.append([])
            for x in range(self.w):
                self.buff[y].append([32, 0, 0xaaaaaa])
        self.modified = [pygame.Rect(0,0,self.w, self.h)]
        self.cursor = 0
        self.cursorloc = (0,0)
        self.cursorback = self.buff[0][0][:]
        self.charbuffer = pygame.Surface((self.letter_w, self.letter_h), HWSURFACE)
        self.charbuffer.set_colorkey(0)
        self.cursortimer = 0
        self.cursortoggle = True
        self.update()

    def uninit(self):
        pygame.display.quit()

    def update(self):
        self.lock.acquire()
        self.cursorback = self.buff[self.cursorloc[0]][self.cursorloc[1]][:]
        for area in self.modified:
            for y in range(area.y, area.y+area.h):
                for x in range(area.x, area.x+area.w):
                    self._drawchar(self.buff[y][x], y, x)
        self.modified = []
#        self.display.blit(self.displaybuff, (0,0))
        pygame.display.flip()
        self.lock.release()

    def _drawchar(self, c, y, x):
        self.charbuffer.fill(c[2])
        sx = c[0] % 16 * self.letter_w
        sy = c[0] // 16 * self.letter_h
        self.charbuffer.blit(self.font,(-sx,-sy), special_flags=BLEND_MULT)
        self.display.fill(c[1], pygame.Rect(x*self.letter_w, y*self.letter_h, self.letter_w, self.letter_h))
        self.display.blit(self.charbuffer, (x*self.letter_w, y*self.letter_h))

    def draw(self, dt):
        self.lock.acquire()
        self.cursortimer -= dt
        if self.cursortimer <= 0:
            if self.cursortoggle:
                self._drawchar([self.cursorback[0], self.cursorback[2], self.cursorback[1]],
                        *self.cursorloc)
#                self.display.blit(self.displaybuff, (0,0))
                pygame.display.flip()
            else:
                self._drawchar(self.cursorback, *self.cursorloc)
#                self.display.blit(self.displaybuff, (0,0))
                pygame.display.flip()
            self.cursortoggle = not self.cursortoggle
            self.cursortimer = 600
        self.lock.release()

    def resize(self, w, h):
        self.lock.acquire()
        oldw = self.w
        oldh = self.h
        self.w = w
        self.h = h
        self.display = pygame.display.set_mode((w*self.letter_w, h*self.letter_h), HWSURFACE|DOUBLEBUF|RESIZABLE)
# remove front buffer
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
        self.lock.release()
        self.update()

    def setCursor(self, c):
        self.lock.acquire()
        self.cursor = c
        self.cursortimer = 0
        self.cursortoggle = True
        self.lock.release()

    def setCursorPosition(self, y, x):
        self.lock.acquire()
        self.cursorloc = (y,x)
        self.cursortimer = 0
        self.cursortoggle = True
        self.lock.release()

    def setBackground(self, x, y, w, h, color):
        self.lock.acquire()
        for i in range(y, y+h):
            for j in range(x, x+w):
                self.buff[i][j][1] = color
        self.modified.append(pygame.Rect(x,y,w,h))
        self.lock.release()

    def setForeground(self, x, y, w, h, color):
        self.lock.acquire()
        for i in range(y, y+h):
            for j in range(x, x+h):
                self.buff[i][j][2] = color
        self.modified.append(pygame.Rect(x,y,w,h))
        self.lock.release()

    def addString(self, message, color=None):
        self.addString(self.cursorloc[0], self.cursorloc[1], message, color)

    def addString(self, y, x, message, color=None):
        self.lock.acquire()
        if type(message) is str:
            message = message.encode("cp437")
        for i in range(min(len(message), self.w - x)):
            self.buff[y][x+i][0] = message[i]
            if color:
                self.buff[y][x+i][2] = color
        self.modified.append(pygame.Rect(x, y, len(message), 1))
        self.lock.release()

    def scroll(self, x, y, w, h, n=1):
        self.lock.acquire()
        if n > 0:
            for i in range(y, y+h-n):
                self.buff[i] = self.buff[i+n]
            for i in range(y+h-n, y+h):
                for j in range(x, x+w):
                    self.buff[i][j][0] = 32
        elif n < 0:
            for i in reversed(range(y-n, y+h)):
                self.buff[i] = self.buff[i+n]
            for i in range(y, y-n):
                for j in range(x, x+w):
                    self.buff[i][j][0] = 32
        self.modified.append(pygame.Rect(x,y,w,h))
        self.lock.release()

    def hscroll(self, x, y, w, h, n=1):
        self.lock.acquire()
        if n > 0:
            for i in range(y, y+h):
                self.buff[i][x:x+h-n] = self.buff[i][x+n:x+h]
                for j in range(x+w-n, x+w):
                    self.buff[i][j][0] = 32
        elif n < 0:
            for i in range(y, y+h):
                self.buff[i][x-n:x+h] = self.buff[i][x:x+h+n]
                for j in range(x, x-n):
                    self.buff[i][j][0] = 32
        self.modified.append(pygame.Rect(x,y,w,h))
        self.lock.release()
