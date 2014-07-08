import curses

std = None
width = None
height = None
sx, sy = None, None
ex, ey = None, None

def init():
    global std, width, height
    std = curses.initscr()
    height, width = std.getmaxyx()
    curses.curs_set(0)
    curses.noecho()
    curses.cbreak()
    std.keypad(1)
    std.scrollok(1)
    std.clear()
    std.refresh()

def uninit():
    curses.curs_set(1)
    curses.echo()
    curses.nocbreak()
    curses.endwin()

def addmsg(msg, startx=0):
    std.scroll()
    std.move(height - 1, startx)
    words = msg.split(" ")
    x = startx
    for word in words:
        while len(word) > width - startx:
            std.scroll()
            std.move(startx)
            std.addnstr(w, width)
            x = std.getyx()[1]
            word = word[width:]
        else:
            if x + len(word) >= width:
                std.scroll()
                std.move(height - 1, startx)
                x = startx
            std.addstr(word)
            x += len(word)
    std.refresh()

def startinput():
    curses.flushinp()
    curses.curs_set(1)
    global sx, sy
    sy, sx = std.getyx()

def stopinput():
    curses.curs_set(0)
    global ex, ey
    ey, ex = std.getyx()

def deny(msg):
    curses.curs_set(1)
    std.move(ey, ex)
    n = (ey - sy) * width + ex - sx
    
