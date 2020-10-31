# -*- coding: utf-8 -*-


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
username = "dma_emeter_0198"
password = "dma_emeter_0198"

# --- DB variables ---
host = 'dma-bd.com'
port = 3306
user = 'dmabdcom_gps987'
password = 'dmabd987'
db = 'dmabdcom_gpstracker'


# --- Generate a random string of fixed length ---
def randomString(stringLength=10):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))


# --- Lat Lon DB Update ---
def latlondbupdate(equipment_id, latitude_dec, longitude_dec, time_stamp, speed, course_direction_dec, bat_power):
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
                    sql3 = """UPDATE device_data SET dvd_latitude = %s, dvd_longitude = %s, updated_at = %s, dvd_speed = %s, dvd_bearing = %s, dvd_battery = %s WHERE dev_id = %s """
                    value3 = (str(latitude_dec), str(longitude_dec), str(time_stamp), str(speed), str(course_direction_dec), str(bat_power), str(data['dev_id']))
                    cursor.execute(sql3, value3)
                    if cursor.rowcount > 0:
                        conn.commit()
                        print("Data Updated successfully")
                else:
                    sql4 = """INSERT INTO device_data(dev_id, dvd_latitude, dvd_longitude, dvd_speed,created_at) VALUES (%s, %s, %s, %s, %s)"""
                    value4 = (data['dev_id'], latitude_dec, longitude_dec, speed, time_stamp)
                    cursor.execute(sql4, value4)
                    if cursor.rowcount > 0:
                        conn.commit()
                        print("DATA Inserted successfully")
    except Exception as e:
        print(e)
        cursor.close()


# --- Fuel Percent DB Update ---
def fueldbupdate(equipment_id, fuel_per):
    # --- db connection ---
    conn = pymysql.connect(host=host, user=user, password=password, db=db, cursorclass=pymysql.cursors.DictCursor)
    cursor = conn.cursor()
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
                    value5 = (fuel_litre)
                    cursor.execute(sql5, value5)
                    if cursor.rowcount > 0:
                        conn.commit()
                        print("DATA Inserted successfully")
    except Exception as e:
        print(e)
        cursor.close()


class Query(Database_GPS_Tracker.Query):
    pass


# --- Responsible for processing data ---
class Processing:
    Query.create_connection()
    # --- Responsible for creating a new object ---
    # --- Class: Processing ---
    # --- Responsible for initialzing instance variables ---
    # --- Self refers to newly created object ---
    # device_number = ''
    # device_data = ''
    # equipment_id = ''
    # datetimee = ''
    latitude = ''
    longitude = ''
    # direction = ''
    # speed = ''
    # bat_power = ''
    packet_length = ''
    device_type = ''

    # --- FIFO queue created to hold gps data ---]
    def __init__(self):
        self.data_queue = queue.Queue()

    # --- Store raw data function ---
    def store_raw_date(self, foldername, raw_data):
        if len(raw_data) > 0:
            florida = timezone('Asia/Dhaka')
            florida_time = datetime.now(florida)
            # time_stamp = florida_time.strftime('%Y-%m-%d %H:%M:%S')
            florida_time = datetime.now(florida)
            time_stamp = florida_time.strftime('%Y-%m-%d %H:%M:%S')
            curr_date = time_stamp.split(' ')[0]
            curr_time = str(time_stamp.split(' ')[1])

            # --- Create Read & Write Source ---
            date_time = time_stamp
            date = datetime.strptime(date_time, '%Y-%m-%d %H:%M:%S')
            year = date.year
            month = date.month
            date = date.date
            # --- Create Folder -> foldername ---
            if os.path.exists(foldername):
                pass
            else:
                os.mkdir(foldername)
            # --- Create Folder ->foldername/year ---
            if os.path.exists(foldername + "/" + str(year)):
                pass
            else:
                os.mkdir(foldername + "/" + str(year))
            # --- Create Folder -> named foldername/year/month ---
            if os.path.exists(foldername + "/" + str(year) + "/" + str(month)):
                pass
            else:
                os.mkdir(foldername + "/" + str(year) + "/" + str(month))
            read_source_all = foldername + "/" + str(year) + "/" + str(month) + "/" + str(time_stamp.split(' ')[0].split('-')[2]) + ".txt"

            # --- All DATA ---
            my_file = Path(read_source_all)
            # --- Check if file mentioned in write source is existing or not ---
            # --- If file exists then overwrite on that file ---
            if my_file.is_file():
                file = open(read_source_all, "a")
            # --- If file does not exist ---
            # --- Then create a file with existing json data in data queue ---
            else:
                file = open(read_source_all, "a+")
            file.write(str(time_stamp) + "\n" + raw_data + "\n")
            num_lines = sum(1 for line in open(read_source_all))

    # --- Device Data Process Starts ---
    def device_data_process(self, client_data, equipment_id):
        if len(client_data) > 0:
            print("---------Equipment ID------------->>>" + str(equipment_id))
            # print(str(client_data))
        packet_length = ''
        device_type = ''
        scale = 16
        # if equipment_id == '':
        # equipment_id = '0868003032433422'

        latitude = ''
        longitude = ''
        # get_height = ''

        # Try-catch block
        try:

            florida = timezone('Asia/Dhaka')
            florida_time = datetime.now(florida)
            # time_stamp = florida_time.strftime('%Y-%m-%d %H:%M:%S')
            florida_time = datetime.now(florida)
            time_stamp = florida_time.strftime('%Y-%m-%d %H:%M:%S')
            curr_date = time_stamp.split(' ')[0]
            curr_time = str(time_stamp.split(' ')[1])

            # -------------Find Day from Date------------------------
            # my_date = date.today()
            # day = calendar.day_name[my_date.weekday()]  #'Wednesday'
            # print("day is --->", day)
            # -------------Find Day from Date------------------------

            # Et300 Data Packet
            # client_data="78781f1213070a0e1b00c7028ccbc609b1c5f100554001d600522200276000032dcd0d0a"
            # client_data='78782112000000080000c7000000000000000000440001cc002622001330402c005fdbe60d0a'
            # client_data = "78782112130b0c0e3604c7028d068e09b1ea2c00154e01d6005222003c4f00000003fbed0d0a"
            # print(type(client_data))
            data_new = client_data

            # -------------------Location Data Decoding Starts--------------------------------

            if data_new[0:4] == "7878" and data_new[-4:].lower() == "0d0a" and data_new[6:8] == "12":
                device_type = 'ET300'
                # print("Location Data Message is from BW09 or ET-300")

                # ------------------Fuel Oil Calculation Starts---------------------------
                if data_new[4:6] == "21":
                    # print("Calculate Oil Percentage")
                    # When BYTE_1 Bit4 is 0 and if "BYTE_1 Bit5" is 0 then ADC value is for voltage,
                    # if "BYTE_1 Bit5" is 1 then ADC value is for
                    # Fuel Oil percentage. if "BYTE_1 Bit4" is 1 then ADC value is for temperature
                    # and BYTE_1 Bit1 is for +/- temperature.
                    # The server can judge the packet type based on these bits
                    fuel_per = ''
                    oil = data_new[50:54]
                    num_of_bits = 16
                    # print(bin(int(my_hexdata, scale))[2:].zfill(num_of_bits))
                    oil_bits = bin(int(oil, scale))[2:].zfill(num_of_bits)
                    # print(oil_bits)

                    byte_1 = oil_bits[0:8]
                    byte_1_bit_7 = byte_1[0]
                    byte_1_bit_6 = byte_1[1]
                    byte_1_bit_5 = byte_1[2]
                    byte_1_bit_4 = byte_1[3]
                    byte_1_bit_1 = byte_1[6]

                    ACC = 'OFF' if byte_1_bit_7 == '0' else 'ON'
                    input_2 = 'OFF' if byte_1_bit_6 == '0' else 'ON'

                    if byte_1_bit_4 == '0' and byte_1_bit_5 == '0':
                        # print("ADC value for voltage")
                        data = oil_bits[3:-3]
                        voltage = round(float(int(data, 2)) / 10, 1)
                    elif byte_1_bit_4 == '0' and byte_1_bit_5 == '1':
                        # print("ADC value for fuel oil percentage")
                        data = oil_bits[3:-3]
                        fuel_per = int(data, 2)
                        # print("Fuel Percent----->", fuel_per)
                    elif byte_1_bit_4 == '1':
                        # print("ADC Value for temperatue")
                        temp_sign = '-ve' if byte_1_bit_4 == '1' else '+ve'
                        data = oil_bits[3:-3]
                        temp = int(data, 2)
                        temp = '+' + \
                               str(temp) if temp_sign == '0' else '-' + str(temp)

                    # if byte_1[4] == '1':
                    #     print("TRUE")
                    if fuel_per == '':
                        fuel_per = '0'

                    fueldbupdate(equipment_id, fuel_per)

                # --------------------------------|||Fuel Oil Calculation|||-----------------------------------

                if data_new[4:6] != '':
                    packet_length = data_new[4:6]
                    # print("Packet Length" + str(packet_length))
                    pck = str(int(packet_length, 16))

                protocol_no = data_new[6:8]
                timedate = data_new[8:20]
                gps_information = data_new[20:22]
                # print(data_new[22:30])
                latitude = int(data_new[22:30], 16)
                lat = ((latitude / 30000) / 60)
                lat_n = math.floor(lat)
                lat_d = (lat - lat_n) * 60

                latitude_new = str(lat_n) + "°" + str(round(lat_d, 4))

                longitude = data_new[30:38]
                longitude = int(longitude, 16)
                lon = ((longitude / 30000) / 60)
                lon_n = math.floor(lon)
                lon_d = (lon - lon_n) * 60

                longitude_new = str(lon_n) + "°" + str(round(lon_d, 4))

                # print(len(client_data[4:-8]))
                from crccheck.crc import CrcX25
                data = bytearray.fromhex(client_data[4:-8])
                crc = hex(CrcX25.calc(data))

                # if crc[2:] == client_data[-8:-4]:
                #     print("Checksum is okay")
                #
                # if len(client_data) == 36 * 2:
                #     print('Old Package')
                # elif len(client_data) == 38 * 2:
                #     print('New Package')
                data_new = client_data

                # print("----------------------------")
                # print("Location Data Message is from ET-300")
                # print("----------------------------")
                start_bit = data_new[0:4]
                packet_length = data_new[4:6]

                protocol_no = data_new[6:8]
                timedate = data_new[8:20]
                gps_information = data_new[20:22]
                latitude = data_new[22:30]
                longitude = data_new[30:38]
                speed = data_new[38:40]

                course_status = data_new[40:44]
                mcc = data_new[44:48]
                mnc = data_new[48:50]

                cell_id = data_new[44:50]
                if len(data_new) == 38 * 2:
                    acc_adc = data_new[50:52]
                iserial_no = data_new[-12:-8]
                error_chk = data_new[-8:-4]
                stop_bit = data_new[-4:-1]

                # print("start_bit-" + start_bit)
                # print("packet_length-" + packet_length)
                # print("timedate-" +timedate)
                # if timedate != '':
                #     year = "20" + str(int(timedate[0:2], 16))
                #     month = str(int(timedate[2:4], 16))
                #     if len(month) < 2:
                #         month = "0" + month
                #     day = str(int(timedate[4:6], 16))
                #     if len(day) < 2:
                #         day = "0" + day
                #     hour = str(int(timedate[6:8], 16))
                #     if len(hour) < 2:
                #         hour = "0" + hour
                #     minute = str(int(timedate[8:10], 16))
                #     if len(minute) < 2:
                #         minute = "0" + minute
                #     second = str(int(timedate[10:12], 16))            
                #     if len(second) < 2:
                #         second = "0" + second
                #     timedate_fmt = year + "-" + month + "-" + day+ " " +hour + ":" +minute + ":" +second
                # else:
                timedate_fmt = time_stamp

                length_gps_info = str(int(gps_information[0:1], 16))
                no_pos_satellites = str(int(gps_information[1:2], 16))
                # latitude = '26B3F3E'
                latitude_dec = int(latitude, 16)
                latitude_dec = (float(latitude_dec) / 30000)
                latitude_dec = round(float(latitude_dec / 60), 6)
                # lat_int = int(latitude_dec)
                # lat_dec = (latitude_dec - lat_int)*60
                # lat_cov = str(lat_int) + "°" + str(round(lat_dec,4))

                longitude_dec = int(longitude, 16)
                longitude_dec = (float(longitude_dec) / 30000)
                longitude_dec = round(float(longitude_dec / 60), 6)
                # lon_int = int(longitude_dec)
                # lon_dec = (longitude_dec - lon_int)*60
                # lon_cov = str(lon_int) + "°" + str(round(lon_dec,4))

                speed = str(int(speed, 16))

                # print("-------------------------")
                # print(latitude_dec, longitude_dec)
                # print("-------------------------")

                course_status = data_new[40:44]
                course_bin = bin(int(course_status, 16))[2:].zfill(16)

                # -----------------------------------
                real_time_gps = course_bin[2:3]
                # if real_time_gps == 0:
                #     print("real_time_gps")
                # else:
                #     print("No real_time_gps")
                # ----------------------------------

                # ----------------------------------
                gps_position = course_bin[3:4]
                # if gps_position == 1:
                #     print("real_time_gps")
                # else:
                #     print("No real_time_gps")
                east_longitude = course_bin[4:5]
                north_latitude = course_bin[4:5]
                # ----------------------------------

                course_direction = course_bin[6:]
                course_direction_dec = int(course_bin[6:], 2)

                # ------------------------------
                mcc = data_new[44:48]
                # convert to decimal
                mcc_dec = int(mcc, 16)
                mcc_dec = "0" + str(mcc_dec)

                mnc = data_new[48:50]
                mnc_dec = int(mnc, 16)

                lac = data_new[50:54]
                # if data_new[44:50]:
                #     print("Cell id available")
                # else:
                #     print("Cell id not available")

                # --------------------------------------------
                cell_id = data_new[54:60]
                cell_id_dec = int(cell_id, 16)
                if len(data_new) == 38:
                    acc_adc = data_new[50:52]
                # ---------------------------------------------

                iserial_no = data_new[-12:-8]
                error_chk = data_new[-8:-4]
                stop_bit = data_new[-4:-1]

                timedate = time_stamp

                # DB Connection
                bat_power = 0

                latlondbupdate(equipment_id, latitude_dec, longitude_dec, time_stamp, speed, course_direction_dec,
                               bat_power)

                # ||||||||||||||||||||||||||||||||||||||||||||||||
                # ______________MQTT SENDING DATA____________
                # print("||||||||||||||||||||||||||||||||||||||||||||||||")
                cl_name = randomString()
                client = paho.Client(cl_name)
                # print("connecting to broker ", broker)
                client.connect(broker)  # connect
                client.loop_start()  # start loop to process received messages
                # print("publishing ")
                datetimee = time_stamp

                # message_all = {"time_date": "2019-10-31 16:11:24", "cell_id": "0868003032433422", "lat": "23.774352", "lon": "90.366212", "bearing": "15", "speed": "1", "battery": "65"}
                message_all = {'time_date': datetimee, 'cell_id': str(equipment_id), 'lat': str(latitude_dec),
                               'lon': str(longitude_dec), 'bearing': str(int(course_direction_dec)),
                               'speed': str(speed), 'battery': str(bat_power)}

                message_all = json.dumps(message_all)
                topic = "dma/gpstracker/" + str(equipment_id)

                # print(message_all)
                # print(topic)
                client_response1 = client.publish(topic, message_all)
                # print(client_response1)

            # -----------------------Location Data Stops--------------------------

            # -----------------------Alarm Data Starts----------------------------
            # data_new = '787825160B0B0F0E241DCF027AC8870C4657E60014020901CC00287D001F726506040101003656A40D0A'

            if data_new[0:4] == "7878" and data_new[-4:].lower() == "0d0a" and data_new[6:8] == "16":
                device_type = 'ET300'
                scale = 16
                # print("Alarm Data Message is from BW09 or ET-300")

                # ------------------Alarm Data Decode Starts-----------------------
                from crccheck.crc import CrcX25
                data_chk = data_new.split("0d0a")
                data = bytearray.fromhex(data_chk[-1])
                crc = hex(CrcX25.calc(data))
                error_chk = data_new[-8:-4]

                # if crc[2:] == error_chk.lower():
                #     print("Alarm Checksum is okay")
                # else:
                #     print("Error check failure!")

                start_bit = data_new[0:4]
                packet_length = data_new[4:6]

                protocol_no = data_new[6:8]
                timedate = data_new[8:20]
                gps_information = data_new[20:22]
                latitude = data_new[22:30]
                longitude = data_new[30:38]
                speed = data_new[38:40]

                course_status = data_new[40:44]
                lbs = data_new[44:46]
                mcc = data_new[46:50]
                mnc = data_new[50:52]
                lac = data_new[52:56]

                cell_id = data_new[56:62]

                # ------------------------------
                terminal_info = data_new[62:64]
                scale = 16  ## equals to hexadecimal
                num_of_bits = 8

                t_bin = bin(int(terminal_info, scale))[2:].zfill(num_of_bits)

                # if t_bin[0] == 1:
                #     print("oil and electricity disconnected")
                # elif t_bin[0] == 0:
                #     print("gas oil and electricity")
                #
                # if t_bin[1] == 1:
                #     print("GPS tracking is on")
                # elif t_bin[1] == 0:
                #     print("GPS tracking is off")
                # if t_bin[2:5] == '100':
                #     print("SOS")
                # elif t_bin[2:5] == '011':
                #     print("Low Battery Alarm")
                # elif t_bin[2:5] == '000':
                #     print("Norma")
                #
                # if t_bin[5:6] == 1:
                #     print("Chgarge on")
                # else:
                #     print("Charge Off")
                # if t_bin[6:7] == 1:
                #     print("ACC high")
                # else:
                #     print("ACC Low")
                # if t_bin[7] == 1:
                #     print("Air Condition ON")
                # else:
                #     print("AC Deactivated")

                # -------------------------------------

                # -------------------------------
                volt_level = data_new[64:66]
                # if volt_level == '00':
                #     print("No power")
                # elif volt_level == '01':
                #     print("Extremely low battery")
                # elif volt_level == '02':
                #     print("Very LowBattery")
                # elif volt_level == '03':
                #     print("Low Battery")
                # elif volt_level == '04':
                #     print("Medium")
                # elif volt_level == '05':
                #     print("High")
                # elif volt_level == '06':
                #     print("Very High")
                # -------------------------------

                # -------------------------------
                gsm_signal = data_new[66:68]
                # if gsm_signal == '00':
                #     print("No signal")
                # elif gsm_signal == '01':
                #     print("Extremely weak signal")
                # elif gsm_signal == '02':
                #     print("Very weak signal")
                # elif gsm_signal == '03':
                #     print("Good signal")
                # elif gsm_signal == '04':
                #     print("Strong signal")
                # -------------------------------

                # -------------------------------
                alarm = data_new[68:72]
                # if alarm[0:2] == '00':
                #     print("Normal(No Alarm)")
                # elif alarm[0:2] == '01':
                #     print("SOS")
                # elif alarm[0:2] == '02':
                #     print("Power Cut Alarm")
                # elif alarm[0:2] == '03':
                #     print("Shock Alarm")
                # elif alarm[0:2] == '04':
                #     print("Fence in Alarm")
                # elif alarm[0:2] == '05':
                #     print("Fence Out Alarm")
                # if alarm[2:4] == '01':
                #     language = "Chinese"
                #     print("Chinese")
                # elif alarm[2:4] == '02':
                #     language = "English"
                #     print("English")
                # -------------------------------

                iserial_no = data_new[-12:-8]
                error_chk = data_new[-8:-4]
                stop_bit = data_new[-4:]

                timedate_fmt = time_stamp

                length_gps_info = str(int(gps_information[0:1], 16))
                no_pos_satellites = str(int(gps_information[1:2], 16))
                # latitude = '26B3F3E'
                latitude_dec = int(latitude, 16)
                latitude_dec = (float(latitude_dec) / 30000)
                latitude_dec = round((latitude_dec / 60), 6)
                # lat_int = int(latitude_dec)
                # lat_dec = (latitude_dec - lat_int)*60
                # lat_cov = str(lat_int) + "°" + str(round(lat_dec,4))

                longitude_dec = int(longitude, 16)
                longitude_dec = (float(longitude_dec) / 30000)
                longitude_dec = round((longitude_dec / 60), 6)
                # lon_int = int(longitude_dec)
                # lon_dec = (longitude_dec - lon_int)*60
                # lon_cov = str(lon_int) + "°" + str(round(lon_dec,4))

                speed = str(int(speed, 16))

                # print("-------------------------")
                # print(latitude_dec, longitude_dec)
                # print("-------------------------")

                course_status = data_new[40:44]
                course_bin = bin(int(course_status, 16))[2:].zfill(16)
                real_time_gps = course_bin[2:3]
                # if real_time_gps == 0:
                #     print("real_time_gps")
                # else:
                #     print("No real_time_gps")
                gps_position = course_bin[3:4]
                # if gps_position == 1:
                #     print("real_time_gps")
                # else:
                #     print("No real_time_gps")
                east_longitude = course_bin[4:5]
                north_latitude = course_bin[4:5]

                course_direction = course_bin[6:]
                course_direction_dec = int(course_bin[6:], 2)

                # ------------------------------

                # ------------------------------
                mcc = data_new[44:48]
                # convert to decimal
                mcc_dec = int(mcc, 16)
                mcc_dec = "0" + str(mcc_dec)

                mnc = data_new[48:50]
                mnc_dec = int(mnc, 16)

                lac = data_new[50:54]
                # if data_new[44:50]:
                #     print("Cell id available")
                # else:
                #     print("Cell id not available")

                # ------------------
                cell_id = data_new[54:60]
                cell_id_dec = int(cell_id, 16)
                if len(data_new) == 38:
                    acc_adc = data_new[50:52]
                # ---------------------------------------------

                iserial_no = data_new[-12:-8]
                error_chk = data_new[-8:-4]
                stop_bit = data_new[-4:-1]
                timedate = time_stamp

                # ------------------Alarm Data Decode Stops-----------------------

                # -----------------DB Connection Starts---------------------------
                bat_power = 0
                conn = pymysql.connect(host=host, user=user, password=password, db=db,
                                       cursorclass=pymysql.cursors.DictCursor)
                cursor = conn.cursor()
                try:
                    sql1 = """SELECT dg.dev_id FROM devices_gateway as dg LEFT JOIN device_data as dd
                            ON dg.dev_id = dd.dev_id WHERE dg.dev_s_n=%s"""
                    value1 = str(equipment_id)
                    cursor.execute(sql1, value1)
                    # print("get existing data")

                    if (cursor.rowcount > 0):
                        data = cursor.fetchone()
                        if data != None:
                            sql2 = """SELECT dvd_id FROM device_data WHERE dev_id=%s"""
                            value2 = str(data['dev_id'])
                            cursor.execute(sql2, value2)
                            # print("get existing data's ID")

                            if (cursor.rowcount > 0):
                                sql3 = """UPDATE device_data SET dvd_latitude = %s, dvd_longitude = %s, updated_at = %s, dvd_speed = %s, dvd_bearing = %s, dvd_battery = %s WHERE dev_id = %s """
                                value3 = (str(latitude_dec), str(longitude_dec), str(time_stamp), str(speed),
                                          str(course_direction_dec), str(bat_power), str(data['dev_id']))
                                cursor.execute(sql3, value3)
                                # print("update existing data")

                                if (cursor.rowcount > 0):
                                    conn.commit()
                                    print("Data Updated successfully")
                            else:
                                sql4 = """INSERT INTO device_data(dev_id, dvd_latitude, dvd_longitude, dvd_speed,created_at)
                                            VALUES (%s, %s, %s, %s, %s)"""
                                value4 = (data['dev_id'], latitude_dec, longitude_dec, speed, time_stamp)
                                cursor.execute(sql4, value4)
                                # print("insert new data if no one exist")

                                if (cursor.rowcount > 0):
                                    conn.commit()
                                    print("DATA Inserted successfully")




                except Exception as e:
                    print(e)
                    cursor.close()
                    # -----------------DB Connection Stops---------------------------

                # ______________MQTT SENDING DATA STARTS____________
                # print("||||||||||||||||||||||||||||||||||||||||||||||||")
                client = paho.Client("dma_emeter_0198")
                # print("connecting to broker ", broker)
                client.connect(broker)  # connect
                client.loop_start()  # start loop to process received messages
                # print("publishing ")
                datetimee = time_stamp
                message_all = {'time_date': datetimee, 'cell_id': str(equipment_id), 'lat': str(latitude_dec),
                               'lon': str(longitude_dec), 'bearing': int(course_direction_dec), 'speed': str(speed),
                               'battery': str(bat_power)}
                # message_all = {'time_date':datetimee, 'cell_id':str(equipment_id), 'lat': latitude_new, 'lon' :longitude_new, 'bearing':  course_direction_dec, 'speed' : speed }
                message_all = json.dumps(message_all)
                topic = "dma/gpstracker/" + str(equipment_id)

                # print(message_all)
                # print(topic)
                client_response1 = client.publish(topic, message_all)
                # print(client_response1)
                # ______________MQTT SENDING DATA STOPS__________________

            # --------------------------Alarm Data Stops-------------------------------

            #############################################################################
            # Required to get current date & time
            # To maintain device offline/online status
            def date_time():
                # ------------Get Date Time Begins----------------
                current_time = datetime.now()

                # Split current time beased on a space to get date & time separately
                current_time = str(current_time).split()

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
                # -----------Get Date Time Ends------------------

            #############################################################################
            # #----------------------------------Dry---------------------------------------

            #############################################################################
            # Keeps track of water level data for a specific device
            # In Json format
            def create_data(time_stamp, equipment_id, latitude, longitude, direction, speed, bat_power):

                # print ("Create Data")
                # ------------------------Create Json Data Begins-----------------------------

                # Json data including
                # Device number
                # Data data
                # DateTime
                # In an OrderedDict, the order in which the items are inserted is remembered and used when creating an iterator
                single_record = collections.OrderedDict()
                # single_record['Device'] = device_number
                single_record['datetimee'] = time_stamp
                single_record['equipment_id'] = equipment_id
                single_record['latitude'] = latitude
                single_record['longitude'] = longitude
                single_record['direction'] = direction
                single_record['speed'] = speed
                single_record['bat_power'] = bat_power

                # Convert python dictionary to json string
                json_data = json.dumps(single_record)
                # ------------------------Create Json Data Ends-------------------------------

                # ------------------------Add Json Data to Queue Begins-----------------------
                # Add Json data to water level data 
                self.data_queue.put(json_data)
                # ------------------------Add Json Data to Queue Ends-------------------------

            #############################################################################
            # ----------------------------------Dry---------------------------------------

            # #############################################################################
            # Check if water level data file exist for a specific device
            def data_file_exist(device_number, date_time):

                if self.data_queue.empty() == False:

                    # ------------------------Create Read & Write Source Begins-------------------
                    date_time = date_time
                    # print("current date ----- > ", str(date_time))
                    date = datetime.strptime(date_time, '%Y-%m-%d %H:%M:%S')
                    year = date.year
                    # print("Year --> ", year)
                    month = date.month
                    date = date.date
                    # print("Date --> ", month)
                    # print("Month --> ", str(date))

                    # -----Create Folder -> GPS_DATA/named Device Number----------

                    if os.path.exists("GPS_DATA"):
                        # print("Folder Exist!")
                        pass
                    else:
                        os.mkdir("GPS_DATA")

                    # -----Create Folder -> GRAPH DATA/named Device Number----------

                    # -----Create Folder -> GPS_DATA/named Device Number----------

                    if os.path.exists("GPS_DATA/" + str(year)):
                        # print("Folder Exist!")
                        pass
                    else:
                        os.mkdir("GPS_DATA/" + str(year))

                    # -----Create Folder -> GRAPH DATA/named Device Number----------

                    # -----Create Folder -> named YEARLY DATA/Device Number----------

                    if os.path.exists("GPS_DATA/" + str(year) + "/" + str(month)):
                        # print("DEVICE  ------->> Folder Exist!")
                        pass
                    else:
                        os.mkdir("GPS_DATA/" + str(year) + "/" + str(month))
                        # print("DEVICE  ------->> Folder CREATE!")

                    # ------Create Folder -> named YEARLY DATA/Device Number----------

                    # ------Create Sub-Folder -> named YEARLY DATA/device_number/year----------

                    if (os.path.exists("GPS_DATA/" + str(year) + "/" + str(month) + "/" + str(
                            time_stamp.split(' ')[0].split('-')[2]))):
                        # print("YEAR  ------->> Folder Exist!")
                        pass
                    else:
                        os.mkdir("GPS_DATA/" + str(year) + "/" + str(month) + "/" + str(
                            time_stamp.split(' ')[0].split('-')[2]))
                        # print("YEAR  ------->> Folder CREATE!")

                    # ------Create Sub-Folder -> named YEARLY DATA/device_number/year---------

                    read_source_all = "GPS_DATA/" + str(year) + "/" + str(month) + "/" + str(
                        time_stamp.split(' ')[0].split('-')[2]) + "/" + "%s.txt" % equipment_id
                    # read_source_hour = "GRAPH DATA/%s/last_one_hour.txt" %device_number
                    # read_source_day = "GRAPH DATA/%s/last_one_day.txt" %device_number
                    # read_source_week = "GRAPH DATA/%s/last_one_week.txt" %device_number
                    # read_source_month = "GRAPH DATA/%s/last_one_month.txt" %device_number
                    # read_source_year = "YEARLY DATA/%s/%s/%s.txt" %(device_number, year, month)

                    # ------------------------Create Read & Write Source Ends---------------------

                    # ------------------------Writing Data from data_queue to file Begins---------
                    # Check if a specific file mentioned in write source exists or not

                    cnt = 0

                    while not self.data_queue.empty():

                        data = self.data_queue.get()
                        # print("Data from queue")
                        # print(data)
                        # print(type(data))

                        # --------------------------All DATA-----------------------------------
                        my_file = Path(read_source_all)
                        # Check if file mentioned in write source is existing or not
                        # If file exists then overwrite on that file
                        if my_file.is_file():
                            file = open(read_source_all, "a")
                        # If file does not exist
                        # Then create a file with existing json data in data queue
                        else:
                            file = open(read_source_all, "a+")

                        file.write(data + "\n")
                        num_lines = sum(1 for line in open(read_source_all))
                        # print(num_lines)
                        # --------------------------All DATA------------------------------------

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

                    # file1.close()
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
            if device_type == 'ET300':
                bat_power = 0
            if datetimee != '' and equipment_id != '' and latitude != '' and course_direction_dec != '' and speed != '' and bat_power != '':
                # #-----------Get Date Time Ends------------------

                # #-----------Device Number Retrieval Begins------

                # #-----------Level Data Retrieval Begins----------
                # device_data = device_data_analysis(get_height)
                # #-----------Level Data Retrieval Ends-----------

                # #-----------Json Data Processing Begins---------
                # # Device number, device data, current date time are passed to be processed as Json data
                # print("==============>>>>>" + str(equipment_id))
                create_data(datetimee, equipment_id, latitude_new, longitude_new, course_direction_dec, speed,
                            bat_power)
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

            print("Caught exception socket.error : %s \n" % e)

            # -----Create Folder -> named Error Log----------

            if os.path.exists("Error_Log/"):
                # print("DEVICE  ------->> Folder Exist!")
                pass
            else:
                os.mkdir("Error_Log/")
                # print("DEVICE  ------->> Folder CREATE!")

            # ------Create Folder -> named YEARLY DATA/Device Number----------

            filenew = open("Error_Log/" + str(time_stamp.split(' ')[0]) + ".txt", 'a+')  # 'error_gps.txt'
            filenew.write(str(time_stamp) + ":" + str(e) + " \n")
            filenew.close()

    #############################################################################
    # ----------------------------------Dry---------------------------------------

    #############################################################################
    # ----------------------------------Dry---------------------------------------

################################################################################
