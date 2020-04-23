#!/usr/bin/env/python
# File name   : server.py
# Production  : GWR
# Website     : www.gewbot.com
# E-mail      : gewubot@163.com
# Author      : William
# Date        : 2019/07/24

import socket
import threading
import time
import pygame

import SpiderG

SpiderG.move_init()
import os
import FPV
import info
import LED
import switch

import ultra

SR_dect = 0

if SR_dect:
	try:
		import SR
		SR_dect = 1
	except:
		SR_dect = 0
		pass

SR_mode = 0

functionMode = 0

try:
	from bluetools import BtAutoPair
except:
	pass

PS3_BUTTON_CROSS = 0
PS3_BUTTON_CIRCLE = 1
PS3_BUTTON_TRIANGLE = 2
PS3_BUTTON_SQUARE = 3
PS3_BUTTON_L1 = 4
PS3_BUTTON_R1 = 5
PS3_BUTTON_L2 = 6
PS3_BUTTON_R2 = 7
PS3_BUTTON_SELECT = 8
PS3_BUTTON_START = 9
PS3_BUTTON_PS = 10
PS3_BUTTON_LP = 11
PS3_BUTTON_RP = 12
PS3_BUTTON_UP = 13
PS3_BUTTON_DOWN = 14
PS3_BUTTON_LEFT = 15
PS3_BUTTON_RIGHT = 16
PS3_AXIS_LEFT_HORIZONTAL = 0
PS3_AXIS_LEFT_VERTICAL = 1
PS3_AXIS_RIGHT_HORIZONTAL = 2
PS3_AXIS_RIGHT_VERTICAL = 3

def controller_thread():
	global autopair
	autopair = BtAutoPair.BtAutoPair()
	autopair.enable_pairing()
	time.sleep(2)
	pygame.init()
	clock = pygame.time.Clock()
	joystickfound = False
	while not joystickfound:
		try:
			pygame.joystick.init()
			if pygame.joystick.get_count() < 1:
				pygame.joystick.quit()
				time.sleep(0.1)
			else:
				joystick = pygame.joystick.Joystick(0)
				joystickfound = True
				break
		except pygame.error:
			pygame.joystick.quit()
			time.sleep(0.1)

	joystick.init()
	while 1:
		hadEvent = False
		for event in pygame.event.get():
			if event.type == pygame.JOYBUTTONDOWN:
				print(event.dict, event.joy, event.button, 'pressed')
				if event.button == PS3_BUTTON_UP:
					SpiderG.walk('forward')
				elif event.button == PS3_BUTTON_DOWN:
					SpiderG.walk('backward')
				elif event.button == PS3_BUTTON_LEFT:
					SpiderG.walk('turnleft')
				elif event.button == PS3_BUTTON_RIGHT:
					SpiderG.walk('turnright')
				elif event.button == PS3_BUTTON_TRIANGLE:
					SpiderG.status_GenOut(0, -150, 0)
					SpiderG.direct_M_move()
				elif event.button == PS3_BUTTON_CROSS:
					SpiderG.status_GenOut(0, 150, 0)
					SpiderG.direct_M_move()
				elif event.button == PS3_BUTTON_CIRCLE:
					SpiderG.status_GenOut(200, 0, 0)
					SpiderG.direct_M_move()
				elif event.button == PS3_BUTTON_SQUARE:
					SpiderG.status_GenOut(-200, 0, 0)
					SpiderG.direct_M_move()
			elif event.type == pygame.JOYBUTTONUP:
				print(event.dict, event.joy, event.button, 'released')
				if event.button == PS3_BUTTON_TRIANGLE:
					SpiderG.status_GenOut(0, 0, 0)
					SpiderG.direct_M_move()
				elif event.button == PS3_BUTTON_CROSS:
					SpiderG.status_GenOut(0, 0, 0)
					SpiderG.direct_M_move()
				elif event.button == PS3_BUTTON_CIRCLE:
					SpiderG.status_GenOut(0, 0, 0)
					SpiderG.direct_M_move()
				elif event.button == PS3_BUTTON_SQUARE:
					SpiderG.status_GenOut(0, 0, 0)
					SpiderG.direct_M_move()
				else:
					SpiderG.servoStop()
#			elif event.type == pygame.JOYAXISMOTION:
#				print(event.dict, event.joy, event.axis, event.value)
		clock.tick(30)
	autopair.disable_pairing()

def ultra_sonic():
	global ultra_distance
	while 1:
		if not SpiderG.autopilot:
			ultra_distance = ultra.checkdist()
		time.sleep(1)

class SR_ctrl(threading.Thread):
	def __init__(self, *args, **kwargs):
		super(SR_ctrl, self).__init__(*args, **kwargs)
		self.__flag = threading.Event()
		self.__flag.set()
		self.__running = threading.Event()
		self.__running.set()

	def run(self):
		global goal_pos, servo_command, init_get, functionMode
		while self.__running.isSet():
			self.__flag.wait()
			if SR_mode:
				voice_command = SR.run()
				if voice_command == 'forward':
					SpiderG.walk('forward')
					time.sleep(2)
					SpiderG.servoStop()

				elif voice_command == 'backward':
					SpiderG.walk('backward')
					time.sleep(2)
					SpiderG.servoStop()

				elif voice_command == 'left':
					SpiderG.walk('turnleft')
					time.sleep(5)
					SpiderG.servoStop()

				elif voice_command == 'right':
					SpiderG.walk('turnright')
					time.sleep(5)
					SpiderG.servoStop()

				elif voice_command == 'stop':
					SpiderG.servoStop()
			else:
				self.pause()

	def pause(self):
		self.__flag.clear()

	def resume(self):
		self.__flag.set()

	def stop(self):
		self.__flag.set()
		self.__running.clear()

def info_send_client():
	global ultra_distance
	SERVER_IP = addr[0]
	SERVER_PORT = 2256  # Define port serial
	SERVER_ADDR = (SERVER_IP, SERVER_PORT)
	Info_Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Set connection value for socket
	Info_Socket.connect(SERVER_ADDR)
	print(SERVER_ADDR)
	while 1:
		try:
			Info_Socket.send((info.get_cpu_tempfunc() + ' ' + info.get_cpu_use() + ' ' + info.get_ram_info() + ' ' + str(SpiderG.get_direction()) + ' ' + str(ultra_distance)).encode())
			time.sleep(1)
		except:
			time.sleep(10)
			pass


def FPV_thread():
	global fpv
	fpv = FPV.FPV()
	fpv.capture_thread(addr[0])


def ap_thread():
	os.system("sudo create_ap wlan0 eth0 DarkPaw 12345678")


def run():
	global ultra_distance, functionMode, direction_command, turn_command

	ultra_distance = 0
	direction_command = 'no'
	turn_command = 'no'

	ultra_threading = threading.Thread(target=ultra_sonic)
	ultra_threading.setDaemon(True)								# 'True' means it is a front thread,it would close when the mainloop() closes
	ultra_threading.start()										# Thread starts

	while True:
		data = ''
		data = str(tcpCliSock.recv(BUFSIZ).decode())
		if not data:
			continue

		elif 'forward' == data:
			print('1')
			SpiderG.walk('forward')

		elif 'backward' == data:
			SpiderG.walk('backward')

		elif 'DS' in data:
			if turn_command == 'no':
				SpiderG.servoStop()

		elif 'left' == data:
			SpiderG.walk('turnleft')

		elif 'right' == data:
			SpiderG.walk('turnright')

		elif 'TS' in data:
			if direction_command == 'no':
				SpiderG.servoStop()


		elif 'Switch_1_on' in data:
			switch.switch(1, 1)
			tcpCliSock.send(('Switch_1_on').encode())

		elif 'Switch_1_off' in data:
			switch.switch(1, 0)
			tcpCliSock.send(('Switch_1_off').encode())

		elif 'Switch_2_on' in data:
			switch.switch(2, 1)
			tcpCliSock.send(('Switch_2_on').encode())

		elif 'Switch_2_off' in data:
			switch.switch(2, 0)
			tcpCliSock.send(('Switch_2_off').encode())

		elif 'Switch_3_on' in data:
			switch.switch(3, 1)
			tcpCliSock.send(('Switch_3_on').encode())

		elif 'Switch_3_off' in data:
			switch.switch(3, 0)
			tcpCliSock.send(('Switch_3_off').encode())


		elif 'function_1_on' in data:  # Steady
			functionMode = 1
			SpiderG.steadyModeOn()
			tcpCliSock.send(('function_1_on').encode())

		elif 'function_2_on' in data:  # Color Find
			functionMode = 2
			fpv.FindColor(1)
			tcpCliSock.send(('function_2_on').encode())

		elif 'function_3_on' in data:  # Watch Dog
			functionMode = 3
			fpv.WatchDog(1)
			tcpCliSock.send(('function_3_on').encode())

		elif 'function_4_on' in data:  # T/D
			functionMode = 4
			SpiderG.gait_set = 0
			tcpCliSock.send(('function_4_on').encode())

		elif 'function_5_on' in data:  # None (Action 1)
			functionMode = 5
			tcpCliSock.send(('function_5_on').encode())
			SpiderG.action_1()
			functionMode = 0
			tcpCliSock.send(('function_5_off').encode())

		elif 'function_6_on' in data:  # None (Action 2)
			functionMode = 6
			tcpCliSock.send(('function_6_on').encode())
			SpiderG.action_2()
			functionMode = 0
			tcpCliSock.send(('function_6_off').encode())

		elif 'function_1_off' in data:
			functionMode = 1
			SpiderG.steadyModeOff()
			tcpCliSock.send(('function_1_off').encode())

		elif 'function_2_off' in data:
			functionMode = 0
			fpv.FindColor(0)
			switch.switch(1, 0)
			switch.switch(2, 0)
			switch.switch(3, 0)
			tcpCliSock.send(('function_2_off').encode())

		elif 'function_3_off' in data:
			functionMode = 0
			fpv.WatchDog(0)
			tcpCliSock.send(('function_3_off').encode())

		elif 'function_4_off' in data:
			functionMode = 0
			SpiderG.gait_set = 1
			tcpCliSock.send(('function_4_off').encode())

		elif 'function_5_off' in data:
			functionMode = 0
			tcpCliSock.send(('function_5_off').encode())

		elif 'function_6_off' in data:
			functionMode = 0
			tcpCliSock.send(('function_6_off').encode())


		elif 'lookleft' == data:
			servo_command = 'lookleft'
			SpiderG.headLeft()

		elif 'lookright' == data:
			servo_command = 'lookright'
			SpiderG.headRight()

		elif 'up' == data:
			servo_command = 'up'
			SpiderG.headUp()

		elif 'down' == data:
			servo_command = 'down'
			SpiderG.headDown()

		elif 'stop' == data:
			if not functionMode:
				SpiderG.headStop()
			servo_command = 'no'
			pass

		elif 'home' == data:
			SpiderG.move_init()

		elif 'ws28' in data:
			try:
				set_ws28 = data.split()
				led.colorWipe(int(set_ws28[1]), int(set_ws28[2]), int(set_ws28[3]))
			except:
				pass

		elif 'StandUp' == data:
			SpiderG.walk('StandUp')

		elif 'StayLow' == data:
			SpiderG.walk('StayLow')

		elif 'Lean-R' == data:
			SpiderG.walk('Lean-R')

		elif 'Lean-L' == data:
			SpiderG.walk('Lean-L')

		elif 'CVFL' in data:  # 2 start
			if not FPV.FindLineMode:
				FPV.FindLineMode = 1
				tcpCliSock.send(('CVFL_on').encode())
			else:
				# move.motorStop()
				# FPV.cvFindLineOff()
				FPV.FindLineMode = 0
				tcpCliSock.send(('CVFL_off').encode())
				SpiderG.servoStop()

		elif 'Render' in data:
			if FPV.frameRender:
				FPV.frameRender = 0
			else:
				FPV.frameRender = 1

		elif 'WBswitch' in data:
			if FPV.lineColorSet == 255:
				FPV.lineColorSet = 0
			else:
				FPV.lineColorSet = 255

		elif 'lip1' in data:
			try:
				set_lip1 = data.split()
				lip1_set = int(set_lip1[1])
				FPV.linePos_1 = lip1_set
			except:
				pass

		elif 'lip2' in data:
			try:
				set_lip2 = data.split()
				lip2_set = int(set_lip2[1])
				FPV.linePos_2 = lip2_set
			except:
				pass

		elif 'err' in data:  # 2 end
			try:
				set_err = data.split()
				err_set = int(set_err[1])
				FPV.findLineError = err_set
			except:
				pass

		elif 'setEC' in data:  # Z
			ECset = data.split()
			try:
				fpv.setExpCom(int(ECset[1]))
			except Exception as e:
				print(e)

		elif 'defEC' in data:  # Z
			fpv.defaultExpCom()

		elif 'headup' in data:  # 3
			SpiderG.status_GenOut(0, -150, 0)
			SpiderG.direct_M_move()

		elif 'headdown' in data:  # 3
			SpiderG.status_GenOut(0, 150, 0)
			SpiderG.direct_M_move()

		elif 'low' in data:  # 3
			SpiderG.status_GenOut(200, 0, 0)
			SpiderG.direct_M_move()

		elif 'high' in data:  # 3
			SpiderG.status_GenOut(-200, 0, 0)
			SpiderG.direct_M_move()

		elif 'home' in data:  # 3
			SpiderG.status_GenOut(0, 0, 0)
			SpiderG.direct_M_move()

		elif 'breath' in data:
			if ledthread.ledfunc != 'breath':
				tcpCliSock.send(('breath_off').encode())
				tcpCliSock.send(('police_off').encode())
				tcpCliSock.send(('rainbow_off').encode())
				ledthread.ledfunc = 'breath'
				ledthread.resume()
				tcpCliSock.send(('breath_on').encode())
			elif ledthread.ledfunc == 'breath':
				ledthread.ledfunc = ''
				ledthread.pause()
				tcpCliSock.send(('breath_off').encode())

		elif 'police' in data:
			if ledthread.ledfunc != 'police':
				tcpCliSock.send(('breath_off').encode())
				tcpCliSock.send(('police_off').encode())
				tcpCliSock.send(('rainbow_off').encode())
				ledthread.ledfunc = 'police'
				ledthread.resume()
				tcpCliSock.send(('police_on').encode())
			elif ledthread.ledfunc == 'police':
				ledthread.ledfunc = ''
				ledthread.pause()
				tcpCliSock.send(('police_off').encode())

		elif 'rainbow' in data:
			if ledthread.ledfunc != 'rainbow':
				tcpCliSock.send(('breath_off').encode())
				tcpCliSock.send(('police_off').encode())
				tcpCliSock.send(('rainbow_off').encode())
				ledthread.ledfunc = 'rainbow'
				ledthread.resume()
				tcpCliSock.send(('rainbow_on').encode())
			elif ledthread.ledfunc == 'rainbow':
				ledthread.ledfunc = ''
				ledthread.pause()
				tcpCliSock.send(('rainbow_off').encode())
		else:
			pass

		print(data)
		print(ultra_distance)


def wifi_check():
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		s.connect(("1.1.1.1", 80))
		ipaddr_check = s.getsockname()[0]
		s.close()
		print(ipaddr_check)

	except:
		ap_threading = threading.Thread(target=ap_thread)	# Define a thread for data receiving
		ap_threading.setDaemon(True)						# 'True' means it is a front thread,it would close when the mainloop() closes
		ap_threading.start()								# Thread starts

		led.colorWipe(0, 16, 50)
		time.sleep(1)

		led.colorWipe(0, 16, 100)
		time.sleep(1)

		led.colorWipe(0, 16, 150)
		time.sleep(1)

		led.colorWipe(0, 16, 200)
		time.sleep(1)

		led.colorWipe(0, 16, 255)
		time.sleep(1)

		led.colorWipe(35, 255, 35)


if __name__ == '__main__':
	switch.switchSetup()
	switch.set_all_switch_off()

	HOST = ''
	PORT = 10223  # Define port serial
	BUFSIZ = 1024  # Define buffer size
	ADDR = (HOST, PORT)

	led = LED.LED()
	led.colorWipe(255, 16, 0)
	ledthread = LED.LED_ctrl()
	ledthread.start()

	if SR_dect:
		sr = SR_ctrl()
		sr.start()

	controller_threading = threading.Thread(target=controller_thread)
	controller_threading.setDaemon(True)
	controller_threading.start()

	while 1:
		wifi_check()
		try:
			tcpSerSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			tcpSerSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
			tcpSerSock.bind(ADDR)
			tcpSerSock.listen(5)  # Start server,waiting for client
			print('waiting for connection...')
			try:
				tcpCliSock, addr = tcpSerSock.accept()
			except KeyboardInterrupt:
				try:
					if tcpCliSock:
						tcpCliSock.close()
				except: pass
				break
			print('...connected from :', addr)

			info_threading = threading.Thread(target=info_send_client)	# Define a thread for FPV and OpenCV
			info_threading.setDaemon(True)								# 'True' means it is a front thread,it would close when the mainloop() closes
			info_threading.start()										# Thread starts

			fpv = FPV.FPV()
			fps_threading = threading.Thread(target=FPV_thread)	# Define a thread for FPV and OpenCV
			fps_threading.setDaemon(True)						# 'True' means it is a front thread,it would close when the mainloop() closes
			fps_threading.start()								# Thread starts
			break
		except:
			led.colorWipe(0, 0, 0)

		try:
			led.colorWipe(0, 80, 255)
		except:
			pass
	run()
	try:
		run()
	except:
		led.colorWipe(0, 0, 0)
