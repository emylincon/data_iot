import paho.mqtt.client as mqtt
import os
from threading import Thread
import matplotlib.pyplot as plt
import psutil
import subprocess as sp
from drawnow import *
import time
import matplotlib.animation as animation


cpu, mem, data = 0


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

'''
while True:
    try:
        message = input('Input Message: ').strip().lower()
        client.publish(topic, message)
        print("Message Sent")
    except KeyboardInterrupt:
        print('\nProgramme Terminated')
'''


def get_cpu():
    global cpu
    prev_t = 0
    next_t = psutil.cpu_percent(percpu=False)
    delta = abs(prev_t - next_t)
    prev_t = next_t
    # return delta     # Returns CPU util in percentage
    cpu = delta


def get_mem():
    global mem
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


def get_network(intf):
    time_quanta = 3
    if_name = intf  # list(psutil.net_if_stats().keys())[0]
    # if if_name == 'lo':
    # if_name = list(psutil.net_if_stats().keys())[1]
    nic_speed = psutil.net_if_stats()[if_name][2]  # get(if_name).speed
    if nic_speed == 0:
        nic_speed = 100
    r_byte_1 = psutil.net_io_counters(pernic=True).get(if_name).bytes_recv
    s_byte_1 = psutil.net_io_counters(pernic=True).get(if_name).bytes_sent
    time.sleep(time_quanta)
    r_byte_delta = int(psutil.net_io_counters(pernic=True).get(if_name).bytes_recv) - int(r_byte_1)
    s_byte_delta = int(psutil.net_io_counters(pernic=True).get(if_name).bytes_sent) - int(s_byte_1)
    byte_per_sec = (r_byte_delta + s_byte_delta) / time_quanta
    per_util_nic = (byte_per_sec * 100 / (nic_speed * 2 ** 17))
    print(byte_per_sec)
    print(per_util_nic)


def get_resource_util():
    h1 = Thread(target=get_mem)
    h2 = Thread(target=get_cpu)
    h3 = Thread(target=get_storage)

    h1.start()
    h2.start()
    h3.start()


def main():
    global v_store

    cmd = ['df -t ext4 | grep sda1 | cut -d " " -f 13 | cut -c 1-2']
    st = str(sp.check_output(cmd, shell=True), 'utf-8')[0:-1]
    if st == '':
        v_store = 'root'
    else:
        v_store = 'sda1'
    try:
        while True:
            get_resource_util()
            time.sleep(2)
    except KeyboardInterrupt:
        print('Programme Terminated')


if __name__ == "__main__":
    main()