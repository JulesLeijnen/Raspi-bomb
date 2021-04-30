#TODO:
# Make a better wire_process.py
# Implement a stop from message (MQTT) in wire_process.py
# Implement in timer_process.py that the function will send the message to start blinken from anywhere without repeating and taking to long
# Implement Logging in all processes (Main_process and MainV2 allready done.)
# Clean up Imports
import logging
import paho.mqtt.client as mqtt                             #import the client needed fot the MQTT broker
from time import sleep
import json                                                 #Imports JSON to convert arrays to strings and back
from sys import exit
import RPi.GPIO as gpio                                     #Imports the GPIO lib to control the GPIO pins
########################################

#These are all the variables that the main process needs to keep track of
amount_mistakes = 0
active_Modules = 0
status = "Sleeping"
time_up = 0
Bomb_active = True

logging.info("Var's set: amount_mistakes, {}; active_Modules, {}; status, {}; time_up, {}".format(amount_mistakes, active_Modules, status, time_up))

########################################

def on_messageMain(client, userdata, message):
    global amount_mistakes, active_Modules, status, time_up, Bomb_active
    new_message = json.loads(str(message.payload.decode("utf-8")))
    logging.info("message received in main_process.py: {}\nMessage topic={}\nMessage qos={}\nMessage retain flag={}\nMessage type={}\n".format(new_message, message.topic, message.qos, message.retain, type(message)))
    if new_message[1] == "CLEARED" or new_message[1] == "BOOM":
        Bomb_active = False
        exit(0)    
    elif new_message[1] == "R": #Register
        active_Modules += 1
        if status == "Sleeping":
            status = "Active"
            logging.info("Changing status from 'Sleeping' to 'Active' And added 1 to active_Modules")
        else:
            logging.info("Added 1 to active_Modules, current total is {}".format(active_Modules))
    elif new_message[1] == "D": #Done
        active_Modules -= 1
        logging.info("Removed 1 from active_Modules, current total is {}".format(active_Modules))
    elif new_message[1] == "T": #Time up
        time_up = 1
        logging.info("Time is up, current state is '{}'".format(bool(time_up)))
    elif new_message[1] == "F": #Fault +1
        amount_mistakes += 1
        logging.info("Added 1 to amount_mistakes, current total is {}".format(amount_mistakes))
        
########################################

def main_process(max_mistakes):
    global amount_mistakes, active_Modules, status, time_up, Bomb_active

    Bomb_active = True

    broker_adress="192.168.178.15"
    instancename = "MAIN"
    client = mqtt.Client(instancename) #create new instance
    client.on_message=on_messageMain #attach function to callback
    client.connect(broker_adress) #connect to broker
    client.loop_start() #start the loop
    client.subscribe("main_channel")
    logging.info("Connected to broker on adress {} with instance-name {} and subscribed to 'main_channel'".format(broker_adress, instancename))
    logging.info("Entering the cleared or boom loop to check if the bomb is done or 'done'")
    while Bomb_active:
        sleep(0.5)
        if status == "Active" and active_Modules < 1:
            dictionary = ["MAIN", "CLEARED"]
            temp1 = json.dumps(dictionary)
            client.publish("main_channel",temp1)
            logging.info("Entered the cleared section of main_processs")
            logging.info("CLEARED\n\namount_mistakes={}\nactive_module={}\nstatus={}\ntime_up={}\n".format(amount_mistakes, active_Modules, status, time_up))
        pass
        if amount_mistakes > (max_mistakes - 1) or time_up == 1:
            dictionary = ["MAIN", "BOOM"]
            temp2 = json.dumps(dictionary)
            client.publish("main_channel",temp2)
            logging.info("Entered the BOOM! section og main_process")
            logging.info("BOOM!\n\namount_mistakes={}\nactive_module={}\nstatus={}\ntime_up={}".format(amount_mistakes, active_Modules, status, time_up))
    gpio.cleanup()
    exit(0)
    client.loop_stop() #stop the loop