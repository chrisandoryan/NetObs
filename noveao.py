from ctypes import *
import ctypes as c
from pprint import pprint
import socket
import requests
import datetime
import atexit
import sys
import ctypes, os
import getpass

'''
From 18-1 with love <3
Project NetObs by AO18-1
https://github.com/chrisandoryan/Noveao
'''

client_key = ""
is_valid_key = 0
proxy_string = ""
use_proxy = ""
hostname = ""

def get_proxy(username, password, host, port):
    return {
        'https': 'https://{}:{}@{}:{}'.format(username, password, host, port),
        'http': 'http://{}:{}@{}:{}'.format(username, password, host, port)
    } 

@c.CFUNCTYPE(None, c.c_char_p)
def inbound_message(m):
    global client_key, hostname
    # print('Just arrived: ', packet)
    r = requests.post("https://netobs.potatoastech.xyz/netobs/endpoint", data={'time': datetime.datetime.now(), 'message': '[{}] {}'.format(hostname, m.decode('utf-8')), 'client_key': client_key}, proxies=proxy_string)

def check_client_key(key):
    r = requests.post("https://netobs.potatoastech.xyz/netobs/check", data={'client_key': key}, proxies=proxy_string)
    return r.status_code

def delete_session():
    global client_key
    r = requests.delete("https://netobs.potatoastech.xyz/netobs/endpoint", data={'client_key': client_key}, proxies=proxy_string)

def exit_handler():
    delete_session()
    print('Goodbye, Stay Petrik')
    print('Noveao Node by AO18-1')
    print('https://github.com/chrisandoryan/Noveao')

if __name__ == "__main__":
    try:
        print("Initiating Noveao Node Application... OK\n")
        hostname = socket.gethostname()
        print("Noveao is starting from " + hostname)
        print('CTRL^C then Enter to exit program\n')
        while use_proxy != 'Y' and use_proxy != 'N':
            use_proxy = input('Do you want to use proxy? [Y/N] ')
            if use_proxy == 'Y':
                proxy_string = get_proxy(input("Username: "), getpass.getpass(), input("Proxy Server: "), input("Proxy Port: "))
        while is_valid_key != 200:
            client_key = input("Input client key: ")
            is_valid_key = check_client_key(client_key)
            if is_valid_key != 200:
                print("Invalid client key!")
        lib = CDLL("Noveao")
        print("Client key verified. Noveao is listening...")
        lib.main(inbound_message)
        atexit.register(exit_handler)
    except KeyboardInterrupt:
        exit_handler()
        sys.exit(0)
