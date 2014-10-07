import curses
import curses.ascii

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
            word = word[width:] #TODO
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
    # TODO

def addstr(msg):
    std.addstr(msg)


def getline():
    buff = []
    c = 0
    while c != ord('\n'):
        c = std.getch()
        y, x = std.getyx()
        ind = (y - sy) * width + x - sx
        if curses.ascii.isprint(c):
            buff.insert(ind, chr(c))
            std.clrtobot()
            addstr("".join(buff[ind:]))
            if x != width -1:
                std.move(y, x+1)
            elif y != height - 1:
                std.move(y+1, 0)
            else:
                std.scroll()
                std.move(y, 0)
        elif c == curses.KEY_LEFT and ind != 0:
            if x != 0:
                std.move(y, x-1)
            else:
                std.move(y-1, width-1)
        elif c == curses.KEY_RIGHT and ind != len(buff):
            if x != width - 1:
                std.move(y, x+1)
            else:
                std.move(y+1, 0)
        elif c == curses.KEY_BACKSPACE and ind != 0:
            del buff[ind-1]
            std.clrtobot()
            if x != 0:
                std.move(y, x-1)
            else:
                std.move(y-1, width-1)
            addstr("".join(buff[ind-1:]))
            if x != 0:
                std.move(y, x-1)
            else:
                std.move(y-1, width-1)
        elif c == curses.KEY_DC and ind != len(buff):
            del buff[ind]
            std.clrtobot()
            addstr("".join(buff[ind:]))
            std.move(y, x)
        elif c == curses.KEY_HOME and ind != 0:
            std.move(sy, sx)
        elif c == curses.KEY_END and ind != len(buff):
            std.move(sy, sx)
            std.clrtobot()
            addstr("".join(buff))
    return "".join(buff)
