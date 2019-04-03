# IoT Data Analysis
Generating IoT data and analysing the data and predicting the next sample using linear regression.

## Server preparation
```
apt update && apt upgrade -y
apt install python3-pip  
pip3 install paho-mqtt
pip3 install psutil  
```

## Client preparation
```
apt update && apt upgrade -y
apt install python3-pip
pip3 install matplotlib
pip3 install drawnow
pip3 install paho-mqtt
```

#
![Network Architecture](arch.png)

### Usage
* Run the client first `python3 iot_client.py`
    * the client subscribes to iot_data topic in the mqtt broker waiting for the server to publish data
* Run the server program `python3 iot_server.py`
    * The server publishes its resource utilization to the iot_data topic
    