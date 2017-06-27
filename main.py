import RPi.GPIO as GPIO
import time
from datetime import datetime
import MySQLdb as db
#import sys


################################# Setting GPIO ################################################

FLOW_SENSOR = 23                    # using GPIO Pin 23 for water flow sensor(BCM)
ir_sensor = 7                       # using GPIO Pin  7 for IR sensor (BOARD) ( we have to change to BCM Mode Pin )

GPIO.setmode(GPIO.BCM)              # water flow sensor
GPIO.setup(FLOW_SENSOR, GPIO.IN, pull_up_down = GPIO.PUD_UP)

GPIO.setmode(GPIO.BOARD)            # IR sensor
GPIO.setup(ir_sensor, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


################################# Global Declaration  ###########################################

global count
count = 0

global check
check = 0

global water_state
water_state = 0

global total_water_used
total_water_used = 0

global person
person = 0

global total_water_wasted
total_water_wasted = 0

global vacancy
vacancy = 0  # 0 = empty , 1 = not empty

sys_time = datetime.now()

################################# Global Declaration End  #####################################


while True:
    time.sleep(3)
    try:

        ################################# WATER FLOW SENSOR ###########################################
        def countPulse(channel):
            global count
            check = count
            count = count+1
            print count




        GPIO.add_event_detect(FLOW_SENSOR, GPIO.FALLING, callback=countPulse)



        while True:
            try:
                time.sleep(0.5)



        while True :
            try:
                if check < count:
                    water_state = 1

                elif check == count:
                    water_state = 0



        #----------------------------------------------------------------------------------#
        # we have to deal with "count" to get water quantity

        #  Pulse frequency(Hz) = 7.5Q,Q is flowrate in Litres / minute
        #  Flow Rate(Litres / hour) = (Pulse frequency x 60min)/7.5Q

        # Sensor Frequency (Hz) = 7.5 * Q (Liters/min)
        # Litres = Q * time elapsed (seconds) / 60 (seconds/minute)
        # Litres = (Frequency (Pulses/second) / 7.5) * time elapsed (seconds) / 60
        # Litres = Pulses / (7.5 * 60)

        # http://www.electroschematics.com/12145/working-with-water-flow-sensors-arduino/
        # ----------------------------------------------------------------------------------#


        total_water_used = " " # to be calculated by count

        ################################# WATER FLOW SENSOR END ###########################################

        ################################# IR SENSOR START       ###########################################

        current = GPIO.input(ir_sensor)
        previous = current

        def printState(current):        # For Test only
            print 'GPIO pin %s is %s' % (ir_sensor, 'HIGH' if current else 'LOW')
        printState(current)

        while True:
            current = GPIO.input(ir_sensor)
            if current != previous:
                printState(current)     # For Test only
                person = 1
                print "Someone is there! \n"
                #return person

            else :
                previous = current
                person = 0
                print "No One is there! \n"


        ################################# IR SENSOR END          ###########################################
        ################################# Analytics Start        ###########################################


        if person == 1 and (water_state == 1 or water_state == 0):
            print "Bathroom is in use"
            vacancy = 1

        elif person == 0 and water_state == 1:
            print "Washroom is vacant and Mis use of water is going on "
            # ALERT STATEMENT
            vacancy = 0

            total_water_wasted =

        elif person == 0 and water_state == 0:
            print "Washroom is vacant"
            vacancy = 0

        ################################# Analytics End          ###########################################


        ################################# DATABASE Work Start    ###########################################
        ir_db = str(person)
        vacancy_db = str(vacancy)
        total_water_used_db = str(total_water_used)
        total_water_wasted_db = str(total_water_wasted)
        time_db = str(sys_time)


        HOST = "remote host"
        PORT = 3306
        USER = "username of remote mysql instance"
        PASSWORD = "password of remote mysql instance"
        DB = "sensor_data"

        sql_query = """INSERT INTO sensor_reading_of_infocity(ir, vacancy, total_water_used, total_water_wasted, time)
                                                      VALUES ('%s', '%s', '%s', '%s', '%s')  % \ (ir_db, vacancy_db, total_water_used_db, total_water_wasted_db, time_db ))"""

        try:
            connection = db.Connection(host=HOST, port=PORT, user=USER, passwd=PASSWORD, db=sensor_data)

            dbhandler = connection.cursor()
            dbhandler.execute(sql_query)
            db.commit()

        except:
            db.rollback()
            print "Error while inserting data into database"

        finally:
            connection.close()

        ################################# DATABASE Work END      ###########################################

    except KeyboardInterrupt:
        print('\nCaught keyboard interrupt!, System is existing ,bye')

    except:
        print "System Failed to work"



    finally:
        GPIO.cleanup()