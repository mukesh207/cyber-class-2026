with open('latitude.txt','r') as latitudes:
    
    for latitude in latitudes:
        if float(latitude.replace('\n','')) < 99 and float(latitude.replace('\n','')) > -99:
            print (latitude)
