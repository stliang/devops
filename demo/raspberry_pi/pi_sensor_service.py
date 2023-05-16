#!/usr/bin/python

import io
import sys
import fcntl
import time
import copy
import string
from AtlasI2C import (
	 AtlasI2C
)
import paho.mqtt.client as mqtt

MQTT_BROKER_URL = "192.168.1.104"
MQTT_PUBLISH_TOPIC = "/sensors/CLE/v1/device5/pH"

def on_connect(client, userdata, flags, rc):
    if rc==0:
        client.connected_flag=True #set flag
        print("connected OK")
    else:
        print("Bad connection Returned code=",rc)
        client.bad_connection_flag=True

def on_disconnect(client, userdata, rc):
    logging.info("disconnecting reason  "  +str(rc))
    client.connected_flag=False
    client.disconnect_flag=True

def get_devices():
    device = AtlasI2C()
    device_address_list = device.list_i2c_devices()
    device_list = []
    
    for i in device_address_list:
        device.set_i2c_address(i)
        response = device.query("I")
        try:
            moduletype = response.split(",")[1] 
            response = device.query("name,?").split(",")[1]
        except IndexError:
            print(">> WARNING: device at I2C address " + str(i) + " has not been identified as an EZO device, and will not be queried") 
            continue
        device_list.append(AtlasI2C(address = i, moduletype = moduletype, name = response))
    return device_list 
       
def main():
    
    mqtt.Client.connected_flag=False

    mqtt.Client.bad_connection_flag=False

    device_list = get_devices()
        
    device = device_list[0]
    
    # delaytime = 300  # 5 minutes

    delaytime = 1.5 # seconds

    try:
        mqttc = mqtt.Client()
        mqttc.on_connect=on_connect
        mqttc.connect(MQTT_BROKER_URL)
        mqttc.loop_start()
        while not mqttc.connected_flag and not mqttc.bad_connection_flag:
            for dev in device_list:
                dev.write("R")
            time.sleep(delaytime)
            for dev in device_list:
                value = dev.read()
                mqttc.publish(MQTT_PUBLISH_TOPIC, value)
                print(value)
        if mqttc.bad_connection_flag:
            client.loop_stop()    #Stop loop
            sys.exit()
        mqttc.disconnect()
    except:
        print("General exception")
        sys.exit(1)

                    
# if __name__ == '__main__':
#     main()