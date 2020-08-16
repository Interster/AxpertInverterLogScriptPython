import time, sys, string
import sqlite3
import json
import datetime
import calendar
import os
import fcntl
import re
import crcmod
from binascii import unhexlify
import paho.mqtt.client as mqtt
from random import randint

def connect():
    global file
    global fd
    # Assumes that the Axpert has a udev rule defined:
    file = open('/dev/hidVoltronic', 'r+')
    fd = file.fileno()
    print('Maak Axpert oop as leer nommer')
    print(fd)

def disconnect():
    file.close()

def serial_command(command):
    print(command)
    try:
        xmodem_crc_func = crcmod.predefined.mkCrcFun('xmodem')
        command_a=command.encode('utf-8')
        command_b=unhexlify(hex(xmodem_crc_func(command_a)).replace('0x','',1))
        command_c='\x0d'.encode('utf-8')
        
        command_crc = command_a + command_b + command_c

        os.write(fd, command_crc)

        response = b''
        timeout_counter = 0
        while response.find(b'\r') < 0:
            if timeout_counter > 500:
                raise Exception('Read operation timed out')
            timeout_counter += 1
            try:
                response += os.read(fd, 500)
            except Exception as e:
                # print("error reading response...: " + str(e))
                time.sleep(0.01)
            #if len(response) > 0 and response[0] != '(' or 'NAKss' in response:
            #    raise Exception('NAKss')

        response = response.rstrip()
        lastI = response.find(b'\r')
        response = response[1:lastI-2]
        return response
    except Exception as e:
        print('error reading inverter...: ' + str(e))
        disconnect()
        time.sleep(0.1)
        connect()
        return serial_command(command)


import datetime
import time
from binascii import unhexlify
import serial



# Maak die Axpert se leer oop
connect()

# Log parameters
monsterfrekwensie = 30 # [sekondes]
totalesekondes = 12*60*60 # [sekondes]


begintyd = datetime.datetime.now()

# Maak leer oop
leer = open('Axpert' + str(datetime.date.today()) + '.log', 'w')
leer.write('Maak nog korrekte opskrifte hier\n')

while (datetime.datetime.now() - begintyd).seconds < totalesekondes:
    print((datetime.datetime.now() - begintyd).seconds)
    response = serial_command('QPIGS')
    teksrespons = response.decode('utf-8')
    print(teksrespons)
    
    # Log data na leer
    leer.write(str(datetime.datetime.now()) + ',' + teksrespons)
    leer.write('\n')
    time.sleep(monsterfrekwensie)

# Maak die Axpert se leer toe
disconnect()
# Klaar gemeet
print('Klaar gemeet')