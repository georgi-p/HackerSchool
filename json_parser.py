import sys
import os
import subprocess

# Input example: "mypc:192.168.0.1,mylaptop:192.168.0.2,router:192.168.1.10" 
# Read arguments
try:
	inputstring = str(sys.argv[1])
except:
	print "Please enter a list with host names and IPs"
	sys.exit()

# Parse the input string to obtain pairs of hosts and ips
inputlist = inputstring.split(',')

json = '{\n  "data": [\n    {\n      '

listsize = len(inputlist)
i = 0
while i < listsize:
	# Get the next host, ip pair
	(host, ip) = inputlist[i].split(':')

	# Try to execute the ping command, an exception is raised if it is unsuccesful i.e. when the packet loss is 100%
	cmd = "ping -c 5 " + ip
	try:
		response = subprocess.check_output(cmd, shell=True)
		packetloss = response.split(',')[2].split('%')[0].replace(' ','')
	except:
		packetloss = '100'

	# Add this host, ip, packetloss tuple to the json string
	newjson = '{\n      "{#NAME}": "%s",\n      "{#IPADDRESS}": "%s",\n      "{#VALUE}" : "%s"\n    }\n' % (host, ip, packetloss)
	json += newjson

	# If this is not the last host, ip pair, add a comma to the json
	if i < listsize-1:
		json += ',\n      '

	i += 1

json += '  ]\n}'

#json = '{\n  "data": [\n    {\n      "{#NAME}": "host1",\n      "{#IPADDRESS}": "10.10.10.10",\n      "{#VALUE}" : "50"\n    }\n  ]\n}'

print json
