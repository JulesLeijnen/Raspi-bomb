import paho.mqtt.client as mqtt
import json

broker_adress="localhost"
instancename = "MAIN"
client = mqtt.Client(instancename)
print("1")
client.connect(broker_adress)
print("2")
dictionary = ["MAIN", "TEST1"]
temp1 = json.dumps(dictionary)
print("3")
client.publish("from_main",temp1)
print("4")

# time_left = 7000
# minu1, sec1 = divmod((time_left//100), 60)
# print(minu1)
# print(type(minu1))
# print(sec1)
# print(type(sec1))
# x = input(str("test")).upper()
# print(x)
# x = "{}".format(False)
# print(x)
# print(type(x))
#from pdc6x1 import PDC6x1
# import time
# print(time.time())
# x = time.time() + 1
# print(x)
# import logging
# def func1():
#     logging.basicConfig(filename='logfile.log', level=logging.DEBUG, format='%(levelname)s: %(asctime)s: %(funcName)s: \n\t%(message)s')
#     logging.debug("TEst1")
# func1()
# while True:
#     x1 = time.time()
#     x2 = time.time()
#     x3 = time.time()
#     x4 = time.time()
#     x5 = time.time()
#     x6 = time.time()
#     x7 = time.time()
#     x8 = time.time()
#     x9 = time.time()
#     x10 = time.time()
#     print( x10 - x1)
#     time.sleep(0.1)
#     print(time.time())
#     time.sleep(0.1)