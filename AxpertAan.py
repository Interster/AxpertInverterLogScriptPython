import os
import crcmod
from binascii import unhexlify


def connect():
    global file
    global fd
    # Assumes that the Axpert has a udev rule defined:
    file = open('/dev/hidVoltronic', 'r+')
    fd = file.fileno()

def disconnect():
    file.close()

def serial_command(command):
    print(command)
    try:
        xmodem_crc_func = crcmod.predefined.mkCrcFun('xmodem')
        command_a=command.encode('utf-8')
        command_b_0=hex(xmodem_crc_func(command_a)).replace('0x','',1)
        # Verwyder \n, want dit is gereserveerde karakter
        # Vervang dit met die hex getal 1 meer as \n
        # Vervang dus 0a met 0b
        command_b=unhexlify(command_b_0.replace('0a','0b',1)) 
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
    
def meet_data():
    response = serial_command('QPIGS')
    
    return response

def na_battery():
    response = serial_command('POP02')
    
    return response

def na_lynkrag():
    response = serial_command('POP00')
    
    return response


import datetime
import time


# Maak die Axpert se leer oop
connect()

response = na_battery()

disconnect()
