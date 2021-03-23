#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import serial.tools.list_ports
import serial
import tcp4
import threading
import time

import curses
# import getkey
from curses import wrapper

EXIT_REQUEST = 0
UART = []
UART_PORT = ''
UART_BAUD = 115200
TCP_PORT = 5025


def wait1ms(ms):
	time.sleep(ms * 1e-3)


def uartrx():  # UART -> TCP
	global EXIT_REQUEST
	print('start uartrx()')
	while 0 == EXIT_REQUEST:
		a = UART.read(2000)
		if b'' == a:
			#			print('timeourt:{}'.format(ct))
			pass
		else:
			if True == tcp4.use_binary:
				tcp4.lprintf(a)
			else:
				print('uart_in():{}'.format(a))
				tcp4.lprintf(a.decode('utf-8'))


def uarttx():  # TCP -> UART
	ct = 0
	global EXIT_REQUEST
	print('start uarttx()')
	while 0 == EXIT_REQUEST:
		a = tcp4.lgetc()
		if None == a:
			pass
		else:
			#			print('tcp_in():{}'.format(a))
			if True == tcp4.use_binary:
				UART.write(a)
			else:
				UART.write(a.encode('utf-8'))


def main_thread():
	global EXIT_REQUEST
	server_ip = tcp4.get_ip('8.8.8.8')
	print('UART-TCP Server (UART:{} BAUD:{}) <--> {}:{}'.format(UART_PORT, UART_BAUD, server_ip, TCP_PORT))
	# stdscr = curses.initscr()
	while 0 == EXIT_REQUEST:
		# c = stdscr.getkey()
		# if 'q' == c:
		# 	EXIT_REQUEST = 1
		# 	print(c)
		# print("main():")
		wait1ms(1000)
	print("exit main_thread()")


def main():
	global UART, UART_BAUD, UART_PORT, TCP_PORT
	TCP_PORT = 5025
	UART_PORT = 'COM1'
	UART_BAUD = 115200
	i = 1
	while i < len(sys.argv):  # in range(1, len(sys.argv)):
		arg2 = sys.argv[i].strip()
		if 0 <= arg2.find('--uart'):
			UART_PORT = sys.argv[i + 1].strip()
			i += 2
			continue
		if 0 <= arg2.find('--baud'):
			UART_BAUD = sys.argv[i + 1].strip()
			i += 2
			continue
		if 0 <= arg2.find('--port'):
			TCP_PORT = sys.argv[i + 1].strip()
			i += 2
			continue
		# normal 処理
		i += 1
	UART = serial.Serial(UART_PORT, UART_BAUD, timeout=0.1)
	global EXIT_REQUEST
	tcp4.use_binary = True
	tcp4.start('0.0.0.0', TCP_PORT)
	thread_1 = threading.Thread(target=uartrx, daemon=True)
	thread_1.start()
	thread_2 = threading.Thread(target=uarttx, daemon=True)
	thread_2.start()
	main_thread()
	EXIT_REQUEST = 1


if __name__ == "__main__":
	# stdscr = curses.initscr()
	# curses.wrapper(main)
	# main(stdscr)
	main()