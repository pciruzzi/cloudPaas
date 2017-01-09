import requests
import json
import sys
import subprocess

global BASE 
BASE = "http://213.32.27.235:8083/"
global V1
V1 = BASE + "v1/"
global V2_BETA
V2_BETA = BASE + "v2-beta/"

global HOSTS
HOSTS = V1 + "hosts"
global CONTAINERS
CONTAINERS = V2_BETA + "projects/1a5/containers"


rancherUser = sys.argv[1]
rancherPassword = sys.argv[2]
response = requests.get(HOSTS, auth=(rancherUser, rancherPassword))
jsonResponse = response.json()
print response.status_code
#print json.dumps(jsonResponse, indent=2)

print "##############################################"
data = '{"description":"Une description", "imageUuid":"docker:pciruzzi/paasinsa1617", "name":"api-test", "ports":["8092:3000/tcp"]}'
# response = requests.post(CONTAINERS, auth=(rancherUser, rancherPassword), data=data)
# jsonResponse = response.json()
# print response.status_code

# TODO: Obtain in what VM was it created...
print "##############################################"
#subprocess.Popen("iptables -t nat -A PREROUTING -p tcp --dport 8092 -j DNAT --to-destination 192.168.0.3:8092")
subprocess.Popen("ls")