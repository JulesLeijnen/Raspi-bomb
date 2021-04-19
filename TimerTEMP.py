from time import sleep

RedOn = 0

def setupclock(mode_timer, seconds, blink):
  global modeselected, timer_length_seconds, blinkred_from
  
  modeselected = mode_timer.lower()

  if modeselected == "d":
    timer_length_seconds = 300
    blinkred_from = 60
    print("You have selected the default setting: with {} seconds".format(timer_length_seconds))
    timer()
    pass
  elif modeselected == "k":
    timer_length_seconds = 600
    blinkred_from = 60
    print("You have selected the kids setting: with {} seconds".format(timer_length_seconds))
    timer()
  elif modeselected == "c":
    timer_length_seconds = seconds
    blinkred_from = blink
    timer()
  else:
    error = 1
    pass
  

def timer():
  global RedOn, blinkred_from, error
  for x in range(1,6):
    print("Starting in: {}".format(5-x))
    sleep(1)
  for x in range(0, timer_length_seconds, 1):
    time_remaining = timer_length_seconds - x
    cycele_tick_time = convert(time_remaining)
    print(cycele_tick_time[0])
    display_sec = cycele_tick_time[2]
    display_min = cycele_tick_time[1]
    print(display_min)
    print(display_sec)
    if time_remaining < blinkred_from:
      print("Blink ON")
      sleep(0.15)
      print("Blink OFF")
      sleep(0.35)
      print("Blink ON")
      sleep(0.15)
      print("Blink OFF")
      sleep(0.35)
      pass
    else:
      sleep(1)
    pass
  print("Time!")

def convert(seconds): 
    seconds = seconds % (3600) 
    minutes = seconds // 60
    seconds %= 60
      
    list = []
    list.append("%02d:%02d" % (minutes, seconds))
    list.append(minutes)
    list.append(seconds)
    return list

#Timer_Setup = threading.Thread(target=setupclock)
#Timer_Core = threading.Thread(target=timer)
setupclock("d", 300, 30)