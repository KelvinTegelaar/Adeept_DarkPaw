#!/usr/bin/env/python
# File name   : server.py
# Production  : GWR
# Website     : www.adeept.com
# Author      : William
# Date        : 2020/03/17

import time
import threading
import move
import SpiderG
SpiderG.move_init()
import Adafruit_PCA9685
import os
import info
import servo

#import functions
import LED
import switch
import socket

#websocket
import asyncio
import websockets

import json
import app

functionMode = 0
speed_set = 100
rad = 0.5
turnWiggle = 60

# modeSelect = 'none'
modeSelect = 'PT'

curpath = os.path.realpath(__file__)
thisPath = "/" + os.path.dirname(curpath)

direction_command = 'no'
turn_command = 'no'

def FPV_thread():
    global fpv
    fpv=FPV.FPV()
    fpv.capture_thread(addr[0])


def ap_thread():
    os.system("sudo create_ap wlan0 eth0 DarkPaw 12345678")


def functionSelect(command_input, response):
    global functionMode
    if 'findColor' == command_input:
        if modeSelect == 'PT':
            flask_app.modeselect('findColor')

    elif 'motionGet' == command_input:
        flask_app.modeselect('watchDog')

    elif 'stopCV' == command_input:
        flask_app.modeselect('none')
        switch.switch(1,0)
        switch.switch(2,0)
        switch.switch(3,0)

    elif 'police' == command_input:
        switch.switch(3,1)

    elif 'policeOff' == command_input:
        switch.switch(3,0)

#    elif 'automatic' == command_input:
#        if modeSelect == 'PT':
#            fuc.automatic()
#        else:
#            fuc.pause()

#    elif 'automaticOff' == command_input:
#        fuc.pause()
#        move.motorStop()

#    elif 'trackLine' == command_input:
#        fuc.trackLine()

#    elif 'trackLineOff' == command_input:
#        fuc.pause()
#        move.motorStop()

    elif 'steadyCamera' == command_input:
        SpiderG.steadyModeOn()

    elif 'steadyCameraOff' == command_input:
        SpiderG.steadyModeOff()
        SpiderG.move_init()


def switchCtrl(command_input, response):
    if 'Switch_1_on' in command_input:
        switch.switch(1,1)

    elif 'Switch_1_off' in command_input:
        switch.switch(1,0)

    elif 'Switch_2_on' in command_input:
        switch.switch(2,1)

    elif 'Switch_2_off' in command_input:
        switch.switch(2,0)

    elif 'Switch_3_on' in command_input:
        switch.switch(3,1)

    elif 'Switch_3_off' in command_input:
        switch.switch(3,0) 


def robotCtrl(command_input, response):
    global direction_command, turn_command
    if 'forward' == command_input:
        direction_command = 'forward'
        SpiderG.walk('forward')
    
    elif 'backward' == command_input:
        direction_command = 'backward'
        SpiderG.walk('backward')

    elif 'DS' in command_input:
        direction_command = 'no'
        if turn_command == 'no':
            SpiderG.servoStop()

    elif 'left' == command_input:
        turn_command = 'left'
        SpiderG.walk('turnleft')

    elif 'right' == command_input:
        turn_command = 'right'
        SpiderG.walk('turnright')

    elif 'TS' in command_input:
        turn_command = 'no'
        if direction_command == 'no':
            SpiderG.servoStop()
        #else:
        #    move.move(speed_set, direction_command, 'no', rad)


#    elif 'lookleft' == command_input:
#        P_sc.singleServo(14, -1, 3)
#
#    elif 'lookright' == command_input:
#        P_sc.singleServo(14, 1, 3)
#
#    elif 'LRstop' in command_input:
#        P_sc.stopWiggle()

    elif 'up' == command_input:
        direction_command == 'no'
        SpiderG.walk('StandUp')

    elif 'down' == command_input:
        direction_command == 'no'
        SpiderG.walk('StayLow')

#    elif 'UDstop' in command_input:
#        T_sc.stopWiggle()
#

    elif 'handup' == command_input:
        direction_command == 'no'
        SpiderG.status_GenOut(0, -150, 0)
        SpiderG.direct_M_move()

    elif 'handdown' == command_input:
        direction_command == 'no'
        SpiderG.status_GenOut(0, 150, 0)
        SpiderG.direct_M_move()

#
#    elif 'HAstop' in command_input:
#        H1_sc.stopWiggle()
#        H2_sc.stopWiggle()


#    elif 'grab' == command_input:
#        G_sc.singleServo(15, 1, 3)

    elif 'loose' == command_input:
        SpiderG.move_init()

    elif 'stop' == command_input:
        SpiderG.servoStop()

    elif 'home' == command_input:
        SpiderG.move_init()

def wifi_check():
    try:
        s =socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        s.connect(("1.1.1.1",80))
        ipaddr_check=s.getsockname()[0]
        s.close()
        print(ipaddr_check)
    except:
        ap_threading=threading.Thread(target=ap_thread)   #Define a thread for data receiving
        ap_threading.setDaemon(True)                          #'True' means it is a front thread,it would close when the mainloop() closes
        ap_threading.start()                                  #Thread starts
        LED  = LED.LED()
        LED.colorWipe(0,16,50)
        time.sleep(1)
        LED.colorWipe(0,16,100)
        time.sleep(1)
        LED.colorWipe(0,16,150)
        time.sleep(1)
        LED.colorWipe(0,16,200)
        time.sleep(1)
        LED.colorWipe(0,16,255)
        time.sleep(1)
        LED.colorWipe(35,255,35)

async def check_permit(websocket):
    while True:
        recv_str = await websocket.recv()
        cred_dict = recv_str.split(":")
        if cred_dict[0] == "admin" and cred_dict[1] == "123456":
            response_str = "congratulation, you have connect with server\r\nnow, you can do something else"
            await websocket.send(response_str)
            return True
        else:
            response_str = "sorry, the username or password is wrong, please submit again"
            await websocket.send(response_str)

async def recv_msg(websocket):
    global speed_set, modeSelect
    direction_command = 'no'
    turn_command = 'no'

    while True: 
        response = {
            'status' : 'ok',
            'title' : '',
            'data' : None
        }

        data = ''
        data = await websocket.recv()
        try:
            data = json.loads(data)
        except Exception as e:
            print('not A JSON')

        if not data:
            continue

        if isinstance(data,str):
            robotCtrl(data, response)

            switchCtrl(data, response)

            functionSelect(data, response)

            if 'get_info' == data:
                response['title'] = 'get_info'
                response['data'] = [info.get_cpu_tempfunc(), info.get_cpu_use(), info.get_ram_info()]

            if 'wsB' in data:
                try:
                    set_B=data.split()
                    speed_set = int(set_B[1])
                except:
                    pass

            elif 'AR' == data:
                modeSelect = 'AR'
                screen.screen_show(4, 'ARM MODE ON')
                try:
                    fpv.changeMode('ARM MODE ON')
                except:
                    pass

            elif 'PT' == data:
                modeSelect = 'PT'
                screen.screen_show(4, 'PT MODE ON')
                try:
                    fpv.changeMode('PT MODE ON')
                except:
                    pass

            #CVFL
            elif 'CVFL' == data:
                flask_app.modeselect('findlineCV')

            elif 'CVFLColorSet' in data:
                color = int(data.split()[1])
                flask_app.camera.colorSet(color)

            elif 'CVFLL1' in data:
                pos = int(data.split()[1])
                flask_app.camera.linePosSet_1(pos)

            elif 'CVFLL2' in data:
                pos = int(data.split()[1])
                flask_app.camera.linePosSet_2(pos)

            elif 'CVFLSP' in data:
                err = int(data.split()[1])
                flask_app.camera.errorSet(err)

            elif 'defEC' in data:#Z
                fpv.defaultExpCom()

        elif(isinstance(data,dict)):
            if data['title'] == "findColorSet":
                color = data['data']
                flask_app.colorFindSet(color[0],color[1],color[2])

        print(data)
        response = json.dumps(response)
        await websocket.send(response)

async def main_logic(websocket, path):
    await check_permit(websocket)
    await recv_msg(websocket)

if __name__ == '__main__':
    switch.switchSetup()
    switch.set_all_switch_off()

    HOST = ''
    PORT = 10223                              #Define port serial 
    BUFSIZ = 1024                             #Define buffer size
    ADDR = (HOST, PORT)

    global flask_app
    flask_app = app.webapp()
    flask_app.startthread()

    try:
        LED  = LED.LED()
        LED.colorWipe(255,16,0)
    except:
        print('Use "sudo pip3 install rpi_ws281x" to install WS_281x package\n使用"sudo pip3 install rpi_ws281x"命令来安装rpi_ws281x')
        pass

    while  1:
        wifi_check()
        try:                  #Start server,waiting for client
            start_server = websockets.serve(main_logic, '0.0.0.0', 8888)
            asyncio.get_event_loop().run_until_complete(start_server)
            print('waiting for connection...')
            # print('...connected from :', addr)
            break
        except Exception as e:
            print(e)
            LED.colorWipe(0,0,0)

        try:
            LED.colorWipe(0,80,255)
        except:
            pass
    try:
        asyncio.get_event_loop().run_forever()
    except Exception as e:
        print(e)
        LED.colorWipe(0,0,0)
        move.destroy()
