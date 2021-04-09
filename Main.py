import paho.mqtt.client as paho
from reifersSmartDoor import smart_door

#Deployment Specific Variables
broker = 'uwischoolreifers.westus2.cloudapp.azure.com'
home_topic_name = 'infosec/415/home/reifers'
home_access_code = '1337'
open_hours = {"opening_time": "9:00AM", "closing_time": "9:00PM"}

front_door = smart_door(home_topic_name, home_access_code, open_hours)

#define on_message_callback
def on_message(client, userdata, message):
    front_door.process_published_message(message)


#create client object
client = paho.Client(home_topic_name + home_access_code)

######Bind function to callback
client.on_message = on_message

print("connecting to home security MQTT broker ", broker)
client.connect(broker)

for x in front_door.topic_subs:
    print(home_topic_name + " front door client subscribing to " + x)
    client.subscribe(x)

client.loop_forever()