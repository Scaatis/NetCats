import curses

std = curses.initscr()
height, width = std.getmaxyx()
curses.curs_set(1)
curses.noecho()
curses.cbreak()
curses.start_color()

curses.init_pair(4, curses.COLOR_BLUE, curses.COLOR_WHITE)
curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLUE)
curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLUE)
curses.init_pair(3, curses.COLOR_RED, curses.COLOR_WHITE)
curses.init_pair(5, curses.COLOR_BLACK, curses.COLOR_WHITE)

std.bkgdset(" ", curses.color_pair(4) | curses.A_DIM)
std.keypad(1)
std.scrollok(0)
std.clear()
std.refresh()

prompt = curses.newwin(4, 18, 6, 20)
for i in range(18):
    std.addch(10, i+21, curses.ACS_BLOCK, curses.color_pair(5))
for i in range(4):
    std.addch(i+7, 38, curses.ACS_BLOCK, curses.color_pair(5))
std.refresh()
prompt.attrset(curses.color_pair(4) | curses.A_DIM)
prompt.bkgdset(" ", curses.color_pair(4) | curses.A_DIM)
prompt.clear()
prompt.border()
prompt.attrset(0)
prompt.move(0, 1)
prompt.addstr(" BIOS Password ")
for i in range(8):
    prompt.addstr(1, 1 + 2*i, " ", curses.color_pair(1))
prompt.addstr(2, 10, "[Enter]", curses.color_pair(1))

for i in range(8):
    prompt.getch(1, 1+2*i)
    prompt.addstr(1, 1+2*i, "*", curses.color_pair(1))

prompt.addstr(2, 11, "Enter", curses.color_pair(2) | curses.A_BOLD)
curses.curs_set(0)
prompt.getch()

prompt.addstr(1, 1, "INVALID PASSWORD", curses.color_pair(3) | curses.A_BOLD)
prompt.refresh()
curses.napms(800)

prompt.addstr(1, 1, " "*16)
prompt.refresh()

curses.napms(800)
prompt.addstr(1, 1, "INVALID PASSWORD", curses.color_pair(3) | curses.A_BOLD)
prompt.refresh()
curses.napms(800)

prompt.addstr(1, 1, " "*16)
prompt.refresh()
curses.napms(800)

prompt.addstr(1, 1, "INVALID PASSWORD", curses.color_pair(3) | curses.A_BOLD)
prompt.refresh()
curses.napms(800)

del prompt
std.clear()
std.refresh()
curses.napms(300)

curses.curs_set(1)
curses.echo()
curses.nocbreak()
curses.endwin()

