import pyshark
from pprint import pprint
import socket
import requests
import datetime
import atexit
import sys

'''
From 18-1 with love <3
Project NetObs by AO18-1
https://github.com/chrisandoryan/NetObs
'''

client_key = ""
is_valid_key = 0

def packet_captured(packet):
    global client_key
    # print('Just arrived: ', packet)
    message = packet['NCP'].target_message
    r = requests.post("https://ecdcb614.ngrok.io/netobs/endpoint", data={'time': datetime.datetime.now(), 'message': message, 'client_key': client_key})
    # pprint(vars(packet['IP']))

def check_client_key(key):
    r = requests.post("https://ecdcb614.ngrok.io/netobs/check", data={'client_key': key})
    return r.status_code

def delete_session():
    global client_key
    r = requests.delete("https://ecdcb614.ngrok.io/netobs/endpoint", data={'client_key': client_key})

def exit_handler():
    delete_session()
    print('Goodbye, Stay Petrik')
    print('NetObs Node by AO18-1')
    print('https://github.com/chrisandoryan/NetObs')

if __name__ == "__main__":
    try:
        print("Initiating NetObs Node Application... OK\n")
        print("Observer is starting from " + socket.gethostname())
        print('CTRL^C then Enter to exit program\n')
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
