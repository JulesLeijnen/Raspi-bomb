#--------------------------------------Imports---------------------------------------
from pause import until
import logging
import pdc6x1
from time import sleep, time
import paho.mqtt.client as mqtt #import the client1
import json
#--------------------------------------Globals--------------------------------------
MQTT_BROKER = "localhost"
MQTT_TOPIC_TO_MAIN = "to_main"
MQTT_TOPIC_FROM_MAIN = "from_main"
MQTT_QOS = 2
MQTT_RETAIN = True
#-------------------------------------LOGGING---------------------------------------------

#------------------------------------Main Function---------------------------------------
def clock_process(time_total, blinkfrom, DEBUG):
    global bomb_done_timer, time_left, display
    bomb_done_timer = False

    if DEBUG:
        logging.basicConfig(filename='logfile.log', level=logging.DEBUG, format='%(levelname)s: %(asctime)s: %(filename)s: %(funcName)s: \n\t%(message)s')
    if not DEBUG:
        logging.basicConfig(filename='logfile.log', level=logging.WARNING, format='%(levelname)s: %(asctime)s: %(filename)s: %(funcName)s: \n\t%(message)s')

    display = pdc6x1.PDC6x1()
    display.show("  0000", 0, 2)

    starttime = 2507.1973

    time_left = time_total * 100        #Makes the decimel number into an integer that is easyer to work with.
    Timerclient = Timer_PubSubStuff()
    
    starttime = (time() + 2.5)         #Sets time from where all will start.

    dictionary2 = ["TimerModule", "T"]                                      #Preset message to tell the main process that time's up.
    messageT = json.dumps(dictionary2)                                      # "
    dictionary3 = ["TimerModule", "B", time_total, blinkfrom, starttime]    #Preset message to tell the blinking process to start blinking. (Format: ["SendFrom", "Blinking command", "Total time", "Blink from", startfrom]).
    messageB = json.dumps(dictionary3)
    Timerclient.publish(MQTT_TOPIC_FROM_MAIN, messageB)    #Tells the blinking process all the peramiters that are needed for it.
    
    until(starttime)                                #Waits for all the other time based programs to get ready to start and starts after a predeterment time 2.5 seconds.

    #Start Counting part of process
    while time_left > 59999 and not bomb_done_timer:
        temp_time = time()                                      #Takes current time to determen later how lont to wait for.
        minu1, sec1 = divmod((time_left//100), 60)
        minu2, sec2 = str(minu1), str(sec1)
        if sec1 < 10:
            sec2 = "0" + sec2
        if sec1 == 0:
            sec2 = "00"
        display.show("  {}{}".format(minu2, sec2), 1, 2)
        time_left -= 100                                    #Takes one second from the timer.
        until(temp_time + 1.00)                                 #Waits untill excactly one second has passed from the beginning of this while-loop itiration.
        pass

    while 60000 > time_left > 6000 and not bomb_done_timer:    #Is active when time left > 60 seconds.
        temp_time = time()                                      #Takes current time to determen later how lont to wait for.
        minu1, sec1 = divmod((time_left//100), 60)
        minu2, sec2 = str(minu1), str(sec1)
        if sec1 < 10:
            sec2 = "0" + sec2
        if sec1 == 0:
            sec2 = "00"
        display.show("  0{}{}".format(minu2, sec2), 1, 2)
        time_left -= 100                                    #Takes one second from the timer.
        until(temp_time + 1.00)                                 #Waits untill one second has passed from the beginning of this while-loop itiration.
        pass
    
    while -1 < time_left < 6001 and not bomb_done_timer:       #Is activated when time is less than 60.01 seconds and is more them 0.009999999... seconds.
        temp_time = time()                                      #Takes current time to determen later how lont to wait for.
        if time_left > 999:
            space = ""
        if time_left < 1000:
            space = "0"
        if time_left < 100:
            space = "00"
        display.show(("  " + space + str(time_left)), 1, 2) #NOGFORMATTEN VAN DE SPACINGK
        time_left -= 1                                      #Takes one hundreth of a second from the timer.
        until(temp_time + 0.01)                                 #Waits untill one second has passed from the beginning of this while-loop itiration.
        pass        
        

    while time_left < 1:                            #Is activated when time is less than 0.01 seconds
        display.show("  0000", 1, 2)
        Timerclient.publish(MQTT_TOPIC_TO_MAIN, messageT)#Tells the main process that Time's up (Send predefined message).
        display.show("      ", -1, -1)
        exit(0)
    while bomb_done_timer == True:
        print("TIMER: Exited from bomb defused or 3 faults, no time up...")
        Timerclient.loop_stop()
        sleep(2)        #Give program time to finish previous command before shutting down (Superstition from screenshot reading adventure)
        exit(0)

def cleared_clock_blinker(display, time_left):
    minu1, sec1 = divmod((time_left//100), 60)
    if minu1 < 10 and sec1 < 10:
        Cleared_timer_string = "  0{}0{}".format(minu1, sec1)
    elif minu1 < 10 and sec1 > 9:
        Cleared_timer_string = "  0{}{}".format(minu1, sec1)
    elif minu1 > 9 and sec1 < 10:
        Cleared_timer_string = "  {}0{}".format(minu1, sec1)
    elif minu1 > 9 and sec1 > 9:
        Cleared_timer_string = "  {}{}".format(minu1, sec1)
    else:
        Cleared_timer_string = " ERROR"
    for _ in range(10):
        display.show(Cleared_timer_string, 1, 2)
        sleep(0.5)
        display.show("      ", -1, -1)
        sleep(0.5)
#------------------------------------MQTT Functions---------------------------------------
def Timer_PubSubStuff():
    Timerclient = None
    mqtt.Client.connected_flag = False
    mqtt.Client.bad_connection_flag = False

    Timerclient = mqtt.Client("Timerclient")
    Timerclient.on_connect = on_mqtt_connectTIMER
    Timerclient.on_message = on_mqtt_messageTIMER

    try:
        Timerclient.connect(MQTT_BROKER)
        Timerclient.loop_start()
    except:
        print(">>Timer_PubSubStuff: Connection Failed")
    while not Timerclient.connected_flag and not Timerclient.bad_connection_flag:  #wait in loop
	    print(">> Timer_PubSubStuff: in connection wait loop")
	    sleep(1)
    if Timerclient.bad_connection_flag:
        Timerclient.loop_stop()
        sleep(2)
        exit(0)
    return Timerclient

def on_mqtt_connectTIMER(client, userdata, flags, rc):
    if (rc ==0):
        mqtt.Client.connected_flag = True
        print(">> on_mqtt_connectTIMER: mqtt broker connection OK")
        client.subscribe(MQTT_TOPIC_FROM_MAIN, MQTT_QOS)
    else:
        print(">> on_mqtt_connectTIMER: mqtt broker error: {}".format(rc))
        client.bad_connection_flag = True

def on_mqtt_messageTIMER(client, userdata, message):
    new_message = json.loads(str(message.payload.decode("utf-8")))
    print("TIMER: message received in timer_process.py: {}\n".format(new_message,))
    TimerMessageResolver(new_message) #, display) #How do I give the function the display that is made in the main function of this process?
 
def TimerMessageResolver(message): #, display):
    global bomb_done_timer, time_left, display
    if message[1] == "Cleared":
        bomb_done_timer = True
        end_time = time_left
        cleared_clock_blinker(display, time_left)
        print("CLEARED IN TIMER MODULE")
        sleep(2)        #Give program time to finish previous command before shutting down (Superstition from screenshot reading adventure)
        exit(0)
    elif message[1] == "BOOM":
        bomb_done_timer = True
        display.show("", -1, -1)
        print("BOOM IN TIMER MODULE")
        sleep(2)        #Give program time to finish previous command before shutting down (Superstition from screenshot reading adventure)
        exit(0)
    else:
        print("TEMP1")
        bomb_done_timer = False