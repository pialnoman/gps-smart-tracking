# Project AMR Enabled Water Meter Reading
# Water Meter Reading Data Writing Server

import Database_GPS_Tracker
import codecs # For hex conversion
import collections # For creating ordered dictionary
import datetime # For current date time
import json # For creating json data
import os
from pathlib import Path
import queue # For holding data recieved from stream
import shutil # For file processing
import socket # For socket programming
import socketserver # For writing network server
import sys
import threading # For threading
from threading import Thread, current_thread # For current thread
#from datetime import datetime, time
import time
#import binascii


from datetime import datetime, date
from pytz import timezone 

import paho.mqtt.client as paho
import json
import pymysql

from datetime import datetime, timedelta, date

from pytz import timezone 
import calendar
#Global Variables
#MQTT Connection Variables

broker="broker.hivemq.com"
username = "dma_emeter_0198"
password = "dma_emeter_0198"


host = 'dma-bd.com'
port = 3306
user = 'dmabdcom_gps987'
password = 'dmabd987'
db = 'dmabdcom_gpstracker'

#db='dmabdcom_metalprivate'
#############################################################################


class Query(Database_GPS_Tracker.Query):
    pass

#Query.create_connection()



# Responsible for processing data
class Processing:
    Query.create_connection()



    # Responsible for creating a new object
    # Class: Processing
    # Responsible for initialzing instance variables
    # Self refers to newly created object

    device_number = ''
    device_data = ''
    equipment_id = ''
    datetimee = ''
    latitude =''
    longitude = ''
    direction = ''
    speed = ''
    bat_power = ''

    def __init__(self):

        # FIFO queue created
        # To hold water flow data from 22 bytes stream
        self.data_queue = queue.Queue()

    # def process_device_number():
    # 	 device_number = device_number_analysis()
    # 	 return dev
    #        #-----------Device Number Retrieval Ends---------

    #        #-----------Level Data Retrieval Begins----------
    #    device_data = device_data_analysis()


    def device_data_process(self,client_data):
        device_number = ''
        device_data = ''
        equipment_id = ''
        latitude = ''
        longitude = ''
        #florida = timezone('US/Eastern')

        florida = timezone('Asia/Dhaka')
        florida_time = datetime.now(florida)
        time_stamp = florida_time.strftime('%Y-%m-%d %H:%M:%S')
        print("Time is-->", time_stamp)

        curr_date = time_stamp.split(' ')[0]
        curr_time = str(time_stamp.split(' ')[1])
        print("Current DATE is-->", curr_date)
        print("Current TIME is-->", curr_time)

        #-------------Find Day from Date------------------------
        my_date = date.today()

        day = calendar.day_name[my_date.weekday()]  #'Wednesday'
        print("day is --->", day)
        #-------------Find Day from Date------------------------
        try:

            # client_data = '[3G*1703154710*0138*UD2,140719,183939,V,23.767243,N,90.3583433,E,0.00,0.0,0.0,0,100,90,0,0,00000010,4,255,470,1,21027,10989,146,21027,10990,137,21027,10988,129,21034,45079,113,5,DMA,c4:6e:1f:d1:ef:4c,-54,M haque ,84:16:f9:b4:e2:46,-80,NETGEAR2,c0:ff:d4:c2:4e:0,-84,Zaedul Huq,ac:84:c6:5:b7:4c,-85,Mer'
            print(client_data)
            print(len(client_data))
            if len(client_data) > 0:
	            with open('gps_tracker.txt','a+') as file:
	            	file.write(str(time_stamp)+"\n")
	            	file.write(client_data+"\n")



            print(type(client_data))

            data_one = client_data
            if client_data[1:3] == "3G" and len(client_data)>31 and data_one.split("*")[3][0:2] =="UD":
                print("Location Data from BW202 GPS")
                print("Current DATE is-->", curr_date)
                print("Current TIME is-->", curr_time)
                datetimee = time_stamp

                #-------------Find Day from Date------------------------
                my_date = date.today()

                day = calendar.day_name[my_date.weekday()]  #'Wednesday'
                print("day is --->", day)
                #-------------Find Day from Date------------------------                
                manufacturer_id = data_one.split("*")[0][1:]
                equipment_id = data_one.split("*")[1]
                content_length = data_one.split("*")[2]
                content = data_one.split("*")[3][0:2]

                if content == "LK":
                    print("Content is:", "Link Keep")

                if content == "UD":
                    print("Content is:", "Position Data Report")
                    device_data= data_one.split(",")
                    date_from_device = "20" + device_data[1][4:6] +'-'+ device_data[1][2:4] +'-'+device_data[1][0:2]
                    device = device_data[1][0:2]+"-"+device_data[1][2:4]+"-"+device_data[1][4:6]
                    time_from_device = device_data[2]
                    if len(time_from_device) == 6:
                        time_from_device = device_data[2][0:2] + ':' + device_data[2][2:4] + ':' + device_data[2][4:6]
                        location = device_data[3]
                        print(location)

                    if location == "A":
                        positioning = "positioning"
                        print(positioning)
                    elif location == "V":
                        positioning = "No positioning"
                        print(positioning)
                    latitude = device_data[4]
                    mark_of_latitude = device_data[5]
                    longitude = device_data[6]
                    mark_of_longitude = device_data[7]
                    speed = device_data[8] 
                    speed_unit = "km\h"
                    direction = device_data[9]
                    altitude = device_data[10]


                    if len(device_data) > 20:
                        satellite_number = device_data[11]
                        signal_intensity_density = device_data[12]
                        bat_power = device_data[13]
                        print("Battery power:" + str(bat_power))
                        time.sleep(3)
                        number_of_steps = device_data[14]
                        roll_number = device_data[15]
                        terminal_state = device_data[16]
                        base_station_numer = device_data[17]#gsm time delay
                        base_station_tower = device_data[18]
                        mcc_country_code = device_data[19]
                        mnc_network_number = device_data[20]
                        bs_location_code = device_data[21]
                        bs_number = device_data[22]
                        bs_signal_strength = device_data[23]

                        bs1_location_code  = device_data[24]
                        bs1_number = device_data[25]
                        bs1_signal_strength = device_data[26]
                        bs2_location_code  = device_data[27]
                        bs2_number = device_data[28]
                        bs2_signal_strength = device_data[29]

                        bs3_location_code  = device_data[30]
                        bs3_number = device_data[31]
                        bs3_signal_strength = device_data[32]

                        wifi_information_quantity  = device_data[33]
                        #for i in range(1,len(wifi_information_quantity)):

                        wifi_1_name  = device_data[34]
                        wifi_1_mac_add  = device_data[35]
                        wifi_1_signal_strength  = device_data[36]
                        wifi_2_name  = device_data[37]
                        wifi_2_mac_add  = device_data[38]

                        wifi_2_signal_strength = device_data[39]
                        # print("___________________________________________")
                        # print("           Data from GPS Tracker")
                        # print("___________________________________________")
                        # print("Manufacturer id-", manufacturer_id)
                        # print("Equipment Id-", equipment_id)
                        # print("Content Length", content_length)
                        # print("Content", content)  
                        # print("Date from device: ", date_from_device)
                        # print("Time from device: ", time_from_device)

                        # print("location: ", location)
                        # print("positioning: ", positioning)
                        # print("latitude: ", latitude)
                        # print("mark_of_latitude: ", mark_of_latitude)
                        # print("longitude: ", longitude)
                        # print("mark_of_longitude: ", mark_of_longitude)
                        # print("speed: ", speed)
                        # print("speed_unit: ", speed_unit)
                        # print("direction: ", direction)
                        # print("altitude", altitude)

                        # if len(device_data) > 20:					
                        # print("satellite_number: ", satellite_number)
                        # print("signal_intensity_density: ", signal_intensity_density)
                        # print("power: ", power)
                        # print("number_of_steps: ", number_of_steps)
                        # print("roll_number: ", roll_number)
                        # print("terminal_state: ", terminal_state)
                        # print("base_station_numer: ", base_station_numer)
                        # print("base_station_tower: ", base_station_tower)
                        # print("mcc_country_code: ", mcc_country_code)
                        # print("mnc_network_number", mnc_network_number)


                        # print("bs_location_code: ", bs_location_code)
                        # print("bs_number: ", bs_number)
                        # print("bs_signal_strength: ", bs_signal_strength)





                        # print("bs1_signal_strength: ", bs1_signal_strength)
                        # print("bs2_location_code: ", bs2_location_code)
                        # print("bs2_number: ", bs2_number)
                        # print("bs2_signal_strength: ", bs2_signal_strength)
                        # print("bs3_location_code: ", bs3_location_code)
                        # print("bs3_number: ", bs3_number)
                        # print("bs3_nubs3_signal_strengthmber: ", bs3_signal_strength)
                        # print("wifi_information_quantity", wifi_information_quantity)       

                        # print("wifi_1_name: ", wifi_1_name)
                        # print("wifi_1_mac_add: ", wifi_1_mac_add)
                        # print("wifi_1_signal_strength: ", wifi_1_signal_strength)
                        # print("wifi_2_name: ", wifi_2_name)
                        # print("wifi_2_mac_add", wifi_2_mac_add)    
                        # print("wifi_2_signal_strength", wifi_2_signal_strength)       



                        # print("data to be inserted in databse")
                        # print("Manufacturer id-", manufacturer_id)
                        # print("Equipment Id-", equipment_id)
                        # print("Content Length", content_length)
                        # print("Content", content)        
                        # print("Date from device: ", date_from_device)
                        # print("Time from device: ", time_from_device)
                    print("___________________________________________")
                    print("-------Important Data----------- ")

                    print("Manufacturer id-", manufacturer_id)
                    print("Equipment Id-", equipment_id)

                    print("location: ", location)
                    print("positioning: ", positioning)
                    print("latitude: ", latitude)
                    print("mark_of_latitude: ", mark_of_latitude)
                    print("longitude: ", longitude)
                    print("mark_of_longitude: ", mark_of_longitude)
                    print("speed: ", speed)
                    print("speed_unit: ", speed_unit)
                    print("direction: ", direction)
                    print("altitude: ", altitude)
                    #time.sleep(3)
                    print("----------------------------------------- ")
                    #equipment_id="1703164704" bat_power = "30" direction = "300"
                    #latitude = "23.999928"
                    #longitude = "90.420182"
                    conn = pymysql.connect(host=host, user=user, password=password, db=db, cursorclass=pymysql.cursors.DictCursor)
                    cursor = conn.cursor()
                    try:
                        sql1 = """SELECT dg.dev_id FROM devices_gateway as dg LEFT JOIN device_data as dd
                                ON dg.dev_id = dd.dev_id WHERE dg.dev_s_n=%s"""
                        value1 = str(equipment_id)
                        cursor.execute(sql1,value1)
                        
                        if(cursor.rowcount>0):
                            data = cursor.fetchone()
                            if data != None:
                                sql2 = """SELECT dvd_id FROM device_data WHERE dev_id=%s"""
                                value2 = str(data['dev_id'])
                                cursor.execute(sql2,value2)
 
                                
                                if(cursor.rowcount>0):                                  
                                    sql3 ="""UPDATE device_data SET dvd_latitude = %s, dvd_longitude = %s, updated_at = %s, dvd_speed = %s, dvd_bearing = %s, dvd_battery = %s WHERE dev_id = %s """                               
                                    value3 = (str(latitude),str(longitude),str(time_stamp),str(speed), str(direction), str(bat_power), str(data['dev_id']))
                                    cursor.execute(sql3,value3)
                                
                                    if(cursor.rowcount>0):
                                        conn.commit()
                                        print("Data Updated successfully")
                                else:
                                    sql4 = """INSERT INTO device_data(dev_id, dvd_latitude, dvd_longitude, dvd_speed,created_at)
                                             VALUES (%s, %s, %s, %s, %s)"""                   
                                    value4 = (data['dev_id'], latitude, longitude, speed, time_stamp)
                                    cursor.execute(sql4,value4)
                                    
                                    if(cursor.rowcount>0):
                                        conn.commit()
                                        print("DATA Inserted successfully")

                        #______________MQTT SENDING DATA____________
                        client= paho.Client("dma_emeter_0198")
                        print("connecting to broker ",broker)
                        client.connect(broker)#connect
                        client.loop_start() #start loop to process received messages
                        print("publishing ")
                        #dev_id = '123456'
                        message_all = {'time_date':datetimee, 'cell_id': str(equipment_id), 'lat': latitude, 'lon' :longitude, 'bearing':  direction, 'speed' : speed , 'battery' : bat_power}
                        message_all = json.dumps(message_all)
                        print(message_all)
                        #with open('demofile3.txt','a+') as file:
                        #    file.write(message_all+"\n")
                        mqtt_topic = "dma/gpstracker/" + str(equipment_id)
                        print(mqtt_topic)
                        client_response1 = client.publish(mqtt_topic,message_all)#publish
                        print(client_response1)
                        #time.sleep(1)
                        cursor.close() 

                    except Exception as e:
                        print (e)
                    cursor.close() 


                #-------------------------------------------------------------------------------
                print("Waiting for5 seconds")
                #time.sleep(20)




		            #return water_level


            # ##################################################################################3

            # #############################################################################
            # # Required for retrieving device number from data stream
            # def device_number_analysis():

            #     # String format
            #     device_number = ''
            #     for x in hex_client_data[0:2]:
            #         device_number +=x
            #     print ("Device Number: %s" %device_number)

            #     # Return device number
            #     return device_number
            # #############################################################################
            # #----------------------------------Dry---------------------------------------


            #    # Retrieve device number to create water level data
            # device_number = device_number_analysis()
            # #-----------Device Number Retrieval Ends---------



            # get_tank_id_query =("SELECT tank_id, tank_type FROM tbl_tank_details where device_id = '%s'" %(device_number))
            # get_tank_id_data = Query.get_a_record(get_tank_id_query)
            # print("Tank id is: ")
            # print(get_tank_id_data)
            # tank_id_from_db = get_tank_id_data[0]
            # print(tank_id_from_db) 

            # #print("Tank TYPE is: ")
            # tank_type_from_db = get_tank_id_data[1]
            # #print(tank_type_from_db) 

            # #### If tank type  is Cylindrical
            # if(tank_type_from_db == "cylindrical"):
            #     get_height_query = ("SELECT tank_height FROM tbl_tank_cylindrical where tank_id = '%s'" %(tank_id_from_db))
            #     print("Cylindrical HEIGHT is -------> ")
            #     get_height_arr = Query.get_a_record(get_height_query)
            #     get_height = get_height_arr[0]
            #     print(get_height)
            #     #print(type(get_height))

            # #### If tank type  is Cubicle
            # if(tank_type_from_db == "cubicle"):
            #     get_height_query = ("SELECT tank_height FROM tbl_tank_cubicle where tank_id = '%s'" %(tank_id_from_db))
            #     print("Cubicl HEIGHT is -------> ")
            #     get_height_arr = Query.get_a_record(get_height_query)
            #     get_height = get_height_arr[0]
            #     print(get_height)


            #  #############################################################################
            # #---------------------Create Device Data--------------
            # def device_data_analysis(get_height):

            #     str_client_data = ''
            #     for x in hex_client_data[6:10]:
            #         str_client_data +=x

            #     print("Level Data in hex ", str_client_data)

            #     decimal_device_data = int(str_client_data, 16)
            #     print("decimal_device_data in float ", decimal_device_data)

            #     #device_data = 0.0000

            #     print("Height in Data analysis function-->", get_height)

            #     device_data = (decimal_device_data/1000.0)
            #     print(device_data)
            #     #print("Water Level Data after divide by 1000 ->", device_data)

            #     print("Water level is in before calculation---->>", device_data)

            #     # Pass received data stream as an argument of function device_data_process
            #     #device_data = get_height(device_number, device_data_div)
            #     print("############Calculate water percentage")
            #     device_data = float(device_data)
            #     get_height = float(get_height)
            #     water_level = ((((device_data*0.78)/0.961)/get_height)*100.0)
            #     water_level = int(water_level)
            #     print("FINAL WATER PERCENTAGE (DATA PROCESSING)---- > ")
            #     print(water_level)

            #     print("Water level is in Device Data analysis after calculation ---->>", device_data)


            #     return device_data
            # #---------------------Create Device Data---------------
            # #############################################################################

            # ##################################################################################3


         

            #############################################################################
            # Required to get current date & time
            # To maintain device offline/online status
            def date_time():
                #------------Get Date Time Begins----------------
                current_time = datetime.now()

                # Split current time beased on a space to get date & time separately
                current_time = str(current_time).split( )

                # Date portion
                date = current_time[0]

                # Time portion
                time = current_time[1]

                # Exclude millisecond portion
                time = current_time[1].split('.')

                # Final time portion
                time = time[0]

                # Current date & time
                # String format
                dateTime = str(date) + ' ' + str(time)
                # print ("Current Time Stamp: %s" %dateTime)

                # Return current date time
                return dateTime
                #-----------Get Date Time Ends------------------
             #############################################################################
            # #----------------------------------Dry---------------------------------------


            #############################################################################
            # Keeps track of water level data for a specific device
            # In Json format
            def create_data(time_stamp, equipment_id,latitude, longitude, direction, speed ,bat_power):

                # print ("Create Data")
                #------------------------Create Json Data Begins-----------------------------

                # Json data including
                # Device number
                # Data data
                # DateTime
                # In an OrderedDict, the order in which the items are inserted is remembered and used when creating an iterator
                single_record = collections.OrderedDict()
                #single_record['Device'] = device_number
                single_record['datetimee'] = time_stamp
                single_record['equipment_id'] = equipment_id
                single_record['latitude'] = latitude
                single_record['longitude'] = longitude
                single_record['direction'] = direction
                single_record['speed'] = speed
                single_record['bat_power'] = bat_power

                # Convert python dictionary to json string
                json_data = json.dumps(single_record)
                #------------------------Create Json Data Ends-------------------------------

                #------------------------Add Json Data to Queue Begins-----------------------
                # Add Json data to water level data 
                self.data_queue.put(json_data)
                #------------------------Add Json Data to Queue Ends-------------------------
            #############################################################################
            #----------------------------------Dry---------------------------------------

            # #############################################################################
            # Check if water level data file exist for a specific device
            def data_file_exist(device_number, date_time):

                if (self.data_queue.empty() == False):

                    #------------------------Create Read & Write Source Begins-------------------
                    date_time = date_time
                    print("current date ----- > ", str(date_time))
                    date = datetime.strptime(date_time, '%Y-%m-%d %H:%M:%S')
                    year = date.year
                    print("Year --> ", year)
                    month = date.month
                    date = date.date
                    print("Date --> ", month)
                    print("Month --> ", str(date))

                    #-----Create Folder -> GPS_DATA/named Device Number----------
                    
                    if(os.path.exists("GPS_DATA")):
                        print("Folder Exist!")
                        pass
                    else:
                        os.mkdir("GPS_DATA")

                    #-----Create Folder -> GRAPH DATA/named Device Number----------

                    #-----Create Folder -> GPS_DATA/named Device Number----------
                    
                    if(os.path.exists("GPS_DATA/" + str(year))):
                        print("Folder Exist!")
                        pass
                    else:
                        os.mkdir("GPS_DATA/" + str(year))

                    #-----Create Folder -> GRAPH DATA/named Device Number----------



                    #-----Create Folder -> named YEARLY DATA/Device Number----------

                    if(os.path.exists("GPS_DATA/" +str(year) + "/" + str(month))):
                        #print("DEVICE  ------->> Folder Exist!")
                        pass
                    else:
                        os.mkdir("GPS_DATA/" +str(year) + "/" + str(month))
                        print("DEVICE  ------->> Folder CREATE!")

                    #------Create Folder -> named YEARLY DATA/Device Number----------

                    #------Create Sub-Folder -> named YEARLY DATA/device_number/year----------

                    if(os.path.exists("GPS_DATA/" +str(year) + "/" + str(month) + "/" +str(time_stamp.split(' ')[0].split('-')[2]))):
                        # print("YEAR  ------->> Folder Exist!")
                        pass
                    else:
                        os.mkdir("GPS_DATA/" +str(year) + "/" + str(month) + "/" +str(time_stamp.split(' ')[0].split('-')[2]))
                        #print("YEAR  ------->> Folder CREATE!")

                    #------Create Sub-Folder -> named YEARLY DATA/device_number/year---------


                    read_source_all =  "GPS_DATA/" +str(year) + "/" + str(month) + "/" +str(time_stamp.split(' ')[0].split('-')[2]) + "/" + "%s.txt" %equipment_id 
                    #read_source_hour = "GRAPH DATA/%s/last_one_hour.txt" %device_number
                    #read_source_day = "GRAPH DATA/%s/last_one_day.txt" %device_number
                    #read_source_week = "GRAPH DATA/%s/last_one_week.txt" %device_number
                    #read_source_month = "GRAPH DATA/%s/last_one_month.txt" %device_number
                    #read_source_year = "YEARLY DATA/%s/%s/%s.txt" %(device_number, year, month)
                    
                    #------------------------Create Read & Write Source Ends---------------------

                    #------------------------Writing Data from data_queue to file Begins---------
                    # Check if a specific file mentioned in write source exists or not

                    cnt = 0

                    while not self.data_queue.empty():

                        data = self.data_queue.get() 
                        print("Data from queue")
                        print(data)
                        #print(type(data))

                        #--------------------------All DATA-----------------------------------      
                        my_file = Path(read_source_all)
                        # Check if file mentioned in write source is existing or not
                        # If file exists then overwrite on that file
                        if my_file.is_file():
                            file = open(read_source_all,"a")
                        # If file does not exist
                        # Then create a file with existing json data in data queue
                        else:
                            file = open(read_source_all,"a+")

                        file.write(data + "\n")
                        num_lines = sum(1 for line in open(read_source_all))
                        #print(num_lines)
                        #--------------------------All DATA------------------------------------
                        


                         # #--------------------------YEARLY  DATA------------------------------------
                         # #---------------------------last_one_hour------------------------------

                         # my_file = Path(read_source_hour)
                         # # Check if file mentioned in write source is existing or not
                         # # If file exists then overwrite on that file
                         # if my_file.is_file():
                         #     file1 = open(read_source_hour,"a")
                         # # If file does not exist
                         # # Then create a file with existing json data in data queue
                         # else:
                         #     file1 = open(read_source_hour,"a+")
                        
                         # #number of line in file
                         # num_lines = sum(1 for line in open(read_source_hour))
                         # #print("Hour line---->")
                         # #print(num_lines)
                         # if(num_lines<=4):
                            
                         #     #if no data in file, write first data
                         #     if(num_lines==0):
                         #         file1.write(data + "\n")
                            
                         #     #check last line
                         #     #time diff from last data to 
                         #     #current data should be 15 minutes
                         #     # 15min = 900sec
                         #     else:
                         #         f1 = open (read_source_hour,"r" )
                         #         lineList = f1.readlines()
                         #         #print()
                         #         file_data = lineList[-1]
                         #         #print(file_data)

                         #         dictionary = json.loads(file_data)
                         #         #print("json loaded!")

                         #         #print("dictionary-->", dictionary)

                         #         Device_Data = ''
                         #         last_time = ''

                         #         for key,value in dictionary.items():

                         #             # Get device data
                         #             if key == 'Data':
                         #                 Device_Data = value
                         #                 #print(Device_Data)
                         #             # Get water levelstatus time stamp
                         #             if key == 'Time Stamp':
                         #                 last_time = value
                         #                 #print(last_time)

                         #         #print("Get time from last line-->", last_time)
                         #         current_time = date_time
                         #         #print("Current time: -->", current_time)

                         #         d1 = str(last_time)
                         #         d2 = str(current_time)

                         #         date1 = datetime.datetime.strptime(d1, '%Y-%m-%d %H:%M:%S')
                         #         date2 = datetime.datetime.strptime(d2, '%Y-%m-%d %H:%M:%S')
                         #         timedelta = date2 - date1
                         #         time_sec = timedelta.days * 24 * 3600 + timedelta.seconds
                         #         #print("Time in second:")
                         #         #print(time_sec)

                         #         if(time_sec>900):
                                    

                         #             if(num_lines==4):
                         #                 f1 = open (read_source_hour,"r" )
                         #                 lineList = f1.readlines()
                         #                 f1 = open(read_source_hour, 'w' )
                         #                 #print("------------------------")
                         #                 #print(lineList[1:])
                         #                 #print("------------------------")
                         #                 f1.write( ''.join( lineList[1:] ) )
                         #                 f1.close()
                         #                 #print("Delete one!!")
                         #                 file1.write(data + "\n")
                         #                 #print("write one!")
                         #             else:
                         #                 file1.write(data + "\n")

                         # #-------------------------last_one_hour------------------------
                        
                        
                         # #--------------------------last_one_day-----------------------


                         # my_file = Path(read_source_day)
                         # if my_file.is_file():
                         #     file2 = open(read_source_day,"a")
                         # else:
                         #     file2 = open(read_source_day,"a+")


                         # #number of line in file
                         # num_lines = sum(1 for line in open(read_source_day))
                         # #print(num_lines)
                         # if(num_lines<=16):

                         #     #if no data in file, write first data
                         #     if(num_lines==0):
                         #         file2.write(data + "\n")
                            
                         #     #check last line
                         #     #time diff from last data to 
                         #     #current data should be 1.5 hour
                         #     # 1.5 hour = (90*60) = 5400sec
                         #     else:

                         #         f2 = open (read_source_day,"r" )
                         #         lineList = f2.readlines()
                         #         #print()
                         #         file_data = lineList[-1]
                         #         #print(file_data)

                         #         dictionary = json.loads(file_data)
                         #         #print("json loaded!")

                         #         #print("dictionary-->", dictionary)

                         #         Device_Data = ''
                         #         last_time = ''

                         #         for key,value in dictionary.items():

                         #             # Get device data
                         #             if key == 'Data':
                         #                 Device_Data = value
                         #                 #print(Device_Data)
                         #             # Get water levelstatus time stamp
                         #             if key == 'Time Stamp':
                         #                 last_time = value
                         #                 #print(last_time)

                         #         #print("Get time from last line-->", last_time)
                         #         current_time = date_time
                         #         #print("Current time: -->", current_time)

                         #         d1 = str(last_time)
                         #         d2 = str(current_time)

                         #         date1 = datetime.datetime.strptime(d1, '%Y-%m-%d %H:%M:%S')
                         #         date2 = datetime.datetime.strptime(d2, '%Y-%m-%d %H:%M:%S')
                         #         timedelta = date2 - date1
                         #         time_sec = timedelta.days * 24 * 3600 + timedelta.seconds
                         #         #print("Time in second:")
                         #         #print(time_sec)

                         #         #5400
                         #         if(time_sec>5400):
                                    

                         #             if(num_lines==16):
                         #                 f2 = open (read_source_day,"r" )
                         #                 lineList = f2.readlines()
                         #                 f2 = open(read_source_day, 'w' )
                         #                 #print("------------------------")
                         #                 #print(lineList[1:])
                         #                 #print("------------------------")
                         #                 f2.write( ''.join( lineList[1:] ) )
                         #                 f2.close()
                         #                 #print("Delete one!!")
                         #                 file2.write(data + "\n")
                         #                 #print("write one!")
                         #             else:
                         #                 file2.write(data + "\n")




                         # #--------------------------last_one_day-----------------------

                        
                         # #--------------------------last_one_week-----------------------

                         # my_file = Path(read_source_week)
                         # if my_file.is_file():
                         #     file3 = open(read_source_week,"a")
                         # else:
                         #     file3 = open(read_source_week,"a+")


                         # num_lines = sum(1 for line in open(read_source_week))
                         # #print(num_lines)
                         # if(num_lines<=14):

                         #     if(num_lines==0):
                         #         file3.write(data + "\n")


                         #     #check last line
                         #     #data 12am, 12pm
                         #     else:
                         #         f3 = open (read_source_week,"r" )
                         #         lineList = f3.readlines()
                         #         #print()
                         #         file_data = lineList[-1]
                         #         #print(file_data)

                         #         dictionary = json.loads(file_data)

                         #         Device_Data = ''
                         #         last_time = ''

                         #         for key,value in dictionary.items():

                         #             # Get device data
                         #             if key == 'Data':
                         #                 Device_Data = value
                         #                 #print(Device_Data)
                         #             # Get water levelstatus time stamp
                         #             if key == 'Time Stamp':
                         #                 last_time = value
                         #                 #print(last_time)

                         #         #print("Get time from last line-->", last_time)

                         #         current_time = date_time

                         #         #print("Current time: -->", current_time)

                         #         date = datetime.datetime.strptime(last_time, '%Y-%m-%d %H:%M:%S')
                         #         last_only_date = datetime.datetime.strftime(date, '%Y-%m-%d')
                         #         last_only_time = datetime.datetime.strftime(date, '%H:%M:%S')

                         #         date = datetime.datetime.strptime(current_time, '%Y-%m-%d %H:%M:%S')
                         #         current_only_date = datetime.datetime.strftime(date, '%Y-%m-%d')
                         #         current_only_time =  datetime.datetime.strftime(date, '%H:%M:%S')
                         #         #print("current only time --> ", current_only_time)

                         #         check_date = "2000-01-01 12:00:00"
                         #         check_date = datetime.datetime.strptime(check_date, '%Y-%m-%d %H:%M:%S')
                         #         check_time = datetime.datetime.strftime(check_date, '%H:%M:%S')
                         #         #print("check_time is", check_time)

                         #         if(current_only_date>last_only_date):

                         #             if(num_lines==14):
                         #                 f3 = open (read_source_day,"r" )
                         #                 lineList = f2.readlines()
                         #                 f3 = open(read_source_day, 'w' )
                         #                 #print("------------------------")
                         #                 #print(lineList[1:])
                         #                 #print("------------------------")
                         #                 f3.write( ''.join( lineList[1:] ) )
                         #                 f3.close()
                         #                 #print("Delete one!!")
                         #                 file3.write(data + "\n")
                         #                 #print("write one!")
                         #             else:
                         #                 #print("Current date is large")
                         #                 file3.write(data + "\n")
                         #                 cnt = 1

                         #         if(current_only_date==last_only_date and cnt==1 and last_only_time<check_time and current_only_time>=check_time):
                         #             if(num_lines==14):
                         #                 f3 = open (read_source_day,"r" )
                         #                 lineList = f2.readlines()
                         #                 f3 = open(read_source_day, 'w' )
                         #                 #print("------------------------")
                         #                 #print(lineList[1:])
                         #                 #print("------------------------")
                         #                 f3.write( ''.join( lineList[1:] ) )
                         #                 f3.close()
                         #                 #print("Delete one!!")
                         #                 file3.write(data + "\n")
                         #                 #print("write one!")
                         #             else:
                         #                 #print("Equal! and cnt 1")
                         #                 file3.write(data + "\n")
                         #                 cnt = 2

                         #         if(current_only_date==last_only_date and cnt==0 and last_only_time<check_time and current_only_time>=check_time):
                         #             if(num_lines==14):
                         #                 f3 = open (read_source_day,"r" )
                         #                 lineList = f2.readlines()
                         #                 f3 = open(read_source_day, 'w' )
                         #                 #print("------------------------")
                         #                 #print(lineList[1:])
                         #                 #print("------------------------")
                         #                 f3.write( ''.join( lineList[1:] ) )
                         #                 f3.close()
                         #                 #print("Delete one!!")
                         #                 file3.write(data + "\n")
                         #                 #print("write one!")
                         #             else:
                         #                 file3.write(data + "\n")
                         #                 #print("Equal! and cnt 0")
                         #                 cnt = 1




                         # #--------------------------last_one_week-----------------------

                        
                         # #--------------------------last_one_month-----------------------
                         # my_file = Path(read_source_month)
                         # if my_file.is_file():
                         #     file4 = open(read_source_month,"a")
                         # else:
                         #     file4 = open(read_source_month,"a+")


                         # num_lines = sum(1 for line in open(read_source_month))
                         # #print(num_lines)
                         # if(num_lines<=30):

                         #     if(num_lines==0):
                         #         file4.write(data + "\n")

                         #     #check last line
                         #     #data 12am, total 30 data
                         #     else:
                         #         f4 = open (read_source_month,"r" )
                         #         lineList = f4.readlines()
                         #         #print()
                         #         file_data = lineList[-1]
                         #         #print(file_data)

                         #         dictionary = json.loads(file_data)

                         #         Device_Data = ''
                         #         last_time = ''

                         #         for key,value in dictionary.items():

                         #             # Get device data
                         #             if key == 'Data':
                         #                 Device_Data = value
                         #                 #print(Device_Data)
                         #             # Get water levelstatus time stamp
                         #             if key == 'Time Stamp':
                         #                 last_time = value
                         #                 #print(last_time)

                         #         #print("Get time from last line-->", last_time)

                         #         current_time = date_time

                         #         #print("Current time: -->", current_time)

                         #         date = datetime.datetime.strptime(last_time, '%Y-%m-%d %H:%M:%S')
                         #         last_only_date = datetime.datetime.strftime(date, '%Y-%m-%d')
                         #         #print("last only date ", last_only_date)

                         #         date = datetime.datetime.strptime(current_time, '%Y-%m-%d %H:%M:%S')
                         #         current_only_date = datetime.datetime.strftime(date, '%Y-%m-%d')
                         #         #print("current ", current_only_date)


                         #         if(current_only_date>last_only_date):
                         #             if(num_lines==30):
                         #                 f4 = open (read_source_day,"r" )
                         #                 lineList = f4.readlines()
                         #                 f4 = open(read_source_day, 'w' )
                         #                 #print("------------------------")
                         #                 #print(lineList[1:])
                         #                 #print("------------------------")
                         #                 f4.write( ''.join( lineList[1:] ) )
                         #                 f4.close()
                         #                 #print("Delete one!!")
                         #                 file4.write(data + "\n")
                         #                 #print("write one!")
                         #             else:
                         #                 #print("Current date is large")
                         #                 file4.write(data + "\n")



                         # #--------------------------last_one_month-----------------------

                         # #--------------------------GRAPH  DATA------------------------------------



                         # #--------------------------YEARLY  DATA------------------------------------
                        
                         # my_file = Path(read_source_year)
                         # #print("-------------------MY FILE---------------------------")
                         # #print(read_source_year)
                         # #print("-------------------MY FILE---------------------------")
                         # # Check if file mentioned in write source is existing or not
                         # # If file exists then overwrite on that file
                         # if my_file.is_file():
                         #     file5 = open(read_source_year,"a")
                         # # If file does not exist
                         # # Then create a file with existing json data in data queue
                         # else:
                         #     file5 = open(read_source_year,"a+")

                         # num_lines = sum(1 for line in open(read_source_year))

                         # #print(num_lines)

                         # if(num_lines<=30):

                         #     if(num_lines==0):
                         #         file5.write(data + "\n")


                         #     #check last line
                         #     #data 12am, total 30 data
                         #     else:
                         #         f5 = open (read_source_year,"r" )
                         #         lineList = f5.readlines()
                         #         #print()
                         #         file_data = lineList[-1]
                         #         #print(file_data)

                         #         dictionary = json.loads(file_data)

                         #         Device_Data = ''
                         #         last_time = ''

                         #         for key,value in dictionary.items():

                         #             # Get device data
                         #             if key == 'Data':
                         #                 Device_Data = value
                         #                 #print(Device_Data)
                         #             # Get water levelstatus time stamp
                         #             if key == 'Time Stamp':
                         #                 last_time = value
                         #                 #print(last_time)

                         #         #print("Get time from last line-->", last_time)

                         #         current_time = date_time

                         #         #print("Current time: -->", current_time)

                         #         date = datetime.datetime.strptime(last_time, '%Y-%m-%d %H:%M:%S')
                         #         last_only_date = datetime.datetime.strftime(date, '%Y-%m-%d')
                         #         #print("last only date ", last_only_date)

                         #         date = datetime.datetime.strptime(current_time, '%Y-%m-%d %H:%M:%S')
                         #         current_only_date = datetime.datetime.strftime(date, '%Y-%m-%d')
                         #         #print("current ", current_only_date)


                         #         if(current_only_date>last_only_date):
                         #             if(num_lines==30):
                         #                 f5 = open (read_source_year,"r" )
                         #                 lineList = f5.readlines()
                         #                 f5 = open(read_source_year, 'w' )
                         #                 #print("------------------------")
                         #                 #print(lineList[1:])
                         #                 #print("------------------------")
                         #                 f5.write( ''.join( lineList[1:] ) )
                         #                 f5.close()
                         #                 #print("Delete one!!")
                         #                 file5.write(data + "\n")
                         #                 #print("write one!")
                         #             else:
                         #                 #print("Current date is large")
                         #                 file5.write(data + "\n")

                         # #--------------------------YEARLY DATA------------------------------------

                     #file1.close()
                     # file2.close()
                     # file3.close()
                     # file4.close()
                     # file5.close()


            # #############################################################################
            # # Check if water level data file exist for a specific device
            # def data_file_exist(device_number, date_time):

            #     if (self.data_queue.empty() == False):

            #         #------------------------Create Read & Write Source Begins-------------------
            #         #date_time = date_time
            #         #print("current date ----- > ", date_time)
            #         date = datetime.datetime.strptime(date_time, '%Y-%m-%d %H:%M:%S')
            #         year = date.year
            #         #print("Year --> ", year)
            #         month = date.month
            #         #print("Month --> ", month)


            #         #-----Create Folder -> GRAPH DATA/named Device Number----------
                    
            #         if(os.path.exists(("GRAPH DATA/%s" %device_number))):
            #             #print("Folder Exist!")
            #             pass
            #         else:
            #             os.mkdir("GRAPH DATA/%s" %device_number)

            #         #-----Create Folder -> GRAPH DATA/named Device Number----------



            #         #-----Create Folder -> named YEARLY DATA/Device Number----------

            #         if(os.path.exists("YEARLY DATA/%s" %(device_number))):
            #             #print("DEVICE  ------->> Folder Exist!")
            #             pass
            #         else:
            #             os.mkdir("YEARLY DATA/%s" %(device_number))
            #             #print("DEVICE  ------->> Folder CREATE!")

            #         #------Create Folder -> named YEARLY DATA/Device Number----------

            #         #------Create Sub-Folder -> named YEARLY DATA/device_number/year----------

            #         if(os.path.exists("YEARLY DATA/%s/%s" %(device_number, year))):
            #            # print("YEAR  ------->> Folder Exist!")
            #             pass
            #         else:
            #             os.mkdir("YEARLY DATA/%s/%s" %(device_number, year))
            #             #print("YEAR  ------->> Folder CREATE!")

            #         #------Create Sub-Folder -> named YEARLY DATA/device_number/year---------


            #         read_source_all =  "ALL DATA/%s.txt" %device_number 
            #         read_source_hour = "GRAPH DATA/%s/last_one_hour.txt" %device_number
            #         read_source_day = "GRAPH DATA/%s/last_one_day.txt" %device_number
            #         read_source_week = "GRAPH DATA/%s/last_one_week.txt" %device_number
            #         read_source_month = "GRAPH DATA/%s/last_one_month.txt" %device_number
            #         read_source_year = "YEARLY DATA/%s/%s/%s.txt" %(device_number, year, month)
                    
            #         #------------------------Create Read & Write Source Ends---------------------

            #         #------------------------Writing Data from data_queue to file Begins---------
            #         # Check if a specific file mentioned in write source exists or not

            #         cnt = 0

            #         while not self.data_queue.empty():

            #             data = self.data_queue.get() 
            #             print("Data from queue")
            #             print(data)
            #             #print(type(data))

            #             #--------------------------All DATA-----------------------------------      
            #             my_file = Path(read_source_all)
            #             # Check if file mentioned in write source is existing or not
            #             # If file exists then overwrite on that file
            #             if my_file.is_file():
            #                 file = open(read_source_all,"a")
            #             # If file does not exist
            #             # Then create a file with existing json data in data queue
            #             else:
            #                 file = open(read_source_all,"a+")

            #             file.write(data + "\n")
            #             num_lines = sum(1 for line in open(read_source_all))
            #             #print(num_lines)
            #             #--------------------------All DATA------------------------------------
                        


            #             #--------------------------YEARLY  DATA------------------------------------
            #             #---------------------------last_one_hour------------------------------

            #             my_file = Path(read_source_hour)
            #             # Check if file mentioned in write source is existing or not
            #             # If file exists then overwrite on that file
            #             if my_file.is_file():
            #                 file1 = open(read_source_hour,"a")
            #             # If file does not exist
            #             # Then create a file with existing json data in data queue
            #             else:
            #                 file1 = open(read_source_hour,"a+")
                        
            #             #number of line in file
            #             num_lines = sum(1 for line in open(read_source_hour))
            #             #print("Hour line---->")
            #             #print(num_lines)
            #             if(num_lines<=4):
                            
            #                 #if no data in file, write first data
            #                 if(num_lines==0):
            #                     file1.write(data + "\n")
                            
            #                 #check last line
            #                 #time diff from last data to 
            #                 #current data should be 15 minutes
            #                 # 15min = 900sec
            #                 else:
            #                     f1 = open (read_source_hour,"r" )
            #                     lineList = f1.readlines()
            #                     #print()
            #                     file_data = lineList[-1]
            #                     #print(file_data)

            #                     dictionary = json.loads(file_data)
            #                     #print("json loaded!")

            #                     #print("dictionary-->", dictionary)

            #                     Device_Data = ''
            #                     last_time = ''

            #                     for key,value in dictionary.items():

            #                         # Get device data
            #                         if key == 'Data':
            #                             Device_Data = value
            #                             #print(Device_Data)
            #                         # Get water levelstatus time stamp
            #                         if key == 'Time Stamp':
            #                             last_time = value
            #                             #print(last_time)

            #                     #print("Get time from last line-->", last_time)
            #                     current_time = date_time
            #                     #print("Current time: -->", current_time)

            #                     d1 = str(last_time)
            #                     d2 = str(current_time)

            #                     date1 = datetime.datetime.strptime(d1, '%Y-%m-%d %H:%M:%S')
            #                     date2 = datetime.datetime.strptime(d2, '%Y-%m-%d %H:%M:%S')
            #                     timedelta = date2 - date1
            #                     time_sec = timedelta.days * 24 * 3600 + timedelta.seconds
            #                     #print("Time in second:")
            #                     #print(time_sec)

            #                     if(time_sec>900):
                                    

            #                         if(num_lines==4):
            #                             f1 = open (read_source_hour,"r" )
            #                             lineList = f1.readlines()
            #                             f1 = open(read_source_hour, 'w' )
            #                             #print("------------------------")
            #                             #print(lineList[1:])
            #                             #print("------------------------")
            #                             f1.write( ''.join( lineList[1:] ) )
            #                             f1.close()
            #                             #print("Delete one!!")
            #                             file1.write(data + "\n")
            #                             #print("write one!")
            #                         else:
            #                             file1.write(data + "\n")

            #             #-------------------------last_one_hour------------------------
                        
                        
            #             #--------------------------last_one_day-----------------------


            #             my_file = Path(read_source_day)
            #             if my_file.is_file():
            #                 file2 = open(read_source_day,"a")
            #             else:
            #                 file2 = open(read_source_day,"a+")


            #             #number of line in file
            #             num_lines = sum(1 for line in open(read_source_day))
            #             #print(num_lines)
            #             if(num_lines<=16):

            #                 #if no data in file, write first data
            #                 if(num_lines==0):
            #                     file2.write(data + "\n")
                            
            #                 #check last line
            #                 #time diff from last data to 
            #                 #current data should be 1.5 hour
            #                 # 1.5 hour = (90*60) = 5400sec
            #                 else:

            #                     f2 = open (read_source_day,"r" )
            #                     lineList = f2.readlines()
            #                     #print()
            #                     file_data = lineList[-1]
            #                     #print(file_data)

            #                     dictionary = json.loads(file_data)
            #                     #print("json loaded!")

            #                     #print("dictionary-->", dictionary)

            #                     Device_Data = ''
            #                     last_time = ''

            #                     for key,value in dictionary.items():

            #                         # Get device data
            #                         if key == 'Data':
            #                             Device_Data = value
            #                             #print(Device_Data)
            #                         # Get water levelstatus time stamp
            #                         if key == 'Time Stamp':
            #                             last_time = value
            #                             #print(last_time)

            #                     #print("Get time from last line-->", last_time)
            #                     current_time = date_time
            #                     #print("Current time: -->", current_time)

            #                     d1 = str(last_time)
            #                     d2 = str(current_time)

            #                     date1 = datetime.datetime.strptime(d1, '%Y-%m-%d %H:%M:%S')
            #                     date2 = datetime.datetime.strptime(d2, '%Y-%m-%d %H:%M:%S')
            #                     timedelta = date2 - date1
            #                     time_sec = timedelta.days * 24 * 3600 + timedelta.seconds
            #                     #print("Time in second:")
            #                     #print(time_sec)

            #                     #5400
            #                     if(time_sec>5400):
                                    

            #                         if(num_lines==16):
            #                             f2 = open (read_source_day,"r" )
            #                             lineList = f2.readlines()
            #                             f2 = open(read_source_day, 'w' )
            #                             #print("------------------------")
            #                             #print(lineList[1:])
            #                             #print("------------------------")
            #                             f2.write( ''.join( lineList[1:] ) )
            #                             f2.close()
            #                             #print("Delete one!!")
            #                             file2.write(data + "\n")
            #                             #print("write one!")
            #                         else:
            #                             file2.write(data + "\n")




            #             #--------------------------last_one_day-----------------------

                        
            #             #--------------------------last_one_week-----------------------

            #             my_file = Path(read_source_week)
            #             if my_file.is_file():
            #                 file3 = open(read_source_week,"a")
            #             else:
            #                 file3 = open(read_source_week,"a+")


            #             num_lines = sum(1 for line in open(read_source_week))
            #             #print(num_lines)
            #             if(num_lines<=14):

            #                 if(num_lines==0):
            #                     file3.write(data + "\n")


            #                 #check last line
            #                 #data 12am, 12pm
            #                 else:
            #                     f3 = open (read_source_week,"r" )
            #                     lineList = f3.readlines()
            #                     #print()
            #                     file_data = lineList[-1]
            #                     #print(file_data)

            #                     dictionary = json.loads(file_data)

            #                     Device_Data = ''
            #                     last_time = ''

            #                     for key,value in dictionary.items():

            #                         # Get device data
            #                         if key == 'Data':
            #                             Device_Data = value
            #                             #print(Device_Data)
            #                         # Get water levelstatus time stamp
            #                         if key == 'Time Stamp':
            #                             last_time = value
            #                             #print(last_time)

            #                     #print("Get time from last line-->", last_time)

            #                     current_time = date_time

            #                     #print("Current time: -->", current_time)

            #                     date = datetime.datetime.strptime(last_time, '%Y-%m-%d %H:%M:%S')
            #                     last_only_date = datetime.datetime.strftime(date, '%Y-%m-%d')
            #                     last_only_time = datetime.datetime.strftime(date, '%H:%M:%S')

            #                     date = datetime.datetime.strptime(current_time, '%Y-%m-%d %H:%M:%S')
            #                     current_only_date = datetime.datetime.strftime(date, '%Y-%m-%d')
            #                     current_only_time =  datetime.datetime.strftime(date, '%H:%M:%S')
            #                     #print("current only time --> ", current_only_time)

            #                     check_date = "2000-01-01 12:00:00"
            #                     check_date = datetime.datetime.strptime(check_date, '%Y-%m-%d %H:%M:%S')
            #                     check_time = datetime.datetime.strftime(check_date, '%H:%M:%S')
            #                     #print("check_time is", check_time)

            #                     if(current_only_date>last_only_date):

            #                         if(num_lines==14):
            #                             f3 = open (read_source_day,"r" )
            #                             lineList = f2.readlines()
            #                             f3 = open(read_source_day, 'w' )
            #                             #print("------------------------")
            #                             #print(lineList[1:])
            #                             #print("------------------------")
            #                             f3.write( ''.join( lineList[1:] ) )
            #                             f3.close()
            #                             #print("Delete one!!")
            #                             file3.write(data + "\n")
            #                             #print("write one!")
            #                         else:
            #                             #print("Current date is large")
            #                             file3.write(data + "\n")
            #                             cnt = 1

            #                     if(current_only_date==last_only_date and cnt==1 and last_only_time<check_time and current_only_time>=check_time):
            #                         if(num_lines==14):
            #                             f3 = open (read_source_day,"r" )
            #                             lineList = f2.readlines()
            #                             f3 = open(read_source_day, 'w' )
            #                             #print("------------------------")
            #                             #print(lineList[1:])
            #                             #print("------------------------")
            #                             f3.write( ''.join( lineList[1:] ) )
            #                             f3.close()
            #                             #print("Delete one!!")
            #                             file3.write(data + "\n")
            #                             #print("write one!")
            #                         else:
            #                             #print("Equal! and cnt 1")
            #                             file3.write(data + "\n")
            #                             cnt = 2

            #                     if(current_only_date==last_only_date and cnt==0 and last_only_time<check_time and current_only_time>=check_time):
            #                         if(num_lines==14):
            #                             f3 = open (read_source_day,"r" )
            #                             lineList = f2.readlines()
            #                             f3 = open(read_source_day, 'w' )
            #                             #print("------------------------")
            #                             #print(lineList[1:])
            #                             #print("------------------------")
            #                             f3.write( ''.join( lineList[1:] ) )
            #                             f3.close()
            #                             #print("Delete one!!")
            #                             file3.write(data + "\n")
            #                             #print("write one!")
            #                         else:
            #                             file3.write(data + "\n")
            #                             #print("Equal! and cnt 0")
            #                             cnt = 1




            #             #--------------------------last_one_week-----------------------

                        
            #             #--------------------------last_one_month-----------------------
            #             my_file = Path(read_source_month)
            #             if my_file.is_file():
            #                 file4 = open(read_source_month,"a")
            #             else:
            #                 file4 = open(read_source_month,"a+")


            #             num_lines = sum(1 for line in open(read_source_month))
            #             #print(num_lines)
            #             if(num_lines<=30):

            #                 if(num_lines==0):
            #                     file4.write(data + "\n")

            #                 #check last line
            #                 #data 12am, total 30 data
            #                 else:
            #                     f4 = open (read_source_month,"r" )
            #                     lineList = f4.readlines()
            #                     #print()
            #                     file_data = lineList[-1]
            #                     #print(file_data)

            #                     dictionary = json.loads(file_data)

            #                     Device_Data = ''
            #                     last_time = ''

            #                     for key,value in dictionary.items():

            #                         # Get device data
            #                         if key == 'Data':
            #                             Device_Data = value
            #                             #print(Device_Data)
            #                         # Get water levelstatus time stamp
            #                         if key == 'Time Stamp':
            #                             last_time = value
            #                             #print(last_time)

            #                     #print("Get time from last line-->", last_time)

            #                     current_time = date_time

            #                     #print("Current time: -->", current_time)

            #                     date = datetime.datetime.strptime(last_time, '%Y-%m-%d %H:%M:%S')
            #                     last_only_date = datetime.datetime.strftime(date, '%Y-%m-%d')
            #                     #print("last only date ", last_only_date)

            #                     date = datetime.datetime.strptime(current_time, '%Y-%m-%d %H:%M:%S')
            #                     current_only_date = datetime.datetime.strftime(date, '%Y-%m-%d')
            #                     #print("current ", current_only_date)


            #                     if(current_only_date>last_only_date):
            #                         if(num_lines==30):
            #                             f4 = open (read_source_day,"r" )
            #                             lineList = f4.readlines()
            #                             f4 = open(read_source_day, 'w' )
            #                             #print("------------------------")
            #                             #print(lineList[1:])
            #                             #print("------------------------")
            #                             f4.write( ''.join( lineList[1:] ) )
            #                             f4.close()
            #                             #print("Delete one!!")
            #                             file4.write(data + "\n")
            #                             #print("write one!")
            #                         else:
            #                             #print("Current date is large")
            #                             file4.write(data + "\n")



            #             #--------------------------last_one_month-----------------------

            #             #--------------------------GRAPH  DATA------------------------------------



            #             #--------------------------YEARLY  DATA------------------------------------
                        
            #             my_file = Path(read_source_year)
            #             #print("-------------------MY FILE---------------------------")
            #             #print(read_source_year)
            #             #print("-------------------MY FILE---------------------------")
            #             # Check if file mentioned in write source is existing or not
            #             # If file exists then overwrite on that file
            #             if my_file.is_file():
            #                 file5 = open(read_source_year,"a")
            #             # If file does not exist
            #             # Then create a file with existing json data in data queue
            #             else:
            #                 file5 = open(read_source_year,"a+")

            #             num_lines = sum(1 for line in open(read_source_year))

            #             #print(num_lines)

            #             if(num_lines<=30):

            #                 if(num_lines==0):
            #                     file5.write(data + "\n")


            #                 #check last line
            #                 #data 12am, total 30 data
            #                 else:
            #                     f5 = open (read_source_year,"r" )
            #                     lineList = f5.readlines()
            #                     #print()
            #                     file_data = lineList[-1]
            #                     #print(file_data)

            #                     dictionary = json.loads(file_data)

            #                     Device_Data = ''
            #                     last_time = ''

            #                     for key,value in dictionary.items():

            #                         # Get device data
            #                         if key == 'Data':
            #                             Device_Data = value
            #                             #print(Device_Data)
            #                         # Get water levelstatus time stamp
            #                         if key == 'Time Stamp':
            #                             last_time = value
            #                             #print(last_time)

            #                     #print("Get time from last line-->", last_time)

            #                     current_time = date_time

            #                     #print("Current time: -->", current_time)

            #                     date = datetime.datetime.strptime(last_time, '%Y-%m-%d %H:%M:%S')
            #                     last_only_date = datetime.datetime.strftime(date, '%Y-%m-%d')
            #                     #print("last only date ", last_only_date)

            #                     date = datetime.datetime.strptime(current_time, '%Y-%m-%d %H:%M:%S')
            #                     current_only_date = datetime.datetime.strftime(date, '%Y-%m-%d')
            #                     #print("current ", current_only_date)


            #                     if(current_only_date>last_only_date):
            #                         if(num_lines==30):
            #                             f5 = open (read_source_year,"r" )
            #                             lineList = f5.readlines()
            #                             f5 = open(read_source_year, 'w' )
            #                             #print("------------------------")
            #                             #print(lineList[1:])
            #                             #print("------------------------")
            #                             f5.write( ''.join( lineList[1:] ) )
            #                             f5.close()
            #                             #print("Delete one!!")
            #                             file5.write(data + "\n")
            #                             #print("write one!")
            #                         else:
            #                             #print("Current date is large")
            #                             file5.write(data + "\n")

            #             #--------------------------YEARLY DATA------------------------------------

            #         file1.close()
            #         file2.close()
            #         file3.close()
            #         file4.close()
            #         file5.close()


            # #############################################################################
            # #----------------------------------Dry---------------------------------------
            

            # #------------Get Date Time Begins---------------
            # # get current date & time
            date_time = date_time()
            datetimee = time_stamp
            if datetimee != ''  and equipment_id != '' and latitude != '' and direction != '' and speed != '' and bat_power != '':
                # #-----------Get Date Time Ends------------------

                # #-----------Device Number Retrieval Begins------

                # #-----------Level Data Retrieval Begins----------
                # device_data = device_data_analysis(get_height)
                # #-----------Level Data Retrieval Ends-----------

                # #-----------Json Data Processing Begins---------
                # # Device number, device data, current date time are passed to be processed as Json data
                print("==============>>>>>" + str(equipment_id))
                create_data(datetimee, equipment_id, latitude, longitude, direction, speed ,bat_power)
                # #-----------Json Data Processing Ends-----------

                # #-----------File Shifting Processing Begins-----
                # # Pass device number
                # # To check if a record exists for this device number
                # # Process on return type
                data_file_exist(equipment_id, date_time)
                # #-----------File Shifting Processing Ends-------

                # # Return feedback
                # # Indicating successful file creation
                # return 1

                # #############################################################################
                # #----------------------------------Dry---------------------------------------

        except Exception as e:
            print ("Caught exception socket.error : %s \n" % e)

            #-----Create Folder -> named Error Log----------

            if(os.path.exists("Error_Log/" )):
                #print("DEVICE  ------->> Folder Exist!")
                pass
            else:
                os.mkdir("Error_Log/" )
                print("DEVICE  ------->> Folder CREATE!")

            #------Create Folder -> named YEARLY DATA/Device Number----------

            filenew = open( "Error_Log/"+ str(time_stamp.split(' ')[0]) +".txt",'a+')#'error_gps.txt'
            filenew.write(str(time_stamp) + ":" +str(e) + " \n")
            filenew.close()

    #############################################################################
    #----------------------------------Dry---------------------------------------

    #############################################################################
    #----------------------------------Dry---------------------------------------


################################################################################


