import codecs
import socketserver
from threading import Thread, current_thread
import time
import socket
import Data_Processing
import Data_Processing_BW21
from crccheck.crc import CrcX25
from datetime import datetime, date
from pytz import timezone

# --- global variables ---
dev_ip_list = {}


class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        def calculate_checksum(data):
            data = bytearray.fromhex(data[4:-8])  # Returns a new bytearray object initialized from a string of hex numbers.
            crc = hex(CrcX25.calc(data))
            return crc

        equipment_id = ''

        while True:
            # --- Print device ip ---
            # client_address = self.client_address[0]
            # print('{} - Incoming connection from {}'.format(time.strftime('%d.%m.%Y %H:%M:%S', time.localtime())))
            # print("\n")

            # --- Data received ---
            data = self.request.recv(76)
            data_new = data.hex()
            # data_new = "78780d0108680030320624030026cc820d0a78781f1214021a101c3bc7028d849709b3518d0014f101d6005218002b86000388220d0a78780a1344060400020006c96b0d0a"
            # print("Response from GPS Tracker:", data_new)
            # print("Data type:", type(data_new))
            # print("Data length:", len(data_new))

            # --- make a list of received data packet ---
            data_count = data_new.count("0d0a")
            data_list = data_new.split("0d0a")[:-1]
            counter = 0
            while counter < data_count:
                data_list[counter] = data_list[counter] + "0d0a"
                counter += 1
            # print(data_list)

            for item in data_list:
                # --- Login message ---
                if item[0:4] == "7878" and item[4:6].lower() == "0d" and item[6:8].lower() == "01":
                    print("Login message")
                    print(item)
                    start_bit = item[0:4]
                    packet_length = item[4:6]
                    protocol_no = item[6:8]
                    equipment_id = item[8:24]
                    serial_no = item[24:28]
                    error_chk = item[28:32]
                    error_chk_sum = calculate_checksum(item)
                    stop_bit = item[32:36]

                    # --- store device's IP against respective device ID ---
                    # --- check if equipment id is in the list ---
                    if dev_ip_list.get(equipment_id) is None:
                        dev_ip_list[equipment_id] = client_address
                    # --- update client address in the list for new address ---
                    if dev_ip_list.get(equipment_id) != client_address:
                        dev_ip_list[equipment_id] = client_address
                    # print("IP list: ", dev_ip_list)

                    # --- response to terminal ---
                    response_pkt = start_bit + "0501" + serial_no + error_chk_sum[2:] + stop_bit
                    response_pkt = response_pkt.lower()
                    # print(response_pkt)

                    # --- convert response to hex ---
                    if len(response_pkt) == 20:
                        res_hex = codecs.decode(response_pkt, "hex_codec")
                        # print(res_hex)
                        self.request.send(res_hex)
                        # print("Response send for GPS Tracker: ", str(response_pkt))
                # --- Status Information data ---
                elif item[0:4] == "7878" and item[4:6].lower() == "0a" and item[6:8].lower() == "13":
                    print("Status Information")
                    print(item)
                    start_bit = item[0:4]
                    packet_length = item[4:6]
                    protocol_no = item[6:8]
                    status_info = item[8:18]
                    serial_no = item[18:22]
                    error_chk = item[22:26]
                    error_chk_sum = calculate_checksum(item)
                    stop_bit = item[26:30]

                    # --- response to terminal ---
                    response_pkt = start_bit + "0501" + serial_no + error_chk_sum[2:] + stop_bit
                    response_pkt = response_pkt.lower()
                    # print(response_pkt)

                    # --- convert response to hex ---
                    if len(response_pkt) == 20:
                        res_hex = codecs.decode(response_pkt, "hex_codec")
                        # print(res_hex)
                        self.request.send(res_hex)
                        # print("Response send for GPS Tracker: ", str(response_pkt))
                # --- Location data ---
                elif item[0:4] == "7878" and (item[4:6].lower() == "1f" or item[4:6].lower() == "21") and item[6:8].lower() == "12":
                    print("Location data")
                    print(item)
                    # --- get ID of which equipment is sending the data ---
                    for id, ip in dev_ip_list.items():
                        # print("location data come from IP: ", ip)
                        # print("location data come from client address: ", client_address)
                        if ip == client_address:
                            # print("location data come from ID: ", id)
                            # print("item: ", item)
                            equipment_id = id
                            # --- Create an object for processing data(BW09 or BW906) ---
                            data_processing = Query()
                            # --- Pass received data stream as an argument of function device_data_process ---
                            data_processing.device_data_process(item, equipment_id)
                            del data_processing
                # --- Alarm data ---
                elif item[0:4] == "7878" and item[4:6].lower() == "25" and item[6:8].lower() == "16":
                    print("Alarm data")
                    print(item)
                    # --- get ID of which equipment is sending the data ---
                    for id, ip in dev_ip_list.items():
                        # print("location data come from IP: ", ip)
                        # print("location data come from client address: ", client_address)
                        if ip == client_address:
                            # print("location data come from ID: ", id)
                            # print("item: ", item)
                            equipment_id = id
                            # --- Create an object for processing data(BW09 or BW906) ---
                            data_processing = Query()
                            # --- Pass received data stream as an argument of function device_data_process ---
                            data_processing.device_data_process(item, equipment_id)
                            del data_processing


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


if __name__ == "__main__":
    host = 'localhost'
    port = 8100
    print('Host ip: ', host, '\nPort: ', port)

    # --- Class name: Query ---
    # --- Inherits a class: ---
    # --- File: Data_Processing ---
    # --- Class: Processing ---
    class Query(Data_Processing.Processing):
        pass

    # --- Class name: Query2 ---
    # --- Inherits a class: ---
    # --- File: Data_Processing_BW21 ---
    # --- Class: Processing ---
    class Query2(Data_Processing_BW21.Processing):
        pass

    server = ThreadedTCPServer((host, port), ThreadedTCPRequestHandler)
    print("Server loop running in thread:\n")
    server.serve_forever()
