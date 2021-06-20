import json
import paho.mqtt.client as mqtt
from time import sleep

MQTT_BROKER = "localhost"
MQTT_TOPIC_TO_MAIN = "to_main"
MQTT_TOPIC_FROM_MAIN = "from_main"
MQTT_QOS = 2
MQTT_RETAIN = True

BOOMArray = ["Main_Process", "BOOM"]
BOOMJSONdump = json.dumps(BOOMArray)

def on_mqtt_connectKILLALL(client, userdata, flags, rc):
    if (rc ==0):
        mqtt.Client.connected_flag = True
        print(">> on_mqtt_connectKiller: mqtt broker connection OK")

        client.publish(MQTT_TOPIC_TO_MAIN, BOOMJSONdump)
        client.publish(MQTT_TOPIC_FROM_MAIN, BOOMJSONdump)

    else:
        print(">> on_mqtt_connectKiller: mqtt broker error: {}".format(rc))
        client.bad_connection_flag = True

def Killer_PubSubStuff():
    KillerClient = None
    mqtt.Client.connected_flag = False
    mqtt.Client.bad_connection_flag = False

    KillerClient = mqtt.Client("KillerClient")
    KillerClient.on_connect = on_mqtt_connectKILLALL

    try:
        KillerClient.connect(MQTT_BROKER)
        KillerClient.loop_start()
    except:
        print(">> Main_PubSubStuff: Connection Failed")
    while not KillerClient.connected_flag and not KillerClient.bad_connection_flag:  #wait in loop
	    print(">> Main_PubSubStuff(): in connection wait loop")
	    sleep(1)
    if KillerClient.bad_connection_flag:
        KillerClient.loop_stop()
        sleep(2)
        exit(0)
    return KillerClient