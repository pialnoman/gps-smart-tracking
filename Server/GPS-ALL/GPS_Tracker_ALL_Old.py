import codecs
import socketserver
from threading import Thread, current_thread
import time
import socket
import Data_Processing
import Data_Processing_BW21
from crccheck.crc import CrcX25
# import crcmod
# import paho.mqtt.client as paho
# import json
import datetime
from datetime import datetime, date
from pytz import timezone

global equipment_id
global history_data_update_flag
equipment_id = ''


# define callback
# def on_message(client, userdata, message):
#     time.sleep(1)
#     print("received message =",str(message.payload.decode("utf-8")))


# -----------------------------------------------------------------------#
class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):

    def handle(self):
        def calculate_checksum(data):
            data = bytearray.fromhex(data[4:-8])  # Returns a new bytearray object initialized from a string of hex numbers.
            crc = hex(CrcX25.calc(data))
            return crc

        history_data_update_flag = False
        inc = 1

        time_start_count = time.time()

        history_data_update_flag = False
        inc = 1

        time_start_count = time.time()
        dev_ip_ = {}

        while (True):

            # self.request.settimeout(1)

            # print('{} - Incoming connection from {}'.format(time.strftime('%d.%m.%Y %H:%M:%S', time.localtime()),
            #                                                 self.client_address))

            thread = current_thread()
            # print("\n")
            # Print device ip
            client_address = self.client_address[0]
            # print("{} wrote: ".format(self.client_address[0]))
            # print("Current Thread: %s " % thread)

            # ETS 300 or BW09 Data Format
            # data_new= "78780d0108680030311961450010e2b90d0a" #Login msg
            # data_new= "78780a130401040002001176820d0a"#Status Msg
            # data_new = "78782112130b0d111a26c7028d068e09b1ea2c0014b101d6005222002760000000d67abd0d0a"
            # client_address='182.143.112.234'

            # self.request.send(response_hex)
            # print("Response send for energy meter device-DZS100-1P: ", str(response))

            data = self.request.recv(76)

            # data_hex= data.hex();
            # Python2 
            # data_new = codecs.encode(data,"hex_codec");
            # print(data_new)

            # Python3
            data_new = data.hex()
            # data_new = data.decode()
            # print(data_new)
            # print("Response from GPS Tracker:", data_new)
            if data_new == "":
                time.sleep(3)

            # print(type(data_new))
            # print(len(data_new))

            if len(data_new) > 10:
                data_chk = data_new.split("0d0a")[0] + "0d0a"
                chk = calculate_checksum(data_chk)

                # if chk[2:] == data_chk[-8:-4]:
                #     print("Checksum is okay")

                if data_new[0:4] == "7878" and data_new[-4:].lower() == "0d0a":
                    # print("Message is from ET-300 or BW09")
                    if data_new[6:8] == "01":
                        # print("Login Message is from ET-300 or BW09")
                        start_bit = data_new[0:4]
                        packet_length = data_new[4:6]
                        protocol_no = data_new[6:8]

                        # print(protocol_no)
                        terminal_id = data_new[8:24]
                        equipment_id = terminal_id
                        serial_no = data_new[24:28]
                        error_chk = data_new[28:32]
                        stop_bit = data_new[32:36]

                        equip_serial = {equipment_id: serial_no}
                        # print(equip_serial)
                        error_chk = calculate_checksum(data_new)
                        # Checking checksum

                        inter_data = "0501" + serial_no
                        response_pkt = start_bit + "0501" + serial_no + error_chk[2:] + stop_bit
                        response_pkt = response_pkt.lower()
                        data = bytearray.fromhex(inter_data)
                        crc = hex(CrcX25.calc(data))
                        response_pkt = start_bit + inter_data + crc[2:] + stop_bit
                        # print(response_pkt)
                        # response_pkt = "0x780x780x050x010x000x010xD90xDC0x0D0x0A"
                        # For Python2
                        # res_hex = codecs.decode(response_pkt, "hex_codec")
                        # print(res_hex)
                        # For Python3
                        res_hex = codecs.decode(response_pkt, "hex_codec")
                        # print(res_hex)

                        dev_ip_[equipment_id] = client_address
                        # print(dev_ip_)

                        self.request.send(res_hex)
                        # print("Response send for GPS Tracker: ", str(response_pkt))
                        time.sleep(5)
                    elif protocol_no == "13":
                        # print(protocol_no)
                        # print("Status(Heart-beat) packet from BW-09 or ET300")
                        # print("-----------------")
                        # print("Serial NO")

                        start_bit = "7878"
                        pakt_lenghth = "05"
                        protocol_no = "13"
                        serial_no = data_new[-12:-8]
                        # print(serial_no)
                        # print("-----------------")

                        for item in equip_serial:
                            # print(item, equip_serial[item])
                            if int(equip_serial[item], 16) == int(serial_no, 16) - 1:
                                equip_serial[item] = serial_no
                                # print("####################")
                                # print("Serial Increment")
                                # print("####################")

                        error_control = calculate_checksum(data_new)
                        error_control = error_control[2:]
                        stop_bit = "0d0a"
                        response_pkt = start_bit + pakt_lenghth + protocol_no + serial_no + error_control + stop_bit
                        # print(response_pkt)

                        self.request.send(response_pkt)
                        # print("Status Response send for GPS Tracker: ", str(response_pkt))

            for item in dev_ip_:
                # print(dev_ip_[item])

                if dev_ip_[item] == client_address:
                    equipment_id = item
                else:
                    equipment_id = ''
            # print("--------------------")
            # print(dev_ip_)
            # print("--------------------")

            # ----------------------------For BW21-----------------------
            if len(data) == 31 or len(data) == 30:
                # ata ="["
                data = data.split("*")[0] + "*" + data.split("*")[1] + "*" + "0002" + "*" + "LK]"
                # ata = data.split(",")[0] + ']'
                # ata =
                # print(data)
                if len(data) > 0:
                    self.request.send(data)
                    # print("Response send for BW GPS Tracker: ", str(data))

            # ---------------------------------------
            # Create an object for processing data(BW09 or BW906)
            new_object = Query()

            # Pass received data stream as an argument of function store_raw_date
            new_object.store_raw_date("RAW_DATA", data_new)
            # Pass received data stream as an argument of function device_data_process
            new_object.device_data_process(data_new, equipment_id, client_address)

            del new_object

            # ---------------------------------------
            # Create an object for processing data(BW21)
            new_object2 = Query2()

            # Pass received data stream as an argument of function device_data_process
            new_object2.device_data_process(data_new)

            del new_object2


# -----------------------------------------------------------------------#


# -----------------------------------------------------------------------#
class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


# -----------------------------------------------------------------------#


if __name__ == "__main__":
    host = '0.0.0.0'

    port = 8100  # 6090#
    print('Host ip: \n', host, 'Port:', port)

    #############################################################################
    # Class name: Query
    # Inherits a class:
    # File: Data_Processing
    # Class: Processing
    class Query(Data_Processing.Processing):
        pass


    class Query2(Data_Processing_BW21.Processing):
        pass


    server = ThreadedTCPServer((host, port), ThreadedTCPRequestHandler)
    print("Server loop running in thread:\n")
    server.serve_forever()
# -----------------------------------------------------------------------#
