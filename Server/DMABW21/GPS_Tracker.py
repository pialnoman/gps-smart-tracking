import codecs   
import socketserver  
from threading import Thread, current_thread
import time
import socket
import Data_Processing
# import crcmod

# import paho.mqtt.client as paho
# import json

import datetime

from datetime import datetime, date
from pytz import timezone 

#Global Variables
sleep_time = 10




#-----------------------------------------------------------------------#
class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):

    def handle(self):
        global history_data_update_flag
        history_data_update_flag = False
        inc = 1

        time_start_count = time.time()

        while (True):



            #self.request.settimeout(1)

            print('{} - Incoming connection from {}'.format(time.strftime('%d.%m.%Y %H:%M:%S', time.localtime()), self.client_address))

            thread = current_thread()
            print("\n")
            # Print device ip
            print ("{} wrote: ".format(self.client_address[0]))
            print ("Current Thread: %s " %thread)


            #Combined active energy
            #response = '01030000000D840F'#get all the data-181013380043
            #New register data
            # response = '05030000000D858B'#get all the data--wallsocket            
            # response_hex = codecs.decode(response,"hex_codec")
            # #00000fc300000fc30000000008cf000000000000000000001396

            # self.request.send(response_hex)
            # print("Response send for energy meter device-DZS100-1P: ", str(response))

            data = self.request.recv(300)
            #print("data type")
            #print(type(data))
            #import codecs # For hex conversion
            #data_hex= data.hex();#data_new = codecs.encode(data,"hex_codec");
            #print(data_hex)
            print("Response from GPS Tracker:", data)
            #print(data_hex)
            time.sleep(5)

            print(type(data))
            print(len(data))
            #time.sleep(2)

            if len(data) == 31 or len(data) == 30:
                #ata ="["
                data =  data.split("*")[0]+ "*" +      data.split("*")[1]+"*"+"0002"+"*"+"LK]"
                #ata = data.split(",")[0] + ']'
                #ata = 
                print(data)
                if len(data) > 0:
                    self.request.send(data)
                    print("Response send for BW GPS Tracker: ", str(data))
            
            # if inc ==2:
            #     history_data_update_flag = False

            # time_now_count = time.time()
            # print(str(time_now_count - time_start_count) + " seconds has passed")

            # #Hiorical update after 300 seconds

            # if time_now_count - time_start_count > 300:
            #     #print(time_start_count)
            #     #print("300 seconds have passed")
            #     history_data_update_flag = True
            #     time_start_count = time_now_count
            #     #print(time_start_count)
            #     inc = 2
            #     #time.sleep(2)            

            # # Create an object for processing data
            new_object = Query()

            # # Pass received data stream as an argument of function device_data_process
            new_object.device_data_process(data)

            del new_object
            # time.sleep(5)




            
            
     

             
#-----------------------------------------------------------------------#


#-----------------------------------------------------------------------#
class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass    

#-----------------------------------------------------------------------#
if __name__ == "__main__":

    host = '182.163.112.219'
    
    port = 8099
    print('Host ip: \n', host, 'Port:', port)

    #############################################################################
    # Class name: Query
    # Inherits a class:
    # File: Data_Processing
    # Class: Processing
    class Query(Data_Processing.Processing):
        pass

    server = ThreadedTCPServer((host, port), ThreadedTCPRequestHandler)
    print("Server loop running in thread:\n")
    server.serve_forever()
#-----------------------------------------------------------------------#   


