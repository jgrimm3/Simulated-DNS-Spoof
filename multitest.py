import subprocess
import time
import sys

if len(sys.argv) != 2:
	print('Usage: python multitest.py <hostname>')

command = 'nslookup %s.bombast.com' % sys.argv[1]

while True:
	process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
	proc_stdout = process.communicate()[0].strip()
	print(proc_stdout)
	time.sleep(1)
