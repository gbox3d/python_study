import os
import sys
import termios
import tty

def getKey():
	fd = sys.stdin.fileno()
	old = termios.tcgetattr(fd)
	new = termios.tcgetattr(fd)
	new[3] = new[3] & ~termios.ICANON & ~termios.ECHO
	new[6][termios.VMIN] = 1
	new[6][termios.VTIME] = 0
	termios.tcsetattr(fd, termios.TCSANOW, new)
	key = None
	try:
		key = os.read(fd, 3)
	finally:
		termios.tcsetattr(fd, termios.TCSAFLUSH, old)
	return key
print(sys.version)
print("esc key to exit.")

while 1:
    x = str(getKey())
    if  x  == "b'\\x1b'" : 
        print('found esc')
        print('exit')
        break;
    else :
        print(x)
