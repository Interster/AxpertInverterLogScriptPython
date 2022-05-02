
import paho.mqtt.client as mqtt  #import the client1
import time
from queue import Queue
q=Queue()
messages=[]
def on_connect(client, userdata, flags, rc):
    client1.connected_flag=True
    #messages.append(m)
    #print(m)

def on_message(client1, userdata, message):
    #global messages
    m="message received  "  ,str(message.payload.decode("utf-8"))
    messages.append(m)#put messages in list
    q.put(m) #put messages on queue
    print("message received  ",m)
def on_publish (client, userdata, mid):
    global messages
    m="on publish callback mid "+str(mid)
    #messages.append(m)
def on_subscribe(client, userdata, mid, granted_qos):
    m="on_subscribe callback mid "+str(mid)
  
Q0S=0
broker_address="192.168.1.68"
#broker_address="iot.eclipse.org"
client1 = mqtt.Client("P1")    #create new instance
client1.on_connect= on_connect        #attach function to callback
client1.on_message=on_message        #attach function to callback
client1.on_publish =on_publish        #attach function to callback
#client1.on_subscribe =on_subscribe        #attach function to callback
time.sleep(1)
print("connecting to broker")
client1.connected_flag=False
client1.connect(broker_address)      #connect to broker
print("starting the loop")
client1.loop_start()    #start the loop
print("subscribing QOS=",Q0S)
r=client1.subscribe("house/bulbs/#",Q0S)
while not client1.connected_flag:
    print("waiting for connect")
    time.sleep(0.5)
for i in range(3):
    print("publishing")
    m="test message number =" +str(i)
    client1.publish("house/bulbs/bulb1",m)
    time.sleep(1)
while len(messages)>0:
    print(messages.pop(0))
while not q.empty():
    message = q.get()
    print("queue: ",message)
client1.disconnect()
client1.loop_stop()


