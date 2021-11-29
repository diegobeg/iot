import json
import random
import re
import sys
import threading
import time

from azure.iot.device import IoTHubDeviceClient, Message

AUX_CONNECTION_STRING = sys.argv[1]

DEVICE_NAME=AUX_CONNECTION_STRING.split(";")[1].split("=")[1]

#SENSOR DATA WILL HOST SENSOR METRICS
action = {}
m={}
#METHOD FOR OBBTAINING TEMP
def get_action():
    if m["humidity"] > 40:
        act="Abrir"

    elif m["humiodity"] < 35:
        act="Cerrar"

	return act


	
def aux_validate_connection_string():
    if not AUX_CONNECTION_STRING.startswith( 'HostName=' ):
        print ("ERROR  - YOUR IoT HUB CONNECTION STRING IS NOT VALID")
        print ("FORMAT - HostName=your_iot_hub_name.azure-devices.net;DeviceId=your_device_name;SharedAccessKey=your_shared_access_key")
        sys.exit()


# FOR WAITING FOR MESSAGES
def message_listener(client):
    while True:
        message = client.receive_message()
        #print("Message received")
        m = json.loads(message)

def aux_iothub_client_init():
    client = IoTHubDeviceClient.create_from_connection_string(AUX_CONNECTION_STRING)
    return client

def iothub_client_telemetry_sample_run():
    try:
        aux_validate_connection_string()
        client = aux_iothub_client_init()

        print ( "IoT weather data" )
        print ( "Press Ctrl-C to exit" )

        #ENABLE THE RECEPTION THREAD, DEFINING THE TARGET METHOD
        message_listener_thread = threading.Thread(target=message_listener, args=(client,))
        message_listener_thread.daemon = True
        message_listener_thread.start()

	#IT WILL RUN FOREVER UNLESS YOU STOP IT
        while True:

		#STORING SENSOR VALUES IN DATA STRUCTURE
		#NEW METRIC COLLECTION SHOULD ADD CODE HERE
            action["value"] = get_action()

		#TRANFORMING IT TO JSON			
            json_action = json.dumps(action)

		#CREATING AN AZURE IOT MESSAGE OBJECT		
            azure_iot_message = Message(json_action)

        #SETTING PROPER MESSAGE ENCODING
            azure_iot_message.content_encoding='utf-8'
            azure_iot_message.content_type='application/json'

        #SENDING THE MESSAGE
            print( "Sending azure_iot_message: {}".format(azure_iot_message) )
            client.send_message(azure_iot_message)
            print ( "Message successfully sent" )
        #SLEEPING FOR A SECOND BEFORE RESTARTING
            time.sleep(10)

    except KeyboardInterrupt:
        print ( "IoTHubClient sample stopped" )

if __name__ == '__main__':
    iothub_client_telemetry_sample_run()

#"HostName=simpleweather10-iothub.azure-devices.net;DeviceId=Raspberrypi;SharedAccessKey=xzItfSxl7+G7SL95PAwcO8LB5TE+qmAVydeMMANlWvs="