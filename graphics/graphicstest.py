import pygame
import pygameGraphics
from pygame.locals import *

pygame.init()

clock = pygame.time.Clock()

running = True

gr = pygameGraphics.pygameGraphics()
gr.init((20, 10))
gr.setCursorPosition(2, 1)
gr.setCursor(1)
gr.addString(0, 0, [5, 16, 28, 13, 4])
gr.addString(1, 1, "Shiny!")
gr.addString(3, 1, "This is a test")
gr.update()

while running:
    dt = clock.tick(10)
    pygame.event.pump()
    gr.draw(dt)
    for evt in pygame.event.get():
        if evt.type==QUIT or evt.type==KEYDOWN and evt.dict["key"] == K_ESCAPE:
            gr.uninit()
            pygame.quit()
            running = False
            break
        elif evt.type==VIDEORESIZE:
            size = evt.dict["size"]
            gr.resize(size[0] // gr.letter_w, size[1] // gr.letter_h)
