# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from UiMainDesk import Ui_MainWindow
from Table import TableSubwindow
from modbus_tk import modbus_rtu
from RunDialog_SerialConnect import Serial_set
from RunDialog_ModbusDefinition import Modbus_definition
import serial
import json
from tuya_api.openapi import TuyaOpenAPI



class MainDesk(QMainWindow, Ui_MainWindow):
    tableCount = 0
    tableDefinition = []
    modbus_conn = {}
    cbox_conn = {}
    last_file_path = None
    # 定义一个信号

    def __init__(self, parent=None):
        super(MainDesk, self).__init__(parent)
        self.setupUi(self)
        self.setAcceptDrops(True)
        # 设定标题和子窗口
        self.setWindowTitle("数据记录与分析")
        self.mdi = QMdiArea()
        self.setCentralWidget(self.mdi)
        # 工具栏设定
        bar = self.menuBar()
        # file菜单
        self.file = bar.addMenu("File")
        self.file.addAction("New")
        self.open = QAction("Open", self)
        self.file.addAction(self.open)
        self.save = QAction("Save", self)
        self.file.addAction(self.save)
        self.saveAs = QAction("Save as", self)
        self.file.addAction(self.saveAs)
        self.file.addSeparator()
        self.file.addAction("Close")
        # modbus菜单
        self.ModbusRTU = bar.addMenu("ModbusRTU")
        self.modbusConn = QAction("Connect", self)
        self.ModbusRTU.addAction(self.modbusConn)
        self.modbusDisconn = QAction("Disconnect", self)
        self.ModbusRTU.addAction(self.modbusDisconn)
        self.modbusDisconn.setDisabled(True)
        self.ModbusRTU.addSeparator()
        self.ModbusRTU.addAction("Read/Write Definition")
        self.AutomissionStart = QAction("Automission start", self)
        self.ModbusRTU.addAction(self.AutomissionStart)
        self.AutomissionStart.setDisabled(True)
        self.AutomissionStop = QAction("Automission stop", self)
        self.ModbusRTU.addAction(self.AutomissionStop)
        self.AutomissionStop.setDisabled(True)
        # cbox菜单
        self.Cbox = bar.addMenu("C_Box")
        self.CboxConn = QAction("Connect", self)
        self.Cbox.addAction(self.CboxConn)
        self.CboxDisconn = QAction("Disconnect", self)
        self.Cbox.addAction(self.CboxDisconn)
        self.CboxDisconn.setDisabled(True)
        self.Cbox.addSeparator()
        self.Cbox.addAction("Device ID")
        self.Cbox.addAction("Set scan rate")
        # 工具栏按钮信号槽连接
        self.file.triggered.connect(self.fileAction)
        self.ModbusRTU.triggered.connect(self.ModbusRTUAction)
        self.Cbox.triggered.connect(self.CboxAction)


    def dragEnterEvent(self, e):
        """
        拖拽进入控件
        :param e:
        :return:
        """
        if e.mimeData().hasText():
            e.accept()
        else:
            e.ignore()


    def dropEvent(self, e):
        """
        拖拽释放
        :param e:
        :return:
        """
        if e.mimeData().text()[-4:] == '.tab':
            with open(e.mimeData().text()[8:], "r") as f:
                data = json.load(f)
                self.tableCount += 1
                print("table counter: ", self.tableCount)
                sub = TableSubwindow()
                sub.modbus = self.modbus_conn
                sub.Cbox = self.cbox_conn
                sub.slave_id = data['slave_id']
                sub.function_code = data['function_code']
                sub.address = data['address']
                sub.quantity = data['quantity']
                sub.scanRate = data['scanRate']
                sub.widgetSize = data['widgetSize']
                sub.file_path = e.mimeData().text()[8:]
                sub.deviceID = data['deviceID']
                sub.resetTable()
                self.mdi.addSubWindow(sub)
                sub.show()


    def fileAction(self,q):
        """
        File菜单栏功能实现
        """
        if q.text() == "New":
            self.tableCount += 1
            print("table counter: ", self.tableCount)
            sub = TableSubwindow()
            self.mdi.addSubWindow(sub)
            sub.resetTable()
            sub.modbus = self.modbus_conn
            sub.Cbox = self.cbox_conn
            sub.show()
        elif q.text() == "Open":
            fname, _ = QFileDialog.getOpenFileName(self,'Open File',self.last_file_path,'table(*.tab)')
            if fname:
                self.last_file_path = fname
                with open(fname, "r") as f:
                    data = json.load(f)
                    self.tableCount += 1
                    print("table counter: ", self.tableCount)
                    sub = TableSubwindow()
                    sub.modbus = self.modbus_conn
                    sub.Cbox = self.cbox_conn
                    sub.slave_id = data['slave_id']
                    sub.function_code = data['function_code']
                    sub.address = data['address']
                    sub.quantity = data['quantity']
                    sub.scanRate = data['scanRate']
                    sub.widgetSize = data['widgetSize']
                    sub.file_path = fname
                    sub.deviceID = data['deviceID']
                    sub.resetTable()
                    self.mdi.addSubWindow(sub)
                    sub.show()
        elif q.text() == "Save":
            selected_sub_window = self.mdi.currentSubWindow()
            if selected_sub_window != None:
                if selected_sub_window.file_path == None:
                    selected_sub_window.file_path, _ = QFileDialog.getSaveFileName(None, "Save File", self.last_file_path, "All Files (*.tab);;Config Files (*.tab)")
                if selected_sub_window.file_path:
                    self.last_file_path = selected_sub_window.file_path
                    with open(selected_sub_window.file_path, "w") as f:
                        data = {'slave_id': selected_sub_window.slave_id}
                        data['function_code'] = selected_sub_window.function_code
                        data['address'] = selected_sub_window.address
                        data['quantity'] = selected_sub_window.quantity
                        data['scanRate'] = selected_sub_window.scanRate
                        data['widgetSize'] = selected_sub_window.widgetSize
                        data['file_path'] = selected_sub_window.file_path
                        data['deviceID'] = selected_sub_window.deviceID
                        json.dump(data, f)
        elif q.text() == "Save as":
            selected_sub_window = self.mdi.currentSubWindow()
            if selected_sub_window != None:
                selected_sub_window.file_path, _ = QFileDialog.getSaveFileName(None, "Save File", self.last_file_path, "All Files (*.tab);;Config Files (*.tab)")
                if selected_sub_window.file_path:
                    self.last_file_path = selected_sub_window.file_path
                    with open(selected_sub_window.file_path, "w") as f:
                        data = {'slave_id': selected_sub_window.slave_id}
                        data['function_code'] = selected_sub_window.function_code
                        data['address'] = selected_sub_window.address
                        data['quantity'] = selected_sub_window.quantity
                        data['scanRate'] = selected_sub_window.scanRate
                        data['widgetSize'] = selected_sub_window.widgetSize
                        data['file_path'] = selected_sub_window.file_path
                        data['deviceID'] = selected_sub_window.deviceID
                        json.dump(data, f)
        elif q.text() == "Close":
            self.close()


    def ModbusRTUAction(self,q):
        """
        ModbusRTU菜单栏功能实现
        """
        if q.text() == "Connect":
            result, parameter = Serial_set.getParameter()
            if result == True:
                self.mSerial = serial.Serial()
                self.mSerial.port = parameter['port']
                self.mSerial.baudrate = int(parameter['baudrate'])
                self.mSerial.bytesize = int(parameter['bytesize'])
                self.mSerial.parity = parameter['parity']
                self.mSerial.stopbits = float(parameter['stopbits'])
                self.mSerial.xonxoff = 0
                try:
                    # modbus建立连接
                    self.modbus_conn['master'] = modbus_rtu.RtuMaster(self.mSerial)
                except:
                    QMessageBox.warning(self, '警告', '端口连接失败', QMessageBox.Yes, QMessageBox.Yes)
                else:
                    self.modbusConn.setDisabled(True)
                    self.modbusDisconn.setEnabled(True)
                    self.Cbox.setDisabled(True)

        elif q.text() == "Disconnect":
            self.modbusConn.setEnabled(True)
            self.modbusDisconn.setDisabled(True)
            self.AutomissionStart.setEnabled(True)
            self.Cbox.setEnabled(True)
            self.modbus_conn.clear()

        elif q.text() == "Read/Write Definition":
            selected_sub_window = self.mdi.currentSubWindow()
            if selected_sub_window != None:
                print(selected_sub_window)
                modbusFunc = Modbus_definition()
                modbusFunc.lineEdit_SlaveID.setText(str(selected_sub_window.slave_id))
                modbusFunc.comboBox_function.setCurrentIndex(selected_sub_window.function_code-1);
                modbusFunc.lineEdit_address.setText(str(selected_sub_window.address))
                modbusFunc.lineEdit_quantity.setText(str(selected_sub_window.quantity))
                modbusFunc.lineEdit_scanRate.setText(str(selected_sub_window.scanRate))
                result = modbusFunc.exec()
                if  result == True:
                    selected_sub_window.slave_id = int(modbusFunc.lineEdit_SlaveID.text())
                    selected_sub_window.function_code = int(modbusFunc.lineEdit_SlaveID.text())+1
                    selected_sub_window.address = int(modbusFunc.lineEdit_address.text())
                    selected_sub_window.quantity = int(modbusFunc.lineEdit_quantity.text())
                    selected_sub_window.scanRate = int(modbusFunc.lineEdit_scanRate.text())
                    selected_sub_window.resetTable()

        elif q.text() == "Automission start":
            self.AutomissionStart.setDisabled(True)
            self.AutomissionStop.setEnabled(True)
            pass

        elif q.text() == "Automission stop":
            self.AutomissionStart.setEnabled(True)
            self.AutomissionStop.setDisabled(True)
            pass


    def CboxAction(self, q):
        """
        Cbox菜单栏功能实现
        """
        # 建立连接
        if q.text() == "Connect":
            # 读取配置文件
            with open('../config.json', 'r', encoding='utf8') as fp:
                config_data = json.load(fp)
                try:
                    # 连接涂鸦网
                    self.cbox_conn['master'] = TuyaOpenAPI(config_data['Cbox']['URL_BASE'], config_data['Cbox']['CLIENT_ID'], config_data['Cbox']['CLIENT_SECRET'], 'en')
                except:
                    pass
                else:
                    self.ModbusRTU.setDisabled(True)
                    self.CboxDisconn.setEnabled(True)
                    self.CboxConn.setDisabled(True)
                fp.close()
        # 断开连接
        elif q.text() == "Disconnect":
            self.cbox_conn.clear()
            self.ModbusRTU.setEnabled(True)
            self.CboxDisconn.setDisabled(True)
            self.CboxConn.setEnabled(True)
            for i in self.mdi.subWindowList():
                print(i)
                i.resetTable()
        # 修改表格
        elif q.text() == "Device ID":
            text, ok = QInputDialog.getText(self, 'Device ID input', 'Device ID')
            if ok and text:
                selected_sub_window = self.mdi.currentSubWindow()
                selected_sub_window.deviceID = text
                selected_sub_window.CboxInit = False
        # 修改扫描时间
        elif q.text() == "Set scan rate":
            num, ok = QInputDialog.getInt(self, 'Set scan rate in ms', 'Scan Rate',  value=1000, min=1000)
            if ok and num:
                selected_sub_window = self.mdi.currentSubWindow()
                selected_sub_window.scanRate = num
                selected_sub_window.CboxInit = False





if __name__ == '__main__':
    # 创建QApplication类的实例
    app = QApplication(sys.argv)
    # 创建一个窗口
    MainDesk = MainDesk()
    # 显示窗口
    MainDesk.show()
    sys.exit(app.exec_())
