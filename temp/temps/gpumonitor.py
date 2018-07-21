import socket
import json
import sys
sys.path.append('/home/pi')
from minerips import minerips
from apicalls import ethmanpsw


def claymore_check_rig(host):
	port = int('3333')
	min_hashes=int('200000')
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.settimeout(2)

	try:
		s.connect((host, port))
        	s.send('{"id":0,"jsonrpc":"2.0","method":"miner_getstat1","psw":"' + ethmanpsw + '"}'.encode("utf-8"))
		j=s.recv(2048)
        	s.close()
        	res=json.loads(j.decode("utf-8"))
        	res=res['result']
        	hashes = int(res[2].split(';')[0])
        	hash_ok=min_hashes < hashes
		return hash_ok
	except socket.error:
		offline = str('offline')
		return offline

        return False

