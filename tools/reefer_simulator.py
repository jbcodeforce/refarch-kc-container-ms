import csv, sys, json, datetime
import random
import numpy as np
import pandas as pd

'''
Simulate the metrics for a Reefer container.
'''
# Define constants for average
simulation_type = "nopower"

CO2_LEVEL = 4 # in %
O2_LEVEL = 21 # in %
NITROGEN_LEVEL = 0.78 # in %
POWER_LEVEL= 7.2 # in kW
NB_RECORDS_IMPACTED = 7

Today= datetime.datetime.today()
nb_records = 1000
fname = "testdata"
tgood = 4.4
id = 101

df = pd.DataFrame(columns=['Timestamp', 'ID', 'Temperature(celsius)', 'Target_Temperature(celsius)', 'Power', 'PowerConsumption', 'ContentType', 'O2', 'CO2', 'Time_Door_Open', 
'Maintenance_Required', 'Defrost_Cycle'])

def saveFile():
    print("Save to file ", fname)    

def generatePowerOff():
    global nb_records,id, tgood
    range_list=np.linspace(1,2,nb_records)
    ctype=random.randint(1,5)   # ContentType
    print("Generating ",nb_records, " poweroff metrics")
    count_pwr = 0  # generate n records with power off
    maintenance_flag = 0
    temp = random.gauss(tgood, 2.0)
    for i in range_list:
        adate = Today + datetime.timedelta(minutes=10*i)
        timestamp =  adate.strftime('%Y-%m-%d T%H:%M Z')
        oldtemp = temp
        temp =  random.gauss(tgood, 2.0)
        pwr =  random.gauss(POWER_LEVEL,8)   # Power at this time - 
        # as soon as one amp record < 0 then poweroff for n records
        if  pwr < 0.0:
            pwr = 0
            count_pwr = count_pwr + 1
            temp = oldtemp
        elif 0 < count_pwr < NB_RECORDS_IMPACTED:
            # when powerer off the T increase
            count_pwr = count_pwr + 1
            pwr = 0
            temp = oldtemp + 0.8 * count_pwr
        if count_pwr == NB_RECORDS_IMPACTED:
            maintenance_flag = 1
        df.loc[i] = [timestamp, 
                    id,
                    temp, # Temperature(celsius)
                    tgood,             # Target_Temperature(celsius)
                    pwr,    
                    random.gauss(POWER_LEVEL,1.0), # PowerConsumption
                    ctype,                # ContentType
                    random.randrange(O2_LEVEL),  # O2
                    random.randrange(CO2_LEVEL), # CO2
                    random.gauss(8.0, 2.0), # Time_Door_Open
                    maintenance_flag,    # maintenance required
                    6]    # defrost cycle
    print(df)    
        
 

def parseArguments():
    global simulation_type, nb_records, tgood
    if len(sys.argv) != 5:
        print("Need to have at least 3 arguments: ")
        print("\tthe simulation type one of (poweroff, co2sensor)")
        print("\tthe number of records to generate")
        print("\texpected temperature for the goods")
        print("\tthe filename to create (without .csv)")
        exit(1)
    else:
        simulation_type = sys.argv[1]
        nb_records = sys.argv[2]
        tgood = int(sys.argv[3])
        fname = sys.argv[4]

def generateCo2():
    print("Generating Co2 metrics")



if __name__ == "__main__":
    parseArguments()
    if simulation_type == "poweroff":
        generatePowerOff()
        saveFile()
    elif  simulation_type == "co2sensor":
        generateCo2()
        saveFile()
    else:
        print("Not a valid simulation")
    