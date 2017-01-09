import requests
import json
import sys

global BASE 
BASE = "http://213.32.27.235:8083/v1/"
global HOSTS
HOSTS = BASE + "hosts"

username = sys.argv[1]
password = sys.argv[2]
response = requests.get(HOSTS, auth=(username, password))
jsonResponse = response.json()
print response.status_code
#print json.dumps(jsonResponse, indent=2)