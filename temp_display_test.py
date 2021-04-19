import pdc6x1
from time import sleep

sleep(1)
i = 1
display = pdc6x1.PDC6x1()
display.show("1234", 1, 1)
while True:
    display.show(str(i), 0, 0)
    i = i + 1