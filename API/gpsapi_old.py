from flaskext.mysql import MySQL
from flask import Flask, request, make_response, Response
import pymysql
import datetime
import json
from flask import jsonify
from datetime import datetime, timedelta, date
import calendar
import math
import decimal
from pprint import pprint
from pytz import timezone
import os
import base64
from pytz import timezone
import datetime
from datetime import datetime, date
import hashlib

app = Flask(__name__)

host = 'localhost'
port = 3306
user = 'root'
password = ''
db = 'dmabdcom_gpstracker'


# host = 'dma-bd.com'
# port = 3306
# user = 'dmabdcom_alldb'
# password = 'dmabd987'
# db = 'dmabdcom_gpstracker'


@app.route('/', methods=['GET', 'POST'])
def hello():
    return "WELCOME TO 2020 GPS Tracker API"


###########################################################################################################
############################################GPS TRACKER####################################################
###########################################################################################################

# --------------------------------------- Dashboard start -------------------------------------------------
@app.route('/dashboard', methods=['POST'])
def dashboard():
    conn = pymysql.connect(host=host, user=user, password=password, db=db, cursorclass=pymysql.cursors.DictCursor)
    cursor = conn.cursor()
    try:
        # --- get current date ---
        # florida = timezone('Asia/Dhaka')
        # florida_time = datetime.now(florida)
        # time_stamp = florida_time.strftime('%Y-%m-%d %H:%M:%S')
        # print("Time is-->", time_stamp)
        # curr_date = time_stamp.split(' ')[0]
        # curr_time = str(time_stamp.split(' ')[1])

        # --- requests list for API call ---
        user_id = request.form['usr_email']

        if user_id != "":
            query = """SELECT dd.dev_id, pp.pro_id, pp.pro_name, dl.loc_lat, dl.loc_long, dg.dev_s_n FROM device_data as dd 
									LEFT JOIN product_profile as pp ON pp.dev_id=dd.dev_id  
									LEFT JOIN dev_location as dl ON dl.dev_id=dd.dev_id
									LEFT JOIN devices_gateway as dg ON dg.dev_id=dd.dev_id"""
            results = cursor.execute(query)
            # print(results)
            if cursor.rowcount > 0:
                conn.commit()
                results = cursor.fetchall()
                print(results)
                for result in results:
                    result['topic'] = 'dma/gpstracker/' + result['dev_s_n']
                    del result['dev_s_n']
                res = {"err": "false", "data": results}
                return jsonify(res)
            else:
                return jsonify({"err": "true", "data": "Wrong Parameters"})
    except Exception as e:
        print(e)
        return jsonify({"err": "true", "data": e})
    cursor.close()


# ------------------------------------- Dashboard end -----------------------------------------------------

# ----------------------------------- Registration start --------------------------------------------------
@app.route('/reg', methods=['POST'])
def usr_registration():
    conn = pymysql.connect(host=host, user=user, password=password, db=db, cursorclass=pymysql.cursors.DictCursor)
    cursor = conn.cursor()
    try:
        # --- get current date ---
        florida = timezone('Asia/Dhaka')
        florida_time = datetime.now(florida)
        time_stamp = florida_time.strftime('%Y-%m-%d %H:%M:%S')
        # print("Time is-->", time_stamp)
        curr_date = time_stamp.split(' ')[0]
        curr_time = str(time_stamp.split(' ')[1])

        # --- find Day from date ---
        # my_date = date.today()
        # day = calendar.day_name[my_date.weekday()]
        # print("day is --->", day)

        # --- requests list for API call ---
        usr_name_ = request.form['usr_name']
        usr_email_ = request.form['usr_email']
        usr_phone_ = request.form['usr_phone']
        usr_address_ = request.form['usr_address']
        usr_password_ = request.form['usr_password']
        usr_account_type_ = request.form['usr_account_type']
        app_id_ = request.form['app_id']
        # print(usr_name_, usr_email_, usr_phone_, usr_address_, usr_password_, usr_account_type_, app_id_)

        if usr_name_ != "" and usr_email_ != "" and usr_phone_ != "" and usr_address_ != "" and usr_password_ != "" and usr_account_type_ != "" and int(
                usr_account_type_) <= 2:
            usr_password_ = hashlib.md5(usr_password_.encode()).hexdigest()
            # print(usr_password_)
            # --- Check if any user exists with the same name and email ---
            sql = """SELECT * from user_profile WHERE usr_name=%s and usr_email=%s"""
            values = (usr_name_, usr_email_)
            cursor.execute(sql, values)
            if cursor.rowcount == 0:
                # --- If no user exists then register the user ---
                sql1 = """INSERT INTO user_profile(usr_name, usr_email, usr_phone, usr_address, usr_password, usr_account_type, app_id, usr_create_time, usr_create_date, usr_fcmtoken) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
                values1 = (
                    usr_name_, usr_email_, "1", "1", usr_password_, usr_account_type_, app_id_, curr_time, curr_date,
                    "")
                cursor.execute(sql1, values1)
                if cursor.rowcount > 0:
                    print("Registration data has been successfully inserted.")
                    # --- get the new user's id from DB ---
                    sql2 = """SELECT usr_id from user_profile WHERE usr_name=%s and usr_email=%s"""
                    values2 = (usr_name_, usr_email_)
                    cursor.execute(sql2, values2)
                    if cursor.rowcount > 0:
                        data1 = cursor.fetchone()
                        # --- Insert user's address ---
                        sql3 = """INSERT INTO usr_address(usr_id, add_village) VALUES (%s,%s)"""
                        values3 = (data1["usr_id"], usr_address_)
                        cursor.execute(sql3, values3)
                        if cursor.rowcount > 0:
                            conn.commit()
                            # --- Insert user's phone number ---
                            sql4 = """INSERT INTO usr_phone(usr_id, phn_business) VALUES (%s,%s)"""
                            values4 = (data1["usr_id"], usr_phone_)
                            cursor.execute(sql4, values4)
                            if cursor.rowcount > 0:
                                conn.commit()
                                return jsonify({"des": "Address and Phone insert Success", "err": "false"})
                            else:
                                return jsonify({"des": "Address and Phone insert Failure", "err": "true"})
                else:
                    return jsonify({"des": "Registration data insertion failed", "err": "true"})
            else:
                return jsonify({"des": "Duplicate entry", "err": "true"})
        else:
            return jsonify({"des": "Parameters empty!", "err": "true"})
    except Exception as e:
        print(e)


# ------------------------------------------ Registration end --------------------------------------------


# --------------------------------------------- Login start ----------------------------------------------
@app.route('/login', methods=['POST'])
def login():
    conn = pymysql.connect(host=host, user=user, password=password, db=db, cursorclass=pymysql.cursors.DictCursor)
    cursor = conn.cursor()
    try:
        # --- requests list for API call ---
        usr_email_ = request.form['usr_email']
        usr_password_ = request.form['usr_password']
        usr_fcmtoken_ = request.form['usr_fcmtoken']
        user_mail_status = False
        # print(usr_email_, usr_password_, usr_fcmtoken_)

        if usr_email_ != "" and usr_password_ != "":
            usr_password_ = hashlib.md5(usr_password_.encode()).hexdigest()
            # print(usr_password_)
            usr_name = usr_email_.split("@")
            # print(usr_name, len(usr_name), type(usr_name))
            if len(usr_name) > 1:
                if usr_name[1] == "hotmail.com" or usr_name[1] == "gmail.com" or usr_name[1] == "yahoo.com":
                    print("Valid Email address")
                    user_mail_status = True
                    print(user_mail_status)
            if user_mail_status:
                # --- get valid the user form DB with mail ---
                cursor.execute(
                    "SELECT usr_account_type, usr_email FROM user_profile WHERE usr_email=%s AND usr_password=%s",
                    (usr_email_, usr_password_))
            else:
                # --- get valid the user form DB with name ---
                cursor.execute(
                    "SELECT usr_account_type, usr_email FROM user_profile WHERE usr_name=%s AND usr_password=%s",
                    (usr_name, usr_password_))
            acc_type = cursor.fetchone()
            # print(acc_type)
            if acc_type is not None:
                acc_type = acc_type['usr_account_type']
                # print(acc_type)
                if acc_type is not None:
                    print(usr_fcmtoken_, usr_email_)
                    if user_mail_status:
                        # --- update fcmToken with mail ---
                        cursor.execute("UPDATE user_profile SET usr_fcmtoken = %s WHERE usr_email=%s",
                                       (usr_fcmtoken_, usr_email_))
                    else:
                        # --- update fcmToken with name ---
                        cursor.execute("UPDATE user_profile SET usr_fcmtoken = %s WHERE usr_name=%s",
                                       (usr_fcmtoken_, usr_email_))
                    conn.commit()
                    return jsonify({'err': 'false', 'des': 'success', "acc_type": acc_type})
                else:
                    return jsonify({'err': 'true', 'des': 'failure', "acc_type": ""})
            else:
                return jsonify({"des": "Wrong username or password!", "err": "true", "acc_type": ""})
        else:
            return jsonify({"des": "Parameters empty.", "err": "true", "acc_type": ""})
    except Exception as e:
        print(e)
        return jsonify({"des": "Parameters empty.", "err": "true", "acc_type": str(e)})
    cursor.close()


# --------------------------------------------- Login end ------------------------------------------------


# --------------------------------------- Device details start -------------------------------------------
@app.route('/devicedetails/<dev_type>', methods=['POST'])
@app.route('/devicedetails/<dev_type>/<dev_id>', methods=['POST'])
def devicedetails(dev_type=None, dev_id=None):
    print("device type: ", dev_type, ", device ID: ", dev_id, ", root url: ", request.url_root)

    conn = pymysql.connect(host=host, user=user, password=password, db=db)
    cursor = conn.cursor()

    # --- requests list for API call ---
    app_time = request.form['curr_time']

    if dev_id is None:
        if dev_type == 'all' and dev_id is None:
            try:
                # --- get Apps current time ---
                florida = timezone('Asia/Dhaka')
                florida_time = datetime.now(florida)
                time_stamp = florida_time.strftime('%Y-%m-%d %H:%M:%S')
                app_time = time_stamp

                if app_time != "":
                    # --- get all the product from "product_profile" table ---
                    product_sql = """SELECT pt.type_name, count(*) FROM product_profile as pp LEFT JOIN product_type as pt ON pp.type_id = pt.type_id GROUP BY pp.type_id"""
                    cursor.execute(product_sql)
                    if cursor.rowcount > 0:
                        products = cursor.fetchall()
                        # print("All products list: ", products)
                        dev_total = {}  # device total array
                        for product in products:
                            dev_total[product[0]] = product[1]
                            dev_total["status"] = "Total"
                        print("Total device details list: ", dev_total)
                        # --- count the total devices to show in admin apps/dashboard display ---
                        total_sql = "SELECT COUNT(*) FROM `product_profile`"
                        cursor.execute(total_sql)
                        if cursor.rowcount > 0:
                            dev_total_count = cursor.fetchone()[0]
                            print("total devices: ", dev_total_count)
                            # --- get all the device's that sent data less than 30 min ago ---
                            online_sql = """SELECT * FROM `device_data` WHERE TimeDiff(%s,updated_at) < '00:30:00'
                                            GROUP BY dev_id ORDER BY dev_id DESC"""
                            cursor.execute(online_sql, time_stamp)
                            if cursor.rowcount > 0:
                                # online_dev = cursor.rowcount  # cursor.fetchone()[0]
                                # --- get product type and id ---
                                dev_name_sql = "SELECT type_name,type_id FROM `product_type`"
                                cursor.execute(dev_name_sql)
                                dev_names = cursor.fetchall()

                                dev_online = {}  # device online array
                                dev_offline = {}  # device offline array
                                # --- loop through all product type with the id ---
                                for dev_name in dev_names:
                                    # print(dev_name[1], app_time) # output in console: ('Tractor', 1)
                                    # --- get which devices are online ---
                                    dev_online_sql = """SELECT COUNT(*) FROM `devices_gateway` as dg JOIN `product_profile` as pp ON dg.dev_id = pp.dev_id AND pp.type_id = '%s' JOIN device_data as dd ON pp.dev_id = dd.dev_id 
                                            WHERE TimeDiff(%s, dd.updated_at) < '00:30:00'"""
                                    cursor.execute(dev_online_sql, (dev_name[1], app_time))
                                    dev_online_count = cursor.fetchone()[0]  # assign counted number in dev_online_count
                                    dev_online[dev_name[0]] = str(dev_online_count)
                                    dev_online["status"] = "Online"
                                    # --- get which devices are offline ---
                                    dev_offline_sql = """SELECT COUNT(*) FROM `devices_gateway` as dg JOIN `product_profile` as pp ON dg.dev_id = pp.dev_id AND pp.type_id = '%s' JOIN device_data as dd ON pp.dev_id = dd.dev_id 
                                            WHERE TimeDiff(%s, dd.updated_at) > '00:30:00'"""
                                    cursor.execute(dev_offline_sql, (dev_name[1], app_time))
                                    dev_offline_count = cursor.fetchone()[
                                        0]  # assign counted number in dev_offline_count
                                    dev_offline[dev_name[0]] = str(dev_offline_count)
                                    dev_offline["status"] = "Offline"
                                print("Online device details list:", dev_online)
                                print("Offline device details list:", dev_offline)
                                return jsonify(
                                    {'err': 'false', 'des': 'success', 'data': [dev_total, dev_online, dev_offline]})
                            else:
                                ofl_arr = {}
                                tot_arr = {}
                                onl_arr = {}
                                for product in products:
                                    # print(product)
                                    ofl_arr[product[0]] = str(product[1])
                                    tot_arr[product[0]] = str(product[1])
                                    onl_arr[product[0]] = str(product[1])
                                print("---------NEWWW-----")
                                print(dev_total)
                                ofl = {}
                                tot = {}
                                print("--------------------")
                                ofl = dev_total
                                ofl_arr['status'] = "Offline"
                                print(ofl)
                                tot = dev_total
                                tot_arr['status'] = "Total"
                                print(tot)
                                onl = dev_total
                                print(tot)
                                onl_arr['status'] = "Online"
                                onl_arr['Diesel Generator'] = str(0)
                                onl_arr['Portable Generator'] = str(0)
                                onl_arr['Tractor'] = str(0)
                                # print(dev_total)
                                # print(onl, ofl, tot)
                                print(tot)
                                return jsonify({'err': 'false', 'des': 'success', 'data': [ofl_arr, tot_arr, onl_arr]})
                        else:
                            # print(products)
                            return jsonify({'err': 'true', 'des': 'failure', 'data': []})
            except Exception as e:
                print(e)
                return jsonify({'err': 'true', 'des': str(e)})
        # device details with the type parameter
        elif dev_type.lower() == "tractor" or dev_type.lower() == "porgen" or dev_type.lower() == "dieselgen" and dev_id == None:
            print(dev_type, dev_id)
            if dev_type == "porgen":
                dev_type = "Portable Generator"
                print(dev_type)
            elif dev_type == "dieselgen":
                dev_type = "Diesel Generator"
                print(dev_type)
            try:
                if app_time != "":
                    conn = pymysql.connect(host=host, user=user, password=password, db=db,
                                           cursorclass=pymysql.cursors.DictCursor)
                    cursor = conn.cursor()
                    # print(cursor)
                    product_sql = """SELECT pp.pro_name, pp.pro_id,up.usr_fname,up.usr_lname, dg.dev_s_n FROM product_profile as pp LEFT JOIN assign_info as ai 
                                   ON pp.pro_id = ai.pro_id LEFT JOIN user_profile as up ON ai.usr_id = up.usr_id
                                   LEFT JOIN devices_gateway as dg ON pp.dev_id = dg.dev_id
                                   LEFT JOIN product_type as pt ON pp.type_id=
                                   pt.type_id WHERE pt.type_name = '""" + dev_type + """'"""
                    cursor.execute(product_sql)
                    if cursor.rowcount > 0:
                        products = cursor.fetchall()
                        print(products)
                        for product in products:
                            product["name"] = product["usr_fname"] + " " + product["usr_lname"]
                            product["track_no"] = product["dev_s_n"]
                            del product["usr_fname"]
                            del product["usr_lname"]
                            del product["dev_s_n"]
                    return jsonify({'err': 'false', 'des': 'success', 'data': products})
            except Exception as e:
                print(e)
                return jsonify({'err': 'true', 'des': str(e)})
    elif id is not None:
        if dev_type.lower() == "tractor" or dev_type.lower() == "porgen" or dev_type.lower() == "dieselgen":
            print(dev_type)
            print(id)
            if dev_type == "porgen":
                dev_type = "Portable Generator"
                print(dev_type)
            elif dev_type == "dieselgen":
                dev_type = "Diesel Generator"
                print(dev_type)
            try:
                if app_time != "":
                    conn = pymysql.connect(host=host, user=user, password=password, db=db,
                                           cursorclass=pymysql.cursors.DictCursor)
                    cursor = conn.cursor()
                    # print(cursor)
                    product_sql2 = """SELECT pp.pro_name, pp.pro_id,up.usr_fname,up.usr_lname, dg.dev_s_n FROM product_profile as pp LEFT JOIN assign_info as ai 
                                   ON pp.pro_id = ai.pro_id LEFT JOIN user_profile as up ON ai.usr_id = up.usr_id
                                   LEFT JOIN devices_gateway as dg ON pp.dev_id = dg.dev_id
                                   LEFT JOIN product_type as pt ON pp.type_id=
                                   pt.type_id WHERE pt.type_name = '""" + dev_type + """' AND pp.pro_id ='""" + id + """'"""
                    print(product_sql2)
                    cursor.execute(product_sql2)
                    if cursor.rowcount > 0:
                        products = cursor.fetchall()
                        print(products)
                        for product in products:
                            product["name"] = product["usr_fname"] + " " + product["usr_lname"]
                            product["track_no"] = product["dev_s_n"]
                            del product["usr_fname"]
                            del product["usr_lname"]
                            del product["dev_s_n"]
                    return jsonify({'err': 'false', 'des': 'success', 'data': products})
            except Exception as e:
                print(e)
                return jsonify({'err': 'true', 'des': str(e)})
        cursor.close()


# --------------------------------------- Device details end ---------------------------------------------


# --------------------------------------- Device list start ----------------------------------------------
@app.route('/devicelist/<type>', methods=['POST'])
@app.route('/devicelist/<type>/<id>', methods=['POST'])
def devicelist(type=None, id=None):
    print("device type: ", type, ", device ID: ", id, ", root url: ", request.url_root)

    dhaka = timezone('Asia/Dhaka')
    dhaka_time = datetime.now(dhaka)

    conn = pymysql.connect(host=host, user=user, password=password, db=db, cursorclass=pymysql.cursors.DictCursor)
    cursor = conn.cursor()

    if id is None:
        if (type == 'all' and id is None) or (type is None and id is None):
            try:
                dev_sql = """SELECT dl.loc_lat, dl.loc_long, dl.loc_name, pt.type_name, ai.usr_id, up.usr_name, 
                            ua.add_village, pp.pro_id, dd.dvd_haulage, dg.dev_id, dd.dvd_start_hour, dd.dvd_end_hour, 
                            dd.dvd_mileages, dd.dvd_speed,dd.dvd_running_hour, dg.dev_name,dg.dev_model,dg.dev_s_n,
                            dd.dvd_latitude, dd.dvd_longitude, dd.updated_at, dd.dvd_fuel_consumption, 
                            dd.dvd_odometer_reading, pm.pmo_title FROM product_profile as pp 
                            LEFT JOIN device_data as dd ON pp.dev_id = dd.dev_id 
                            LEFT JOIN devices_gateway as dg ON dg.dev_id = pp.dev_id 
                            LEFT JOIN assign_info as ai ON ai.pro_id = pp.pro_id 
                            LEFT JOIN user_profile as up ON up.usr_id = ai.usr_id 
                            LEFT JOIN usr_address as ua ON ua.usr_id = ai.usr_id 
                            LEFT JOIN product_type as pt ON pt.type_id = pp.type_id 
                            LEFT JOIN dev_location as dl ON dl.dev_id = pp.dev_id 
                            LEFT JOIN product_model as pm ON pp.pmo_id = pm.pmo_id
                            WHERE ai.ass_type = '1'"""
                # print(dev_sql)dev_model
                data = cursor.execute(dev_sql)
                # print(data)
                if cursor.rowcount > 0:
                    datas = cursor.fetchall()
                    datalist = []
                    # print(datas)
                    for data in datas:
                        data['dev_model'] = data['pmo_title']
                        del data['pmo_title']
                        if data['dvd_speed'] is None:
                            data['dvd_speed'] = 0
                        data['dvd_speed'] = str(data['dvd_speed']) + ' km/h'
                        if data['dvd_haulage'] == 1:
                            data['Haulage status'] = '1'
                            data["cultivation status"] = '0'
                        else:
                            data['Haulage status'] = '0'
                            data["cultivation status"] = '1'
                        if data['updated_at'] is None:
                            # print('updated_at is none')
                            data['updated_at'] = dt = datetime(1970, 1, 1, 11)
                        if data['dvd_fuel_consumption'] is None:
                            data['dvd_fuel_consumption'] = 0
                        if data['dvd_mileages'] is None:
                            data['dvd_mileages'] = 0
                        if data['dvd_odometer_reading'] is None:
                            data['dvd_odometer_reading'] = 0
                        if data['dvd_running_hour'] is None:
                            data['dvd_running_hour'] = 0
                        if data['dvd_start_hour'] is None:
                            data['dvd_start_hour'] = '00:00'
                        data['dvd_odometer_reading'] = str(data['dvd_odometer_reading'])
                        data['notification'] = ''
                        data['usr_address'] = data['add_village']
                        data['dvd_latitude'] = data['loc_lat']
                        data['dvd_longitude'] = data['loc_long']
                        data['topic'] = "dma/gpstracker/" + data['dev_s_n']
                        data['dvd_start_hour'] = str(data['dvd_start_hour'])
                        data['dvd_end_hour'] = str(data['dvd_end_hour'])
                        data['dvd_running_hour'] = str(data['dvd_running_hour'])
                        data['dvd_mileages'] = str(data['dvd_mileages'])

                        curtime = dhaka.localize(data['updated_at'])
                        print(curtime)
                        # print(data['updated_at'])
                        # print(dhaka_time)
                        # print(type(data['updated_at']))
                        # print(type(curtime))
                        # print('-----------------------')

                        data['updated_at'] = str(data['updated_at'])
                        if dhaka_time - curtime > timedelta(minutes=30):
                            print('Greater')
                            print(data['updated_at'])
                            data['Status'] = 'Offline'
                            data['Engine Status'] = 'Offline'
                        else:
                            data['Status'] = 'Online'
                            data['Engine Status'] = 'Online'

                        del data['add_village']
                        del data['dvd_haulage']
                        datalist.append(data)
                    return jsonify({'error': 'false', 'datas': datalist, 'desc': 'success'})
                else:
                    datas = []
                    return jsonify({'error': 'true', 'datas': datas, 'desc': 'empty'})
            except Exception as e:
                print(e)
                return jsonify({'error': 'true', 'datas': str(e), 'desc': 'failure'})
        elif type == 'Tractor' and id is None:
            print(type)
            print(id)

            # if type == None and id == None or type==all and id ==None:

            try:

                dev_sql = """SELECT dl.loc_lat, dl.loc_long, dl.loc_name, pt.type_name, ai.usr_id, up.usr_name, ua.add_village, pp.pro_id, dd.dvd_haulage, dg.dev_id, dd.dvd_start_hour, dd.dvd_end_hour, dd.dvd_mileages, dd.dvd_speed,dd.dvd_running_hour,
                      dg.dev_name,dg.dev_model,dg.dev_s_n,dd.dvd_latitude, dd.dvd_longitude, dd.updated_at, dd.dvd_fuel_consumption, dd.dvd_odometer_reading
                      FROM product_profile as pp LEFT JOIN device_data as dd ON
                      pp.dev_id = dd.dev_id LEFT JOIN devices_gateway as dg ON
                      dg.dev_id = pp.dev_id LEFT JOIN assign_info as ai ON
                      ai.pro_id = pp.pro_id LEFT JOIN user_profile as up ON
                      up.usr_id = ai.usr_id LEFT JOIN usr_address as ua ON
                      ua.usr_id = ai.usr_id LEFT JOIN product_type as pt ON
                      pt.type_id = pp.type_id LEFT JOIN dev_location as dl ON
                      dl.dev_id = pp.dev_id LEFT JOIN product_model as pm ON pp.pmo_id = pm.pmo_id
                      WHERE ai.ass_type = '1' and pt.type_id = '1'"""
                # print(dev_sql)
                data = cursor.execute(dev_sql)
                # print(data)
                if cursor.rowcount > 0:
                    datas = cursor.fetchall()
                    # print(datas)
                    for data in datas:

                        if data['dvd_speed'] is None:
                            data['dvd_speed'] = 0
                        data['dvd_speed'] = str(data['dvd_speed']) + ' km/h'
                        if data['dvd_haulage'] == 1:
                            data['Haulage status'] = '1'
                            data["cultivation status"] = '0'
                        else:
                            data['Haulage status'] = '0'
                            data["cultivation status"] = '1'
                        if data['updated_at'] is None:
                            # print('updated_at is none')
                            data['updated_at'] = dt = datetime(1970, 1, 1, 11)

                        if data['dvd_fuel_consumption'] is None:
                            data['dvd_fuel_consumption'] = 0
                        if data['dvd_mileages'] is None:
                            data['dvd_mileages'] = 0
                        if data['dvd_odometer_reading'] is None:
                            data['dvd_odometer_reading'] = 0
                        if data['dvd_running_hour'] is None:
                            data['dvd_running_hour'] = 0
                        if data['dvd_start_hour'] is None:
                            data['dvd_start_hour'] = '00:00'
                        data['dvd_odometer_reading'] = str(data['dvd_odometer_reading'])
                        data['notification'] = ''
                        data['usr_address'] = data['add_village']
                        data['dvd_latitude'] = data['loc_lat']
                        data['dvd_longitude'] = data['loc_long']
                        data['topic'] = "dma/gpstracker/" + data['dev_s_n']
                        data['dvd_start_hour'] = str(data['dvd_start_hour'])
                        data['dvd_end_hour'] = str(data['dvd_end_hour'])
                        data['dvd_running_hour'] = str(data['dvd_running_hour'])
                        data['dvd_mileages'] = str(data['dvd_mileages'])

                        curtime = dhaka.localize(data['updated_at'])
                        print(curtime)
                        # print(data['updated_at'])
                        # print(dhaka_time)
                        # print(type(data['updated_at']))
                        # print(type(curtime))
                        # print('-----------------------')

                        data['updated_at'] = str(data['updated_at'])
                        if dhaka_time - curtime > timedelta(minutes=30):
                            print('Greater')
                            print(data['updated_at'])
                            data['Status'] = 'Offline'
                            data['Engine Status'] = 'Offline'
                        else:
                            data['Status'] = 'Online'
                            data['Engine Status'] = 'Online'

                        del data['add_village']
                        del data['dvd_haulage']
                    return jsonify({'error': 'false', 'datas': datas, 'desc': 'success'})
                else:
                    datas = []
                    return jsonify({'error': 'true', 'datas': datas, 'desc': 'empty'})
            except Exception as e:
                print(e)
                return jsonify({'error': 'true', 'datas': str(e), 'desc': 'failure'})
        elif type == 'porgen' and id == None:
            print(type)
            print(id)

            # if type == None and id == None or type==all and id ==None:

            try:

                dev_sql = """SELECT dl.loc_lat, dl.loc_long, dl.loc_name, pt.type_name, ai.usr_id, up.usr_name, ua.add_village, pp.pro_id, dd.dvd_haulage, dg.dev_id, dd.dvd_start_hour, dd.dvd_end_hour, dd.dvd_mileages, dd.dvd_speed,dd.dvd_running_hour,
                      dg.dev_name,dg.dev_model,dg.dev_s_n,dd.dvd_latitude, dd.dvd_longitude, dd.updated_at, dd.dvd_fuel_consumption, dd.dvd_odometer_reading
                      FROM product_profile as pp LEFT JOIN device_data as dd ON
                      pp.dev_id = dd.dev_id LEFT JOIN devices_gateway as dg ON
                      dg.dev_id = pp.dev_id LEFT JOIN assign_info as ai ON
                      ai.pro_id = pp.pro_id LEFT JOIN user_profile as up ON
                      up.usr_id = ai.usr_id LEFT JOIN usr_address as ua ON
                      ua.usr_id = ai.usr_id LEFT JOIN product_type as pt ON
                      pt.type_id = pp.type_id LEFT JOIN dev_location as dl ON
                      dl.dev_id = pp.dev_id LEFT JOIN product_model as pm ON pp.pmo_id = pm.pmo_id
                      WHERE ai.ass_type = '1' and pt.type_id = '3'"""
                # print(dev_sql)
                data = cursor.execute(dev_sql)
                # print(data)
                if cursor.rowcount > 0:
                    datas = cursor.fetchall()
                    # print(datas)
                    for data in datas:

                        if data['dvd_speed'] is None:
                            data['dvd_speed'] = 0
                        data['dvd_speed'] = str(data['dvd_speed']) + ' km/h'
                        if data['dvd_haulage'] == 1:
                            data['Haulage status'] = '1'
                            data["cultivation status"] = '0'
                        else:
                            data['Haulage status'] = '0'
                            data["cultivation status"] = '1'
                        if data['updated_at'] is None:
                            # print('updated_at is none')
                            data['updated_at'] = dt = datetime(1970, 1, 1, 11)

                        if data['dvd_fuel_consumption'] is None:
                            data['dvd_fuel_consumption'] = 0
                        if data['dvd_mileages'] is None:
                            data['dvd_mileages'] = 0
                        if data['dvd_odometer_reading'] is None:
                            data['dvd_odometer_reading'] = 0
                        if data['dvd_running_hour'] is None:
                            data['dvd_running_hour'] = 0
                        if data['dvd_start_hour'] is None:
                            data['dvd_start_hour'] = '00:00'
                        data['dvd_odometer_reading'] = str(data['dvd_odometer_reading'])
                        data['notification'] = ''
                        data['usr_address'] = data['add_village']
                        data['dvd_latitude'] = data['loc_lat']
                        data['dvd_longitude'] = data['loc_long']
                        data['topic'] = "dma/gpstracker/" + data['dev_s_n']
                        data['dvd_start_hour'] = str(data['dvd_start_hour'])
                        data['dvd_end_hour'] = str(data['dvd_end_hour'])
                        data['dvd_running_hour'] = str(data['dvd_running_hour'])
                        data['dvd_mileages'] = str(data['dvd_mileages'])

                        curtime = dhaka.localize(data['updated_at'])
                        print(curtime)
                        # print(data['updated_at'])
                        # print(dhaka_time)
                        # print(type(data['updated_at']))
                        # print(type(curtime))
                        # print('-----------------------')

                        data['updated_at'] = str(data['updated_at'])
                        if dhaka_time - curtime > timedelta(minutes=30):
                            print('Greater')
                            print(data['updated_at'])
                            data['Status'] = 'Offline'
                            data['Engine Status'] = 'Offline'
                        else:
                            data['Status'] = 'Online'
                            data['Engine Status'] = 'Online'
                        del data['add_village']
                        del data['dvd_haulage']
                    return jsonify({'error': 'false', 'datas': datas, 'desc': 'success'})
                else:
                    datas = []
                    return jsonify({'error': 'true', 'datas': datas, 'desc': 'empty'})
            except Exception as e:
                print(e)
                return jsonify({'error': 'true', 'datas': str(e), 'desc': 'failure'})
        elif type == 'dieselgen' and id is None:
            print(type)
            print(id)

            # if type == None and id == None or type==all and id ==None:

            try:

                dev_sql = """SELECT dl.loc_lat, dl.loc_long, dl.loc_name, pt.type_name, ai.usr_id, up.usr_name, ua.add_village, pp.pro_id, dd.dvd_haulage, dg.dev_id, dd.dvd_start_hour, dd.dvd_end_hour, dd.dvd_mileages, dd.dvd_speed,dd.dvd_running_hour,
                      dg.dev_name,dg.dev_model,dg.dev_s_n,dd.dvd_latitude, dd.dvd_longitude, dd.updated_at, dd.dvd_fuel_consumption, dd.dvd_odometer_reading
                      FROM product_profile as pp LEFT JOIN device_data as dd ON
                      pp.dev_id = dd.dev_id LEFT JOIN devices_gateway as dg ON
                      dg.dev_id = pp.dev_id LEFT JOIN assign_info as ai ON
                      ai.pro_id = pp.pro_id LEFT JOIN user_profile as up ON
                      up.usr_id = ai.usr_id LEFT JOIN usr_address as ua ON
                      ua.usr_id = ai.usr_id LEFT JOIN product_type as pt ON
                      pt.type_id = pp.type_id LEFT JOIN dev_location as dl ON
                      dl.dev_id = pp.dev_id LEFT JOIN product_model as pm ON pp.pmo_id = pm.pmo_id
                      WHERE ai.ass_type = '1' and pt.type_id = '2'"""
                # print(dev_sql)
                data = cursor.execute(dev_sql)
                # print(data)
                if cursor.rowcount > 0:
                    datas = cursor.fetchall()
                    # print(datas)
                    for data in datas:
                        if data['dvd_speed'] is None:
                            data['dvd_speed'] = 0
                        data['dvd_speed'] = str(data['dvd_speed']) + ' km/h'
                        if data['dvd_haulage'] == 1:
                            data['Haulage status'] = '1'
                            data["cultivation status"] = '0'
                        else:
                            data['Haulage status'] = '0'
                            data["cultivation status"] = '1'
                        if data['updated_at'] is None:
                            # print('updated_at is none')
                            data['updated_at'] = dt = datetime(1970, 1, 1, 11)

                        if data['dvd_fuel_consumption'] is None:
                            data['dvd_fuel_consumption'] = 0
                        if data['dvd_mileages'] is None:
                            data['dvd_mileages'] = 0
                        if data['dvd_odometer_reading'] is None:
                            data['dvd_odometer_reading'] = 0
                        if data['dvd_running_hour'] is None:
                            data['dvd_running_hour'] = 0
                        if data['dvd_start_hour'] is None:
                            data['dvd_start_hour'] = '00:00'
                        data['dvd_odometer_reading'] = str(data['dvd_odometer_reading'])
                        data['notification'] = ''
                        data['usr_address'] = data['add_village']
                        data['dvd_latitude'] = data['loc_lat']
                        data['dvd_longitude'] = data['loc_long']
                        data['topic'] = "dma/gpstracker/" + data['dev_s_n']
                        data['dvd_start_hour'] = str(data['dvd_start_hour'])
                        data['dvd_end_hour'] = str(data['dvd_end_hour'])
                        data['dvd_running_hour'] = str(data['dvd_running_hour'])
                        data['dvd_mileages'] = str(data['dvd_mileages'])

                        curtime = dhaka.localize(data['updated_at'])
                        print(curtime)
                        # print(data['updated_at'])
                        # print(dhaka_time)
                        # print(type(data['updated_at']))
                        # print(type(curtime))
                        # print('-----------------------')

                        data['updated_at'] = str(data['updated_at'])
                        if dhaka_time - curtime > timedelta(minutes=30):
                            print('Greater')
                            print(data['updated_at'])
                            data['Status'] = 'Offline'
                            data['Engine Status'] = 'Offline'
                        else:
                            data['Status'] = 'Online'
                            data['Engine Status'] = 'Online'

                        del data['add_village']
                        del data['dvd_haulage']
                    return jsonify({'error': 'false', 'datas': datas, 'desc': 'success'})
                else:
                    datas = []
                    return jsonify({'error': 'true', 'datas': datas, 'desc': 'empty'})
            except Exception as e:
                print(e)
                return jsonify({'error': 'true', 'datas': str(e), 'desc': 'failure'})
    cursor.close()


# -----------------------------------------------------------------------------------------------------------------


# ----------------------------------------selectlist---------------------------------------------------------------
@app.route('/devreg', methods=['POST'])
def devreg():
    try:
        dhaka = timezone('Asia/Dhaka')
        dhaka_time = datetime.now(dhaka)
        time_stamp = dhaka_time.strftime('%Y-%m-%d %H:%M:%S')
        # print("Time is-->", time_stamp)

        curr_date = time_stamp.split(' ')[0]
        curr_time = str(time_stamp.split(' ')[1])
        # -------------Find Day from Date------------------------
        my_date = date.today()
        day = calendar.day_name[my_date.weekday()]  # 'Wednesday'
        # print("day is --->", day)
        # -------------Find Day from Date------------------------

        pro_name_ = request.form['pro_name']
        dev_sn_ = request.form['dev_sn']
        pmo_id_ = request.form['pmo_id']
        ven_id_ = request.form['ven_id']
        type_id_ = request.form['type_id']
        usr_id_ = request.form['usr_id']
        a_usr_id_ = request.form['a_usr_id']
        loc_lat_ = request.form['loc_lat']
        loc_long_ = request.form['loc_long']
        loc_name_ = request.form['loc_name']

        conn = pymysql.connect(host=host, user=user, password=password, db=db, cursorclass=pymysql.cursors.DictCursor)
        cursor = conn.cursor()
        if pro_name_ != "" and dev_sn_ != "" and pmo_id_ != "" and ven_id_ != "" and type_id_ != "" and usr_id_ != "" and a_usr_id_ != "" and loc_lat_ != "" and loc_long_ != "" and loc_name_ != "":
            print("Parameters Okay")
            dev_sql = """SELECT pp.pmo_id,dg.dev_id FROM devices_gateway as dg LEFT JOIN product_profile as pp
			ON dg.dev_id = pp.dev_id WHERE dg.dev_s_n = %s"""
            values = dev_sn_
            cursor.execute(dev_sql, values)
            if (cursor.rowcount == 0):
                data = cursor.fetchone()
                print(data)
                # print(data["pmo_id"])
                # print(data["dev_id"])
                if data["pmo_id"] == None and data["dev_id"] != None:
                    print("Not assigned")
                    # return jsonify({"des": data, "err": "asd"})

                    sql1 = """INSERT INTO product_profile(pro_name,dev_id,pmo_id, ven_id, type_id, pro_status,created_by, created_at) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"""
                    values1 = (pro_name_, data["dev_id"], pmo_id_, ven_id_, type_id_, "1", usr_id_, time_stamp)
                    # print(values)
                    cursor.execute(sql1, values1)

                    print("--------------------------------")

                    # print(cursor.rowcount)
                    if (cursor.rowcount > 0):
                        # print(" Data has been successfully inserted")

                        sql2 = """SELECT pro_id from product_profile WHERE dev_id=%s"""
                        values2 = data["dev_id"]
                        # print(values)
                        cursor.execute(sql2, values2)
                        if (cursor.rowcount > 0):
                            data1 = cursor.fetchone()
                            print(data1["pro_id"])
                            sql3 = """INSERT INTO assign_info(usr_id, pro_id,ass_type,created_by, created_at) VALUES (%s,%s,%s,%s,%s)"""
                            values3 = (usr_id_, data1["pro_id"], "1", usr_id_, time_stamp)
                            # print(values)
                            cursor.execute(sql3, values3)

                            print(cursor.rowcount)
                            if (cursor.rowcount > 0):
                                # data1 = cursor.fetchone()
                                # print(data1["pro_id"])
                                sql3 = """INSERT INTO dev_location(dev_id, loc_name,loc_country,loc_address,loc_lat, loc_long) VALUES (%s,%s,%s,%s,%s,%s)"""
                                values3 = (data["dev_id"], loc_name_, "Bangladesh", loc_name_, loc_lat_, loc_long_)
                                # print(values)
                                cursor.execute(sql3, values3)

                                print(cursor.rowcount)
                                if (cursor.rowcount > 0):
                                    conn.commit()
                                    return jsonify({"des": "Insert Success", "err": "false"})

                            else:
                                return jsonify({"des": "Insert Failure", "err": "true"})
                        else:
                            return jsonify({"des": "Insert Failure", "err": "true"})


                    elif (cursor.rowcount == 0):
                        return jsonify({"des": "Insert Failure", "err": "true"})

                elif data["pmo_id"] != None and data["dev_id"] != None:
                    return jsonify({"des": "Already assigned", "err": "true"})

            else:
                return jsonify({"des": "Insert Failure", "err": "true"})

        else:
            return jsonify({"des": "Empty Parameters", "err": "true"})
    except Exception as e:
        print(e)
        return jsonify({"des": str(e), "err": "true"})


# # # ----------------------------------------------Select List----------------------------------------------------------


# -----------------------------------------------------------------------------------------------------------------
# ----------------------------------------Select List-----------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------
@app.route('/selectlist', methods=['POST'])
def selectlist():
    try:

        dhaka = timezone('Asia/Dhaka')
        dhaka_time = datetime.now(dhaka)
        time_stamp = dhaka_time.strftime('%Y-%m-%d %H:%M:%S')
        curr_date = time_stamp.split(' ')[0]
        curr_time = str(time_stamp.split(' ')[1])
        my_date = date.today()
        day = calendar.day_name[my_date.weekday()]  # 'Wednesday'

        conn = pymysql.connect(host=host, user=user, password=password, db=db, cursorclass=pymysql.cursors.DictCursor)
        cursor = conn.cursor()

        dev_sql = """SELECT pt.type_id, pt.type_name FROM product_type as pt"""
        # print(dev_sql)
        cursor.execute(dev_sql)
        # print(data)
        if cursor.rowcount > 0:
            product_type = cursor.fetchall()
            # print(product_type)
            sql2 = """SELECT pm.pmo_id, pm.pmo_title FROM product_model as pm"""
            cursor.execute(sql2)
            if cursor.rowcount > 0:
                product_model = cursor.fetchall()
                # print(product_model)
                datas = {'pt': product_type, 'pm': product_model}
                sql3 = """SELECT vp.ven_id, vp.ven_name FROM vendor_profile as vp"""
                cursor.execute(sql3)
                if cursor.rowcount > 0:
                    vendors = cursor.fetchall()
                    # print(product_model)
                    datas = {'pt': product_type, 'pm': product_model, 'vd': vendors}
                    return jsonify({'error': 'false', 'datas': datas, 'desc': 'success'})
                else:
                    datas = {}
                    return jsonify({'error': 'true', 'datas': datas, 'desc': 'empty'})
            else:
                datas = {}
                return jsonify({'error': 'true', 'datas': datas, 'desc': 'empty'})
        else:
            datas = {}
            return jsonify({'error': 'true', 'datas': datas, 'desc': 'empty'})


    except Exception as e:
        print(e)
        return jsonify({'error': 'true', 'datas': str(e), 'desc': 'failure'})

    cursor.close()


# #-----------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------

@app.route('/getfarmerinfo', methods=['POST'])
def getfarmerinfo():
    try:

        florida = timezone('Asia/Dhaka')
        florida_time = datetime.now(florida)
        time_stamp = florida_time.strftime('%Y-%m-%d %H:%M:%S')
        # print("Time is-->", time_stamp)

        curr_date = time_stamp.split(' ')[0]
        curr_time = str(time_stamp.split(' ')[1])
        # -------------Find Day from Date------------------------
        my_date = date.today()
        day = calendar.day_name[my_date.weekday()]  # 'Wednesday'
        # print("day is --->", day)
        # -------------Find Day from Date------------------------

        farmerinfo = [{"f_name": "Shohan", "f_address": "Gazipur"},
                      {"f_name": "Monshi", "f_address": "Kaliakor"},
                      {"f_name": "Nasir", "f_address": "Chittagong"}]
        return jsonify({'error': 'false', 'farmerinfo': farmerinfo})


    except Exception as e:
        print(e)
        return jsonify({'error': 'true', 'farmerinfo': str(e)})

    cursor.close()


# -----------------------------------------------------------------------------------------


# --------------------------------------------agentaccount------------------------------------------------

@app.route('/agentaccount', methods=['POST'])
def agentaccount():
    conn = pymysql.connect(host=host, user=user, password=password, db=db, cursorclass=pymysql.cursors.DictCursor)
    cursor = conn.cursor()
    try:
        acc_admin_id_ = request.form['acc_admin_id']
        acc_agent_id_ = request.form['acc_agent_id']
        acc_farmer_id_ = request.form['acc_farmer_id']
        acc_due_ = request.form['acc_due']
        acc_due_date_ = request.form['acc_due_date']
        status_ = 0
        # time data '2019-12-17' does not match format '%Y-%m-%d %H:%M:%S'

        acc_due_date_ = acc_due_date_ + ' 00:00:00'
        print(acc_due_date_)

        florida = timezone('Asia/Dhaka')
        florida_time = datetime.now(florida)
        time_stamp = florida_time.strftime('%Y-%m-%d %H:%M:%S')
        curr_date = time_stamp.split(' ')[0]
        curr_time = str(time_stamp.split(' ')[1])
        # date_time_str = '2018-06-29 08:15:27.243860'
        # date_time_obj = datetime.strptime(acc_due_date_, '%Y-%m-%d %H:%M:%S.%f')
        date_time_obj = datetime.strptime(acc_due_date_, '%Y-%m-%d %H:%M:%S')
        my_date = date.today()
        day = calendar.day_name[my_date.weekday()]  # 'Wednesday'
        # 2-admin, 3-farmer, 4-agent

        adm_chk_sql = "SELECT usr_id FROM user_profile WHERE usr_id=%s AND usr_account_type=%s" % (acc_admin_id_, 2)
        cursor.execute(adm_chk_sql)
        adm_chk = cursor.rowcount
        if adm_chk > 0:
            print(cursor.fetchone())

        agent_chk_sql = "SELECT usr_id FROM user_profile WHERE usr_id=%s AND usr_account_type=%s" % (acc_agent_id_, 4)
        cursor.execute(agent_chk_sql)
        agent_chk = cursor.rowcount
        if agent_chk > 0:
            print(cursor.fetchone())

        far_chk_sql = "SELECT usr_id FROM user_profile WHERE usr_id=%s AND usr_account_type=%s" % (acc_farmer_id_, 3)
        cursor.execute(far_chk_sql)
        far_chk = cursor.rowcount
        if far_chk > 0:
            print(cursor.fetchone())

        if adm_chk > 0 and agent_chk > 0 and far_chk > 0:
            print("-----------------------")

            sql = "INSERT into agent_account(acc_admin_id, acc_agent_id, acc_farmer_id, acc_due, acc_due_date, status, created_date) VALUES (%s,%s,%s,%s,%s,%s,%s)"
            values = (acc_admin_id_, acc_agent_id_, acc_farmer_id_, acc_due_, date_time_obj, status_, florida_time)
            cursor.execute(sql, values)
            if cursor.rowcount > 0:
                # print(cursor.rowcount)
                conn.commit()
                return jsonify({'error': 'false', 'desc': 'db_insert_success'})
            else:
                return jsonify({'error': 'true', 'desc': 'db_insert_failure'})
        else:
            return jsonify({'error': 'true', 'desc': 'mismatch_values'})

    except Exception as e:
        print(e)
        return jsonify({'error': 'true', 'desc': str(e)})

    cursor.close()


# -----------------------------------------------------------------------------------------

# --------------------------------------------Insertlatlong------------------------------------------------

@app.route('/insertlatlong', methods=['POST'])
def insertlatlong():
    conn = pymysql.connect(host=host, user=user, password=password, db=db, cursorclass=pymysql.cursors.DictCursor)
    cursor = conn.cursor()
    try:
        usr_id_ = request.form['usr_id']
        device_type_ = request.form['device_type']
        longitude_ = request.form['longitude']
        latitude_ = request.form['latitude']
        device_time_ = request.form['device_time']
        loc_imei_ = request.form['device_id']

        # -------------Get current time
        # florida = timezone('US/Eastern')
        florida = timezone('Asia/Dhaka')
        florida_time = datetime.now(florida)
        time_stamp = florida_time.strftime('%Y-%m-%d %H:%M:%S')
        print("Time is-->", time_stamp)

        curr_date = time_stamp.split(' ')[0]
        curr_time = str(time_stamp.split(' ')[1])
        # print("Current DATE is-->", curr_date)
        # print("Current TIME is-->", curr_time)

        # -------------Find Day from Date------------------------
        my_date = date.today()
        day = calendar.day_name[my_date.weekday()]  # 'Wednesday'
        # print("day is --->", day)
        # -------------Find Day from Date------------------------

        if usr_id_ != "" and device_type_ != "" and longitude_ != "" and latitude_ != "" and device_time_ != "" and loc_imei_ != "":

            # chk_sql = "SELECT usr_id FROM usr_location WHERE loc_imei=%s"            
            # values = (loc_imei_)
            # cursor.execute(chk_sql,values)

            # if(cursor.rowcount == 0):
            sql = "INSERT into usr_location(usr_id, loc_long, loc_lati, loc_imei, loc_date_time) VALUES (%s,%s,%s,%s,%s)"
            values = (usr_id_, longitude_, latitude_, loc_imei_, time_stamp)
            cursor.execute(sql, values)
            if cursor.rowcount > 0:
                conn.commit()
                return jsonify({'error': 'false', 'desc': 'db insert success'})
            else:
                return jsonify({'error': 'true', 'desc': 'db insert unsuccess'})

            # elif(cursor.rowcount > 0):

            #     update_sql ="UPDATE usr_location SET loc_long = %s, loc_lati = %s, loc_date_time=%s WHERE loc_imei=%s;"
            #     update_val = (longitude_,latitude_,time_stamp,loc_imei_)
            #     cursor.execute(update_sql,update_val)

            #     if(cursor.rowcount>0):
            #         conn.commit()
            #         return jsonify({'error' : 'false', 'desc': 'db update success'})
            #     else:
            #         return jsonify({'error' : 'false', 'desc': 'db update none'})
        else:
            return jsonify({'error': 'true', 'desc': 'db insert none'})



    except Exception as e:
        print(e)
        return jsonify({'error': 'true', 'desc': str(e)})

    cursor.close()


# -----------------------------------------------------------------------------------------


# ---------------------------------Add Farmer---------------------------------

@app.route('/addfarmer', methods=['POST'])
def addfarmer():
    conn = pymysql.connect(host=host, user=user, password=password, db=db, cursorclass=pymysql.cursors.DictCursor)
    cursor = conn.cursor()
    try:
        farmer_name = request.form['farmer_name']
        address = request.form['address']
        mobile_number = request.form['mobile_number']

        florida = timezone('Asia/Dhaka')
        florida_time = datetime.now(florida)
        time_stamp = florida_time.strftime('%Y-%m-%d %H:%M:%S')
        print("Time is-->", time_stamp)

        curr_date = time_stamp.split(' ')[0]
        curr_time = str(time_stamp.split(' ')[1])

        if farmer_name != "" and address != "" and mobile_number != "":

            query = "INSERT into tbl_farmer(farmer_name, address, mobile_number,time_date)  VALUES(%s,%s,%s,%s)"
            sql_values = (farmer_name, address, mobile_number, time_stamp)
            x = cursor.execute(query, sql_values)

            print(x)
            if (cursor.rowcount > 0):
                conn.commit()

                res = {"error": "false", "msg": "insert success", }
                return jsonify(res)
            else:
                return jsonify({"error": "true", "msg": "Wrong farmer_name or address or mobile_number"})


    except Exception as e:
        print(e)
        return jsonify({"error": "true", "msg": e.args[1]})

    cursor.close()


# -----------------------------------------------------------------------------------------

# ---------------------------------Farmer Money Collection---------------------------------

@app.route('/moneycollection', methods=['POST'])
def moneycollection():
    conn = pymysql.connect(host=host, user=user, password=password, db=db, cursorclass=pymysql.cursors.DictCursor)
    cursor = conn.cursor()
    try:
        farmer_name = request.form['farmer_name']
        money = request.form['money']
        address = request.form['address']
        mobile_number = request.form['mobile_number']
        user_id = request.form['user_id']
        farmer_pic = request.form['farmer_pic']

        print(farmer_name, money, address, mobile_number)

        florida = timezone('Asia/Dhaka')
        florida_time = datetime.now(florida)
        time_stamp = florida_time.strftime('%Y-%m-%d %H:%M:%S')
        print("Time is-->", time_stamp)

        if farmer_name != "" and money != "" and address != "" and mobile_number != "" and user_id != "" and farmer_pic != "":
            print("Parameters Okay")
            dir_path = "images/farmers_pic/"

            # image_64_decode = base64.decodestring(student_pic)
            # image_64_decode = base64.decodebytes(student_pic.encode())
            # base64.decodebytes
            image_64_decode = base64.b64decode(farmer_pic.encode('utf-8'))
            filename = dir_path + str(farmer_name) + "_" + str(mobile_number) + ".png"
            image_result = open(filename, 'wb')
            image_result.write(image_64_decode)

            # Get image size

            image_size = os.path.getsize(filename)
            if image_size > 51200:
                print("Image is larger than 50 Kb")
                os.remove(filename)
                print("File Removed!")
                return jsonify({"description": "Image is larger than 50 Kb", "error": "true", "data": ""})

            else:
                print("Image is smaller than 50 Kb")

            query = "SELECT farmer_name, id, address FROM tbl_farmer WHERE mobile_number = %s"
            sql_values = (mobile_number)
            cursor.execute(query, sql_values)

            data = cursor.fetchone()
            print(data)

            farmer_name_db = data['farmer_name']
            farmer_id = data['id']
            address = data['address']

            print(farmer_name_db, farmer_id, address)

            # query = "INSERT into tbl_farmer(farmer_name, address, mobile_number,time_date)  VALUES(%s,%s,%s,%s)"
            # sql_values = (farmer_name, address, mobile_number,time_stamp)
            # x = cursor.execute(query,sql_values)

            # print(x)
            if (cursor.rowcount > 0):
                if farmer_name_db == farmer_name:
                    print("TRUE")
                    query = "INSERT into tbl_money_collection(farmer_id, money, collector_id,time_date,farmer_pic)  VALUES(%s,%s,%s,%s,%s)"
                    sql_values = (farmer_id, money, user_id, time_stamp, filename)
                    cursor.execute(query, sql_values)

                    if (cursor.rowcount > 0):
                        conn.commit()

                        res = {"error": "false", "msg": "insert success"}
                        return jsonify(res)
                    else:
                        res = {"error": "false", "msg": "insert failed"}
                        return jsonify(res)
                else:
                    res = {"error": "false", "msg": "wrong farmer_name"}
                    return jsonify(res)
        else:
            return jsonify({"error": "true", "msg": "Wrong farmer_name or address or mobile_number"})


    except Exception as e:
        print(e)
        return jsonify({"error": "true", "msg": str(e)})

    cursor.close()


# -------------------------------------------------------------------------------------------------------


# ---------------------------------Assign Visit Schedule---------------------------------

@app.route('/assignschedule', methods=['POST'])
def assignschedule():
    conn = pymysql.connect(host=host, user=user, password=password, db=db, cursorclass=pymysql.cursors.DictCursor)
    cursor = conn.cursor()
    try:
        device_id = request.form['device_id']
        user_id = request.form['user_id']
        agent_id = request.form['agent_id']
        start_time = request.form['start_time']
        end_time = request.form['end_time']
        start_location = request.form['start_location']
        end_location = request.form['end_location']

        florida = timezone('Asia/Dhaka')
        florida_time = datetime.now(florida)
        time_stamp = florida_time.strftime('%Y-%m-%d %H:%M:%S')
        print("Time is-->", time_stamp)

        curr_date = time_stamp.split(' ')[0]
        curr_time = str(time_stamp.split(' ')[1])

        if device_id != "" and user_id != "" and start_time != "" and end_time != "":

            query = "INSERT into tbl_visit_schedule(device_id, user_id, start_time,end_time,start_location,end_location,entryTime,addedBy)  VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"
            sql_values = (device_id, agent_id, start_time, end_time, start_location, end_location, time_stamp, user_id)
            x = cursor.execute(query, sql_values)

            print(x)
            if (cursor.rowcount > 0):
                conn.commit()

                res = {"error": "false", "msg": "insert success", }
                return jsonify(res)
            else:
                return jsonify({"error": "true", "msg": "Wrong Parameters"})


    except Exception as e:
        print(e)
        return jsonify({"error": "true", "msg": e.args[1]})

    cursor.close()


# -----------------------------------------------------------------------------------------


# ---------------------------------Get  Schedule List---------------------------------

@app.route('/getschedulelist', methods=['POST'])
def getschedulelist():
    conn = pymysql.connect(host=host, user=user, password=password, db=db, cursorclass=pymysql.cursors.DictCursor)
    cursor = conn.cursor()
    try:
        user_id = request.form['user_id']
        current_date = request.form['current_date']

        florida = timezone('Asia/Dhaka')
        florida_time = datetime.now(florida)
        time_stamp = florida_time.strftime('%Y-%m-%d %H:%M:%S')
        print("Time is-->", time_stamp)

        curr_date = time_stamp.split(' ')[0]
        curr_time = str(time_stamp.split(' ')[1])

        if user_id != "" and current_date != "":
            # query = "SELECT * FROM tbl_visit_schedule WHERE user_id = (%s) and DATE(start_time) =(%s)"

            query = "SELECT tvs.*, tf.farmer_name, tf.address, tf.mobile_number FROM tbl_visit_schedule as tvs LEFT JOIN tbl_farmer as tf \
					ON tvs.farmer_id=tf.id WHERE tvs.user_id = (%s) and DATE(tvs.start_time) =(%s)"

            # query = "INSERT into tbl_visit_schedule(device_id, user_id, start_time,end_time,start_location,end_location,entryTime,addedBy)  VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"
            sql_values = (user_id, current_date)
            x = cursor.execute(query, sql_values)

            # print(x)
            if (cursor.rowcount > 0):
                data = cursor.fetchall()
                print(type(data))
                print()
                print(data)

                for i in range(0, len(data)):
                    print(data[i])
                    print(type(data[i]))
                    print(data[i]['device_id'])
                # data[i]['gps']

                # data = json.dumps(data)
                # print(data)
                # for row in data:
                # print(data['device_id'])

                res = {"error": "false", "msg": "db query success", "data": data}
                return jsonify(res)
            else:
                return jsonify({"error": "false", "msg": "no values", "data": []})
        else:
            return jsonify({"error": "true", "msg": "Empty Parameters!", "data": []})



    except Exception as e:
        print(e)
        return jsonify({"error": "true", "msg": e.args[1], "data": []})

    cursor.close()


# -----------------------------------------------------------------------------------------
# --------------------------------------------xxxxxxxxxxxxxx---------------------------------------

# --------------------------------------------xxxxxxxxxxxxxx---------------------------------------

# --------------------------------------------xxxxxxxxxxxxxx---------------------------------------


# -----------------------------------------------------------------------------------------
# ---------------------------------Branch List <-code below->---------------------------------

@app.route('/branch', methods=['POST'])
def branchList():
    conn = pymysql.connect(host=host, user=user, password=password, db=db, cursorclass=pymysql.cursors.DictCursor)
    cursor = conn.cursor()
    try:
        school_id = request.form['school_id']

        if school_id != "":
            sql = "SELECT branch_id, branch_name,longitude, latitude FROM tbl_branch where school_id=%s" % (school_id)
            cursor.execute(sql)

            if (cursor.rowcount > 0):
                users = cursor.fetchall()
                return jsonify({'brachList': users, 'branch_status': 'True', 'error_msg': 'No error'})
            else:
                blank_branch = []
                # res= {"response": "School ID didn't match!"}
                res = {'brachList': blank_branch, 'branch_status': 'False', 'error_msg': 'No branch list to show'}
            return jsonify(res)
        else:
            return jsonify(
                {"branch_status": "False", "error_msg": "No branch list to show! Please select a School ID."})


    except Exception as e:
        print(e)

    cursor.close()


# -----------------------------------------------------------------------------------------
# --------------------------------Floor List <-code below->--------------------------------


# --------------------------------Floor List <-code below->--------------------------------


@app.route('/floor', methods=['POST'])
def floorList():
    conn = pymysql.connect(host=host, user=user, password=password, db=db, cursorclass=pymysql.cursors.DictCursor)
    cursor = conn.cursor()
    try:
        branch_id = request.form['branch_id']
        school_id = request.form['school_id']

        if branch_id != "" and school_id != "":

            sql = "SELECT tbl_floor.floor_id, tbl_floor.floor_no FROM tbl_floor JOIN tbl_branch ON tbl_floor.branch_id = tbl_branch.branch_id WHERE tbl_branch.school_id = '%s' and tbl_branch.branch_id = '%s'" % (
                school_id, branch_id)
            cursor.execute(sql)

            if (cursor.rowcount > 0):
                floors = cursor.fetchall()
                return jsonify({'floor_list': floors, 'floor_status': 'True', 'error_msg': 'No error'})
            else:
                blank_floor = []
                res = {"floorList": blank_floor, "floor_status": "False", "error_msg": "There is no floor list!"}
            return jsonify(res)
        else:
            return jsonify({"floor_status": "False",
                            "error_msg": "No floor list to show! Please select both School and Branch ID."})


    except Exception as e:
        print(e)


# SELECT tbl_floor.floor_id, tbl_floor.floor_no FROM `tbl_floor` JOIN `tbl_branch` ON tbl_floor.branch_id = tbl_branch.branch_id WHERE tbl_branch.school_id = 1 and tbl_branch.branch_id = 1
# ----------------------------------------------------------------------------------------------

# ---------------------------------Get No of students-------------------------------------

@app.route('/no_of_students', methods=['POST'])
def no_of_students():
    conn = pymysql.connect(host=host, user=user, password=password, db=db)
    cursor = conn.cursor()
    # school_id = request.form['school_id']
    branch_id = request.form['branch_id']
    floor_id = request.form['floor_id']
    current_time = request.form['current_time']

    curr_date = current_time.split(' ')[0]
    curr_time = str(current_time.split(' ')[1])
    print("Current time is-->", curr_time)

    # --------------------Get room id and room no ina floor---------------------------------

    sql = "SELECT tbl_room.room_id, tbl_room.room_no FROM `tbl_room` JOIN `tbl_floor` ON tbl_floor.floor_id = '%s' AND tbl_floor.floor_id = tbl_room.floor_id WHERE tbl_floor.branch_id = '%s'" % (
        floor_id, branch_id)
    cursor.execute(sql)
    # users = cursor.fetchall()
    # print(users[0])

    room_id_list = []
    romm_no_list = []

    i = 0
    for row in cursor.fetchall():
        room_id_list.append(row[0])
        romm_no_list.append(row[1])

    # current_time = '2019-03-04 10:52:51'
    data2 = []
    # updated_time  = '2019-03-04 10:53:53'
    # --------------------Get room id and room no in a floor---------------------------------
    for row in room_id_list:
        print(row)
        sql = "SELECT student_id FROM `tbl_attends_students_list` where room_id='%s' AND TIME(updated_time)>=('%s') and DATE(updated_time)=('%s')" % (
            row, curr_time, curr_date)
        print(sql)
        cursor.execute(sql)
        rows_affected = cursor.rowcount
        print("Room Id Rows affected - > ", row, rows_affected)
        students = cursor.fetchall()
        # print(students)
        for row2 in students:
            data = {"room_id": row, "student_id": row2[0]}

        # -----------------Show room-no---------------------

        # room_no_sql = "SELECT room_no from tbl_room where room_id='%s'"%(row)
        # cursor.execute(room_no_sql)
        # room_no_arr = cursor.fetchone()
        # room_no = room_no_arr[0]
        # print("Room noo is --->", room_no)
        # data2.append({"room_no": room_no, "no_of_students": rows_affected})
        # -----------------Show room-no---------------------

        data2.append({"room_id": row, "no_of_students": rows_affected})

    print(data2)
    data_return = {"room_list": data2, "error": "No Error"}
    print(data_return)
    print("Error")
    return jsonify(data_return)
    cursor.close()


# --------------------Get Student list and RSSI with Room Wise---------------------------------
@app.route('/student_list_room_wise', methods=['POST'])
def student_list_room_wise():
    conn = pymysql.connect(host=host, user=user, password=password, db=db)
    cursor = conn.cursor()
    # school_id = request.form['school_id']
    branch_id = request.form['branch_id']
    floor_id = request.form['floor_id']
    current_time = request.form['current_time']

    curr_date = current_time.split(' ')[0]
    curr_time = str(current_time.split(' ')[1])
    print("Current time is-->", curr_time)

    sql = "SELECT tbl_room.room_id, tbl_room.room_no FROM `tbl_room` JOIN `tbl_floor` ON tbl_floor.floor_id = '%s' AND tbl_floor.floor_id = tbl_room.floor_id WHERE tbl_floor.branch_id = '%s'" % (
        floor_id, branch_id)
    cursor.execute(sql)
    # users = cursor.fetchall()
    # print(users[0])

    room_id_list = []
    romm_no_list = []

    i = 0
    for row in cursor.fetchall():
        room_id_list.append(row[0])
        romm_no_list.append(row[1])

    # current_time = '2019-03-04 10:52:51'
    data2 = []
    student_list = []
    # updated_time  = '2019-03-04 10:53:53'
    # --------------------Get room id and room no ina floor---------------------------------
    for row in room_id_list:
        print(row)
        sql = "SELECT student_id, student_name, rssi_value FROM `tbl_attends_students_list` where room_id=%s AND updated_time>=('%s') AND DATE(updated_time)=('%s')" % (
            row, current_time, curr_date)
        cursor.execute(sql)
        rows_affected = cursor.rowcount
        if (rows_affected > 0):
            students = cursor.fetchall()
            # print(students)
            student_list = []
            for row2 in students:
                # student_list.append({ "student_name": row2[1]})
                student_list.append({"student_name": row2[1], "rssi_value": row2[2]})
                # print(student_list)

        else:
            student_list = []

        data2.append({"room_id": row, "no_of_students": rows_affected, "student_list": student_list})
    # print(data2)

    data4 = {"room_list": data2, "error": "No Error"}
    print(data4)

    return jsonify(data4)
    cursor.close()


# ------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------

# ---------------------------------API ROOM Details-----------------------------------
# ---------------------------------API ROOM Details-----------------------------------
@app.route('/room_details', methods=['POST'])
def room_details():
    # ------------------------------------------------------------------------------------
    branch_id = request.form['branch_id']
    room_id = request.form['room_id']
    current_time = request.form['current_time']

    # branch_id = 1
    # room_id = 1
    # current_time ='2019-03-04 10:13:52'

    curr_date = current_time.split(' ')[0]
    curr_time = str(current_time.split(' ')[1])
    print("Current time is-->", curr_time)

    curr_date = datetime.strptime(curr_date, '%Y-%m-%d')

    day = calendar.day_name[curr_date.weekday()]  # 'Wednesday'
    print("day is --->", day)

    conn = pymysql.connect(host=host, user=user, password=password, db=db)
    cursor = conn.cursor()
    try:

        # -----------------Find class id, subject and teacher's name ------------------------------------
        sql = (
                "SELECT class_id, subject, teacher from tbl_class_time where room_id = ('%s') and start_time<='%s' and '%s'<=end_time and day='%s'" % (
            room_id, curr_time, curr_time, day))
        cursor.execute(sql)
        class_id_arr = cursor.fetchone()

        student_list = []

        if (str(class_id_arr) == 'None'):

            room_details = {
                'error': 'true',
                'error msg': 'Wrong Brnach id or room id',
                'subject': '',
                'teacher': '',
                'student_list': student_list

            }

            return jsonify(room_details)
            cursor.close()
        else:

            class_id = class_id_arr[0]
            subject = class_id_arr[1]
            teachers_name = class_id_arr[2]

            print("class id is-->", class_id)
            print("Subject name --->", subject)
            print("teachers_name-->", teachers_name)

            # -----------------Find class id, subject and teacher's name ------------------------------------

            # ---------- Find present student list------------------------------
            cursor.execute("SELECT start_time FROM tbl_class_time WHERE class_id = ('%s') AND branch_id = ('%s')" % (
                class_id, branch_id))
            class_data = cursor.fetchone()

            if (str(class_data) == 'None'):
                room_details = {
                    'error': 'true',
                    'error msg': 'This is break time',
                    'subject': '',
                    'teacher': '',
                    'student_list': student_list
                }

                return jsonify(room_details)
                cursor.close()

            else:
                class_time = class_data[0]
                present_time = class_time + timedelta(minutes=10)
                # print(present_time)
                sql = (
                        "SELECT tsi.student_id,tsi.student_first_name,tsi.student_last_name,tsi.contact FROM tbl_attends_students_list as tasl JOIN tbl_student_info as tsi ON tsi.id=tasl.student_id  WHERE tasl.class_id = ('%s') AND tasl.branch_id = ('%s') AND tasl.room_id = ('%s') AND TIME(tasl.updated_time) >= ('%s') AND DATE(tasl.updated_time)=('%s')" % (
                    class_id, branch_id, room_id, curr_time, curr_date))
                print(sql)
                cursor.execute(sql)
                rows_affected_present = cursor.rowcount
                print("Present is---?>", rows_affected_present)

                if (rows_affected_present > 0):
                    students_present = cursor.fetchall()
                    for row in students_present:
                        student_list.append({
                            "student_id": row[0],
                            "student_name": row[1] + " " + row[2],
                            'present': 'true',
                            'absent': 'false',
                            'remarks': ''
                        })
                # ---------- Find present student list------------------------------

                # ---------- Find Absent student list------------------------------
                sql = "SELECT student_id FROM tbl_student_class WHERE class_id = %s AND student_id NOT IN(SELECT student_id FROM tbl_attends_students_list WHERE TIME(updated_time)>='%s' AND DATE(updated_time)= '%s' and class_id = %s and room_id = %s)" % (
                    class_id, curr_time, curr_date, class_id, room_id)

                print(sql)
                cursor.execute(sql)

                rows_affected_absent = cursor.rowcount
                print("Absent List-->", rows_affected_absent)

                absents_student_list = []

                for row in cursor.fetchall():
                    student_id = row[0]
                    print("student_id is-->", student_id)
                    sql = "SELECT student_id, student_first_name, student_last_name, contact from tbl_student_info Where id = %s" % (
                        student_id)
                    cursor.execute(sql)
                    data = cursor.fetchone()
                    print("Student info---->", data[0])
                    student_list.append({
                        "student_id": data[0],
                        "student_name": data[1] + " " + data[2],
                        'present': 'false',
                        'absent': 'true',
                        'remarks': ''
                    })

                print(student_list)

                room_details = {
                    'error': 'false',
                    'error msg': '',
                    'subject': subject,
                    'teacher': teachers_name,
                    'student_list': student_list
                }

                return jsonify(room_details)
                cursor.close()
                # ---------- Find Absent student list------------------------------

    except Exception as e:
        print(e)


# -----------------------------------Room details API------------------------------


# -----------------------------------------------------------------------------------------------------------------
# ----------------------------------------taskcount---------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------
@app.route('/taskcount', methods=['POST'])
def taskcount():
    try:
        dhaka = timezone('Asia/Dhaka')
        dhaka_time = datetime.now(dhaka)
        time_stamp = dhaka_time.strftime('%Y-%m-%d %H:%M:%S')
        # print("Time is-->", time_stamp)

        curr_date = time_stamp.split(' ')[0]
        curr_time = str(time_stamp.split(' ')[1])
        # -------------Find Day from Date------------------------
        my_date = date.today()
        day = calendar.day_name[my_date.weekday()]  # 'Wednesday'
        # print("day is --->", day)
        # -------------Find Day from Date------------------------

        agent_id = request.form['agent_id']

        conn = pymysql.connect(host=host, user=user, password=password, db=db, cursorclass=pymysql.cursors.DictCursor)
        cursor = conn.cursor()

        tot_sql = """SELECT COUNT(*) FROM agent_account WHERE (acc_agent_id='%s' AND status=0 AND DATE(created_date)='%s') OR (acc_agent_id='%s' AND status=2 AND DATE(created_date)='%s')""" % (
            agent_id, curr_date, agent_id, curr_date)
        cursor.execute(tot_sql)
        total = cursor.fetchone()['COUNT(*)']
        print(str(total))

        com_sql = "SELECT COUNT(*) FROM agent_account WHERE DATE(created_date)='%s' AND acc_agent_id='%s' AND status=2" % (
            curr_date, 2)
        cursor.execute(com_sql)
        complete = cursor.fetchone()['COUNT(*)']
        print(str(complete))

        inp_sql = "SELECT COUNT(*) FROM agent_account WHERE DATE(created_date)='%s' AND acc_agent_id=%s AND status=0" % (
            curr_date, agent_id)
        cursor.execute(inp_sql)
        inprogress = cursor.fetchone()['COUNT(*)']
        print(str(inprogress))
        conn.close()

        outofplan = 0
        if outofplan < 0:
            outofplan = 0
        if agent_id != "":
            data = {}
            # data['total'] = '15'
            data['total'] = total
            data['completed'] = complete
            data['inprogress'] = inprogress
            data['outofplan'] = outofplan
            if (data['total'] == 0):
                data['done'] = 0
                data['todo'] = 0
            else:
                data['done'] = int(data['completed']) / int(data['total'])
                data['todo'] = int(data['inprogress']) / int(data['total'])

            data['work'] = str(100 - int(data['done'] * 100) - int(data['todo'] * 100))
            data['done'] = str(int(data['done']))
            data['todo'] = str(int(data['todo']))
            data['end_time'] = curr_date + ' 09:00'
            data['start_time'] = curr_date + ' 19:00'
            print(data)
            return jsonify({"des": "success", "err": "false", "data": data})
        else:
            data = {}
            return jsonify({"des": "Empty Parameters", "err": "true", "data": data})

    except Exception as e:
        print(e)
        return jsonify({"des": str(e), "err": "true"})

    # -----------------------------------------------------------------------------------------------------------------


# ----------------------------------------tasklist---------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------
@app.route('/tasklist', methods=['POST'])
def tasklist():
    try:
        dhaka = timezone('Asia/Dhaka')
        dhaka_time = datetime.now(dhaka)
        time_stamp = dhaka_time.strftime('%Y-%m-%d %H:%M:%S')
        # print("Time is-->", time_stamp)

        curr_date = time_stamp.split(' ')[0]
        curr_time = str(time_stamp.split(' ')[1])
        # -------------Find Day from Date------------------------
        my_date = date.today()
        day = calendar.day_name[my_date.weekday()]  # 'Wednesday'
        # print("day is --->", day)
        # -------------Find Day from Date------------------------

        agent_id = request.form['agent_id']
        if agent_id != "":
            conn = pymysql.connect(host=host, user=user, password=password, db=db,
                                   cursorclass=pymysql.cursors.DictCursor)
            cursor = conn.cursor()
            sql = """SELECT ac.acc_farmer_id, ac.acc_rcv_date, ac.status,dl.loc_lat, dl.loc_long, upp.phn_business, 
                ac.acc_id, dl.loc_name, up.usr_name, ac.acc_due_date, up.usr_gender, pp.pro_name, ac.acc_agent_id, ac.acc_due FROM `agent_account` as ac 
                LEFT JOIN user_profile as up ON ac.acc_farmer_id = up.usr_id 
                LEFT JOIN usr_address as ua ON up.usr_id=ua.usr_id 
                LEFT JOIN assign_info as ai ON ua.usr_id = ai.usr_id 
                LEFT JOIN product_profile as pp ON ai.pro_id = pp.pro_id 
                LEFT JOIN dev_location as dl ON dl.dev_id = pp.dev_id 
                LEFT JOIN usr_phone  as upp ON upp.usr_id = up.usr_id
                WHERE (ac.acc_agent_id='%s' AND ac.status=0) 
                OR (ac.acc_agent_id='%s' AND ac.status=2)""" % (agent_id, agent_id)
            cursor.execute(sql)
            if cursor.rowcount > 0:
                datas = cursor.fetchall()
                conn.close()

                tasks = []

                for data in datas:
                    task = {}
                    task['address'] = data['loc_name']
                    if data['status'] == 0:
                        task['status'] = 'current'
                    elif data['status'] == 2:
                        task['status'] = 'completed'
                    task['product_name'] = data['pro_name']
                    task['f_name'] = data['usr_name']
                    task['current_payable_amount'] = math.floor(data['acc_due'] / 12)
                    task['due_date'] = data['acc_due_date'].strftime("%Y-%m-%d")
                    task['lat'] = data['loc_lat']
                    task['lon'] = data['loc_long']
                    task['task_id'] = str(data['acc_id'])
                    task['agent_id'] = str(data['acc_agent_id'])
                    task['owner_id'] = str(data['acc_farmer_id'])
                    task['datetime'] = time_stamp.split(" ")[0]

                    # task['taskname'] = data['loc_name']
                    # task['f_contact'] = data['phn_business']
                    # task['desc'] = 'Visit ' + str(data['loc_name'])
                    # task['gender'] = data['usr_gender']
                    # task['stt_time'] = time_stamp.split(" ")[0] + ' 10:00:00.000000'
                    # task['end_time'] = time_stamp.split(" ")[0] + ' 19:00:00.000000'
                    tasks.append(task)
                return jsonify({"des": "success", "err": "false", "data": tasks})

                print(len(tasks))
            else:
                tasks = []
                print(len(tasks))
                return jsonify({"des": "success", "err": "false", "data": tasks})


    except Exception as e:
        print(e)
        return jsonify({"des": str(e), "err": "true"})


# -----------------------------------------------------------------------------------------------------------------
# ----------------------------------------taskdetails---------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------
@app.route('/taskdetails', methods=['POST'])
def taskdetails():
    print("Task Details Api")
    try:
        dhaka = timezone('Asia/Dhaka')
        dhaka_time = datetime.now(dhaka)
        time_stamp = dhaka_time.strftime('%Y-%m-%d %H:%M:%S')
        curr_date = time_stamp.split(' ')[0]
        curr_time = str(time_stamp.split(' ')[1])
        my_date = date.today()
        day = calendar.day_name[my_date.weekday()]  # 'Wednesday'

        acc_id = request.form['task_id']
        print("--------------")
        print(acc_id)
        print("--------------")
        data_new = []

        conn = pymysql.connect(host=host, user=user, password=password, db=db, cursorclass=pymysql.cursors.DictCursor)
        cursor = conn.cursor()
        sql = """SELECT dl.loc_name, up.usr_gender, ac.acc_due - ac.acc_rcv, up.usr_name, upp.phn_business, 
              ac.acc_farmer_id, ac.acc_agent_id, ac.status, ac.acc_due, uo.occ_title FROM `agent_account` as ac 
              LEFT JOIN user_profile as up ON ac.acc_farmer_id = up.usr_id 
              LEFT JOIN usr_address as ua ON up.usr_id=ua.usr_id 
              LEFT JOIN assign_info as ai ON ua.usr_id = ai.usr_id 
              LEFT JOIN product_profile as pp ON ai.pro_id = pp.pro_id 
              LEFT JOIN dev_location as dl ON dl.dev_id = pp.dev_id 
              LEFT JOIN usr_occupation as uo ON ac.acc_farmer_id = uo.usr_id 
              LEFT JOIN usr_phone as upp ON upp.usr_id = up.usr_id WHERE ac.acc_id = '%s'""" % (acc_id)
        cursor.execute(sql)

        task = {}

        if cursor.rowcount > 0:
            data = cursor.fetchone()
            conn.close()

            task['owner_id'] = data['acc_farmer_id']
            task['f_name'] = data['usr_name']
            task['address'] = data['loc_name']
            task['f_contact'] = data['phn_business']
            task['status'] = data['status']
            task['loan_amount'] = str(int(data['ac.acc_due - ac.acc_rcv']))
            task['amount_due'] = str(int(data['acc_due'] / 12))
            task['agent_id'] = data['acc_agent_id']
            task['f_occupation'] = 'farmer'  # data['occ_title']

            # task['taskname'] = 'Visit ' + data['loc_name']
            # task['gender'] = data['usr_gender']
            data_new.append(task)
            return jsonify({"des": "success", "err": "false", "data": data_new})
        else:
            data_new.append(task)
            return jsonify({"des": "Empty Parameters", "err": "true", "data": data_new})


    except Exception as e:
        print(e)
        return jsonify({"des": str(e), "err": "true"})


# # -----------------------------------------------------------------------------------------------------------------
# # ----------------------------------------taskdetails---------------------------------------------------------------
# # ----------------------------------------------------------------------------------------------------------------
# @app.route('/taskdetails', methods=['POST'])                     
# def taskdetails():
#   try:
#     dhaka = timezone('Asia/Dhaka')
#     dhaka_time = datetime.now(dhaka)
#     time_stamp = dhaka_time.strftime('%Y-%m-%d %H:%M:%S')
#     #print("Time is-->", time_stamp)

#     curr_date = time_stamp.split(' ')[0]
#     curr_time = str(time_stamp.split(' ')[1])
#     #-------------Find Day from Date------------------------
#     my_date = date.today()        
#     day = calendar.day_name[my_date.weekday()]  #'Wednesday'


#     task_id = request.form['task_id']
#     print(task_id)
#     if task_id != "":
#       data =[]
#       #for i in range(0,3):
#       task = {}
#       if task_id =='1':
#         task['address'] = 'Gazipur Chowrasta'
#         task['taskname'] = 'Chowrasta'
#         task['gender'] = 'male'
#         task['due_amt'] = '600'
#         task['f_contact'] = '01711419092'
#         task['f_name'] ='Mahfuz'
#       elif task_id == '2':
#         task['address'] = 'Gazipur'
#         task['taskname'] = 'Tank More'
#         task['taskname'] = 'completed'
#         task['due_amt'] = '1000'
#         task['gender'] = 'male'
#         task['f_contact'] = '01911227945'
#         task['f_name'] ='Simbu'
#       elif task_id == '3':
#         task['address'] = 'Station Road'
#         task['taskname'] = 'Station Road'
#         task['taskname'] = 'current'
#         task['due_amt'] = '2000'
#         task['gender'] = 'male'
#         task['f_contact'] = '01911123456'
#         task['f_name'] ='Zubaer'
#       data.append(task)
#         #print(data)

#       return jsonify({"des": "success","err": "false", "data":data})
#     else:
#       data = {}
#       return jsonify({"des": "Empty Parameters", "err": "true", "data":data})

#   except Exception as e:
#     print(e)
#     return jsonify({"des": str(e), "err": "true"})  


# ----------------------------------------------Agent ---------------------------------------------------
# --------------------------------------------agenttarget------------------------------------------------

@app.route('/agenttarget', methods=['POST'])
def agenttarget():
    conn = pymysql.connect(host=host, user=user, password=password, db=db, cursorclass=pymysql.cursors.DictCursor)
    cursor = conn.cursor()
    try:
        ata_agent_id_ = request.form['ata_agent_id']
        ata_amount_ = request.form['ata_amount']
        ata_from_date_ = request.form['ata_from_date']
        ata_to_date_ = request.form['ata_to_date']
        created_by_ = request.form['created_by']
        created_at_ = request.form['created_at']

        # -------------Get current time
        # florida = timezone('US/Eastern')
        florida = timezone('Asia/Dhaka')
        florida_time = datetime.now(florida)
        time_stamp = florida_time.strftime('%Y-%m-%d %H:%M:%S')
        print("Time is-->", time_stamp)

        curr_date = time_stamp.split(' ')[0]
        curr_time = str(time_stamp.split(' ')[1])
        # print("Current DATE is-->", curr_date)
        # print("Current TIME is-->", curr_time)

        # -------------Find Day from Date------------------------
        my_date = date.today()
        day = calendar.day_name[my_date.weekday()]  # 'Wednesday'
        # print("day is --->", day)
        # -------------Find Day from Date------------------------

        sql = "INSERT into agent_target(ata_agent_id, ata_amount, ata_from_date, ata_to_date, created_by, created_at) VALUES (%s,%s,%s,%s,%s,%s)"
        values = (ata_agent_id_, ata_amount_, ata_from_date_, ata_to_date_, created_by_, created_at_)
        cursor.execute(sql, values)
        if cursor.rowcount > 0:
            return jsonify({'error': 'false', 'desc': 'db insert success'})
        else:
            return jsonify({'error': 'true', 'desc': 'db insert failure'})

    except Exception as e:
        print(e)
        return jsonify({'error': 'true', 'desc': str(e)})

    cursor.close()


# -----------------------------------------------------------------------------------------

# --------------------------------------------agenttarget------------------------------------------------

@app.route('/targetlist', methods=['POST'])
def targetlist():
    conn = pymysql.connect(host=host, user=user, password=password, db=db, cursorclass=pymysql.cursors.DictCursor)
    cursor = conn.cursor()
    try:

        # -------------Get current time
        # florida = timezone('US/Eastern')
        florida = timezone('Asia/Dhaka')
        florida_time = datetime.now(florida)
        time_stamp = florida_time.strftime('%Y-%m-%d %H:%M:%S')
        print("Time is-->", time_stamp)

        curr_date = time_stamp.split(' ')[0]
        curr_time = str(time_stamp.split(' ')[1])
        # print("Current DATE is-->", curr_date)
        # print("Current TIME is-->", curr_time)

        # -------------Find Day from Date------------------------
        my_date = date.today()
        day = calendar.day_name[my_date.weekday()]  # 'Wednesday'
        # print("day is --->", day)
        # -------------Find Day from Date------------------------

        sql = "SELECT * FROM agent_target"
        # values = (ata_agent_id_, ata_amount_, ata_from_date_, ata_to_date_, created_by_, created_at_)
        cursor.execute(sql)
        if cursor.rowcount > 0:
            datas = cursor.fetchall()
            for data in datas:
                print(data)
                data['ata_agent_id'] = str(data['ata_agent_id'])
                data['ata_id'] = str(data['ata_id'])
                data['created_by'] = str(data['created_by'])
                data['ata_amount'] = str(data['ata_amount'])
                data['ata_from_date'] = str(data['ata_from_date'])
                data['ata_to_date'] = str(data['ata_to_date'])
                data['created_at'] = str(data['created_at'])
            return jsonify({'error': 'false', 'desc': 'success', 'data': datas})
        else:
            return jsonify({'error': 'true', 'desc': 'failure', 'data': ''})

    except Exception as e:
        print(e)
        return jsonify({'error': 'true', 'desc': str(e)})

    cursor.close()


# -----------------------------------------------------------------------------------------
# ----------------------------------------------Task ---------------------------------------------------
# --------------------------------------------Task Schedule------------------------------------------------

@app.route('/taskschedule', methods=['POST'])
def taskschedule():
    conn = pymysql.connect(host=host, user=user, password=password, db=db, cursorclass=pymysql.cursors.DictCursor)
    cursor = conn.cursor()
    try:
        acc_admin_id_ = request.form['created_by']
        acc_agent_id_ = request.form['acc_agent_id']
        acc_farmer_id_ = request.form['acc_farmer_id']
        acc_due_date_ = request.form['acc_due_date']
        acc_due_ = request.form['due_amt']

        # -------------Get current time
        # florida = timezone('US/Eastern')
        florida = timezone('Asia/Dhaka')
        florida_time = datetime.now(florida)
        time_stamp = florida_time.strftime('%Y-%m-%d %H:%M:%S')
        print("Time is-->", time_stamp)

        curr_date = time_stamp.split(' ')[0]
        curr_time = str(time_stamp.split(' ')[1])
        # print("Current DATE is-->", curr_date)
        # print("Current TIME is-->", curr_time)

        # -------------Find Day from Date------------------------
        my_date = date.today()
        day = calendar.day_name[my_date.weekday()]  # 'Wednesday'
        # print("day is --->", day)
        # -------------Find Day from Date------------------------

        sql = "INSERT into agent_account(acc_admin_id, acc_agent_id, acc_farmer_id, acc_due, acc_due_date,status) VALUES (%s,%s,%s,%s,%s,%s)"
        values = (acc_admin_id_, acc_agent_id_, acc_farmer_id_, acc_due_, acc_due_date_, '0')
        cursor.execute(sql, values)
        if cursor.rowcount > 0:
            return jsonify({'error': 'false', 'desc': 'db insert success'})
        else:
            return jsonify({'error': 'true', 'desc': 'db insert failure'})

    except Exception as e:
        print(e)
        return jsonify({'error': 'true', 'desc': str(e)})

    cursor.close()


# -----------------------------------------------------------------------------------------

# # -----------------------------------------------------------------------------------------------------------------
# # ----------------------------------------taskcount---------------------------------------------------------------
# # ----------------------------------------------------------------------------------------------------------------
# @app.route('/tasksubmit', methods=['POST'])                     
# def tasksubmit():
#   try:
#     dhaka = timezone('Asia/Dhaka')
#     dhaka_time = datetime.now(dhaka)
#     time_stamp = dhaka_time.strftime('%Y-%m-%d %H:%M:%S')
#     #print("Time is-->", time_stamp)

#     curr_date = time_stamp.split(' ')[0]
#     curr_time = str(time_stamp.split(' ')[1])
#     #-------------Find Day from Date------------------------
#     my_date = date.today()        
#     day = calendar.day_name[my_date.weekday()]  #'Wednesday'
#     #print("day is --->", day)
#     #-------------Find Day from Date------------------------

#     task_id = request.form['task_id']
#     task_amt = request.form['task_amt']
#     task_due = request.form['task_due']
#     date_rec = request.form['date_rec']
#     data = {}
#     data['amt_rec'] = str(task_amt)
#     data['amt_due'] = str(3*int(task_amt) - int(task_amt))
#     data['amt_due'] = time_stamp
#     if task_amt != '' and task_id != '' and date_rec != '':
#       sql ="INSERT into agent_account(acc_admin_id, acc_agent_id, acc_farmer_id, acc_due, acc_due_date,status) VALUES (%s,%s,%s,%s,%s,%s)"
#       values = (acc_admin_id_, acc_agent_id_, acc_farmer_id_, acc_due_, acc_due_date_, '0')
#       cursor.execute(sql,values)
#       if cursor.rowcount > 0:
#         return jsonify({'error' : 'false', 'desc': 'db insert success'})
#       else:
#         return jsonify({'error' : 'true', 'desc': 'db insert failure'})
#       return jsonify({"des": "Collection successful", "err": "false"})
#     else:
#       return jsonify({"des": "Collection failed", "err": "true"})


#   except Exception as e:
#     print(e)
#     return jsonify({"des": str(e), "err": "true"})  

# # -----------------------------------------------------------------------------------------------------------------------
# # -----------------------------------------------------------------------------------------------------------------------
# # -----------------------------------------------------------------------------------------------------------------------

# -----------------------------------------------------------------------------------------------------------------
# ----------------------------------------TaskSubmit---------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------
@app.route('/tasksubmit', methods=['POST'])
def tasksubmit():
    conn = pymysql.connect(host=host, user=user, password=password, db=db, cursorclass=pymysql.cursors.DictCursor)
    cursor = conn.cursor()
    try:
        dhaka = timezone('Asia/Dhaka')
        dhaka_time = datetime.now(dhaka)
        time_stamp = dhaka_time.strftime('%Y-%m-%d %H:%M:%S')
        # print("Time is-->", time_stamp)

        curr_date = time_stamp.split(' ')[0]
        curr_time = str(time_stamp.split(' ')[1])
        # -------------Find Day from Date------------------------
        my_date = date.today()
        day = calendar.day_name[my_date.weekday()]  # 'Wednesday'
        # print("day is --->", day)
        # -------------Find Day from Date------------------------
        agent_id = request.form['agent_id']
        task_id = request.form['task_id']
        task_amt = request.form['task_amt']
        # task_due = request.form['task_due']
        # date_rec = request.form['date_rec']
        print(agent_id, task_id, task_amt)
        # task_id = 1

        if agent_id != '' and task_amt != '' and task_id != '':
            sql1 = "SELECT acc_farmer_id, acc_due, acc_due_date FROM agent_account WHERE acc_id=%s" % (task_id)
            cursor.execute(sql1)
            if cursor.rowcount > 0:
                # print(cursor.fetchone())
                data = cursor.fetchone()
                acc_farmer_id = data['acc_farmer_id']
                acc_due = data['acc_due']
                # print(acc_farmer_id, acc_due)
                # print("-------------")

                sql2 = "INSERT into agent_account(acc_admin_id, acc_agent_id, acc_farmer_id, acc_rcv, acc_rcv_date,status) VALUES (%s,%s,%s,%s,%s,%s)"
                values2 = (8, agent_id, acc_farmer_id, task_amt, time_stamp, 1)
                cursor.execute(sql2, values2)
                if cursor.rowcount > 0 and (acc_due - decimal.Decimal(task_amt)) > 0:
                    conn.commit()
                    sql3 = "UPDATE agent_account SET status=%s, acc_due=%s WHERE acc_id=%s"
                    values3 = (0, acc_due - decimal.Decimal(task_amt), task_id)
                    cursor.execute(sql3, values3)
                    if cursor.rowcount > 0:
                        conn.commit()
                        print("DB Insert success")
                        return jsonify({'err': 'false', 'des': 'success',
                                        'loan_paid': task_amt,
                                        'current_loan_amount': acc_due - decimal.Decimal(task_amt),
                                        'loan_paid_off_date': data['acc_due_date'],
                                        'date_created': time_stamp
                                        })
                    else:
                        return jsonify({'err': 'true', 'des': 'failure'})
                elif cursor.rowcount > 0 and (acc_due - decimal.Decimal(task_amt)) == 0:
                    conn.commit()
                    sql4 = "UPDATE agent_account SET status=%s, acc_due=%s WHERE acc_id=%s"
                    values4 = (2, acc_due - decimal.Decimal(task_amt), task_id)
                    cursor.execute(sql4, values4)
                    if cursor.rowcount > 0:
                        conn.commit()
                        print("DB Insert success")
                        return jsonify({'err': 'false', 'des': 'success',
                                        'loan_paid': task_amt,
                                        'current_loan_amount': acc_due - decimal.Decimal(task_amt),
                                        'loan_paid_off_date': data['acc_due_date'],
                                        'date_created': time_stamp
                                        })
                    else:
                        return jsonify({'err': 'true', 'des': 'failure'})
                else:
                    return jsonify({'err': 'true', 'des': 'failure'})

            else:
                return jsonify({'err': 'true', 'des': 'failure'})

            return jsonify({"des": "Cdone", "err": "false"})

        else:
            return jsonify({"des": "Collection failed", "err": "true"})

    except Exception as e:
        print(e)
        return jsonify({"des": str(e), "err": "true"})

    # -----------------------------------------------------------------------------------------------------------------------


# -----------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------


# -----------------------------------------------------------------------------------------------------------------
# ----------------------------------------taskcount---------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------
@app.route('/moneysubmit', methods=['POST'])
def moneysubmit():
    try:
        dhaka = timezone('Asia/Dhaka')
        dhaka_time = datetime.now(dhaka)
        time_stamp = dhaka_time.strftime('%Y-%m-%d %H:%M:%S')
        # print("Time is-->", time_stamp)

        curr_date = time_stamp.split(' ')[0]
        curr_time = str(time_stamp.split(' ')[1])
        # -------------Find Day from Date------------------------
        my_date = date.today()
        day = calendar.day_name[my_date.weekday()]  # 'Wednesday'
        # print("day is --->", day)
        # -------------Find Day from Date------------------------

        farmer_name = request.form['farmer_name']
        money_amt = request.form['money_amt']
        data = {}
        # data['amt_rec'] = str(task_amt)
        # data['amt_due'] = str(3*int(task_amt) - int(task_amt))

        if farmer_name != '' and money_amt != '':
            return jsonify({"des": "Collection successful", "err": "false", "data": data})
        else:
            return jsonify({"des": "Collection failed", "err": "true"})


    except Exception as e:
        print(e)
        return jsonify({"des": str(e), "err": "true"})

    # -----------------------------------------------------------------------------------------------------------------------


# -----------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------

# -----------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=9000)
