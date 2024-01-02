# -*- coding: utf-8 -*-

import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import modbus_tk.defines as cst
from PyQt5.QtCore import QTimer


class Table4Subwindow(QMdiSubWindow, ):
    slave_id = 1
    function_code = cst.READ_INPUT_REGISTERS
    address = 40000
    quantity = 30
    scanRate = 1000
    widgetSize = {"width": 430, "height": 730}
    file_path = None
    modbus = None
    Cbox = None
    CboxInit = False
    deviceID = "6c8fe57f6191f18c6750fi"
    isOnline = False
    pass


    def __init__(self):
        super(TableSubwindow, self).__init__()
        self.resize(self.widgetSize["width"], self.widgetSize["height"])
        self.SubWinWidget = QWidget()
        self.setWidget(self.SubWinWidget)
        layout = QVBoxLayout(self.SubWinWidget)
        self.tablewidget = QTableWidget()
        self.tablewidget.setRowCount(self.quantity)
        self.tablewidget.setColumnCount(3)
        layout.addWidget(self.tablewidget)
        self.tablewidget.setHorizontalHeaderLabels(['Alias', str(self.address), 'comments'])
        headlist = []
        for i in range(self.address, self.address+self.quantity):
            headlist.append(str(i))
        self.tablewidget.setVerticalHeaderLabels(headlist)
        self.tablewidget.resizeColumnsToContents()
        self.tablewidget.resizeRowsToContents()
        self.setLayout(layout)

        self.mTimer = QTimer()
        self.mTimer.timeout.connect(self.ReceiverPortData)
        self.mTimer.start(self.scanRate)


    def closeEvent(self,event):
        # 获取主窗口
        parent = self.parent().parent().parent()
        parent.tableCount = parent.tableCount-1
        print("table counter: ", parent.tableCount)
        self.deleteLater()


    def resetTable(self):
        self.CboxInit = False
        self.tablewidget.clear()
        self.tablewidget.setRowCount(self.quantity)
        self.tablewidget.setColumnCount(3)
        self.tablewidget.setHorizontalHeaderLabels(['Alias', str(self.address), 'comments'])
        headlist = []
        for i in range(self.address, self.address+self.quantity):
            headlist.append(str(i))
        self.tablewidget.setVerticalHeaderLabels(headlist)
        self.tablewidget.resizeColumnsToContents()
        self.tablewidget.resizeRowsToContents()
        if self.file_path:
            self.SubWinWidget.setWindowTitle(self.file_path)
        else:
            parent = self.parent().parent().parent()
            self.SubWinWidget.setWindowTitle(f"Mbpoll {str(parent.tableCount)}")
        self.mTimer.start(self.scanRate)


    def ReceiverPortData(self):
        if self.modbus:
            try:
                # Connect to the slave
                self.modbus['master'].set_timeout(1)
                self.modbus['master'].set_verbose(True)
                # 读取下位机的寄存器值，地址为4,，长度为1，采用cst.READ_INPUT_REGISTERS  与   cst.READ_HOLDING_REGISTERS方法效果是一致的
                x = self.modbus['master'].execute(1, cst.READ_INPUT_REGISTERS, self.address, self.quantity)
                print(x)  # 此处是获取的值，注意符号，本例中下位机也使用16位无符号数
                for i in range(len(x)):
                    newItem = QTableWidgetItem(str(x[i]))
                    self.tablewidget.setItem(i, 1, newItem)
            except:
                print('unknown')
                print("run")
            pass
                # print(self.modbus)
        elif self.Cbox:
            specification = []
            status = []
            # 读取变量名
            if not self.CboxInit:
                result = self.Cbox["master"].get(
                    f'/v1.0/iot-03/devices/{self.deviceID}/specification')
                if not (result['success']):
                    print(f"Get device specification failed: '{result['code']}' '{result['msg']}")
                    return
                else:
                    # print(result)
                    for i in (result['result']['status']):
                        specification.append(i['name'])
                    # 重置表格
                    self.tablewidget.setColumnCount(2)
                    self.tablewidget.setRowCount(len(specification))
                    self.tablewidget.setHorizontalHeaderLabels(['Name', ' Value '])
                    headlist = []
                    for i in range(0, self.address + self.quantity):
                        headlist.append(str(i))
                    self.tablewidget.setVerticalHeaderLabels(headlist)
                    for i in range(len(specification)):
                        newItem = QTableWidgetItem(specification[i])
                        self.tablewidget.setItem(i, 0, newItem)
                    self.tablewidget.resizeColumnsToContents()
                    self.tablewidget.resizeRowsToContents()
                    self.mTimer.start(self.scanRate)
                    self.CboxInit = True
                result.clear()
            # 判断是否在线
            result = self.Cbox["master"].get(
                f'/v2.0/cloud/thing/{self.deviceID}')
            if not (result['success']):
                print(f"Get device details failed: '{result['code']}' '{result['msg']}")
            else:
                self.isOnline = result["result"]["is_online"]
            result.clear()
            # 读取变量
            if self.isOnline:
                self.SubWinWidget.setWindowTitle(f"deviec_id: {self.deviceID}, online")
                result = self.Cbox["master"].get(
                    f'/v1.0/iot-03/devices/{self.deviceID}/status')
                if not (result['success']):
                    print(f"Get device status failed: '{result['code']}' '{result['msg']}")
                else:
                    print(result)
                    for i in (result['result']):
                        status.append(i['value'])
                    # 填入数据
                    for i in range(len(status)):
                        newItem = QTableWidgetItem(str(status[i]))
                        self.tablewidget.setItem(i, 1, newItem)
                result.clear()
            else:
                self.SubWinWidget.setWindowTitle(f"deviec_id: {self.deviceID}, offline")




if __name__ == '__main__':
    # 创建QApplication类的实例
    app = QApplication(sys.argv)
    # 创建一个窗口
    MainDesk = TableSubwindow()
    # 显示窗口
    MainDesk.show()
    sys.exit(app.exec_())

