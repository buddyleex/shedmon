from pysnmp.hlapi import *
import sys
sys.path.append('/home/pi')
from minerips import pduips

pduAll = []
pduAllAppend = []
totalwatts = int("0")
totalamps = float("0")

def pdustats():
	x = 0
	pduAll = []
	pduAllAppend = []
	totalwatts = int("0")  
	totalamps = float("0")
	for line in pduips:
		if x < len(pduips):
			errorIndication, errorStatus, errorIndex, varBinds = next(
    				getCmd(SnmpEngine(),
          				CommunityData('pub', mpModel=0),
           				UdpTransportTarget((pduips[x], 161)),
           				ContextData(),
					ObjectType(ObjectIdentity('iso.3.6.1.2.1.1.5.0')),
					ObjectType(ObjectIdentity('iso.3.6.1.4.1.232.165.2.3.1.1.4.1')))
					)

			if errorIndication:
				x=x+1
    				continue
			elif errorStatus:
				x=x+1
    				continue
			else:
				x=x+1
				pduAllAppend = []
				for varBind in varBinds:
                                        try:                              
                                                pduAllAppend.append(int(varBind[1]))
                                                ampz = round(float(varBind[1]) / float("250"),2)
                                                pduAllAppend.append(float(ampz))
                                        except ValueError:
						if varBind[1] == "None":
                                                	break
						else:
							pduAllAppend.append(str(varBind[1]))
		pduAll.append(pduAllAppend)

	
	x = 0

	for pdu in pduAll:
		totalwatts = int(totalwatts) +  int(pduAll[x][1])
		totalamps = round(float(totalamps) + float(pduAll[x][2]),2)
		x=x+1

	totalwatts = str(round(float(totalwatts) / float("1000"),2)) + " KwH"

	return pduAll, totalwatts, totalamps
