import curses
import time


def generatemap(list):  # print out the list file(currently containing only the borders)
    global screen
    for i in range(0, len(list)):
        yxz = list[i].split()
        y = int(yxz[0])
        x = int(yxz[1])
        z = int(yxz[2])
        if z == 1:
            screen.addstr(y, x, 'X', curses.color_pair(z))
        if z == 2:
            screen.addstr(y, x, '*', curses.color_pair(z))
        if z == 3:
            screen.addstr(y, x, '+', curses.color_pair(z))
        if z == 4:
            screen.addstr(y, x, '#', curses.color_pair(z))
        if z == 5:
            screen.addstr(y, x, 'N', curses.color_pair(z))
    screen.addch(9, 58, 554)
    screen.refresh()


def creating(coordinates):  # moving the cursor and creating the map with objectives
    global screen
    screen.addstr(1, 1, " ")
    y, x = 1, 1
    while True:
        q = screen.getch()
        if q == curses.KEY_UP and y > 0:
            y -= 1
            screen.move(y, x)
            screen.refresh()
        if q == curses.KEY_DOWN and y < 23:
            y += 1
            screen.move(y, x)
            screen.refresh()
        if q == curses.KEY_LEFT and x > 0:
            x -= 1
            screen.move(y, x)
            screen.refresh()
        if q == curses.KEY_RIGHT and x < 79:
            x += 1
            screen.move(y, x)
            screen.refresh()
        if q == ord('x'):
            screen.addstr(y, x, 'X', curses.color_pair(1))
            screen.refresh()
            strng = str(y) + " " + str(x) + " 1\n"
            coordinates.append(strng)
        if q == ord('c'):
            screen.addstr(y, x, '*', curses.color_pair(2))
            screen.refresh()
            strng = str(y) + " " + str(x) + " 2\n"
            coordinates.append(strng)
        if q == ord('v'):
            screen.addstr(y, x, '+', curses.color_pair(3))
            screen.refresh()
            strng = str(y) + " " + str(x) + " 3\n"
            coordinates.append(strng)
        if q == ord('b'):
            screen.addstr(y, x, '#', curses.color_pair(4))
            screen.refresh()
            strng = str(y) + " " + str(x) + " 4\n"
            coordinates.append(strng)
        if q == ord('n'):
            screen.addstr(y, x, 'N', curses.color_pair(5))
            screen.refresh()
            strng = str(y) + " " + str(x) + " 5\n"
            coordinates.append(strng)
        if q == ord('q'):
            break
        time.sleep(0.1)
    return coordinates


def recording_border():  # save the coordinates of the wall objectives at the border
    border_coords = []
    for i in range(0, 80):
        border_coords.append("0 " + str(i) + " 1\n")
        border_coords.append("23 " + str(i) + " 1\n")
        if i < 24 and i > 0:
            border_coords.append(str(i) + " 0" + " 1\n")
            border_coords.append(str(i) + " 79" + " 1\n")
    return border_coords


def main():
    global screen
    coordinates = recording_border()
    generatemap(coordinates)
    coordinates = creating(coordinates)
    curses.endwin()
    record = open('newmap.txt', 'w')
    for i in range(0, len(coordinates)):
        record.write(coordinates[i])
    record.close()


print("Welcome to the map generator!\nYour new map will be saved in the 'newmap.txt' file.")
print("Use arrows to move the cursor.\nHere are your other control buttons:")
print("x: Put down a wall objective\nc: Put down a '*'(malicious) objective\nv: Put down a '+'(grav-changer) objective")
print("b: Put down a '#'(goal) objective\nn: Put down a 'N'(grav-off) objective\nq: Save and quit")
input("Press Enter to start!")
screen = curses.initscr()
curses.start_color()
curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_RED)
curses.init_pair(3, curses.COLOR_MAGENTA, curses.COLOR_GREEN)
curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLUE)
curses.init_pair(5, curses.COLOR_YELLOW, curses.COLOR_MAGENTA)
screen.keypad(1)
curses.cbreak()
curses.noecho()
screen.nodelay(1)
curses.resize_term(25, 81)
main()
