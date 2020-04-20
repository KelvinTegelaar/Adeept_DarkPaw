#!/usr/bin/python
# -*- coding: UTF-8 -*-
# File name   : GUI.py
# Description : graphical client
# Website     : www.adeept.com
# E-mail      : support@adeept.com
# Author      : TangoCash
# Date        : 2020/04/17
# 

import threading as thread
import time
import tkinter as tk
from socket import *
from tkinter import messagebox

try:
	import cv2
	import numpy as np
except:
	print("Couldn't import OpenCV, you need to install it first. pip3 install opencv-contrib-python")

try:
	import base64
except:
	print("Couldn't import base64, you need to install it first. pip3 install pybase64")

try:
	import zmq
except:
	print("Couldn't import zmq, you need to install it first. pip3 install pyzmq")


def global_init():
	global ip_stu, c_f_stu, c_b_stu, c_l_stu, c_r_stu, c_ls_stu, c_rs_stu, funcMode, tcpClicSock, root
	global Switch_3, Switch_2, Switch_1, LED_Switch_3, LED_Switch_2, LED_Switch_1, SmoothMode
	global color_bg, color_text, color_btn, color_line, color_can, color_oval, target_color
	ip_stu = 1
	c_f_stu = 0
	c_b_stu = 0
	c_l_stu = 0
	c_r_stu = 0
	c_ls_stu = 0
	c_rs_stu = 0
	funcMode = 0
	tcpClicSock = None
	root = None

	Switch_3 = 0
	Switch_2 = 0
	Switch_1 = 0
	LED_Switch_3 = 0
	LED_Switch_2 = 0
	LED_Switch_1 = 0
	SmoothMode = 0

	# Set background color
	color_bg = '#000000'
	# Set text color
	color_text = '#E1F5FE'
	# Set button color
	color_btn = '#0277BD'
	# Set line color
	color_line = '#01579B'
	# Set canvas color
	color_can = '#212121'
	# Set oval color
	color_oval = '#2196F3'
	# Set target color
	target_color = '#FF6D00'


global_init()


########>>>>>VIDEO<<<<<########

def video_thread():
	global footage_socket, font, frame_num, fps
	context = zmq.Context()
	footage_socket = context.socket(zmq.SUB)
	footage_socket.bind('tcp://*:5555')
	footage_socket.setsockopt_string(zmq.SUBSCRIBE, np.unicode(''))

	font = cv2.FONT_HERSHEY_SIMPLEX

	frame_num = 0
	fps = 0


def get_FPS():
	global frame_num, fps
	while 1:
		try:
			time.sleep(1)
			fps = frame_num
			frame_num = 0
		except:
			time.sleep(1)


def opencv_r():
	global frame_num
	while True:
		try:
			frame = footage_socket.recv_string()
			img = base64.b64decode(frame)
			npimg = np.frombuffer(img, dtype=np.uint8)
			source = cv2.imdecode(npimg, 1)
			cv2.putText(source, ('PC FPS: %s' % fps), (40, 20), font, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
			try:
				cv2.putText(source, ('CPU Temperature: %s' % CPU_TEP), (370, 350), font, 0.5, (128, 255, 128), 1, cv2.LINE_AA)
				cv2.putText(source, ('CPU Usage: %s' % CPU_USE), (370, 380), font, 0.5, (128, 255, 128), 1, cv2.LINE_AA)
				cv2.putText(source, ('RAM Usage: %s' % RAM_USE), (370, 410), font, 0.5, (128, 255, 128), 1, cv2.LINE_AA)
				cv2.putText(source, ('Distance: %s' % DISTANCE), (370, 440), font, 0.5, (128, 255, 128), 1, cv2.LINE_AA)

				# cv2.line(source,(320,240),(260,300),(255,255,255),1)
				# cv2.line(source,(210,300),(260,300),(255,255,255),1)

				# cv2.putText(source,('%sm'%ultra_data),(210,290), font, 0.5,(255,255,255),1,cv2.LINE_AA)
			except:
				pass
			# cv2.putText(source,('%sm'%ultra_data),(210,290), font, 0.5,(255,255,255),1,cv2.LINE_AA)
			cv2.imshow("Stream", source)
			frame_num += 1
			cv2.waitKey(1)

		except:
			time.sleep(0.5)
			break


fps_threading = thread.Thread(target=get_FPS)
fps_threading.setDaemon(True)
fps_threading.start()

video_threading = thread.Thread(target=video_thread)
video_threading.setDaemon(True)
video_threading.start()


########>>>>>VIDEO<<<<<########


def replace_num(initial, new_num):
	newline = ""
	str_num = str(new_num)
	with open("ip.txt", "r") as f:
		for line in f.readlines():
			if (line.find(initial) == 0):
				line = initial + "%s" % (str_num)
			newline += line
	with open("ip.txt", "w") as f:
		f.writelines(newline)


def num_import(initial):
	with open("ip.txt") as f:
		for line in f.readlines():
			if (line.find(initial) == 0):
				r = line
	begin = len(list(initial))
	snum = r[begin:]
	n = snum
	return n


def all_btn_red():
	Btn_Steady.config(bg='#FF6D00', fg='#000000')
	Btn_FindColor.config(bg='#FF6D00', fg='#000000')
	Btn_WatchDog.config(bg='#FF6D00', fg='#000000')
	Btn_Fun4.config(bg='#FF6D00', fg='#000000')
	Btn_Fun5.config(bg='#FF6D00', fg='#000000')
	Btn_Fun6.config(bg='#FF6D00', fg='#000000')


def all_btn_normal():
	Btn_Steady.config(bg=color_btn, fg=color_text)
	Btn_FindColor.config(bg=color_btn, fg=color_text)
	Btn_WatchDog.config(bg=color_btn, fg=color_text)
	Btn_Fun4.config(bg=color_btn, fg=color_text)
	Btn_Fun5.config(bg=color_btn, fg=color_text)
	Btn_Fun6.config(bg=color_btn, fg=color_text)


def connection_thread():
	global funcMode, Switch_3, Switch_2, Switch_1, SmoothMode
	while 1:
		data = (tcpClicSock.recv(BUFSIZ)).decode()
		if not data:
			continue

		elif 'FindColor' in data:
			funcMode = 1
			all_btn_red()
			Btn_FindColor.config(bg='#00E676')

		elif 'steady' in data:
			funcMode = 1
			all_btn_red()
			Btn_Steady.config(bg='#00E676')

		elif 'WatchDog' in data:
			funcMode = 1
			all_btn_red()
			Btn_WatchDog.config(bg='#00E676')

		elif 'Smooth_on' in data:
			SmoothMode = 1
			Btn_Smooth.config(bg='#4CAF50')

		elif 'Smooth_off' in data:
			SmoothMode = 0
			Btn_Smooth.config(bg=color_btn)

		elif 'Switch_3_on' in data:
			Switch_3 = 1
			Btn_Switch_3.config(bg='#4CAF50')

		elif 'Switch_2_on' in data:
			Switch_2 = 1
			Btn_Switch_2.config(bg='#4CAF50')

		elif 'Switch_1_on' in data:
			Switch_1 = 1
			Btn_Switch_1.config(bg='#4CAF50')

		elif 'Switch_3_off' in data:
			Switch_3 = 0
			Btn_Switch_3.config(bg=color_btn)

		elif 'Switch_2_off' in data:
			Switch_2 = 0
			Btn_Switch_2.config(bg=color_btn)

		elif 'Switch_1_off' in data:
			Switch_1 = 0
			Btn_Switch_1.config(bg=color_btn)

		elif 'rainbow_on' in data:
			LED_Switch_3 = 1
			Btn_LED_Switch_3.config(bg='#4CAF50')

		elif 'breath_on' in data:
			LED_Switch_2 = 1
			Btn_LED_Switch_2.config(bg='#4CAF50')

		elif 'police_on' in data:
			LED_Switch_1 = 1
			Btn_LED_Switch_1.config(bg='#4CAF50')

		elif 'rainbow_off' in data:
			LED_Switch_3 = 0
			Btn_LED_Switch_3.config(bg=color_btn)

		elif 'breath_off' in data:
			LED_Switch_2 = 0
			Btn_LED_Switch_2.config(bg=color_btn)

		elif 'police_off' in data:
			LED_Switch_1 = 0
			Btn_LED_Switch_1.config(bg=color_btn)

		elif 'FunEnd' in data:
			funcMode = 0
			all_btn_normal()

		print(data)


def Info_receive():
	global CPU_TEP, CPU_USE, RAM_USE, DIS_lab, DIRECTION, DISTANCE
	HOST = ''
	INFO_PORT = 2256
	ADDR = (HOST, INFO_PORT)
	InfoSock = socket(AF_INET, SOCK_STREAM)
	InfoSock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
	InfoSock.bind(ADDR)
	InfoSock.listen(5)
	InfoSock, addr = InfoSock.accept()
	print('Info connected')
	while 1:
		try:
			info_data = ''
			info_data = str(InfoSock.recv(BUFSIZ).decode())
			try:
				info_get = info_data.split()
				CPU_TEP = info_get[0]
				CPU_USE = info_get[1]
				RAM_USE = info_get[2]
				DIRECTION = info_get[3]
				DISTANCE = info_get[4]
			except:
				pass
			# print('cpu_tem:%s\ncpu_use:%s\nram_use:%s'%(CPU_TEP,CPU_USE,RAM_USE))
			CPU_TEP_lab.config(text='CPU Temp: %s℃' % CPU_TEP)
			CPU_USE_lab.config(text='CPU Usage: %s' % CPU_USE)
			RAM_lab.config(text='RAM Usage: %s' % RAM_USE)
			DIS_lab.config(text='Distance: %s' % DISTANCE)
		except:
			pass


def socket_connect_thread():
	global ADDR, tcpClicSock, BUFSIZ, ip_stu, ipaddr
	# Get the IP address from Entry
	ip_adr = E1.get()

	# If no input IP address in Entry,import a default IP
	if ip_adr == '':
		ip_adr = num_import('IP:')
		l_ip_4.config(text='Connecting')
		l_ip_4.config(bg='#FF8F00')
		l_ip_5.config(text='Default:%s' % ip_adr)
		pass

	SERVER_IP = ip_adr
	SERVER_PORT = 10223
	BUFSIZ = 1024
	ADDR = (SERVER_IP, SERVER_PORT)
	tcpClicSock = socket(AF_INET, SOCK_STREAM)

	# Try 5 times if disconnected
	for i in range(1, 6):
		# try:
		if ip_stu == 1:
			print("Connecting to server @ %s:%d..." % (SERVER_IP, SERVER_PORT))
			print("Connecting")
			tcpClicSock.connect(ADDR)

			print("Connected")

			l_ip_5.config(text='IP:%s' % ip_adr)
			l_ip_4.config(text='Connected')
			l_ip_4.config(bg='#558B2F')

			replace_num('IP:', ip_adr)
			E1.config(state='disabled')
			Btn14.config(state='disabled')

			# '0' means connected
			ip_stu = 0

			connection_threading = thread.Thread(target=connection_thread)
			connection_threading.setDaemon(	True)
			connection_threading.start()

			info_threading = thread.Thread(target=Info_receive)
			info_threading.setDaemon(True)
			info_threading.start()

			opencv_threading = thread.Thread(target=opencv_r)
			opencv_threading.setDaemon(True)
			opencv_threading.start()

			break
		else:
			print("Cannot connecting to server,try it latter!")
			l_ip_4.config(text='Try %d/5 time(s)' % i)
			l_ip_4.config(bg='#EF6C00')
			print('Try %d/5 time(s)' % i)
			ip_stu = 1
			time.sleep(1)
			continue

	if ip_stu == 1:
		l_ip_4.config(text='Disconnected')
		l_ip_4.config(bg='#F44336')


def draw_scale_FL(x, y, w):
	global Btn_CVFL

	def lip1_send(event):
		time.sleep(0.03)
		tcpClicSock.send(('lip1 %s' % var_lip1.get()).encode())

	def lip2_send(event):
		time.sleep(0.03)
		tcpClicSock.send(('lip2 %s' % var_lip2.get()).encode())

	def err_send(event):
		time.sleep(0.03)
		tcpClicSock.send(('err %s' % var_err.get()).encode())

	def call_Render(event):
		tcpClicSock.send(('Render').encode())

	def call_CVFL(event):
		tcpClicSock.send(('CVFL').encode())

	def call_WB(event):
		tcpClicSock.send(('WBswitch').encode())

	Scale_lip1 = tk.Scale(root, label=None,
						  from_=0, to=480, orient=tk.HORIZONTAL, length=w,
						  showvalue=1, tickinterval=None, resolution=1, variable=var_lip1, troughcolor='#212121',
						  command=lip1_send, fg=color_text, bg=color_bg, highlightthickness=0)
	Scale_lip1.place(x=x, y=y)

	Scale_lip2 = tk.Scale(root, label=None,
						  from_=0, to=480, orient=tk.HORIZONTAL, length=w,
						  showvalue=1, tickinterval=None, resolution=1, variable=var_lip2, troughcolor='#212121',
						  command=lip2_send, fg=color_text, bg=color_bg, highlightthickness=0)
	Scale_lip2.place(x=x, y=y + 30)

	Scale_err = tk.Scale(root, label=None,
						 from_=0, to=200, orient=tk.HORIZONTAL, length=w,
						 showvalue=1, tickinterval=None, resolution=1, variable=var_err, troughcolor='#212121',
						 command=err_send, fg=color_text, bg=color_bg, highlightthickness=0)
	Scale_err.place(x=x, y=y + 60)

	canvas_cover = tk.Canvas(root, bg=color_bg, height=30, width=510, highlightthickness=0)
	canvas_cover.place(x=x, y=y + 90)

	Btn_Render = tk.Button(root, width=7, text='Render', fg=color_text, bg=color_btn, relief='ridge')
	Btn_Render.place(x=x + w + 111, y=y + 20)
	Btn_Render.bind('<ButtonPress-1>', call_Render)

	Btn_CVFL = tk.Button(root, width=7, text='CV FL', fg=color_text, bg=color_btn, relief='ridge')
	Btn_CVFL.place(x=x + w + 21, y=y + 20)
	Btn_CVFL.bind('<ButtonPress-1>', call_CVFL)

	Btn_WB = tk.Button(root, width=18, text='LineColorSwitch', fg=color_text, bg=color_btn, relief='ridge')
	Btn_WB.place(x=x + w + 21, y=y + 60)
	Btn_WB.bind('<ButtonPress-1>', call_WB)


def draw_switch_button(x, y):
	global Btn_Switch_1, Btn_Switch_2, Btn_Switch_3

	def call_Switch_1(event):
		if Switch_1 == 0:
			tcpClicSock.send(('Switch_1_on').encode())
		else:
			tcpClicSock.send(('Switch_1_off').encode())

	def call_Switch_2(event):
		if Switch_2 == 0:
			tcpClicSock.send(('Switch_2_on').encode())
		else:
			tcpClicSock.send(('Switch_2_off').encode())

	def call_Switch_3(event):
		if Switch_3 == 0:
			tcpClicSock.send(('Switch_3_on').encode())
		else:
			tcpClicSock.send(('Switch_3_off').encode())

	Btn_Switch_1 = tk.Button(root, width=8, text='Switch 1', fg=color_text, bg=color_btn, relief='ridge')
	Btn_Switch_2 = tk.Button(root, width=8, text='Switch 2', fg=color_text, bg=color_btn, relief='ridge')
	Btn_Switch_3 = tk.Button(root, width=8, text='Switch 3', fg=color_text, bg=color_btn, relief='ridge')

	Btn_Switch_1.place(x=x, y=y)
	Btn_Switch_2.place(x=x + 95, y=y)
	Btn_Switch_3.place(x=x + 190, y=y)

	Btn_Switch_1.bind('<ButtonPress-1>', call_Switch_1)
	Btn_Switch_2.bind('<ButtonPress-1>', call_Switch_2)
	Btn_Switch_3.bind('<ButtonPress-1>', call_Switch_3)


def draw_led_switch_button(x, y):
	global Btn_LED_Switch_1, Btn_LED_Switch_2, Btn_LED_Switch_3

	def call_LED_Switch_1(event):
		tcpClicSock.send(('police').encode())

	def call_LED_Switch_2(event):
		tcpClicSock.send(('breath').encode())

	def call_LED_Switch_3(event):
		tcpClicSock.send(('rainbow').encode())

	Btn_LED_Switch_1 = tk.Button(root, width=8, text='Police', fg=color_text, bg=color_btn, relief='ridge')
	Btn_LED_Switch_2 = tk.Button(root, width=8, text='Breath', fg=color_text, bg=color_btn, relief='ridge')
	Btn_LED_Switch_3 = tk.Button(root, width=8, text='Rainbow', fg=color_text, bg=color_btn, relief='ridge')

	Btn_LED_Switch_1.place(x=x, y=y)
	Btn_LED_Switch_2.place(x=x + 95, y=y)
	Btn_LED_Switch_3.place(x=x + 190, y=y)

	Btn_LED_Switch_1.bind('<ButtonPress-1>', call_LED_Switch_1)
	Btn_LED_Switch_2.bind('<ButtonPress-1>', call_LED_Switch_2)
	Btn_LED_Switch_3.bind('<ButtonPress-1>', call_LED_Switch_3)


def draw_direction_button(x, y):
	def call_forward(event):
		global c_f_stu
		if c_f_stu == 0:
			tcpClicSock.send(('forward').encode())
			c_f_stu = 1

	def call_back(event):
		global c_b_stu
		if c_b_stu == 0:
			tcpClicSock.send(('backward').encode())
			c_b_stu = 1

	def call_FB_stop(event):
		global c_f_stu, c_b_stu, c_l_stu, c_r_stu, c_ls_stu, c_rs_stu
		c_f_stu = 0
		c_b_stu = 0
		tcpClicSock.send(('DS').encode())

	def call_turn_stop(event):
		global c_f_stu, c_b_stu, c_l_stu, c_r_stu, c_ls_stu, c_rs_stu
		c_l_stu = 0
		c_r_stu = 0
		c_ls_stu = 0
		c_rs_stu = 0
		tcpClicSock.send(('TS').encode())

	def call_left(event):
		global c_l_stu
		if c_l_stu == 0:
			tcpClicSock.send(('left').encode())
			c_l_stu = 1

	def call_right(event):
		global c_r_stu
		if c_r_stu == 0:
			tcpClicSock.send(('right').encode())
			c_r_stu = 1

	def call_leftside(event):
		global c_ls_stu
		if c_ls_stu == 0:
			tcpClicSock.send(('leftside').encode())
			c_ls_stu = 1

	def call_rightside(event):
		global c_rs_stu
		if c_rs_stu == 0:
			tcpClicSock.send(('rightside').encode())
			c_rs_stu = 1

	Btn0 = tk.Button(root, width=8, text='Left', fg=color_text, bg=color_btn, relief='ridge')
	Btn0.place(x=x, y=y + 17)
	Btn0.bind('<ButtonPress-1>', call_left)
	Btn0.bind('<ButtonRelease-1>', call_turn_stop)
	root.bind('<KeyPress-a>', call_left)
	root.bind('<KeyRelease-a>', call_turn_stop)

	Btn1 = tk.Button(root, width=8, text='Forward', fg=color_text, bg=color_btn, relief='ridge')
	Btn1.place(x=x + 95, y=y)
	Btn1.bind('<ButtonPress-1>', call_forward)
	Btn1.bind('<ButtonRelease-1>', call_FB_stop)
	root.bind('<KeyPress-w>', call_forward)
	root.bind('<KeyRelease-w>', call_FB_stop)

	Btn2 = tk.Button(root, width=8, text='Backward', fg=color_text, bg=color_btn, relief='ridge')
	Btn2.place(x=x + 95, y=y + 35)
	Btn2.bind('<ButtonPress-1>', call_back)
	Btn2.bind('<ButtonRelease-1>', call_FB_stop)
	root.bind('<KeyPress-s>', call_back)
	root.bind('<KeyRelease-s>', call_FB_stop)

	Btn3 = tk.Button(root, width=8, text='Right', fg=color_text, bg=color_btn, relief='ridge')
	Btn3.place(x=x + 190, y=y + 17)
	Btn3.bind('<ButtonPress-1>', call_right)
	Btn3.bind('<ButtonRelease-1>', call_turn_stop)
	root.bind('<KeyPress-d>', call_right)
	root.bind('<KeyRelease-d>', call_turn_stop)

	### these buttons has no function yet
	# Btn_LeftSide = tk.Button(root, width=8, text='<--',fg=color_text,bg=color_btn,relief='ridge')
	# Btn_LeftSide.place(x=30,y=195)
	# Btn_LeftSide.bind('<ButtonPress-1>', call_leftside)
	# Btn_LeftSide.bind('<ButtonRelease-1>', call_turn_stop)
	# root.bind('<KeyPress-q>', call_leftside)
	# root.bind('<KeyRelease-q>', call_turn_stop)

	# Btn_RightSide = tk.Button(root, width=8, text='-->',fg=color_text,bg=color_btn,relief='ridge')
	# Btn_RightSide.place(x=170,y=195)
	# Btn_RightSide.bind('<ButtonPress-1>', call_rightside)
	# Btn_RightSide.bind('<ButtonRelease-1>', call_turn_stop)
	# root.bind('<KeyPress-e>', call_rightside)
	# root.bind('<KeyRelease-e>', call_turn_stop)


def draw_position_button(x, y):
	def call_headup(event):
		tcpClicSock.send(('headup').encode())

	def call_headdown(event):
		tcpClicSock.send(('headdown').encode())

	def call_low(event):
		tcpClicSock.send(('low').encode())

	def call_high(event):
		tcpClicSock.send(('high').encode())

	def call_headhome(event):
		tcpClicSock.send(('headhome').encode())

	Btn_up = tk.Button(root, width=8, text='Up', fg=color_text, bg=color_btn, relief='ridge')
	Btn_up.place(x=x, y=y)
	Btn_up.bind('<ButtonPress-1>', call_headup)
	Btn_up.bind('<ButtonRelease-1>', call_headhome)
	root.bind('<KeyPress-o>', call_headup)
	root.bind('<KeyRelease-o>', call_headhome)

	Btn_down = tk.Button(root, width=8, text='Down', fg=color_text, bg=color_btn, relief='ridge')
	Btn_down.place(x=x, y=y + 70)
	Btn_down.bind('<ButtonPress-1>', call_headdown)
	Btn_down.bind('<ButtonRelease-1>', call_headhome)
	root.bind('<KeyPress-l>', call_headdown)
	root.bind('<KeyRelease-l>', call_headhome)

	Btn_low = tk.Button(root, width=8, text='Low', fg=color_text, bg=color_btn, relief='ridge')
	Btn_low.place(x=x + 95, y=y + 70)
	Btn_low.bind('<ButtonPress-1>', call_low)
	Btn_low.bind('<ButtonRelease-1>', call_headhome)
	root.bind('<KeyPress-k>', call_low)
	root.bind('<KeyRelease-k>', call_headhome)

	Btn_high = tk.Button(root, width=8, text='High', fg=color_text, bg=color_btn, relief='ridge')
	Btn_high.place(x=x + 95, y=y)
	Btn_high.bind('<ButtonPress-1>', call_high)
	Btn_high.bind('<ButtonRelease-1>', call_headhome)
	root.bind('<KeyPress-i>', call_high)
	root.bind('<KeyRelease-i>', call_headhome)

	Btn_home = tk.Button(root, width=8, text='Home', fg=color_text, bg=color_btn, relief='ridge')
	Btn_home.place(x=x + 47, y=y + 35)
	Btn_home.bind('<ButtonPress-1>', call_headhome)
	root.bind('<KeyPress-p>', call_headhome)


def draw_information_screen(x, y):
	global CPU_TEP_lab, CPU_USE_lab, RAM_lab, DIS_lab

	CPU_TEP_lab = tk.Label(root, width=18, text='CPU Temp:', fg=color_text, bg='#212121')
	CPU_TEP_lab.place(x=x, y=y)

	CPU_USE_lab = tk.Label(root, width=18, text='CPU Usage:', fg=color_text, bg='#212121')
	CPU_USE_lab.place(x=x, y=y + 30)

	RAM_lab = tk.Label(root, width=18, text='RAM Usage:', fg=color_text, bg='#212121')
	RAM_lab.place(x=x, y=y + 60)

	DIS_lab = tk.Label(root, width=18, text='Distance:', fg=color_text, bg='#212121')
	DIS_lab.place(x=x, y=y + 90)


def draw_status_screen(x, y):
	global l_ip_4
	l_ip = tk.Label(root, width=18, text='Status', fg=color_text, bg=color_btn)
	l_ip.place(x=x, y=y)

	label_openCV = tk.Label(root, width=28, text='OpenCV Status', fg=color_text, bg=color_btn)
	label_openCV.place(x=x + 150, y=y)

	l_ip_4 = tk.Label(root, width=18, text='Disconnected', fg=color_text, bg='#F44336')
	l_ip_4.place(x=x + 370, y=y)


def draw_connect_screen(x, y):
	global E1, l_ip_5, Btn14

	def connect(event):
		if ip_stu == 1:
			sc = thread.Thread(target=socket_connect_thread)
			sc.setDaemon(True)
			sc.start()

	def connect_click():
		if ip_stu == 1:
			sc = thread.Thread(target=socket_connect_thread)
			sc.setDaemon(True)
			sc.start()

	l_ip_3 = tk.Label(root, width=10, text='IP Address:', fg=color_text, bg='#000000')
	l_ip_3.place(x=x, y=y)

	E1 = tk.Entry(root, show=None, width=16, bg="#37474F", fg='#eceff1')
	E1.place(x=x, y=y + 35)

	l_ip_5 = tk.Label(root, width=16, text='Use default IP', fg=color_text, bg=color_btn)
	l_ip_5.place(x=x, y=y + 70)

	Btn14 = tk.Button(root, width=8, text='Connect', fg=color_text, bg=color_btn, command=connect_click, relief='ridge')
	Btn14.place(x=x + 150, y=y + 35)

	root.bind('<Return>', connect)


def draw_scale_RGB(x, y, w):
	def set_R(event):
		time.sleep(0.03)
		tcpClicSock.send(('ws28 %s %s %s' % (var_R.get(), var_G.get(), var_B.get())).encode())

	def set_G(event):
		time.sleep(0.03)
		tcpClicSock.send(('ws28 %s %s %s' % (var_R.get(), var_G.get(), var_B.get())).encode())

	def set_B(event):
		time.sleep(0.03)
		tcpClicSock.send(('ws28 %s %s %s' % (var_R.get(), var_G.get(), var_B.get())).encode())

	Scale_R = tk.Scale(root, label=None,
					   from_=0, to=255, orient=tk.HORIZONTAL, length=w,
					   showvalue=1, tickinterval=None, resolution=1, variable=var_R, troughcolor='#F44336',
					   command=set_R, fg=color_text, bg=color_bg, highlightthickness=0)
	Scale_R.place(x=x, y=y)

	Scale_G = tk.Scale(root, label=None,
					   from_=0, to=255, orient=tk.HORIZONTAL, length=w,
					   showvalue=1, tickinterval=None, resolution=1, variable=var_G, troughcolor='#00E676',
					   command=set_G, fg=color_text, bg=color_bg, highlightthickness=0)
	Scale_G.place(x=x, y=y + 30)

	Scale_B = tk.Scale(root, label=None,
					   from_=0, to=255, orient=tk.HORIZONTAL, length=w,
					   showvalue=1, tickinterval=None, resolution=1, variable=var_B, troughcolor='#448AFF',
					   command=set_B, fg=color_text, bg=color_bg, highlightthickness=0)
	Scale_B.place(x=x, y=y + 60)

	canvas_cover = tk.Canvas(root, bg=color_bg, height=30, width=510, highlightthickness=0)
	canvas_cover.place(x=x, y=y + 90)


def draw_scale_expcom(x, y, w):
	def EC_send(event):
		tcpClicSock.send(('setEC %s' % var_ec.get()).encode())
		time.sleep(0.03)

	def EC_default(event):
		var_ec.set(0)
		tcpClicSock.send(('defEC').encode())

	Scale_ExpCom = tk.Scale(root, label='Exposure Compensation Level',
							from_=-25, to=25, orient=tk.HORIZONTAL, length=w,
							showvalue=1, tickinterval=None, resolution=1, variable=var_ec, troughcolor='#212121',
							command=EC_send, fg=color_text, bg=color_bg, highlightthickness=0)
	Scale_ExpCom.place(x=x, y=y)

	canvas_cover_exp = tk.Canvas(root, bg=color_bg, height=30, width=510, highlightthickness=0)
	canvas_cover_exp.place(x=x, y=y + 50)

	Btn_dEC = tk.Button(root, width=18, height=2, text='Set Default Exposure\nCompensation Level', fg=color_text,
						bg=color_btn, relief='ridge')
	Btn_dEC.place(x=x + w + 21, y=y + 3)
	Btn_dEC.bind('<ButtonPress-1>', EC_default)


def draw_function_button(x, y):
	global Btn_Steady, Btn_FindColor, Btn_WatchDog, Btn_Fun4, Btn_Fun5, Btn_Fun6

	def call_steady(event):
		if funcMode == 0:
			tcpClicSock.send(('steady').encode())
		else:
			tcpClicSock.send(('funEnd').encode())

	def call_FindColor(event):
		if funcMode == 0:
			tcpClicSock.send(('FindColor').encode())
		else:
			tcpClicSock.send(('funEnd').encode())

	def call_WatchDog(event):
		if funcMode == 0:
			tcpClicSock.send(('WatchDog').encode())
		else:
			tcpClicSock.send(('funEnd').encode())

	def call_func4(event):
		if funcMode == 0:
			tcpClicSock.send(('function_4_on').encode())
		else:
			tcpClicSock.send(('function_4_off').encode())

	def call_func5(event):
		if funcMode == 0:
			tcpClicSock.send(('function_5_on').encode())
		else:
			tcpClicSock.send(('function_5_off').encode())

	def call_func6(event):
		if funcMode == 0:
			tcpClicSock.send(('function_6_on').encode())
		else:
			tcpClicSock.send(('function_6_off').encode())

	Btn_Steady = tk.Button(root, width=7, text='Steady', fg=color_text, bg=color_btn, relief='ridge')
	Btn_Steady.place(x=x, y=y)
	root.bind('<KeyPress-1>', call_steady)
	Btn_Steady.bind('<ButtonPress-1>', call_steady)

	Btn_FindColor = tk.Button(root, width=7, text='FindColor', fg=color_text, bg=color_btn, relief='ridge')
	Btn_FindColor.place(x=x + 85, y=y)
	root.bind('<KeyPress-2>', call_FindColor)
	Btn_FindColor.bind('<ButtonPress-1>', call_FindColor)

	Btn_WatchDog = tk.Button(root, width=7, text='WatchDog', fg=color_text, bg=color_btn, relief='ridge')
	Btn_WatchDog.place(x=x + 85 + 85, y=y)
	root.bind('<KeyPress-3>', call_WatchDog)
	Btn_WatchDog.bind('<ButtonPress-1>', call_WatchDog)

	Btn_Fun4 = tk.Button(root, width=7, text='Function 4', fg=color_text, bg=color_btn, relief='ridge')
	Btn_Fun4.place(x=x + 85 + 85 + 85, y=y)
	root.bind('<KeyPress-4>', call_func4)
	Btn_Fun4.bind('<ButtonPress-1>', call_func4)

	Btn_Fun5 = tk.Button(root, width=7, text='Function 5', fg=color_text, bg=color_btn, relief='ridge')
	Btn_Fun5.place(x=x + 85 + 85 + 85 + 85, y=y)
	root.bind('<KeyPress-5>', call_func5)
	Btn_Fun5.bind('<ButtonPress-1>', call_func5)

	Btn_Fun6 = tk.Button(root, width=7, text='Function 6', fg=color_text, bg=color_btn, relief='ridge')
	Btn_Fun6.place(x=x + 85 + 85 + 85 + 85 + 85, y=y)
	root.bind('<KeyPress-6>', call_func6)
	Btn_Fun6.bind('<ButtonPress-1>', call_func6)


def loop():
	global root, tcpClicSock, connect, canvas_ultra, var_R, var_B, var_G, var_lip1, var_lip2, var_err, var_ec

	def on_closing():
		if messagebox.askokcancel("Quit", "Do you want to quit?"):
			root.destroy()

	root = tk.Tk()
	root.title('Adeept DarkPaw Controller')
	root.geometry('580x700')
	root.config(bg=color_bg)
	root.protocol("WM_DELETE_WINDOW", on_closing)

	var_lip1 = tk.StringVar()
	var_lip1.set(440)
	var_lip2 = tk.StringVar()
	var_lip2.set(380)
	var_err = tk.StringVar()
	var_err.set(20)
	var_R = tk.StringVar()
	var_R.set(0)
	var_G = tk.StringVar()
	var_G.set(0)
	var_B = tk.StringVar()
	var_B.set(0)
	var_ec = tk.StringVar()
	var_ec.set(0)

	try:
		logo = tk.PhotoImage(file='logo.png')
		l_logo = tk.Label(root, image=logo, bg=color_bg)
		l_logo.place(x=30, y=13)
	except:
		pass

	draw_information_screen(400, 15)

	draw_status_screen(30, 130)

	draw_connect_screen(150, 15)

	draw_switch_button(30, 265)

	draw_led_switch_button(30, 300)

	draw_direction_button(30, 170)

	draw_position_button(330, 195)

	draw_scale_RGB(30, 330, 505)

	draw_scale_expcom(30, 610, 315)

	draw_function_button(30, 445)

	draw_scale_FL(30, 490, 315)

	root.mainloop()


if __name__ == '__main__':
	try:
		loop()
	except:
		tcpClicSock.close()
		footage_socket.close()
		cv2.destroyAllWindows()
		pass
