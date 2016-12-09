from pyproxmox import *
import sys

ip = sys.argv[1]
user = sys.argv[2]
password = sys.argv[3]
a = prox_auth(ip, user, password)
b = pyproxmox(a)
status = b.getClusterStatus()
print json.dumps(status, indent=2)
