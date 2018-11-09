##i=0    
##def main():
##
##    global i
##print("\n\n************** Loop " + str(i) + " **************\n")    
while True:    
    s = Sensor()
    
    time.sleep(4)
    s.dataReady() 
    s.readMeasurement()
##        i += 1
    
#main()
# SCD30_Python_Library