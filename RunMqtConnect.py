# -*- coding: utf-8 -*-

import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from MQT_Setup import *
import random
from paho.mqtt import client as mqtt_client


broker = "1c570066c5.imwork.net"
port = 51686
client_id = f"python-mqtt-{random.randint(0, 1000)}"
username = "test"  # 如果 broker 需要鉴权，设置用户名密码
password = "test"
topic1 = "srdc/lab/xct9/1/data"
topic2 = "srdc/lab/xct9/1/data1"
client = mqtt_client.Client()

class MQT_Connect(QMainWindow, Ui_MQT_Setup):
    def __init__(self):
        super(MQT_Connect, self).__init__()
        self.setupUi(self)
        # 端口号整形范围：[1, 99999]
        pIntValidator = QIntValidator(self)
        pIntValidator.setRange(1, 99999)
        self.Port_lineEdit.setValidator(pIntValidator)
        # 设定初始值
        self.Client_ID_lineEdit.setText(client_id)
        self.Host_lineEdit.setText(broker)
        self.Port_lineEdit.setText(str(port))
        self.Topic1_lineEdit.setText(topic1)
        self.Topic2_lineEdit.setText(topic2)
        self.username_lineEdit.setText(username)
        self.password_lineEdit.setText(password)
        self.connect_fail_label.setVisible(False)
        # 连接信号和槽
        self.connect_pushButton.clicked.connect(self.btn_clicked)

    def btn_clicked(self):
        global client
        client_id = self.Client_ID_lineEdit.text()+f"-{random.randint(0, 1000)}"
        broker = self.Host_lineEdit.text()
        port = int(self.Port_lineEdit.text())
        topic1 = self.Topic1_lineEdit.text()
        topic2 = self.Topic2_lineEdit.text()
        username = self.username_lineEdit.text()
        password = self.password_lineEdit.text()
        client.loop_stop()
        client.reinitialise(client_id)
        client.username_pw_set(username, password)
        client.on_connect = on_connect
        client.on_connect_fail = on_connect_fail
        client.on_disconnect = on_disconnect
        client.connect(broker, port)
        client.loop_start()


class MQTT_Singal(QObject):
    on_connect_msg = pyqtSignal()
    on_connect_fail_msg = pyqtSignal()
    on_disconnect_msg = pyqtSignal()
    on_message = pyqtSignal(object)

mqtt_signal =  MQTT_Singal()
def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT Broker!\n")
    client.subscribe(topic1)
    client.subscribe(topic2)
    client.on_message = on_message
    mqtt_signal.on_connect_msg.emit()

def on_connect_fail(client, userdata, flags, rc):
    print("Failed to connect, return code!\n")
    mqtt_signal.on_connect_fail_msg.emit()

def on_disconnect(client, userdata, flags):
    print("on_disconnect, return code!\n")
    client.disconnect()
    client.loop_stop()
    mqtt_signal.on_disconnect_msg.emit()

def on_message(client, userdata, msg):
    # print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
    mqtt_signal.on_message.emit(msg)




def publish(client, topic, msg):
    result = client.publish(topic, msg)
    # print(result)



# data = {'onoff': 0}

# if __name__ == "__main__":
#     client = connect_mqtt()
#     subscribe(client)
#     client.loop_start()
#
#     while True:
#         time.sleep(5)
#         if data["onoff"] == 0:
#             data["onoff"] = 1
#         else:
#             data["onoff"] = 0








