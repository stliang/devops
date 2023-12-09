#!/usr/bin/python

import io
import signal
import socket
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
MQTTC = mqtt.Client("pH sensor")

# Broker reachability test parameters
port = 80
retry = 5
delay = 10
timeout = 3

def isOpen(ip, port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        try:
                s.connect((ip, int(port)))
                s.shutdown(socket.SHUT_RDWR)
                return True
        except:
                return False
        finally:
                s.close()

def checkHost(ip, port):
        ipup = False
        for i in range(retry):
                if isOpen(ip, port):
                        ipup = True
                        break
                else:
                        time.sleep(delay)
        return ipup

def on_log(client, userdata, level, buf):
    print(f"log: {buf}")

def on_disconnect(client, userdata, flags, rc=0):
    print(f"Disconnected flags: {flags} return code: {rc}")
    client.connected_flag=False

def on_connect(client, userdata, flags, rc):
    if rc==0:
        client.connected_flag=True
        print("connected OK")
    else:
        print("Bad connection Returned code=",rc)
        client.bad_connection_flag=True

def sigterm_handler(_signo, _stack_frame):
    MQTTC.loop_stop()
    MQTTC.disconnect()
    sys.exit(0)

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
    
    signal.signal(signal.SIGTERM, sigterm_handler)

    mqtt.Client.connected_flag=False

    mqtt.Client.bad_connection_flag=False
    
    # delaytime = 300  # 5 minutes

    delaytime = 1.5 # seconds

    # TODO read run_flag from env var
    run_flag = True

    try:
        MQTTC.on_log=on_log
        MQTTC.on_connect=on_connect
        MQTTC.on_disconnect=on_disconnect
        # Check broker is reachable otherwise connection failure will exit
        if checkHost(MQTT_BROKER_URL, port):
            print(f"{MQTT_BROKER_URL} is UP")
        # As a service, it is better to start the loop before connecting
        MQTTC.loop_start()
        MQTTC.connect(MQTT_BROKER_URL)
        while not MQTTC.connected_flag and not MQTTC.bad_connection_flag:
            print("Waiting for MQTT connection")
            time.sleep(1)
            if MQTTC.bad_connection_flag:
                MQTTC.loop_stop()
                sys.exit(1)
        try:
            while run_flag:
                device_list = get_devices()
                device = device_list[0]
                for dev in device_list:
                    dev.write("R")
                time.sleep(delaytime)
                for dev in device_list:
                    value = dev.read()
                    MQTTC.publish(MQTT_PUBLISH_TOPIC, value)
                    print(value)
                # run_flag = read from env var
                # delaytime = read from env var
                # MQTT_PUBLISH_TOPIC = read from env var
        except Exception as e:
            print(f"i2c or mqtt error\n{e}")
        MQTTC.loop_stop()
        MQTTC.disconnect()
    except Exception as e:
        print(f"Exception:\n{e}")
        sys.exit(1)

if __name__ == '__main__':
    main()