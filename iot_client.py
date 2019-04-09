import paho.mqtt.client as mqtt
import os
from threading import Thread
from drawnow import *
import time
import getpass as gp

__author__ = 'Emmanuel'

cpu = []
store = []
mem = []
net = []

fig = plt.figure()
ax1 = fig.add_subplot(221)
ax2 = fig.add_subplot(222)
ax3 = fig.add_subplot(223)
ax4 = fig.add_subplot(224)

os.system('clear')
print('-----------------------------------')
print('Welcome to MQTT Subscriber client ')
print('-----------------------------------')

username = input('Username of Broker: ').strip()
password = gp.getpass('Password of Broker: ').strip()
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
    received = str(msg.payload, 'utf-8')
    # print('Publisher: ', received)
    data = received.split()  # cpu, net, mem, store
    cpu.append(data[0])
    net.append(data[1])
    mem.append(data[2])
    store.append(data[3])
    print('Publisher: CPU: {}, Network: {}, Memory: {}, Store {}'.format(data[0], data[1], data[2], data[3]))


# client connection declaration
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.username_pw_set(username, password)
client.connect(broker_ip, broker_port_no, 60)


def client_loop():
    client.loop_forever()


def plot_resource_util():
    global mem
    global store
    global cpu

    try:
        plot_cpu()
        plot_mem()
        plot_storage()
        plot_net()
        fig.suptitle('Resource Utilization (CPU|MEMORY|STORAGE|NETWORK)')
    except Exception as e:
        print(e)


def draw_loop():
    while True:
        drawnow(plot_resource_util)


def plot_mem():
    global mem

    ax1.grid(True, color='k')
    ax1.plot(mem, linewidth=5, label='Memory', color='r')
    ax1.set_ylabel('Utilization in percentage')
    ax1.set_title('Memory Utilization')
    ax1.legend()
    plt.subplot(ax1)


def plot_cpu():
    global cpu

    ax2.grid(True, color='k')
    ax2.plot(cpu, linewidth=5, label='CPU', color='g')
    ax2.set_title('CPU Utilization')
    ax2.legend()
    plt.subplot(ax2)


def plot_storage():
    global store

    ax3.grid(True, color='k')
    ax3.plot(store, linewidth=5, label='Storage', color='m')
    ax3.set_title('Storage Utilization')
    ax3.legend()
    plt.subplot(ax3)


def plot_net():
    global store

    ax4.grid(True, color='k')
    ax4.plot(net, linewidth=5, label='Network', color='c')
    ax4.set_title('Network Utilization')
    ax4.legend()
    plt.subplot(ax4)


def start():
    h1 = Thread(target=client_loop)
    h1.start()
    time.sleep(2)
    h2 = Thread(target=draw_loop())
    h2.start()


def main():
    try:
        start()
    except KeyboardInterrupt:
        cmd = "echo 'cpu {}' > data/data.txt".format(cpu)
        os.system(cmd)
        cmd = "echo 'net {}' >> data/data.txt".format(net)
        os.system(cmd)
        cmd = "echo 'store {}' >> data/data.txt".format(store)
        os.system(cmd)
        cmd = "echo 'mem {}' >> data/data.txt".format(mem)
        os.system(cmd)
        print('\n {} \n {} \n {} \n {}'.format(cpu, net, store, mem))
        print('\nProgramme terminated')


if __name__ == "__main__":
    main()
