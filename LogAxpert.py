# Te doen:
# Sit die Axpert serial command in 'n module
# Maak die Axpert serial command so dat dit foutiewe boodskappe weggooi.
# Gebruik scheduler om meet taak elke 30 sekondes te doen
# Breek die meetstring op in getalle en stuur dit na die mqtt broker.
# Skryf 'n logger vir die mqtt broker wat die mqtt data na 'n leer skryf as daar genoeg data is

import os
import crcmod
from binascii import unhexlify
from pyAxpert import *

import datetime
import time
import paho.mqtt.client as mqtt #import the client1

# Adres van die broker
broker_address="192.168.9.161" 
client = mqtt.Client("P1") #create new instance
client.connect(broker_address) #connect to broker


# Maak die Axpert se leer oop
connect()

# Log parameters
monsterfrekwensie = 30 # [sekondes]
totalesekondes = 24*60*60 # [sekondes]


begintyd = datetime.datetime.now()

# Maak leer oop
leer = open('Axpert' + str(datetime.date.today()) + '.log', 'w')
leer.write('Maak nog korrekte opskrifte hier\n')

while (datetime.datetime.now() - begintyd).seconds < totalesekondes:
    print((datetime.datetime.now() - begintyd).seconds)
    response = meet_data()
    teksrespons = response.decode('utf-8')
    #print(teksrespons)
    
    # Indien dit hierdie stringe bevat, het foutiewe lesing plaasgevind
    if 'NAK' not in teksrespons and '(' not in teksrespons:
        # Stuur hele gemete string
        client.publish("son-yskasteTV/inverter", teksrespons)#publish
        
        #lysgetalle = teksrespons.split(' ')
        #client.publish("son-yskasteTV/inverter/Las drywing", int(lysgetalle[5]))#publish
        #client.publish("son-yskasteTV/inverter/PV drywing", int(lysgetalle[19]))#publish
        
        # Log data na leer
        leer.write(str(datetime.datetime.now()) + ',' + teksrespons)
        leer.write('\n')
    else:
        print('Fout met lesing \n')
        print(teksrespons)
    
    time.sleep(monsterfrekwensie)

# Maak die Axpert se leer toe
disconnect()
# Klaar gemeet
print('Klaar gemeet')