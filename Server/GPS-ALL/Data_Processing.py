import Database_GPS_Tracker
try:
    import queuedevice_data_process
except ImportError:
    import queue
import codecs  # For hex conversion
import collections  # For creating ordered dictionary
import datetime  # For current date time
import json  # For creating json data
import os
from pathlib import Path
import shutil  # For file processing
import sys
import threading  # For threading
from threading import Thread, current_thread  # For current thread
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
import random
import string

# --- MQTT Connection Variables ---
broker = "broker.hivemq.com"

# --- DB variables ---
# host = 'dma-bd.com'
# port = 3306
# user = 'dmabdcom_gps987'
# password = 'dmabd987'
# db = 'dmabdcom_gpstracker'

# --- DB variables ---
host = 'localhost'
port = 3306
user = 'root'
password = ''
db = 'dmabdcom_gpstracker'


# --- Generate a random string of fixed length ---
def randomString(stringLength=10):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))


# --- Lat Lon DB Update ---
def lat_lon_db_update(equipment_id, latitude, longitude, time_stamp, speed, course_direction_dec):
    # --- db connection ---
    conn = pymysql.connect(host=host, user=user, password=password, db=db, cursorclass=pymysql.cursors.DictCursor)
    cursor = conn.cursor()
    try:
        sql1 = """SELECT dg.dev_id FROM devices_gateway as dg LEFT JOIN device_data as dd ON dg.dev_id = dd.dev_id WHERE dg.dev_s_n=%s"""
        value1 = str(equipment_id)
        cursor.execute(sql1, value1)
        if cursor.rowcount > 0:
            data = cursor.fetchone()
            if data is not None:
                sql2 = """SELECT dvd_id FROM device_data WHERE dev_id=%s"""
                value2 = str(data['dev_id'])
                cursor.execute(sql2, value2)
                if cursor.rowcount > 0:
                    sql3 = """UPDATE device_data SET dvd_latitude = %s, dvd_longitude = %s, updated_at = %s, dvd_speed = %s, dvd_bearing = %s WHERE dev_id = %s """
                    value3 = (str(latitude), str(longitude), str(time_stamp), str(speed), str(course_direction_dec), str(data['dev_id']))
                    cursor.execute(sql3, value3)
                    if cursor.rowcount > 0:
                        conn.commit()
                        print("Data Updated successfully")
                else:
                    sql4 = """INSERT INTO device_data(dev_id, dvd_latitude, dvd_longitude, dvd_speed,created_at) VALUES (%s, %s, %s, %s, %s)"""
                    value4 = (data['dev_id'], latitude, longitude, speed, time_stamp)
                    cursor.execute(sql4, value4)
                    if cursor.rowcount > 0:
                        conn.commit()
                        print("DATA Inserted successfully")
    except Exception as e:
        print(e)
    cursor.close()


# --- Fuel Percent DB Update ---
def fuel_db_update(equipment_id, fuel_per):
    # --- db connection ---
    conn = pymysql.connect(host=host, user=user, password=password, db=db, cursorclass=pymysql.cursors.DictCursor)
    cursor = conn.cursor()
    fuel_litre = ""
    try:
        sql1 = """SELECT dg.dev_id FROM devices_gateway as dg LEFT JOIN device_data as dd ON dg.dev_id = dd.dev_id WHERE dg.dev_s_n=%s"""
        value1 = str(equipment_id)
        cursor.execute(sql1, value1)
        if cursor.rowcount > 0:
            data1 = cursor.fetchone()
            if data1 is not None:
                sql2 = """SELECT dvd_id FROM device_data WHERE dev_id=%s"""
                value2 = str(data1['dev_id'])
                cursor.execute(sql2, value2)
                if cursor.rowcount > 0:
                    sql3 = """SELECT pro_ft_vol FROM product_profile WHERE dev_id = %s """
                    value3 = (str(data1['dev_id']))
                    cursor.execute(sql3, value3)
                    if cursor.rowcount > 0:
                        data2 = cursor.fetchone()
                        if data2 is None:
                            fuel_litre = fuel_per
                        fuel_litre = int((float(fuel_per) / 100) * data2['pro_ft_vol'])
                        fuel_litre = str(fuel_litre) + ' L'
                        sql4 = """UPDATE device_data SET dvd_fuel_consumption = %s WHERE dev_id = %s """
                        value4 = (str(fuel_litre), data1['dev_id'])
                        cursor.execute(sql4, value4)
                        if cursor.rowcount > 0:
                            conn.commit()
                            print("Data Updated successfully")
                else:
                    sql5 = """INSERT INTO device_data(dvd_fuel_consumption) VALUES (%s)"""
                    value5 = fuel_litre
                    cursor.execute(sql5, value5)
                    if cursor.rowcount > 0:
                        conn.commit()
                        print("DATA Inserted successfully")
    except Exception as e:
        print(e)
        cursor.close()


# --- update device status if online or offline ---
def dev_online_status(equipment_id):
    # --- db connection ---
    conn = pymysql.connect(host=host, user=user, password=password, db=db, cursorclass=pymysql.cursors.DictCursor)
    cursor = conn.cursor()
    try:
        sql1 = """SELECT dg.dev_id FROM devices_gateway as dg LEFT JOIN device_data as dd ON dg.dev_id = dd.dev_id WHERE dg.dev_s_n=%s"""
        value1 = str(equipment_id)
        cursor.execute(sql1, value1)
    except Exception as e:
        print(e)
        cursor.close()


# --- dump from text file to DB every 10 minute ---
def text_to_database():
    print("text_to_database executed.")
    conn = pymysql.connect(host=host, user=user, password=password, db=db, cursorclass=pymysql.cursors.DictCursor)
    cursor = conn.cursor()
    try:
        file = open("GPS_DATA/demofile2.txt", "r")
        lines = file.readlines()
        for line in lines:
            # print(line)
            line_to_json = json.loads(line)
            sql = """INSERT INTO history_log (datetime, equipment_id, latitude, longitude, direction, speed, bat_power) VALUES (%s, %s, %s, %s, %s, %s, %s)"""
            val = (line_to_json['datetimee'], line_to_json['equipment_id'], line_to_json['latitude'], line_to_json['longitude'], line_to_json['direction'], line_to_json['speed'], line_to_json['bat_power'])
            cursor.execute(sql, val)

            conn.commit()
            # if cursor.rowcount > 0:
            #     conn.commit()
            #     print("DATA Inserted successfully")
        file.close()
        # file_erase = open("GPS_DATA/demofile2.txt", "w")
        # file_erase.truncate()
        # file_erase.close()
    except Exception as e:
        print(e)
        cursor.close()


# ticker = threading.Event()
# while not ticker.wait(30):
#     text_to_database()


# --- MQTT data publishing ---
def mqtt_publisher(message_all):
    cl_name = randomString()
    client = paho.Client(cl_name)
    # print("connecting to broker ", broker)
    client.connect(broker)
    # --- start loop to process received messages ---
    client.loop_start()
    message_all = json.dumps(message_all)
    topic = "dma/gpstracker/" + str(equipment_id)
    client.publish(topic, message_all)


class Query(Database_GPS_Tracker.Query):
    pass


# --- Responsible for processing data ---
class Processing:
    Query.create_connection()

    # --- FIFO queue created to hold gps data ---]
    def __init__(self):
        self.data_queue = queue.Queue()

    # --- Device Data Process Starts ---
    @staticmethod
    def device_data_process(client_data, equipment_id):
        print("---------Equipment ID--------->>>" + str(equipment_id))
        try:
            # --- get time & date ---
            florida = timezone('Asia/Dhaka')
            florida_time = datetime.now(florida)
            # time_stamp = florida_time.strftime('%Y-%m-%d %H:%M:%S')
            florida_time = datetime.now(florida)
            time_stamp = florida_time.strftime('%Y-%m-%d %H:%M:%S')
            curr_date = time_stamp.split(' ')[0]
            curr_time = str(time_stamp.split(' ')[1])

            # --- status information ---
            if client_data[4:6].lower() == "0a":
                print("status information")
                terminal_info = bin(int(client_data[8:10], 16))[2:].zfill(8)
                if terminal_info[0:1] == '0':
                    oil_electricity_connected = True
                else:
                    oil_electricity_connected = False
                if terminal_info[1:2] == '0':
                    gps_tracking_on = False
                else:
                    gps_tracking_on = True
                if terminal_info[5:6] == '0':
                    battery_charging = False
                else:
                    battery_charging = True
                if terminal_info[6:7] == '0':
                    acc = False
                else:
                    acc = True
                terminal_battery_info = int(client_data[8:10], 16)
                gsm_strength = int(client_data[8:10], 16)

                # --- data update to DB ---
                dev_online_status(equipment_id)

            # --- location data without ADC value ---
            if client_data[4:6].lower() == "1f":
                print("location data without fuel value")
                device_year = int(client_data[8:10], 16)
                device_month = int(client_data[10:12], 16)
                device_day = int(client_data[12:14], 16)
                device_hour = int(client_data[14:16], 16)
                device_minute = int(client_data[16:18], 16)
                device_second = int(client_data[18:20], 16)
                time_date = str(device_year) + "-" + str(device_month) + "-" + str(device_day) + " " + str(device_hour) + ":" + str(device_minute) + ":" + str(device_second)
                # print("date: ", str(device_year) + "-" + str(device_month) + "-" + str(device_day) + " " + str(device_hour) + ":" + str(device_minute) + ":" + str(device_second))
                latitude = int(client_data[22:30], 16)
                latitude = float(latitude) / 30000
                latitude = round(float(latitude / 60), 6)
                longitude = int(client_data[30:38], 16)
                longitude = float(longitude) / 30000
                longitude = round(float(longitude / 60), 6)
                print("lat: ", latitude, " lon: ", longitude)
                speed = int(client_data[38:40], 16)
                course_status = bin(int(client_data[40:44], 16))[2:].zfill(16)
                acc = course_status[0:1]
                input2 = course_status[1:2]
                real_time_gps = course_status[2:3]
                gps_positioning = course_status[3:4]
                east_or_west_longitude = course_status[4:5]
                south_or_north_longitude = course_status[5:6]
                course = int(course_status[6:].zfill(8), 2)
                mcc = int(client_data[44:48], 16)
                mnc = int(client_data[48:50], 16)
                lac = int(client_data[50:54], 16)
                cell_id = int(client_data[54:60], 16)

                # message_all = {"time_date": "2019-10-31 16:11:24", "cell_id": "0868003032433422", "lat": "23.774352", "lon": "90.366212", "bearing": "15", "speed": "1", "battery": "65"}
                message_all = {"time_date": time_date, 'cell_id': str(equipment_id), 'lat': str(latitude), 'lon': str(longitude), "bearing": course, 'speed': str(speed)}
                # --- publish to mqtt ---
                mqtt_publisher(message_all)

                # --- data update to DB if gps positioning is valid ---
                if gps_positioning == '1':
                    lat_lon_db_update(equipment_id, latitude, longitude, time_date, speed, course)

            # --- location data with ADC value ---
            if client_data[4:6].lower() == "21":
                print("location data with fuel value")
                device_year = int(client_data[8:10], 16)
                device_month = int(client_data[10:12], 16)
                device_day = int(client_data[12:14], 16)
                device_hour = int(client_data[14:16], 16)
                device_minute = int(client_data[16:18], 16)
                device_second = int(client_data[18:20], 16)
                time_date = str(device_year) + "-" + str(device_month) + "-" + str(device_day) + " " + str(device_hour) + ":" + str(device_minute) + ":" + str(device_second)
                # print("date: ", str(device_year) + "-" + str(device_month) + "-" + str(device_day) + " " + str(device_hour) + ":" + str(device_minute) + ":" + str(device_second))
                latitude = int(client_data[22:30], 16)
                latitude = (float(latitude) / 30000)
                latitude = round(float(latitude / 60), 6)
                longitude = int(client_data[30:38], 16)
                longitude = (float(longitude) / 30000)
                longitude = round(float(longitude / 60), 6)
                print("lat: ", latitude, " lon: ", longitude)
                speed = int(client_data[38:40], 16)
                course_status = bin(int(client_data[40:44], 16))[2:].zfill(16)
                acc = course_status[0:1]
                input2 = course_status[1:2]
                real_time_gps = course_status[2:3]
                gps_positioning = course_status[3:4]
                east_or_west_longitude = course_status[4:5]
                south_or_north_longitude = course_status[5:6]
                course = int(course_status[6:].zfill(8), 2)
                mcc = int(client_data[44:48], 16)
                mnc = int(client_data[48:50], 16)
                lac = int(client_data[50:54], 16)
                cell_id = int(client_data[54:60], 16)
                adc_data = bin(int(client_data[60:64], 16))[2:].zfill(16)
                # --- ADC value for voltage ---
                if adc_data[2:3] == "0":
                    adc_voltage = int(adc_data[6:].zfill(8), 2)
                    print("ADC voltage: ", adc_voltage)
                # --- ADC value for fuel percentage ---
                if adc_data[2:3] == "1":
                    adc_fuel_percent = int(adc_data[6:].zfill(8), 2)
                    print("ADC fuel percentage: ", adc_fuel_percent)
                # --- ADC value for temperature ---
                if adc_data[3:4] == "1":
                    adc_temperature = int(adc_data[6:].zfill(8), 2)
                    print("ADC temperature: ", adc_temperature)

                # message_all = {"time_date": "2019-10-31 16:11:24", "cell_id": "0868003032433422", "lat": "23.774352", "lon": "90.366212", "bearing": "15", "speed": "1", "battery": "65"}
                message_all = {"time_date": time_date, 'cell_id': str(equipment_id), 'lat': str(latitude), 'lon': str(longitude), "bearing": course, 'speed': str(speed)}
                # --- publish to mqtt ---
                mqtt_publisher(message_all)

                # --- data update to DB if gps positioning is valid ---
                if gps_positioning == '1':
                    lat_lon_db_update(equipment_id, latitude, longitude, time_date, speed, course)
                    fuel_db_update(equipment_id, adc_fuel_percent)

            # --- Alarm data Calculation ---
            if client_data[4:6].lower() == "25":
                device_year = int(client_data[8:10], 16)
                device_month = int(client_data[10:12], 16)
                device_day = int(client_data[12:14], 16)
                device_hour = int(client_data[14:16], 16)
                device_minute = int(client_data[16:18], 16)
                device_second = int(client_data[18:20], 16)
                time_date = str(device_year) + "-" + str(device_month) + "-" + str(device_day) + " " + str(device_hour) + ":" + str(device_minute) + ":" + str(device_second)
                # print("date: ", str(device_year) + "-" + str(device_month) + "-" + str(device_day) + " " + str(device_hour) + ":" + str(device_minute) + ":" + str(device_second))
                latitude = int(client_data[22:30], 16)
                latitude = (float(latitude) / 30000)
                latitude = round(float(latitude / 60), 6)
                longitude = int(client_data[30:38], 16)
                longitude = (float(longitude) / 30000)
                longitude = round(float(longitude / 60), 6)
                print("lat: ", latitude, " lon: ", longitude)
                speed = int(client_data[38:40], 16)
                course_status = bin(int(client_data[40:44], 16))[2:].zfill(16)
                acc = course_status[0:1]
                input2 = course_status[1:2]
                real_time_gps = course_status[2:3]
                gps_positioning = course_status[3:4]
                east_or_west_longitude = course_status[4:5]
                south_or_north_longitude = course_status[5:6]
                course = int(course_status[6:].zfill(8), 2)
                lbs_length = int(client_data[44:46], 16)
                mcc = int(client_data[46:50], 16)
                mnc = int(client_data[50:52], 16)
                lac = int(client_data[52:56], 16)
                cell_id = int(client_data[56:62], 16)
                terminal_info = bin(int(client_data[62:64], 16))[2:].zfill(8)
                if terminal_info[0:1] == '0':
                    oil_electricity_connected = True
                    print("oil electricity connected.")
                else:
                    oil_electricity_connected = False
                    print("oil electricity disconnected.")
                if terminal_info[1:2] == '0':
                    gps_tracking_on = False
                    print("gps tracking off.")
                else:
                    gps_tracking_on = True
                    print("gps tracking on.")
                if terminal_info[2:5] == '100':
                    sos_alarm = True
                    print("sos alarm")
                if terminal_info[2:5] == '011':
                    low_battery = True
                    print("low battery")
                if terminal_info[2:5] == '010':
                    power_cut = True
                    print("low battery")
                if terminal_info[2:5] == '001':
                    shock_alarm = True
                    print("shock alarm")
                if terminal_info[2:5] == '000':
                    no_alarm = True
                    print("no alarm")
                terminal_battery_info = int(client_data[64:66], 16)
                gsm_strength = int(client_data[66:68], 16)
                alarm = int(client_data[68:70], 16)
                language = int(client_data[70:72], 16)

        except Exception as e:
            print("Caught exception socket.error : %s \n" % e)
