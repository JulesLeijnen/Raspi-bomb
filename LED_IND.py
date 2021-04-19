import threading
from random import randrange
from numpy.random import choice

IND_Names = ["SND", "CLR", "CAR", "IND", "FRQ", "SIG", "NSA", "MSA", "TRN", "BOB", "FRK"]
amountled_clear = False
precent_clear = False
modeselect_clear = False
TEST = False

Led_core = "Null"

def SetUpLED_IND():
  global IND_Names, amount_led, percent_led, amountled_clear, TEST, modeselect_clear, precent_clear, Led_core
  while not modeselect_clear:
    modeselected = str(input("LED_INDICATORS: Do you want the default mode(d), the kids mode(k), or the custom mode(c)?")).upper()
    if modeselected == "D" or modeselected == "K" or modeselected == "C" or modeselected == "TESTRUN":
      modeselect_clear = True
      pass
    else:
      error = 1
      print("INPUTERROR, Input has incorrect format [{}]".format(modeselected))

  print("You have selected: {}!".format(modeselected))

  if modeselected == "D":
    amount_led = 3
    percent_led = (1/3)
  elif modeselected == "K":
    amount_led = 1
    percent_led = (1/2)
    pass
  elif modeselected == "C":
    while not amountled_clear:
      amount_led = int(input("How many LED Indicators do you need in the bomb (Between 1 and 5)"))
      if (amount_led > 0) and (amount_led < 6):
          amountled_clear = True
      else:
          print("Input error: Format incorrect!")
    while not precent_clear:
      percent_led = ((int(input("What procent of the led indicators need to be lit?"))))
      if (percent_led > 0) and (percent_led < 101):
        precent_clear = True
        percent_led = percent_led / 100
      else:
        print("Input error: Format incorrect!")
  elif modeselected == "TESTRUN":
    TEST = True
    amount_led = 10
    percent_led = (1/5)
    pass

def naamloos():
  Complete_lists = []
  naamlooslijst = []
  naamlooslijst.append(amount_led)
  naamlooslijst.append(percent_led)
  for x in range(0, amount_led):
    naamlooslijst.append(IND_Names[randrange(0, 11)])
  Complete_lists.append(naamlooslijst)
  TrueFalselist = TFGenerator(naamlooslijst)
  Complete_lists.append(TrueFalselist)
  showresult(Complete_lists)
  return

def TFGenerator(looslijst):
  elements = [True, False]
  weights=[(looslijst[1]), (1 - looslijst[1])]
  
  TFlist = []
  TFlist.append(looslijst[0])
  TFlist.append(looslijst[1])
  for x in range(0, looslijst[0]):
    TFlist.append(choice(elements, p=weights))
  print(TFlist)
  return TFlist

def showresult(Complete_lists):
  print(Complete_lists)
  print(" ")
  print("DEBUG = {}".format(TEST))
  print("The original list was: {}".format(Complete_lists[0]))
  print("The TF list is:        {}".format(Complete_lists[1]))

  if TEST:
    if len(Complete_lists[0]) == len(Complete_lists[1]) and Complete_lists[0][0] == Complete_lists[1][0] and Complete_lists[0][1] == Complete_lists[1][1]:
      print("Test compleeted succesfully")
    else:
      print("Test was incorrect... Please contect the creator of the program to fix the issue.")

Led_Setup = threading.Thread(target=SetUpLED_IND)
Led_Core = threading.Thread(target=naamloos)