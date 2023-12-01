# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UiDialog_ModbusDefinition.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog_ModbusDefinition(object):
    def setupUi(self, Dialog_ModbusDefinition):
        Dialog_ModbusDefinition.setObjectName("Dialog_ModbusDefinition")
        Dialog_ModbusDefinition.resize(508, 321)
        self.groupBox = QtWidgets.QGroupBox(Dialog_ModbusDefinition)
        self.groupBox.setGeometry(QtCore.QRect(20, 20, 451, 281))
        self.groupBox.setObjectName("groupBox")
        self.formLayoutWidget = QtWidgets.QWidget(self.groupBox)
        self.formLayoutWidget.setGeometry(QtCore.QRect(30, 40, 291, 191))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(self.formLayoutWidget)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.lineEdit_SlaveID = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.lineEdit_SlaveID.setObjectName("lineEdit_SlaveID")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.lineEdit_SlaveID)
        self.label_2 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.comboBox_function = QtWidgets.QComboBox(self.formLayoutWidget)
        self.comboBox_function.setObjectName("comboBox_function")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.comboBox_function)
        self.label_3 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.lineEdit_address = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.lineEdit_address.setObjectName("lineEdit_address")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.lineEdit_address)
        self.label_4 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.label_5 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_5.setObjectName("label_5")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label_5)
        self.lineEdit_quantity = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.lineEdit_quantity.setObjectName("lineEdit_quantity")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.lineEdit_quantity)
        self.lineEdit_scanRate = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.lineEdit_scanRate.setObjectName("lineEdit_scanRate")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.lineEdit_scanRate)
        self.buttonBox = QtWidgets.QDialogButtonBox(self.groupBox)
        self.buttonBox.setGeometry(QtCore.QRect(340, 50, 81, 121))
        self.buttonBox.setOrientation(QtCore.Qt.Vertical)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")

        self.retranslateUi(Dialog_ModbusDefinition)
        self.buttonBox.accepted.connect(Dialog_ModbusDefinition.accept)
        self.buttonBox.rejected.connect(Dialog_ModbusDefinition.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog_ModbusDefinition)

    def retranslateUi(self, Dialog_ModbusDefinition):
        _translate = QtCore.QCoreApplication.translate
        Dialog_ModbusDefinition.setWindowTitle(_translate("Dialog_ModbusDefinition", "Dialog"))
        self.groupBox.setTitle(_translate("Dialog_ModbusDefinition", "Modbus Definition"))
        self.label.setText(_translate("Dialog_ModbusDefinition", "Slave ID:"))
        self.label_2.setText(_translate("Dialog_ModbusDefinition", "Function:"))
        self.label_3.setText(_translate("Dialog_ModbusDefinition", "Address:"))
        self.label_4.setText(_translate("Dialog_ModbusDefinition", "Quantity:"))
        self.label_5.setText(_translate("Dialog_ModbusDefinition", "Scan Rate:"))

