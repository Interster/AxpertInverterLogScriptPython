#%%
# http://www.steves-internet-guide.com/into-mqtt-python-client/

import paho.mqtt.client as mqtt #import the client1

broker_address="192.168.9.161" 

#%%
#broker_address="iot.eclipse.org" #use external broker
client = mqtt.Client("P1") #create new instance
client.connect(broker_address) #connect to broker
client.publish("son-yskasteTV/inverter/Las drywing", 80)#publish
# %%
