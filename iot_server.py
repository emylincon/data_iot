import paho.mqtt.client as mqtt
import os
from threading import Thread
import matplotlib.pyplot as plt
import psutil
import subprocess as sp
from drawnow import *
import time
import matplotlib.animation as animation


os.system('clear')
print('-----------------------------------')
print('Welcome to MQTT Publisher client')
print('-----------------------------------')
client = mqtt.Client()
username = input('Username of Broker: ').strip()
password = input('Password of Broker: ').strip()
broker_ip = input("Broker's IP: ").strip()
broker_port_no = int(input("Broker's Port no: ").strip())
topic = input("Topic: ").strip()
print('-----------------------------------')


client.username_pw_set(username, password)
client.connect(broker_ip, broker_port_no, 60)

while True:
    try:
        message = input('Input Message: ').strip().lower()
        client.publish(topic, message)
        print("Message Sent")
    except KeyboardInterrupt:
        print('\nProgramme Terminated')

def get_cpu():
    prev_t = 0
    next_t = psutil.cpu_percent(percpu=False)
    delta = abs(prev_t - next_t)
    prev_t = next_t
    # return delta     # Returns CPU util in percentage
    cpu.append(delta)


def get_mem():
    cmd = ['cat /proc/meminfo | grep MemFree |cut -d ":" -f 2 | cut -d "k" -f 1']
    free_mem = str(sp.check_output(cmd, shell=True), 'utf-8')[0:-1]
    cmd = [' cat /proc/meminfo | grep MemAva |cut -d ":" -f 2 | cut -d "k" -f 1']
    total_mem = str(sp.check_output(cmd, shell=True), 'utf-8')[0:-1]
    mem_util = (float(free_mem.strip()) / float(total_mem.strip())) * 100
    # return mem_util  # Returns memory util in percentage
    mem.append(mem_util)


def get_storage():
    cmd = ['df -t ext4 | grep {} | cut -d " " -f 13 | cut -c 1-2'.format(v_store)]
    storage = str(sp.check_output(cmd, shell=True), 'utf-8')[0:-1]
    # return int(storage.strip())  # Returns storage in percentage
    store.append(float(storage.strip()))


def get_resource_util():
    h1 = Thread(target=get_mem)
    h2 = Thread(target=get_cpu)
    h3 = Thread(target=get_storage)

    h1.start()
    h2.start()
    h3.start()
