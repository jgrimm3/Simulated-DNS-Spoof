import subprocess
import sys

if len(sys.argv) != 2:
	print('Usage: python dnssec.py <hostname>')
	exit()

command = 'drill -k Kbombast.com.+008+34584.key -D %s.bombast.com' % sys.argv[1]
process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)

proc_stdout = process.communicate()[0].strip()
validity = proc_stdout.find('Bad data;')
if validity != -1:
	print('DNS Query Failed! Could not validate response.\nRetrying query with vpn...\nResetting routing tables')
	command = 'route del -net 0.0.0.0 gw 10.4.9.2 netmask 0.0.0.0 dev eth0; route del -net 10.4.9.5 gw 10.4.9.2 netmask 255.255.255.255 dev eth0;'
	process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
	print('Adding VPN Path')
	command = 'route add default gw 10.4.9.1; route add 10.4.9.5 gw 10.4.9.1'
	process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
	print('Retrying query thru VPN')
	command = 'drill -k Kbombast.com.+008+34584.key -D %s.bombast.com' % sys.argv[1]
	process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
	proc_stdout = process.communicate()[0].strip()
	newvalidity = proc_stdout.find('Bad data;')
	if newvalidity != -1:
		print('Query still failed! Aborting')
	else:
		print('DNS Query Successful!')
else:
	print('DNS Query Successful')

