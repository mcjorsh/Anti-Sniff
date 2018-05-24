#/usr/bin/python

import configparser
import random
from random import choice
import hashlib
import time
import socket
import sys
import http.server
import subprocess
from http.server import SimpleHTTPRequestHandler
import ssl
import logging
import os, sys

logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

#netsh bridge set adapter 1 forcecompatmode=enable correr eso en cmd de windows para deshabilitar el modo promiscuo

def Config(section):
	Conf = configparser.ConfigParser()
	Conf.read('server_conf/stinky.conf')
	drawer = {}
	options = Conf.options(section)
	for option in options:
		try:
			drawer[option] = Conf.get(section, option)
			if drawer[option]== -1:
				DebugPrint("Skip: %s" % option)
		except:
			print(("Exception %s" % option))
			drawer[option] = None
	return drawer

class Handle(http.server.BaseHTTPRequestHandler):

	def do_GET(self):
		audit_path = str.split(self.path, "?")
		if self.path != "/" and audit_path[0] != "server_conf/login.php" and self.path != "server_conf/favicon.ico":
			self.send_error(404, "file not found")
			return
		self.send_response(200)
		self.send_header("Content-type","text/html")
		self.end_headers()
		try:
			stdout = sys.stdout
			sys.stdout = self.wfile
			self.makepage()
		finally:
			sys.stdout = stdout

	def makepage(self):
		if self.path == "/":
			f = open("server_conf/index.html","r")
		elif self.path == "server_conf/favicon.ico":
			f = open("server_conf/favicon.ico","r")
		else:
			write = True
			whitelist = str.split(Config("WebServ")["whitelist"],',')

			for ip in whitelist:
				if self.address_string() == ip:
					write = False
					break
			if write == True:
				current = str(time.time())
				alert_string = self.address_string() + ":" + self.path + ":" + current + "\n"
				alert = open("server_conf/log.stinky","a")
				alert.write(alert_string)
				alert.close()
			
			f = open("server_conf/login.html","r")
		#Main Page Writing flow
		rep = f.read()
		f.close()
		self.wfile.write(bytes(rep, 'utf8'))
		list_stuff = str.split(Config("WebServ")['list'],',')
		for i in list_stuff:
			chance = random.randint(1,4)
			if chance == 4:
				num = random.randint(90000,9000000)
				hashlib.md5(str(num).encode('utf8')).hexdigest()
