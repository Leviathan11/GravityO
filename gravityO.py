import curses
import time
from curses import wrapper


def generatemap(): #creates the map from an existing mapfinal.txt file (converted into coords list)
    for i in range(0, len(coords)):
        yxz=coords[i].split( ) #one item from a list
        y=int(yxz[0])       #y coordinate
        x=int(yxz[1])       #x coordinate
        z=int(yxz[2])       #which character
        if z==1:
            screen.addstr(y, x, 'X', curses.color_pair(z))
        if z==2:
            screen.addstr(y, x, '*', curses.color_pair(z))
        if z==3:
            screen.addstr(y, x, '+', curses.color_pair(z))
        if z==4:
            screen.addstr(y, x, '#', curses.color_pair(z))
    screen.refresh()

def checkaround():    #checks if the O is connecting to a wall (so we can use gravity change)
    global y, x, gravity
    rtnbool=0
    if not gravity[1]:
        if screen.inch(y+1,x)==344 or screen.inch(y-1,x)==344:
            rtnbool=1
    if gravity[1]:
        if screen.inch(y,x+1)==344 or screen.inch(y,x-1)==344:
            rtnbool=1
    return rtnbool

def move (num): #1:down 2:up 3:left 4:right
    global y, x, gravity
    if num==1:
        screen.addch(y,x, ' ')
        y+=1
        screen.addch(y,x, 'O')
        screen.refresh()
    if num==2:
        screen.addch(y,x, ' ')
        y-=1
        screen.addch(y,x, 'O')
        screen.refresh()
    if num==3:
        screen.addch(y,x, ' ')
        x-=1
        screen.addch(y,x, 'O')
        screen.refresh()
    if num==4:
        screen.addch(y,x, ' ')
        x+=1
        screen.addch(y,x, 'O')
        screen.refresh()


def game():
    global y, x, gravity, gameover
    curses.cbreak()
    curses.noecho()
    curses.curs_set(0)
    screen.nodelay(1)
    screen.addch(y,x, 'O')
    screen.refresh()
    while gameover==0:
        q="0"
        while q=="0":
            q=screen.getch()
            if not gravity[1]:
                if not gravity[0]:
                    if screen.inch(y+1,x)==ord(' '): #can we move
                        move(1)
                        time.sleep(0.1)
                    elif screen.inch(y+1,x)==554:  #die
                        gameover=1
                        break
                    elif screen.inch(y+1,x)==811: #gravity[1] change
                        screen.addch(y,x, ' ')
                        y+=1
                        x+=1
                        screen.addch(y,x, 'O')
                        screen.refresh()
                        gravity[1]=1-gravity[1]
                        time.sleep(0.1)
                    elif screen.inch(y+1,x)==1059: #win
                        gameover=2
                        break
                if gravity[0]:
                    if screen.inch(y-1,x)==ord(' '):
                        move(2)
                        time.sleep(0.1)
                    elif screen.inch(y-1,x)==554:
                        gameover=1
                        break
                    elif screen.inch(y-1,x)==811:
                        screen.addch(y,x, ' ')
                        y-=1
                        x-=1
                        screen.addch(y,x, 'O')
                        screen.refresh()
                        gravity[1]=1-gravity[1]
                        time.sleep(0.1)
                    elif screen.inch(y-1,x)==1059:
                        gameover=2
                        break
            if gravity[1]:
                if gravity[0]:
                    if screen.inch(y,x-1)==ord(' '):
                        move(3)
                        time.sleep(0.1)
                    elif screen.inch(y,x-1)==554:
                        gameover=1
                        break
                    elif screen.inch(y,x-1)==811:
                        screen.addch(y,x, ' ')
                        y-=1
                        x-=1
                        screen.addch(y,x, 'O')
                        screen.refresh()
                        gravity[1]=1-gravity[1]
                        time.sleep(0.1)
                    elif screen.inch(y,x-1)==1059:
                        gameover=2
                        break
                if not gravity[0]:
                    if screen.inch(y,x+1)==ord(' '):
                        move(4)
                        time.sleep(0.1)
                    elif screen.inch(y,x+1)==554:
                        gameover=1
                        break
                    elif screen.inch(y,x+1)==811:
                        screen.addch(y,x, ' ')
                        y+=1
                        x+=1
                        screen.addch(y,x, 'O')
                        screen.refresh()
                        gravity[1]=1-gravity[1]
                        time.sleep(0.1)
                    elif screen.inch(y,x+1)==1059:
                        gameover=2
                        break
        if not gravity[1]:
            if q==ord('a'):
                if screen.inch(y,x-1)==ord(' '):
                    move(3)
                elif screen.inch(y,x-1)==554:
                    gameover=1
                    break
                elif screen.inch(y,x-1)==1059:
                    gameover=2
                    break
            if q==ord('d'):
                if screen.inch(y,x+1)==ord(' '):
                    move(4)
                elif screen.inch(y,x+1)==554:
                    gameover=1
                    break
                elif screen.inch(y,x+1)==1059:
                    gameover=2
                    break
        if gravity[1]:
            if q==ord('a'):
                if screen.inch(y-1,x)==ord(' '):
                    move(2)
                elif screen.inch(y-1,x)==554:
                    gameover=1
                    break
                elif screen.inch(y-1,x)==1059:
                    gameover=2
                    break
            if q==ord('d'):
                if screen.inch(y+1,x)==ord(' '):
                    move(1)
                elif screen.inch(y+1,x)==554:
                    gameover=1
                    break
                elif screen.inch(y,x-1)==1059:
                    gameover=2
                    break
        if q==ord('l') and checkaround():
            gravity[0]=1-gravity[0]
        if q==ord('x'):
            gameover=3
            break
#wrapper(game)
mode=input("Type in P for practice mode, or S to start the GAME!\n (Or anything else to quit!)")
if mode=="S" or mode=="P":
    if mode=="S":
        y, x = 22, 1
    elif mode=="P":
        y, x = 8, 70
    map= open ('mapfinal.txt', 'r+')
    coords=map.readlines()
    map.close()
    screen=curses.initscr()
    curses.resize_term(25,81) #else i could not use the bottom right corner(23,79)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE) #X:wall
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_RED)   #*:obstacle
    curses.init_pair(3, curses.COLOR_MAGENTA, curses.COLOR_GREEN) #+:gravity changer
    curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLUE)   ##:win
    gravity=[0,0]  #gravity[1]: shows if gravity is vertical(0) or horizontal(1) || gravity[0]: shows if falling down/right(0) or up/left(1)
    gameover=0
    generatemap()
    game()
    screen.getch()
    curses.endwin()
    if gameover==1:
        print ("You Lost!")
    elif gameover==2:
        print ("You Win!")
    else:
        print ("You Quit!")
else:
    print ("Maybe next time!:(")