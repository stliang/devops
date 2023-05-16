"""
MQTT Smart temperature Sensor
"""
 
import time
 
import paho.mqtt.client as mqtt
from faker import Faker
 
# connect to the MQTT broker
 
MQTT_BROKER_URL = "192.168.1.104"
MQTT_PUBLISH_TOPIC = "temperature"
 
mqttc = mqtt.Client()
mqttc.connect(MQTT_BROKER_URL)
 
# Init Faker, our fake data provider
fake = Faker()
 
# Infinite loop of fake data sent to the broker
while True:
  temperature = fake.random_int(min=0, max=30)
  mqttc.publish(MQTT_PUBLISH_TOPIC, temperature)
  print(f"Published new temperature measurement: {temperature}")
  time.sleep(1)
