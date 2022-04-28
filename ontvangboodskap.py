#%%
# http://www.steves-internet-guide.com/into-mqtt-python-client/


import paho.mqtt.client as mqtt #import the client1
import time
############
def on_message(client, userdata, message):
    print("message received " ,str(message.payload.decode("utf-8")))
    print("message topic=",message.topic)
    print("message qos=",message.qos)
    print("message retain flag=",message.retain)
########################################


#%%
broker_address="192.168.9.161"
#broker_address="iot.eclipse.org"
print("creating new instance")
client = mqtt.Client("P1") #create new instance
client.on_message=on_message #attach function to callback
print("connecting to broker")
client.connect(broker_address) #connect to broker
client.loop_start() #start the loop
print("Subscribing to topic","inverter/Opbattery")
client.subscribe("inverter/Opbattery")
print("Publishing message to topic","house/bulbs/bulb1")
client.publish("inverter/Opbattery","AF")
time.sleep(4) # wait
client.loop_stop() #stop the loop
# %%
