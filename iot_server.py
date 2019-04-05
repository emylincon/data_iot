import paho.mqtt.client as mqtt
import os
from threading import Thread
import psutil
import time
import getpass as gp

__author__ = 'Emmanuel'

os.system('clear')
print('-----------------------------------')
print('Welcome to MQTT Publisher Server')
print('-----------------------------------')
client = mqtt.Client()
username = input('Username of Broker: ').strip()
password = gp.getpass('Password of Broker: ').strip()
broker_ip = input("Broker's IP: ").strip()
broker_port_no = int(input("Broker's Port no: ").strip())
topic = 'iot_data'
print('-----------------------------------')


client.username_pw_set(username, password)
client.connect(broker_ip, broker_port_no, 60)


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

    mem = psutil.virtual_memory().percent


def get_storage():
    global store

    store = psutil.disk_usage('/').percent


def get_network(intf):
    global net
    time_quanta = 3
    if_name = intf  # list(psutil.net_if_stats().keys())[0]

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

    net = per_util_nic


def get_resource_util():
    h1 = Thread(target=get_mem)
    h2 = Thread(target=get_cpu)
    h3 = Thread(target=get_storage)
    h4 = Thread(target=get_network('eth0'))

    h1.start()
    h2.start()
    h3.start()
    h4.start()


def main():
    global mem, cpu, net, store
    try:
        while True:
            get_resource_util()
            message = '{} {} {} {}'.format(cpu, net, mem, store)
            client.publish(topic, message)
            print(message)
            time.sleep(2)
    except KeyboardInterrupt:
        print('\nProgramme Terminated ')


if __name__ == "__main__":
    main()
