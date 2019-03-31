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
net = []

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
topic = 'iot_data'
print('-----------------------------------')


# Callback Function on Connection with MQTT Server
def on_connect(connect_client, userdata, flags, rc):
    print("Connected with Code :" +str(rc))
    # Subscribe Topic from here
    connect_client.subscribe(topic)


# Callback Function on Receiving the Subscribed Topic/Message
def on_message(message_client, userdata, msg):
    global cpu, net, mem, store
    # print the message received from the subscribed topic
    print('Publisher: ', str(msg.payload, 'utf-8'))
    data = str(msg.payload, 'utf-8').split()  # cpu, net, mem, store
    cpu.append(data[0])
    net.append(data[1])
    mem.append(data[2])
    store.append(data[3])


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.username_pw_set(username, password)
client.connect(broker_ip, broker_port_no, 60)

client.loop_forever()

def plot_resource_util():
    global mem
    global store
    global cpu

    plot_cpu()
    plot_mem()
    plot_storage()
    fig.suptitle('Resource Utilization (CPU|MEMORY|STORAGE)')


def plot_mem():
    global mem

    # ax1.clear()
    ax1.grid(True, color='k')
    ax1.plot(mem, linewidth=5, label='Memory')
    ax1.plot(calculate_mov_avg(mem), linewidth=5, label='Moving Avg Memory')
    ax1.set_ylabel('Utilization in percentage')
    #fig1.set_xlabel('Time (scale of 2 seconds)')
    ax1.set_title('Memory Utilization')
    ax1.legend()
    plt.subplot(ax1)


def plot_cpu():
    global cpu

    # ax2.clear()
    ax2.grid(True, color='k')
    ax2.plot(calculate_mov_avg(cpu), linewidth=5, label='Moving Avg CPU')
    ax2.plot(cpu, linewidth=5, label='CPU')

    #ax2.set_ylabel('Utilization in percentage')
    ax2.set_xlabel('Time (scale of 2 seconds)')
    ax2.set_title('CPU Utilization')
    ax2.legend()
    plt.subplot(ax2)


def plot_storage():
    global store

    # ax3.clear()
    ax3.grid(True, color='k')
    ax3.plot(store, linewidth=5, label='Storage')
    ax3.plot(calculate_mov_avg(store), linewidth=5, label='Moving Avg Storage')

    #ax3.set_ylabel('Utilization in percentage')
    # fig3.set_xlabel('Time (scale of 2 seconds)')
    ax3.set_title('Storage Utilization')
    ax3.legend()
    plt.subplot(ax3)

