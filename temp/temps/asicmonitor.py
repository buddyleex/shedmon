import socket 
import json 
import sys 
sys.path.append('/home/pi')
from minerips import anta3ips, antd3ips, ants9ips, innod9ips


def check_antminer_a3(ip, name, port):
        try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.connect((ip, port))
                sock.settimeout(2)

                sock.send(json.dumps({'command': 'stats'}))

                res = ''
                
                while 1:
                        buf = sock.recv(4096)
                        if buf:
                                res += buf
                        else:
                                break


                sock.shutdown(socket.SHUT_RDWR)
                sock.close()

                chain1 = int(res.find('chain_acs1'))
                chain2 = int(res.find('chain_acs2'))
                chain3 = int(res.find('chain_acs3'))
                temp1 = int(res.find('temp2_1')) 
                temp2 = int(res.find('temp2_2')) 
                temp3 = int(res.find('temp2_3')) 
                hash5s = int(res.find('GHS 5s'))
                chain1_out = res[chain1+13:chain1+81]
                chain2_out = res[chain2+13:chain2+81]
                chain3_out = res[chain3+13:chain3+81]
                chain1_f = int(chain1_out.find('x'))
                chain2_f = int(chain2_out.find('x'))
                chain3_f = int(chain3_out.find('x'))
                temp1_out = int(res[temp1+9:temp1+12].replace(',', ''))
                temp2_out = int(res[temp2+9:temp2+12].replace(',', ''))
                temp3_out = int(res[temp3+9:temp3+12].replace(',', ''))
                hash5s_unf = float(res[hash5s+9:hash5s+12])
                hash5s_out = str(hash5s_unf) + str(' Gh/s')
		color_code = ''


                ### Check for chain errors

                if chain1_f > '0':
                        chain_err = int('1')
                elif chain2_f > int('0'):
                        chain_err = int('1')
                elif chain3_f > int('0'):
                        chain_err = int('1')
                else:
                        chain_err = int('0')

                if chain_err > int('0'):
                        ### Fire off email to warn
                        ### Reboot miner
                        color_code = str('red')

                ### Check for high temp & hashrate
				
                if chain1_f > '0':
                        chain_err = int('1')
                elif chain2_f > int('0'):
                        chain_err = int('1')
                elif chain3_f > int('0'):
                        chain_err = int('1')
                else:
                        chain_err = int('0')

                if chain_err > int('0'):
                        ### Fire off email to warn
                        ### Reboot miner
                        color_code = str('red')

                ### Check for high temp & hashrate
                
                elif hash5s_unf < float('650'):
                        if temp1_out  > int('108') or temp2_out > int('108') or temp3_out > int('108'):
                                ### Fire off email to warn
                                ### Reboot miner
                                color_code = str('red')
                elif temp1_out  > int('114') or temp2_out > int('114') or temp3_out > int('114'):
                        ### Fire off email to warn
                        ### Reboot miner
                        color_code = str('red')

                else:
                        color_code = str('green')

                temp4_out = 'N/A'

        except socket.error:
                temp1_out = 'N/A'
                temp2_out = 'N/A'
                temp3_out = 'N/A'
                temp4_out = 'N/A'
                hash5s_out = 'N/A'
                color_code = 'red'


        return temp1_out, temp2_out, temp3_out, temp4_out, hash5s_out, color_code, name, ip


def check_antminer_s9(ip, name, port):
	color_code = ''
	try:
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.connect((ip, port))
		sock.settimeout(2)

		sock.send(json.dumps({'command': 'stats'}))

		res = ''
		
		while 1:
			buf = sock.recv(4096)
    			if buf:
        			res += buf
   			else:
        			break


		sock.shutdown(socket.SHUT_RDWR)
		sock.close()
		
		chain1 = int(res.find('chain_acs6'))
		chain2 = int(res.find('chain_acs7'))
		chain3 = int(res.find('chain_acs8'))
		temp1 = int(res.find('temp2_6')) 
		temp2 = int(res.find('temp2_7')) 
		temp3 = int(res.find('temp2_8')) 
		hash5s = int(res.find('GHS 5s'))
		chain1_out = res[chain1+13:chain1+84]
		chain2_out = res[chain2+13:chain2+84]
		chain3_out = res[chain3+13:chain3+84]
		chain1_f = int(chain1_out.find('x'))
		chain2_f = int(chain2_out.find('x'))
		chain3_f = int(chain3_out.find('x'))
		temp1_out = int(res[temp1+9:temp1+12].replace(',', ''))
		temp2_out = int(res[temp2+9:temp2+12].replace(',', ''))
		temp3_out = int(res[temp3+9:temp3+12].replace(',', ''))
		hash5s_unf = round(float(res[hash5s+9:hash5s+17]) / float('1000'), 2)
		hash5s_out = str(hash5s_unf) + str(' Th/s')
		color_code = ''

		### Check for chain errors

		if chain1_f > '0':
			chain_err = int('1')
		elif chain2_f > int('0'):
			chain_err = int('1')
		elif chain3_f > int('0'):
                        chain_err = int('1')
		else:
			chain_err = int('0')

		if chain_err > int('0'):
			### Fire off email to warn
			### Reboot miner
			color_code = str('red')

		### Check for high temp & hashrate
		
		elif hash5s_unf < float('12'):
			if temp1_out  > int('108') or temp2_out > int('108') or temp3_out > int('108'):
				### Fire off email to warn
				### Reboot miner
				color_code = str('red')
		elif temp1_out  > int('114') or temp2_out > int('114') or temp3_out > int('114'):
			### Fire off email to warn
			### Reboot miner
                       	color_code = str('red')

		else:
			color_code = str('green')

		temp4_out = 'N/A'

	except socket.error:
		temp1_out = 'N/A'
		temp2_out = 'N/A'
		temp3_out = 'N/A'
		temp4_out = 'N/A'
		hash5s_out = 'N/A'
		color_code = 'red'


	return temp1_out, temp2_out, temp3_out, temp4_out, hash5s_out, color_code, name, ip



def check_antminer_d3(ip, name, port):
	color_code = ''
        try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.connect((ip, port))
                sock.settimeout(2)

                sock.send(json.dumps({'command': 'stats'}))

                res = ''
                
                while 1:
                        buf = sock.recv(4096)
                        if buf:
                                res += buf
                        else:
                                break


                sock.shutdown(socket.SHUT_RDWR)
                sock.close()
                
                chain1 = int(res.find('chain_acs1'))
                chain2 = int(res.find('chain_acs2'))
                chain3 = int(res.find('chain_acs3'))
                temp1 = int(res.find('temp1')) 
                temp2 = int(res.find('temp2')) 
                temp3 = int(res.find('temp3')) 
                hash5s = int(res.find('GHS 5s'))
                chain1_out = res[chain1+13:chain1+81]
                chain2_out = res[chain2+13:chain2+81]
                chain3_out = res[chain3+13:chain3+81]
                chain1_f = int(chain1_out.find('x'))
                chain2_f = int(chain2_out.find('x'))
                chain3_f = int(chain3_out.find('x'))
                temp1_out = int(res[temp1+7:temp1+10].replace(',', ''))
                temp2_out = int(res[temp2+7:temp2+10].replace(',', ''))
                temp3_out = int(res[temp3+7:temp3+10].replace(',', ''))
		hash5s_unf = round(float(res[hash5s+9:hash5s+17].replace('"','')) / float('1000'), 2)
		hash5s_out = str(hash5s_unf) + str(' Gh/s')
		color_code = ''

                ### Check for chain errors

                if chain1_f > '0':
                        chain_err = int('1')
                elif chain2_f > int('0'):
                        chain_err = int('1')
                elif chain3_f > int('0'):
                        chain_err = int('1')
                else:
                        chain_err = int('0')

                if chain_err > int('0'):
                        ### Fire off email to warn
                        ### Reboot miner
                        color_code = str('red')

                ### Check for high temp & hashrate
                
                elif hash5s_unf < float('16'):
                        if temp1_out  > int('92') or temp2_out > int('92') or temp3_out > int('92'):
                                ### Fire off email to warn
                                ### Reboot miner
                                color_code = str('red')
                elif temp1_out  > int('99') or temp2_out > int('99') or temp3_out > int('99'):
                        ### Fire off email to warn
                        ### Reboot miner
                        color_code = str('red')

                else:
                        color_code = str('green')
		
		temp4_out = 'N/A'


        except socket.error:
                temp1_out = 'N/A'
                temp2_out = 'N/A'
                temp3_out = 'N/A'
		temp4_out = 'N/A'
                hash5s_out = 'N/A'
                color_code = 'red'


        return temp1_out, temp2_out, temp3_out, temp4_out, hash5s_out, color_code, name, ip



def check_inno_d9(ip, name, port):
	color_code = ''
        try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.connect((ip, port))
                sock.settimeout(2)

                sock.send(json.dumps({'command': 'summary'}))

                res = ''

                while 1:
                        buf = sock.recv(4096)
                        if buf:
                                res += buf
                        else:
                                break

                sock.shutdown(socket.SHUT_RDWR)
                sock.close()


                hash5s = int(res.find('MHS 5s'))
                hash5m = int(res.find('MHS 5m'))
		elapsed = int(res.find('Elapsed":'))
                hash5s_unf = round(float(res[hash5s+8:hash5s+15].replace('"','')) / float('1000000'), 2)
                hash5s_out = str(hash5s_unf) + str(' Th/s')
                hash5m_unf = round(float(res[hash5m+8:hash5m+15].replace('"','')) / float('1000000'), 2)
                hash5m_out = str(hash5m_unf) + str(' Th/s')
		#elapsed_unf = int(res[elapsed+9:elapsed+18].replace(',',''))
		elapsed_buf = res[elapsed::]
		elapsed_f = int(elapsed_buf.find(','))
		elapsed_unf = int(elapsed_buf[9:elapsed_f])
		color_code = ''

	except socket.error:
                hash5s_out = 'N/A'
		hash5s_out = 'N/A'
		hash5s_unf = float('0')
                color_code = 'red'



        try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.connect((ip, port))
                sock.settimeout(2)

                sock.send(json.dumps({'command': 'stats'}))

                res = ''

                while 1:
                        buf = sock.recv(4096)
                        if buf:
                                res += buf
                        else:
                                break

                sock.shutdown(socket.SHUT_RDWR)
                sock.close()


                temp1 = int(res.find('"Temp":')) 
                temp1_out = int(round(float(res[temp1+7:temp1+11]),0))
		temp2_buf = res[temp1+7::]
		temp2 = int(temp2_buf.find('"Temp":'))
		temp2_out = int(round(float(temp2_buf[temp2+7:temp2+11]),0))
		temp3_buf = temp2_buf[temp2+7::]
		temp3 = int(temp3_buf.find('"Temp":'))
		temp3_out = int(round(float(temp3_buf[temp3+7:temp3+11]),0))

		temp4_out = 'N/A'

        except socket.error:
                temp1_out = 'N/A'         
                temp2_out = 'N/A'
                temp3_out = 'N/A'
		temp4_out = 'N/A'


	### Check for chain errors


	if hash5s_unf < float('1.7'):
		if hash5m_unf < float('1.7'):
			if elapsed_unf > int('300'):
				### Fire off email to warn
				### Reboot miner
				color_code = str('red')
			else:
				color_code = str('green')
		else:
			color_code = str('green')

	else:
		color_code = str('green')


	return temp1_out, temp2_out, temp3_out, temp4_out, hash5s_out, color_code, name, ip

