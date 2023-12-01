# -*- coding: utf-8 -*-

import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


from UiDialog_ModbusDefinition import Ui_Dialog_ModbusDefinition

class Modbus_definition(QDialog, Ui_Dialog_ModbusDefinition):
    function = {'01 Read Coils': 1, '02 Read Discrete Inputs': 2, '03 ReadHolding Registers': 3, '04 Read Input Registers': 4}
    res = {}
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)


        # 设置参数下拉框
        self.comboBox_function.addItem('01 Read Coils')
        self.comboBox_function.addItem('02 Read Discrete Inputs')
        self.comboBox_function.addItem('03 ReadHolding Registers')
        self.comboBox_function.addItem('04 Read Input Registers')


        # 设置对话按钮框
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)




    def getParameter(parent=None):
        """
        获取串口参数
        :return: 对话框结果，参数列表
        """
        setDialog = Modbus_definition(parent)
        result = setDialog.exec()

        return (result == QDialog.Accepted, parent.res)




if __name__ == "__main__":
    app = QApplication([])
    dialog = Serial_set()
    dialog.show()
    app.exec_()