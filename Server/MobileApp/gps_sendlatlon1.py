# -*- coding: utf-8 -*-
"""
Created on Sun Nov  3 12:17:59 2019

@author: DMA-REAL
"""

# -*- coding: utf-8 -*-

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
import time
from datetime import datetime, date
from pytz import timezone 
import paho.mqtt.client as paho
import json
import math
from datetime import datetime, timedelta, date
from pytz import timezone 
import calendar
import pymysql

broker   = "broker.hivemq.com"
username = "dma_emeter_0198"
password = "dma_emeter_0198"

host = 'dma-bd.com'
port = 3306
user = 'dmabdcom_gps987'
password = 'dmabd987'
db = 'dmabdcom_gpstracker'



while True:
    
    conn = pymysql.connect(host=host, user=user, password=password, db=db, cursorclass=pymysql.cursors.DictCursor)
    cursor = conn.cursor()
    try:
        sql1 = """SELECT upp.phn_business, ul.usr_id, ul.loc_long, ul.loc_lati,up.usr_name FROM `usr_location` as ul LEFT JOIN 
                    user_profile as up ON ul.usr_id = up.usr_id LEFT JOIN usr_phone as upp  ON ul.usr_id = upp.usr_id 
                    WHERE up.usr_account_type = '4' GROUP BY up.usr_id  ORDER BY ul.id DESC"""
        #value1 = str(equipment_id)
        cursor.execute(sql1)
        
        
        
    
        
        if(cursor.rowcount>0):
            datas = cursor.fetchall()
       
            florida = timezone('Asia/Dhaka')
            florida_time = datetime.now(florida)
            florida_time = datetime.now(florida)
            time_stamp = florida_time.strftime('%Y-%m-%d %H:%M:%S')
            curr_date = time_stamp.split(' ')[0]
            curr_time = str(time_stamp.split(' ')[1])
            datetimee = time_stamp
            
            for data in datas:
    
                usr_id = data['usr_id']
                lat_cov_new = data['loc_lati']
                lon_cov_new = data['loc_long']
                lat_cov_new = data['loc_lati']
                phn_business = data['phn_business']
                
                message_all = {'time_date':datetimee, 'usr_id': str(usr_id), 'lat': str(lat_cov_new), 'lon' :str(lon_cov_new)}
                
                message_all = json.dumps(message_all)
                topic = "dma/gps_tracker/" + str(phn_business)+"/" + str(usr_id)
     
    
                #print("------------------------------------------------------")
                client= paho.Client("real")
                print("connecting to broker ",client)
                client.connect(broker)#connect
                client.loop_start() #start loop to process received messages
                print("---------------------- ")
                datetimee = time_stamp
                print(message_all)
                print(topic)
                client_response1 = client.publish(topic,message_all)
                print(client_response1)   
                cursor.close() 
            
    
    except Exception as e:
        print (e)
                
    time.sleep(15)




