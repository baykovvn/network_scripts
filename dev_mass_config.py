import sys
import time
import paramiko
import os
import cmd
import datetime
import getpass

#set date and time
os.system('clear')
now = datetime.datetime.now()

# HOSTS = open('devices')  # list of devices ip's
INPUTCOM = open('command_line_input')  # list of commands for apply
USER = 'aa'
PASSWORD = 'xx'

USER = str(raw_input ('Login: '))

PASSWORD = getpass.getpass(prompt='Password: ', stream=None) # request password for connection to switch

HOSTS = open(raw_input ('Please enter switch list file name for mass configuration change: '))


all_ips = [ip.rstrip() for ip in HOSTS] # Collect all IPs to var
all_commands = [comm.rstrip() for comm in INPUTCOM] # Collect all commands from file to massive
save_com = all_commands[:] # save all commands to another var
print save_com
print '  Summary of All IP adresses: ',len(all_ips)
print '  List of IP: ',all_ips


while len(all_ips) > 0:
 	ip = all_ips.pop(0) 
	all_commands = save_com[:]
 	print ' ---- connect to ',ip,' Command for applying:  ',len(all_commands)
	print ' ---- List of command for configuration: \n',all_commands
	#ssh session start
 	client = paramiko.SSHClient()
	client.set_missing_host_key_policy(paramiko.AutoAddPolicy())   #auto accept host key
 	client.connect(ip, username=USER, password=PASSWORD)

	#ssh shell
 	chan = client.invoke_shell()
 	time.sleep(1)

 	chan.send('terminal len 0\n')
 	time.sleep(1)

	while len(all_commands) > 0:		
		comm = all_commands.pop(0)
		print '......applaying: ',comm
		chan.send(comm+'\n')
 		time.sleep(1) 		

	#close ssh session
 	client.close()
 	print ' ---- Successful! ---- '
