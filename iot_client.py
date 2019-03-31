import paho.mqtt.client as mqtt
import os
from threading import Thread
from drawnow import *
import time


cpu = []
store = []
mem = []
net = []

fig = plt.figure()
ax1 = fig.add_subplot(121)
ax2 = fig.add_subplot(122)
ax3 = fig.add_subplot(221)
ax4 = fig.add_subplot(222)

os.system('clear')
print('-----------------------------------')
print('Welcome to MQTT Subscriber client ')
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
    received = str(msg.payload, 'utf-8')
    print('Publisher: ', received)
    data = received.split()  # cpu, net, mem, store
    cpu.append(data[0])
    net.append(data[1])
    mem.append(data[2])
    store.append(data[3])


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

    while True:
        try:
            plot_cpu()
            plot_mem()
            plot_storage()
            fig.suptitle('Resource Utilization (CPU|MEMORY|STORAGE)')
        except Exception as e:
            print(e)


def plot_mem():
    global mem

    ax1.grid(True, color='k')
    ax1.plot(mem, linewidth=5, label='Memory')
    ax1.set_ylabel('Utilization in percentage')
    ax1.set_title('Memory Utilization')
    ax1.legend()
    plt.subplot(ax1)


def plot_cpu():
    global cpu

    ax2.grid(True, color='k')
    ax2.plot(cpu, linewidth=5, label='CPU')
    ax2.set_xlabel('Time (scale of 2 seconds)')
    ax2.set_title('CPU Utilization')
    ax2.legend()
    plt.subplot(ax2)


def plot_storage():
    global store

    ax3.grid(True, color='k')
    ax3.plot(store, linewidth=5, label='Storage')
    ax3.set_title('Storage Utilization')
    ax3.legend()
    plt.subplot(ax3)


def plot_net():
    global store

    ax4.grid(True, color='k')
    ax4.plot(net, linewidth=5, label='Network')
    ax4.set_title('Storage Utilization')
    ax4.legend()
    plt.subplot(ax4)


def main():
    try:
        h1 = Thread(target=client_loop)
        h1.start()
        time.sleep(2)
        h2 = Thread(target=plot_resource_util)
        h2.start()
    except KeyboardInterrupt:
        print('\nProgramme terminated')


if __name__ == "__main__":
    main()
