from random import randrange, choice
import RPi.GPIO as gpio

ERROR = False
SN_odd = choice([0, 1])

wires = []

possible_colors3 = ["Red", "Blue", "White", "Red", "Blue", "White", "Yellow", "Black", "Not_important"]
possible_colors4 = ["Red", "Blue", "Yellow", "Red", "Blue", "Yellow", "White", "Black", "Not_important"]
possible_colors5 = ["red", "Black", "Yellow", "red", "Black", "yellow", "white", "blue", "Not_important"]
possible_colors6 = ["red", "white", "Yellow", "red", "white", "yellow", "black", "blue", "Not_important"]

#---------------------------------------------------------------------------------

def DRAADmode_selection(mode_draad, Custom_colours, testing):
    global possible_colors, ERROR, wires, DEBUG
    DEBUG = testing
    if mode_draad == "D":
        possible_wire_amount = [3, 4, 5, 6]
        select_wireamount = possible_wire_amount[(randrange(4))]
        if select_wireamount == 3:
            possible_colors = possible_colors3
        elif select_wireamount == 4:
            possible_colors = possible_colors4
        elif select_wireamount == 5:
            possible_colors = possible_colors5
        elif select_wireamount == 6:
            possible_colors = possible_colors6
        else:
            ERROR = True
            print("Variable ERROR: Incorrect Integer in int(select_wireamount). The given input was: {}".format(select_wireamount))
        if not ERROR:
            DRAAD_DK_input_setup(select_wireamount)
    elif mode_draad == "K":
        possible_wire_amount = [3, 4]
        select_wireamount = possible_wire_amount[(randrange(2))]
        if select_wireamount == 3:
            possible_colors = possible_colors3
        elif select_wireamount == 4:
            possible_colors = possible_colors4
        else:
            ERROR = True
            print("Variable ERROR: Incorrect Integer in int(select_wireamount). The given input was: {}".format(select_wireamount))
        DRAAD_DK_input_setup(select_wireamount)
    elif mode_draad == "C":
        if len(Custom_colours) > 2 and len(Custom_colours) < 7:
            wires = Custom_colours
        else:
            ERROR = True
            print("Variable ERROR: Incorrect amount of elements in list(wires). The given input was: {}".format(select_wireamount))

    else:
        print("Input ERROR: Incorrect Input in 'DRAADmode_selection' for mode_draad. The given input was: {}".format(mode_draad))

def DRAAD_DK_input_setup(select_wireamount):
    global wires, ERROR, correctwire
    for x in range(0, select_wireamount):
        if x > 6:
            ERROR = True
            print("Loop ERROR: Loop repeats more then possible in DRAAD_DK_input_setup")
        else:
            wires.append(possible_colors[randrange(9)])
    print(wires)
    if select_wireamount == 3:
         correctwire = DRAADsolve_3wires(wires)
    elif select_wireamount == 4:
         correctwire = DRAADsolve_4wires(wires)
    elif select_wireamount == 5:
         correctwire = DRAADsolve_5wires(wires)
    elif select_wireamount == 6:
         correctwire = DRAADsolve_6wires(wires)
    print(correctwire)

#---------------------------------------------------------------------------------

def DRAADsolve_3wires(wires):
    if ((wires.count("Red") == 0) or
            ((wires.count("Blue") > 1 and wires[2] == "Red"))):
        return 2
    return 3  # default waarde

def DRAADsolve_4wires(wires):
    global SN_odd
    if (wires.count("Red")) > 1 and SN_odd == 1:
        return 4 - 1 - wires[::-1].index('Red') + 1
    elif (wires[3] == "Yellow" and (wires.count("Red")) == 0) or (wires.count("Blue")) == 1:
        return 1
    elif (wires.count("Yellow")) > 1:
        return 4
    return 2  # default waarde

def DRAADsolve_5wires(wires):
    global SN_odd
    if wires[4] == "Black" and SN_odd == 1:
        return 4
    elif wires.count("Black") == 0:
        return 2
    return 1  # default waarde

def DRAADsolve_6wires(wires):
    global SN_odd
    if wires.count("Yellow") == 0 and SN_odd == 1:
        return 3
    elif wires.count("Red") == 0:
        return 6
    return 4  # default waarde

#---------------------------------------------------------------------------------
def Check_UI():
    global NOTCLEARED, WINSTATUD
    WINSTATUS = 0
    NOTCLEARED = True
    

    global DRAAD1, DRAAD2, DRAAD3, DRAAD4, DRAAD5, DRAAD6

    DRAAD1 = 7
    DRAAD2 = 13
    DRAAD3 = 15
    DRAAD4 = 8
    DRAAD5 = 10
    DRAAD6 = 12

    gpio.setwarnings(DEBUG)
    gpio.setmode(gpio.BOARD)

    gpio.setup(DRAAD1, gpio.IN, pull_up_down=gpio.PUD_DOWN)
    gpio.setup(DRAAD2, gpio.IN, pull_up_down=gpio.PUD_DOWN)
    gpio.setup(DRAAD3, gpio.IN, pull_up_down=gpio.PUD_DOWN)

    gpio.add_event_detect(DRAAD1, gpio.FALLING, callback=CallbackD1)
    gpio.add_event_detect(DRAAD2, gpio.FALLING, callback=CallbackD2)
    gpio.add_event_detect(DRAAD3, gpio.FALLING, callback=CallbackD3)

    if len(wires) > 3:
        gpio.setup(DRAAD4, gpio.IN, pull_up_down=gpio.PUD_DOWN)
        gpio.add_event_detect(DRAAD4, gpio.FALLING, callback=CallbackD4)
    elif len(wires) > 4:
        gpio.setup(DRAAD5, gpio.IN, pull_up_down=gpio.PUD_DOWN)
        gpio.add_event_detect(DRAAD5, gpio.FALLING, callback=CallbackD5)
    elif len(wires) > 5:
        gpio.setup(DRAAD6, gpio.IN, pull_up_down=gpio.PUD_DOWN)
        gpio.add_event_detect(DRAAD6, gpio.FALLING, callback=CallbackD6)

    while NOTCLEARED:
        if WINSTATUS == 1:
            print("Win!!")
            NOTCLEARED = False
        pass
    gpio.cleanup()
#-------------------------------------------------------------------------------
def CallbackD1(channel):
    gpio.remove_event_detect(DRAAD1)
    print("Draad 1 doorgeknipt")
    return Input_processing(1)


def CallbackD2(channel):
    gpio.remove_event_detect(DRAAD2)
    print("Draad 2 doorgeknipt")
    return Input_processing(2)


def CallbackD3(channel):
    gpio.remove_event_detect(DRAAD3)
    print("Draad 3 doorgeknipt")
    return Input_processing(3)


def CallbackD4(channel):
    gpio.remove_event_detect(DRAAD4)
    print("Draad 4 doorgeknipt")
    return Input_processing(4)


def CallbackD5(channel):
    gpio.remove_event_detect(DRAAD5)
    print("Draad 5 doorgeknipt")
    return Input_processing(5)


def CallbackD6(channel):
    gpio.remove_event_detect(DRAAD6)
    print("Draad 6 doorgeknipt")
    return Input_processing(6)
#-------------------------------------------------------------------------------
def Input_processing(InputWire):
    global result, WINSTATUS
    if InputWire == correctwire:
        print("Succes!")
        WINSTATUS = 1
        gpio.cleanup()
        return "Succes!"
    else:
        print("+1 Fault!")
        return "+1 Fault!"
