import grovepi
import math
import time

while True:
    try:
        [temp,humidity] = grovepi.dht(4,1)  #put the sensor to D4
        if math.isnan(temp) == False and math.isnan(humidity) == False:
            print("temp = %.02f C humidity =%.02f%%"%(temp, humidity))
        time.sleep(1)
    except IOError:
        print ("Error")
