#--------------------------------------Imports---------------------------------------
import logging
import paho.mqtt.client as mqtt
from time import sleep
import json
from sys import exit
#--------------------------------------Globals--------------------------------------
amount_mistakes = 0
active_Modules = 0
active_status = "Sleeping"
bomb_done_main = False

MQTT_BROKER = "localhost"
MQTT_TOPIC_TO_MAIN = "to_main"
MQTT_TOPIC_FROM_MAIN = "from_main"
MQTT_QOS = 2
MQTT_RETAIN = True
#-------------------------------------LOGGING---------------------------------------------

#------------------------------------Main Function---------------------------------------
def main_process(max_mistakes, DEBUG):
    global amount_mistakes, active_Modules, active_status, bomb_done_main
    
    #LOGGING STUFF

    Mainclient = Main_PubSubStuff()

    ClearedArray = ["Main_Process", "Cleared"]
    ClearedJSONdump = json.dumps(ClearedArray)
    BOOMArray = ["Main_Process", "BOOM"]
    BOOMJSONdump = json.dumps(BOOMArray)

    while not bomb_done_main:
        sleep(0.5)
        if active_status == "Active" and active_Modules < 1:
            Mainclient.publish(MQTT_TOPIC_FROM_MAIN, ClearedJSONdump)
            bomb_done_main = True
        if amount_mistakes >= max_mistakes:
            Mainclient.publish(MQTT_TOPIC_FROM_MAIN, BOOMJSONdump)
            bomb_done_main = True
    Mainclient.loop_stop()
    sleep(5)
    exit(0)
#------------------------------------MQTT Functions---------------------------------------
def Main_PubSubStuff():
    Mainclient = None
    mqtt.Client.connected_flag = False
    mqtt.Client.bad_connection_flag = False

    Mainclient = mqtt.Client("Mainclient")
    Mainclient.on_connect = on_mqtt_connectMAIN
    Mainclient.on_message = on_mqtt_messageMAIN

    try:
        Mainclient.connect(MQTT_BROKER)
        Mainclient.loop_start()
    except:
        print(">> Main_PubSubStuff: Connection Failed")
    while not Mainclient.connected_flag and not Mainclient.bad_connection_flag:  #wait in loop
	    print(">> Main_PubSubStuff(): in connection wait loop")
	    sleep(1)
    if Mainclient.bad_connection_flag:
        Mainclient.loop_stop()
        sleep(2)
        exit(0)
    return Mainclient

def on_mqtt_connectMAIN(client, userdata, flags, rc):
    if (rc ==0):
        mqtt.Client.connected_flag = True
        print(">> on_mqtt_connectMAIN: mqtt broker connection OK")

        client.subscribe(MQTT_TOPIC_TO_MAIN, MQTT_QOS)

    else:
        print(">> on_mqtt_connectMAIN: mqtt broker error: {}".format(rc))
        client.bad_connection_flag = True

def on_mqtt_messageMAIN(client, userdata, message):
    new_message = json.loads(str(message.payload.decode("utf-8")))
    print("WIRE: message received in wire_process.py: {}".format(new_message,))
    MainMessageResolver(new_message)

def MainMessageResolver(message):
    global amount_mistakes, active_Modules, active_status

    if message[1] == "R":
        active_Modules += 1
        if active_status == "Sleeping":
            active_status = "Active"
            print("MAIN: Changing status from 'Sleeping' to 'Active' And added 1 to active_Modules")
        else:
            print("MAIN: Added 1 to active_Modules, current total is {}".format(active_Modules))
    
    if message[1] == "D": #Done
        active_Modules -= 1
        print("MAIN: Removed 1 from active_Modules, current total is {}".format(active_Modules))
    
    if message[1] == "T":
        amount_mistakes = 14022002
        print("MAIN: Time is up, current state of amount_mistakes is '{}'".format(amount_mistakes))
    
    if message[1] == "F":
        amount_mistakes += 1
        print("MAIN: A fault was made, current state of amount_mistakes is '{}'".format(amount_mistakes))

    return