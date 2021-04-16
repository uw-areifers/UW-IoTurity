import paho.mqtt.client as paho
from reifersSmartDoor import smart_door

#Deployment Specific Variables
broker = 'uwischoolreifers.westus2.cloudapp.azure.com'
home_topic_name = 'infosec/IoTurity/home/reifers'
home_access_code = '1337'
open_hours = {"opening_time": "9:00AM", "closing_time": "9:00PM"}

front_door = smart_door(home_topic_name, home_access_code, open_hours)

def on_connect(client, userdata, flags, rc):
    print("Connected to " + broker + " with result code "+str(rc))


#define on_message_callback
def on_message(client, userdata, message):
    print("on_message function called.")
    print("Message Topic: " + message.topic + " Message: " + str(message.payload))
    front_door.process_published_message(message)

#create client object
client = paho.Client(home_topic_name + home_access_code)
client.on_connect = on_connect
######Bind function to callback
client.on_message = on_message

print("connecting to home security MQTT broker ", broker)
client.connect(broker)

#loop through the topics property of the front door and subscribe
for topic in front_door.topic_subs:
    #Print out the topic that is being subscribed to
    print("Reifers Smart door client subscribing to " + topic)
    #Use the Paho client to subscribe to the topic
    client.subscribe(topic)

client.loop_forever()