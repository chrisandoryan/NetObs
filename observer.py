import pyshark
from pprint import pprint
import socket
import requests
import datetime
import atexit
import sys
import ctypes, os

'''
From 18-1 with love <3
Project NetObs by AO18-1
https://github.com/chrisandoryan/NetObs
'''

client_key = ""
is_valid_key = 0
proxy_string = ""
use_proxy = ""
hostname = ""
 
def is_admin():
    if os.name == 'nt':
        try:
            # only windows users with admin privileges can read the C:\windows\temp
            temp = os.listdir(os.sep.join([os.environ.get('SystemRoot','C:\\windows'),'temp']))
        except:
            return (os.environ['USERNAME'],False)
        else:
            return (os.environ['USERNAME'],True)
    else:
        if 'SUDO_USER' in os.environ and os.geteuid() == 0:
            return (os.environ['SUDO_USER'],True)
        else:
            return (os.environ['USERNAME'],False)

def get_proxy(username, password, host, port):
    return {
        'https': 'https://{}:{}@{}:{}'.format(username, password, host, port),
        'http': 'http://{}:{}@{}:{}'.format(username, password, host, port)
    } 

def packet_captured(packet):
    global client_key, hostname
    # print('Just arrived: ', packet)
    message = packet['NCP'].target_message
    r = requests.post("https://bcb160b7.ngrok.io/netobs/endpoint", data={'time': datetime.datetime.now(), 'message': '[{}] '.format(hostname) + message, 'client_key': client_key}, proxies=proxy_string)
    print(message)
    # pprint(vars(packet['IP']))

def check_client_key(key):
    r = requests.post("https://bcb160b7.ngrok.io/netobs/check", data={'client_key': key}, proxies=proxy_string)
    return r.status_code

def delete_session():
    global client_key
    r = requests.delete("https://bcb160b7.ngrok.io/netobs/endpoint", data={'client_key': client_key}, proxies=proxy_string)

def exit_handler():
    delete_session()
    print('Goodbye, Stay Petrik')
    print('NetObs Node by AO18-1')
    print('https://github.com/chrisandoryan/NetObs')

if __name__ == "__main__":
    if is_admin():
        try:
            print("Initiating NetObs Node Application... OK\n")
            hostname = socket.gethostname()
            print("Observer is starting from " + hostname)
            print('CTRL^C then Enter to exit program\n')

            while use_proxy != 'Y' and use_proxy != 'N':
                use_proxy = input('Do you want to use proxy? [Y/N] ')
                if use_proxy == 'Y':
                    proxy_string = get_proxy(input("Username: "), input("Password: "), input("Proxy Server: "), input("Proxy Port: "))
            while is_valid_key != 200:
                client_key = input("Input client key: ")
                is_valid_key = check_client_key(client_key)
                if is_valid_key != 200:
                    print("Invalid client key!")
            print("Client key verified. NetObs is listening...")
            # print(pyshark.tshark.tshark.get_tshark_interfaces())
            capture = pyshark.LiveCapture(interface='Ethernet', display_filter='ncp && ip.src == 10.22.64.16 && ncp.subfunc == 11')
            capture.sniff(timeout=1)
            capture.apply_on_packets(packet_captured)

            atexit.register(exit_handler)
        except KeyboardInterrupt:
            exit_handler()
            sys.exit(0)
    else:
        print('NetObs Node Application needs administrator privilege to run.')
        print('Please try a different computer or contact NA 611')
