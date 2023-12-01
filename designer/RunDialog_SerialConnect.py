# -*- coding: utf-8 -*-

import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import serial
import serial.tools.list_ports
import json

from UiDialog_SerialConnect import Ui_Dialog_SerialConnect

class Serial_set(QDialog, Ui_Dialog_SerialConnect):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        # 读取配置文件
        with open('../config.json', 'r', encoding='utf8') as fp:
            config_data = json.load(fp)
            fp.close()
        # 扫描可用的端口
        self.ScanComPort()
        # 设置参数下拉框
        for bitrate in config_data['serialConnect']['baudrates']:
            self.comboBox_bitRate.addItem(str(bitrate))
        self.comboBox_dataLength.addItem('8')
        self.comboBox_dataLength.addItem('7')
        self.comboBox_stopBit.addItem('1')
        self.comboBox_stopBit.addItem('1.5')
        self.comboBox_stopBit.addItem('2')
        self.parity = {'None': 'N', 'Odd': 'O', 'Even': 'E'}
        self.comboBox_paritySet.addItem('None')
        self.comboBox_paritySet.addItem('Odd')
        self.comboBox_paritySet.addItem('Even')
        # 设置下拉框当前选项
        for i in range(self.comboBox_port.count()):
            if config_data['serialConnect']['Set']['port'] == self.comboBox_port.itemText(i):
                self.comboBox_port.setCurrentIndex(i);
        for i in range(self.comboBox_bitRate.count()):
            if config_data['serialConnect']['Set']['baudrate'] == self.comboBox_bitRate.itemText(i):
                self.comboBox_bitRate.setCurrentIndex(i);
        for i in range(self.comboBox_dataLength.count()):
            if config_data['serialConnect']['Set']['bytesize'] == self.comboBox_dataLength.itemText(i):
                self.comboBox_dataLength.setCurrentIndex(i);
        for i in range(self.comboBox_paritySet.count()):
            if config_data['serialConnect']['Set']['parity'] == self.comboBox_paritySet.itemText(i):
                self.comboBox_paritySet.setCurrentIndex(i);
        for i in range(self.comboBox_stopBit.count()):
            if config_data['serialConnect']['Set']['stopbits'] == self.comboBox_stopBit.itemText(i):
                self.comboBox_stopBit.setCurrentIndex(i);
        # 设置对话按钮框
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)


    def ScanComPort(self):
        """
         扫描可用的com端口
        :return:
        """
        self.comboBox_port.clear()
        self.portDict = {}
        self.portlist = list(serial.tools.list_ports.comports())
        for port in self.portlist:
            self.comboBox_port.addItem(port.description)
            self.portDict[port.description] = port.name
        pass

    def getParameter(parent=None):
        """
        获取串口参数
        :return: 对话框结果，参数列表
        """
        setDialog = Serial_set(parent)
        result = setDialog.exec()

        mSerial = {}
        mSerial["port"] = setDialog.portDict[setDialog.comboBox_port.currentText()]
        mSerial["baudrate"] = setDialog.comboBox_bitRate.currentText()
        mSerial["bytesize"] = setDialog.comboBox_dataLength.currentText()
        mSerial["parity"] = setDialog.parity[setDialog.comboBox_paritySet.currentText()]
        mSerial["stopbits"] = setDialog.comboBox_stopBit.currentText()
        with open('../config.json', 'r', encoding='utf8') as fp:
            config_data = json.load(fp)
            config_data['serialConnect']['Set']['port'] = setDialog.comboBox_port.currentText()
            config_data['serialConnect']['Set']['baudrate'] = setDialog.comboBox_bitRate.currentText()
            config_data['serialConnect']['Set']['bytesize'] = setDialog.comboBox_dataLength.currentText()
            config_data['serialConnect']['Set']['parity'] = setDialog.comboBox_paritySet.currentText()
            config_data['serialConnect']['Set']['stopbits'] = setDialog.comboBox_stopBit.currentText()
            fp.close()
        with open('../config.json', 'w', encoding='utf8') as fp:
            json.dump(config_data, fp, ensure_ascii=False)
            fp.close()
        return (result == QDialog.Accepted, mSerial)




if __name__ == "__main__":
    app = QApplication([])
    dialog = Serial_set()
    dialog.show()
    app.exec_()