#Imports
from pdc6x1 import PDC6x1

#-----------------------------------------------
def clock_process(time_total, blinkfrom):
    
    blinking_from = blinkfrom * 100
    time_left = time_total * 100
    blinking = False

    while time_left > 6000:
        #print time on 7Seg
        time_left -= 100
        #Wait so 1 seconds has passed
        pass
    
    while time_left < 6001:
        #print time on 7seg
        time_left -= 1
        if time_left < blinking_from and time_left % 50 == 0:
            blinking = not blinking
            if blinking:
                #leds on
                pass    
            else:
                #leds off
                pass
        #Wait so 0.01 seconds has gone by.
        pass        
        

    if time_left < 1:
        #Send +3 faults
        pass
