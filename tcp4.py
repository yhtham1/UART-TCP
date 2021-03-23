#!/usr/bin/env python3
# web https://docs.python.org/ja/3/library/socketserver.html

"""
	20/06/01(月) 07:49:03
	telnet接続を行った端末をUARTみたいに扱う
	コールバック関数は、なし。
	telnetへの出力: lprintf() 接続されたすべての端末へ同一メッセージを送る
	telnetからの入力 lgetc()
	20/11/02(月) 14:30:48
	get_ip()追加
"""
import time
import socket
import os
import sys
import socket
import threading
import socketserver
from queue import Queue

rxq=Queue()			#各クライアントからの入力をバッファリングする。 lgetc()で読み出す
FD_LIST = []		#ここに接続変数を追加、削除する。接続数分存在する。lprintfで出力する。
mon_tcp = 0			#送受信のデバック
use_binary=False	#バイナリーデータでのやり取り True:False

def lgetc():		#tcp接続先から入力する。
	ans = ''
	if False==rxq.empty():
		ans = rxq.get()
		return ans
	return None

def lprintf(msg):	#tcp接続先へ出力する。
#	print(msg)
	for req in FD_LIST:
		try:
			if True == use_binary:
				req.sendall(msg)
			else:
				req.sendall(msg.encode('utf-8'))
		except:
			pass


def PushRXData(str):
	for c in str:
		rxq.put(c)

class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):
	def handle(self):
		thread_name = threading.current_thread().getName()
		prefix = '[{}]'.format(thread_name)

		r_ip,r_port = self.request.getpeername()

#		print('{} -- connected'.format(self.request.getpeername()))
		print('IP:{} -- connected'.format(r_ip))
#		print(dir(self.request))
#		print(self.request.getpeername())
		FD_LIST.append(self.request)
		while True:
			try:
				dat = self.request.recv(1024)
			except:
				break
			if 0 == len(dat):	#データ長が0なら切断済み
				break
			if mon_tcp:
				print('{} -- RX[{}]'.format(prefix, dat))
			if True == use_binary:
				rxq.put(dat) 			#読んだ文字をキューに積む[teratermのenter入力は '\r\0'なので注意]
			else:
				c1 = dat.decode('utf-8')
				PushRXData(c1) 			#読んだ文字をキューに積む[teratermのenter入力は '\r\0'なので注意]
		print('IP:{} -- disconnect'.format(r_ip))
		FD_LIST.remove(self.request)
		print('FD_LIST is {}'.format(len(FD_LIST)))

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
	pass

def get_ip(server_ip):
	#server_ipに接続してそのときのローカルＩＰを得る
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	try:
		# doesn't even have to be reachable
		s.connect((server_ip, 1))
		IP = s.getsockname()[0]
	except Exception:
		IP = '127.0.0.1'
	finally:
		s.close()
	return IP

def start(host, port):
	#func
	FD_LIST.clear()
	server = ThreadedTCPServer((host, port), ThreadedTCPRequestHandler)
	server.allow_reuse_address = True
	server_thread = threading.Thread(target=server.serve_forever)
	server_thread.daemon = True
	server_thread.start()
	print("TCP4 telnetサーバ tcp4.py listen:{}".format(port))

if __name__ == "__main__":
	ip = get_ip( '192.168.0.3' )
	print('my ip is :{}'.format(ip))
	mon_tcp = 1
	start('0.0.0.0', 5000 )
	while True:
		time.sleep(1)
	server.shutdown()

### EOF ###
