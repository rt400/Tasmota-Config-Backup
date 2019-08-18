import json
import socket
import urllib

import requests
import wget
import ipaddress
import sys


if len(sys.argv) == 1:
    print("No IP address entered !")
    exit()
elif len(sys.argv) == 3:
    try:
        start_ip = ipaddress.ip_address(str(sys.argv[1]))
        end_ip = ipaddress.ip_address(str(sys.argv[2]))
    except:
        print("Wrong IP address !")
        exit()
elif len(sys.argv) == 2:
    try:
        start_ip = ipaddress.ip_address(str(sys.argv[1]))
        end_ip = ipaddress.ip_address(str(sys.argv[1]))
    except:
        print("Wrong IP address !")
        exit()
ip_str = None
for ip_int in range(int(start_ip), int(end_ip + 1)):
    try:
        ip_str = ipaddress.IPv4Address(ip_int).__str__()
        url = 'http://' + ip_str + '/dl?'
        url_ver = 'http://' + ip_str + '/cm?cmnd=status%202'
        try:
            #socket.settimeout(2)
            ip_str = socket.gethostbyaddr(ip_str).__str__()
        except:
            print("No Hostname for " + ip_str + ", using IP")
        backup_file = requests.get(url, allow_redirects=True, timeout=5)
        backup_ver = requests.get(url_ver, allow_redirects=True, timeout=5).json()
        print("Found Tasmota Firmware in " + ip_str)
        with open(ip_str + '_' + backup_ver['StatusFWR']['Version'] +'.dmp', 'wb') as filetowrite:
            filetowrite.write(backup_file.content)
            filetowrite.close()
    except:
        #print(sys.exc_info())
        print("Not found TASMOTA firmware in "+ip_str)
