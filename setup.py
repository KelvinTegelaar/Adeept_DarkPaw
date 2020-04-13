#!/usr/bin/python3
# File name   : setup.py
# Description : DarkPaw Setup Script
# Author      : TangoCash
# Date        : 2020/4/13

import os
import sys
import time

try:
	from bluetools import BtAutoPair
except:
	pass

curpath = os.path.realpath(__file__)
thisPath = "/" + os.path.dirname(curpath)
autostart_dir = "/home/pi/.config/autostart"
autostart_file = autostart_dir + "/darkpaw.desktop"


def replace_num(file, initial, new_num):
	newline = ""
	str_num = str(new_num)
	with open(file, "r") as f:
		for line in f.readlines():
			if (line.find(initial) == 0):
				line = (str_num + '\n')
			newline += line
	with open(file, "w") as f:
		f.writelines(newline)


def run_os_command(cmd, max_runs=4):
	try:
		sys.stdout.write('###################################################\n')
		sys.stdout.write('Command: ' + cmd + '\n')
		for x in range(0, max_runs):
			if os.system(cmd) == 0:
				break
	except:
		print('AN ERROR OCCURRED RUNNING THE FOLLOWING COMMAND: ' + cmd)
		pass


def upgrade_system():
	# Upgrade the existing system
	run_os_command("sudo apt-get update")
	run_os_command("sudo apt-get purge -y wolfram-engine")
	run_os_command("sudo apt-get purge -y libreoffice*")
	run_os_command("sudo apt-get -y clean")
	run_os_command("sudo apt-get -y autoremove")
	run_os_command("sudo apt-get -y upgrade")

	# fix conflict with onboard Raspberry Pi audio
	try:
		run_os_command('sudo touch /etc/modprobe.d/snd-blacklist.conf')
		with open("/etc/modprobe.d/snd-blacklist.conf", 'w') as file_to_write:
			file_to_write.write("blacklist snd_bcm2835")
	except:
		pass


def create_autostart_rc():
	try:
		run_os_command('sudo touch //home/pi/startup.sh')
		with open("//home/pi/startup.sh", 'w') as file_to_write:
			file_to_write.write("#!/bin/sh\nsudo python3 " + thisPath + "/server/server.py")
		run_os_command('sudo chmod 777 //home/pi/startup.sh')
		replace_num('/etc/rc.local', 'fi', 'fi\n//home/pi/startup.sh start'
	except:
		print('Autostart failed.  Please try again')
		pass


def create_autostart_x():
	try:
		if (not os.path.exists(autostart_dir)):
			run_os_command("sudo mkdir '" + autostart_dir + "/'", 1)
		if (not os.path.isfile(autostart_file)):
			run_os_command("sudo touch " + autostart_file, 1)

		with open(autostart_file, 'w') as file_to_write:
			file_to_write.write(
				"[Desktop Entry]\n   Name=DarkPaw\n   Comment=DarkPaw\n   Exec=sudo python3 " + thisPath + "/server/server.py\n   Icon=false\n   Terminal=false\n   MutipleArgs=false\n   Type=Application\n   Catagories=Application;Development;\n   StartupNotify=true")
	except:
		print('Autostart failed.  Please try again')
		pass


def reboot_system():
	# Reboot the server to have the changes take effect
	run_os_command("sudo reboot")


def install_darkpaw():
	# Enable the interface(s)
	try:
		replace_num("/boot/config.txt", '#dtparam=i2c_arm=on', 'dtparam=i2c_arm=on\nstart_x=1\n')
	except:
		pass

	# Prepare to install.  Clean & Update the repositories
	run_os_command("sudo apt-get clean")
	run_os_command("sudo apt-get update")

	# Install software #1
	run_os_command("sudo apt-get install -y python-dev python-pip libfreetype6-dev libjpeg-dev build-essential")
	run_os_command("sudo apt-get install -y i2c-tools")
	run_os_command("sudo apt-get install -y python3-smbus")
	run_os_command(
		"sudo apt-get install -y libqtgui4 libhdf5-dev libhdf5-serial-dev libatlas-base-dev libjasper-dev libqt4-test")

	# Create the Access Point
	run_os_command("git clone https://github.com/oblique/create_ap.git")
	run_os_command("cd //home/pi/create_ap && sudo make install", 1)

	# Install software #2
	run_os_command("sudo apt-get install -y util-linux procps hostapd iproute2 iw haveged dnsmasq")

	# Install python modules
	run_os_command("sudo pip3 install -U pip")
	run_os_command("sudo -H pip3 install --upgrade luma.oled")
	run_os_command("sudo pip3 install adafruit-pca9685")
	run_os_command("sudo pip3 install rpi_ws281x")
	run_os_command("sudo pip3 install mpu6050-raspberrypi")
	run_os_command("sudo pip3 install flask")
	run_os_command("sudo pip3 install flask_cors")
	run_os_command("sudo pip3 install websockets")
	run_os_command("sudo pip3 install opencv-contrib-python==3.4.3.18")
	run_os_command("sudo pip3 install numpy")
	run_os_command("sudo pip3 install imutils zmq pybase64 psutil")

	# Set up the autostart
	create_autostart_rc()


def install_controller():
	# Install Software
	run_os_command("sudo apt-get install bluetooth libbluetooth3 libbluetooth-dev libusb-dev")
	run_os_command("sudo systemctl enable bluetooth.service")
	run_os_command("sudo usermod -G bluetooth -a pi")

	# PS3 controller pairing tool
	run_os_command("mkdir //home/pi/sixpair")
	run_os_command("wget -O //home/pi/sixpair/sixpair.c http://www.pabr.org/sixlinux/sixpair.c")
	run_os_command("cd //home/pi/sixpair && gcc -o sixpair sixpair.c -lusb")

	# Install python modules
	run_os_command("sudo pip3 install dbus-python pexpect pygame")


def set_new_master()
	# Set new bluetooth master for PS3 Controller
	sys.stdout.write('###################################################\n')
	sys.stdout.write('PLEASE CONNECT PS3 CONTROLLER VIA USB..............\n')
	sys.stdout.write('###################################################\n')

	run_os_command("sudo //home/pi/sixpair/sixpair")

	sys.stdout.write('###################################################\n')
	sys.stdout.write('PLEASE DISCONNECT PS3 CONTROLLER...................\n')
	sys.stdout.write('###################################################\n')


def connect_controller()
	# this is still in development
	autopair = BtAutoPair.BtAutoPair()
	autopair.enable_pairing()
	sys.stdout.write('###################################################\n')
	sys.stdout.write('PRESS PS BUTTON ON THE PS3 CONTROLLER (10 sec).....\n')
	sys.stdout.write('###################################################\n')
	time.sleep(10)
	autopair.disable_pairing()


while True:
	try:
		selection = int(input(
			"Select an option:\n    1 = Upgrade OS;\n    2 = Install DarkPaw;\n    3 = Install Game Controller;\n    4 = Pair Game Controller;\n    5 = Reboot;\n    6 = Exit\n\nOption to select: "))

		if selection == 1:
			upgrade_system()
			sys.stdout.write('###################################################\n')
			sys.stdout.write('IT IS RECOMMENDED YOU REBOOT BEFORE CONTINUING.....\n')
			sys.stdout.write('###################################################\n')
		elif selection == 2:
			install_darkpaw()
		elif selection == 3:
			install_controller()
			sys.stdout.write('###################################################\n')
			sys.stdout.write('IT IS RECOMMENDED YOU REBOOT BEFORE CONTINUING.....\n')
			sys.stdout.write('###################################################\n')
		elif selection == 4:
			set_new_master()
			connect_controller()
		elif selection == 5:
			reboot_system()
		elif selection == 6:
			break
		else:
			print("Invalid selection.  Please try again")
	except:
		print("Invalid selection.  Please try again")
		pass
