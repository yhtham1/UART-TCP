#!/usr/bin/env python3
import fcntl
import termios
import sys
import os
import time
#----------------------------------------------------------------------------
class getkey:
	def __init__(self, nonblock=True):
		print('enter key:init()')
		# https://qiita.com/tortuepin/items/9ede6ca603ddc74f91ba
		# https://qiita.com/tortuepin/items/e6c72f48115f20744ace
		#標準入力のファイルディスクリプタを取得
		self.fd = sys.stdin.fileno()
		#fdの端末属性をゲットする
		#oldとnewには同じものが入る。
		#newに変更を加えて、適応する
		#oldは、後で元に戻すため
		self.key_old = termios.tcgetattr(self.fd)
		self.key_new = termios.tcgetattr(self.fd)
		
		#new[3]はlflags
		#ICANON(カノニカルモードのフラグ)を外す
		self.key_new[3] &= ~termios.ICANON
		#ECHO(入力された文字を表示するか否かのフラグ)を外す
		self.key_new[3] &= ~termios.ECHO
		# 書き換えたnewをfdに適応する
		termios.tcsetattr(self.fd, termios.TCSANOW, self.key_new)

		# stdinをNONBLOCKに設定
		self.fcntl_old = fcntl.fcntl(self.fd, fcntl.F_GETFL)
		fcntl.fcntl(self.fd, fcntl.F_SETFL, self.fcntl_old | os.O_NONBLOCK)

	def inkey(self):
		# キーボードから入力を受ける。
		# lfalgsが書き換えられているので、エンターを押さなくても次に進む。echoもしない
		self.ch = sys.stdin.read(1)
		return self.ch

	def __del__(self):
		print('exit key:del()')
		# fdの属性を元に戻す
		# 具体的にはICANONとECHOが元に戻る
		termios.tcsetattr(self.fd, termios.TCSANOW, self.key_old)

if __name__ == "__main__":
	my_key = getkey()
	while 1:
		key = my_key.inkey()
		# enterで終了、キー入力があれば表示
		if key == '\n':
			break
		elif key:
			print(len(key),key.encode('ascii'))


### EOF ###
