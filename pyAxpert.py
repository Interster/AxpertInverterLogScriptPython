#%%

import os
import crcmod
from binascii import unhexlify


def connect():
    global file
    global fd
    # Assumes that the Axpert has a udev rule defined:
    file = open('/dev/hidVoltronic', 'r+')
    fd = file.fileno()
    print('connected')

def disconnect():
    file.close()
    print('disconnected')

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
                print("error reading response...: " + str(e))
                time.sleep(0.01)
            if len(response) > 0 and response[0] != '(' or 'NAK' in response or '(' in response:
                raise Exception('NAK')

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

def na_sonkrag():
    response = serial_command('POP01')
    
    return response

def modus():
    # Antwoord met 'L' as dit op lynkrag is
    # en met 'B' as dit op batterykrag is
    response = serial_command('QMOD')
    
    return response


def toestel_inligting():
    # Antwoord met 'L' as dit op lynkrag is
    # en met 'B' as dit op batterykrag is
    response = serial_command('QPIRI')
    
    return response

def onttrek_data(response):
    # Onttrek die AC drywing en die PV drywing en skryf dit uit as getalle
    
    #teksrespons = response.decode('utf-8')
    
    lysgetalle = response.split(' ')
    # Dit gee:
    # Grid voltage, Grid frequency, AC output voltage, AC output frequency,
    #['233.8', '49.9', '233.8', '49.9', '0210', '0138', '004', '418', '52.00', '000', '100', '0048', '0000', '000.0', '00.00', '00001', '00010101', '00', '00', '00000', '110']
    # Breek dit op in stukke:
    #
    # 0 Grid voltage, 1 Grid frequency, 2 AC output voltage, 3 AC output frequency,
    # ['233.8', '49.9', '233.8', '49.9',
    # 4 AC output apparent power, 5 AC output active power
    #'0210', '0138',
    # 6 Output load percent, 7 BUS voltage, 8 Battery voltage, 9 Battery charging current
    #'004', '418', '52.00', '000',
    # 10 Battery capacity, 11 Inverter heat sink temperature, 
    #'100', '0048',
    # 12 PV Input current 1, 13 PV Input voltage 1, 
    #'0000', '000.0',
    # 14 Battery voltage from SCC 1, 15 Battery discharge current
    #'00.00', '00001',
    # 16 Device status, 17 Battery voltage offset for fans on, 18 EEPROM version
    #'00010101', '00', '00',
    # 19 PV Charging power 1, 20 Device status
    #'00000', '110']
    print('PV charging power ' + lysgetalle[19])
    # Druk nou die waarde wat na 'n getal verander is
    pvchargepower = int(lysgetalle[19])
    print('AC output active power ' + lysgetalle[5])
    acactivepower = int(lysgetalle[5])
    
    return pvchargepower, acactivepower
    
