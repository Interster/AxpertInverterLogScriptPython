import paho.mqtt.client as mqtt #import the client1
import time

import matplotlib.pyplot as plt
#import DataPlot and RealtimePlot from the file plot_data.py
from plot_data import DataPlot, RealtimePlot

broker_address="192.168.9.161" 
#broker_address="iot.eclipse.org"

  
def on_message(client, userdata, message):
    boodskap = message.payload.decode("utf-8")
    print("mqtt boodskap: " ,str(boodskap))
    
    # plot data
    global count
    count+=1
    data.add(count, int(boodskap), 300)
    dataPlotting.plot(data)
    plt.pause(0.001)
    #print("message topic=",message.topic)
    #print("message qos=",message.qos)
    #print("message retain flag=",message.retain)

client = mqtt.Client("P2") #create new instance
print("connecting to broker")
client.connect(broker_address) #connect to broker

# Stel plot op
fig, axes = plt.subplots()
plt.title('Data from TTN console')
data = DataPlot()
dataPlotting= RealtimePlot(axes)

count = 0

client.loop_start() #start the loop

client.on_message=on_message #attach function to callback

print("Subscribing to topics","son-yskasteTV")
# Son stelsel met yskaste en TV as hoofverbruikers:
client.subscribe("son-yskasteTV/inverter/Las drywing")
client.subscribe("son-yskasteTV/inverter/PV drywing")


time.sleep(1000) # wait
client.loop_stop() #stop the loop


