import paho.mqtt.client as mqtt
import os
from threading import Thread
import matplotlib.pyplot as plt
import psutil
import subprocess as sp
from drawnow import *
import time
import matplotlib.animation as animation

cpu = []
store = []
mem = []

fig = plt.figure()
ax1 = fig.add_subplot(131)
ax2 = fig.add_subplot(132)
ax3 = fig.add_subplot(133)

os.system('clear')
print('-----------------------------------')
print('Welcome to MQTT Subscriber client')
print('-----------------------------------')

username = input('Username of Broker: ').strip()
password = input('Password of Broker: ').strip()
broker_ip = input("Broker's IP: ").strip()
broker_port_no = int(input("Broker's Port no: ").strip())
topic = input("Topic: ").strip()
print('-----------------------------------')


# Callback Function on Connection with MQTT Server
def on_connect(connect_client, userdata, flags, rc):
    print("Connected with Code :" +str(rc))
    # Subscribe Topic from here
    connect_client.subscribe(topic)


# Callback Function on Receiving the Subscribed Topic/Message
def on_message(message_client, userdata, msg):
    # print the message received from the subscribed topic
    print('Publisher: ', str(msg.payload, 'utf-8'))


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.username_pw_set(username, password)
client.connect(broker_ip, broker_port_no, 60)

client.loop_forever()
