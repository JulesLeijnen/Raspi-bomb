#TODO: Implement that the function will send the message to start blinken from anywhere without repeating and taking to long

#Imports
from pause import until
import RPi.GPIO as gpio
import logging
import pdc6x1
from time import sleep, time
import paho.mqtt.client as mqtt #import the client1
import json

MQTT_BROKER = "192.168.178.15"
MQTT_TOPIC = "JOUW TOPIC OM NAAR TE LUISTEREN"
MQTT_QOS = 2
MQTT_RETAIN = True

#-----------------------------------------------
def on_messageWires(client, userdata, message):
    global defusedTimer,time_left
    new_message = json.loads(str(message.payload.decode("utf-8")))
    print("TIMER: message received in wire_process.py: {}".format(new_message,))
    WiresMessageResolver(new_message, display)
    
def WiresMessageResolver(message, display):   
    if message[1] == "Cleared":
        #Change thing in clock_process() (Change defused var)
        #Somehow fetch time_left var from clock_process()
        #Cleared_clock_thing(display, time_left)
        exit_proc()
    elif message[1] == "BOOM":
        #Change thing in clock_process() (Change defused var)
        display.show("", -1, -1) 
        exit_proc()

def cleared_clock_blinker(display, time_left):
    display.show()
    return

def exit_proc():
    sleep(2)        #Give program time to finish previous command before shutting down
    gpio.cleanup()  #Just in case ;)
    exit(0)

def on_mqtt_connectWIRE(client, userdata, flags, rc):
    if (rc ==0):
        mqtt.Client.connected_flag = True
        print(">> on_mqtt_connectWIRE: mqtt broker connection OK")
        client.subscribe(MQTT_TOPIC, MQTT_QOS)
    else:
        print(">> on_mqtt_connectWIRE: mqtt broker error: {}".format(rc))
        client.bad_connection_flag = True

def on_mqtt_messageWIRE():
    pass

def Timer_PubSubStuff():
    Timerclient = None
    mqtt.Client.connected_flag = False
    mqtt.Client.bad_connection_flag = False

    Timerclient = mqtt.Client("Timerclient")
    Timerclient.on_connect = on_mqtt_connectWIRE
    Timerclient.on_message = on_mqtt_messageWIRE

    try:
        Timerclient.connect(MQTT_BROKER)
        Timerclient.loop_start()
    except:
        print(">>Timer_PubSubStuff: Connection Failed")
    while not Timerclient.connected_flag and not Timerclient.bad_connection_flag:  #wait in loop
	    print(">> init_mqtt: in connection wait loop")
	    sleep(1)
    if Timerclient.bad_connection_flag:
	    Timerclient.loop_stop()
	    exit_proc()
    return Timerclient

#-----------------------------------------------
def clock_process(time_total, blinkfrom, DEBUG):
    global defusedTimer, time_left
    defusedTimer = False
    if DEBUG:
        logging.basicConfig(filename='logfile.log', level=logging.DEBUG, format='%(levelname)s: %(asctime)s: %(filename)s: %(funcName)s: \n\t%(message)s')
    if not DEBUG:
        logging.basicConfig(filename='logfile.log', level=logging.WARNING, format='%(levelname)s: %(asctime)s: %(filename)s: %(funcName)s: \n\t%(message)s')

    display = pdc6x1.PDC6x1()
    display.show("  0000", 0, 2)

    time_left = time_total * 100        #Makes the decimel number into an integer that is easyer to work with.
    Timerclient = Timer_PubSubStuff()
    
    starttime = (time() + 2.5)         #Sets time from where all will start.

    dictionary2 = ["TimerModule", "T"]                                      #Preset message to tell the main process that time's up.
    messageT = json.dumps(dictionary2)                                      # "
    dictionary3 = ["TimerModule", "B", time_total, blinkfrom, starttime]    #Preset message to tell the blinking process to start blinking. (Format: ["SendFrom", "Blinking command", "Total time", "Blink from", startfrom]).
    messageB = json.dumps(dictionary3)
    Timerclient.publish("main_channel", messageB)    #Tells the blinking process all the peramiters that are needed for it.
    until(starttime)                                #Waits for all the other time based programs to get ready to start and starts after a predeterment time 2.5 seconds.
    #Start Counting
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    while time_left > 59999 and not defusedTimer:
        time1 = time()                                      #Takes current time to determen later how lont to wait for.
        minu1, sec1 = divmod((time_left//100), 60)
        minu2, sec2 = str(minu1), str(sec1)
        if sec1 < 10:
            sec2 = "0" + sec2
        if sec1 == 0:
            sec2 = "00"
        display.show("  {}{}".format(minu2, sec2), 1, 2)
        time_left -= 100                                    #Takes one second from the timer.
        until(time1 + 1.00)                                 #Waits untill excactly one second has passed from the beginning of this while-loop itiration.
        pass

    while 60000 > time_left > 6000 and not defusedTimer:    #Is active when time left > 60 seconds.
        time2 = time()                                      #Takes current time to determen later how lont to wait for.
        minu1, sec1 = divmod((time_left//100), 60)
        minu2, sec2 = str(minu1), str(sec1)
        if sec1 < 10:
            sec2 = "0" + sec2
        if sec1 == 0:
            sec2 = "00"
        display.show("  0{}{}".format(minu2, sec2), 1, 2)
        time_left -= 100                                    #Takes one second from the timer.
        until(time2 + 1.00)                                 #Waits untill one second has passed from the beginning of this while-loop itiration.
        pass
    
    while -1 < time_left < 6001 and not defusedTimer:       #Is activated when time is less than 60.01 seconds and is more them 0.009999999... seconds.
        time3 = time()                                      #Takes current time to determen later how lont to wait for.
        if time_left > 999:
            space = ""
        if time_left < 1000:
            space = "0"
        if time_left < 100:
            space = "00"
        display.show(("  " + space + str(time_left)), 1, 2) #NOGFORMATTEN VAN DE SPACINGK
        time_left -= 1                                      #Takes one hundreth of a second from the timer.
        until(time3 + 0.01)                                 #Waits untill one second has passed from the beginning of this while-loop itiration.
        pass        
        

    while time_left < 1:                            #Is activated when time is less than 0.01 seconds
        display.show("  0000", 1, 2)
        Timerclient.publish("main_channel", messageT)#Tells the main process that Time's up (Send predefined message).
        display.show("      ", -1, -1)
        exit(0)