#!/usr/bin/env python3

import curses
import sys
import os
import time
#----------------------------------------------------------------------------
def wait1ms(ms):
	time.sleep(ms*1e-3)






def main(stdscr):
#	stdscr = curses.initscr()
#	curses.cbreak()
#	stdscr.nodelay(True)
#	stdscr.clear()
#	stdscr.addstr(0,0,'test')
#	stdscr.refresh()
	print('test')
	while True:
		a = stdscr.getkey()
		print('getkey:{}'.format(a))
		if a == 'q':
			sys.exit(0)
			print('OK')

#	curses.nocbreak()
#	stdscr.keypad(False)
#	curses.echo()

if __name__ == "__main__":
	stdscr = curses.initscr()
	curses.wrapper(main)
	main(stdscr)
#	main()




### EOF ###
