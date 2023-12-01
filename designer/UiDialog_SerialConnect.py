# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UiDialog_SerialConnect.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog_SerialConnect(object):
    def setupUi(self, Dialog_SerialConnect):
        Dialog_SerialConnect.setObjectName("Dialog_SerialConnect")
        Dialog_SerialConnect.resize(528, 257)
        self.groupBox = QtWidgets.QGroupBox(Dialog_SerialConnect)
        self.groupBox.setGeometry(QtCore.QRect(10, 10, 501, 231))
        self.groupBox.setObjectName("groupBox")
        self.formLayoutWidget = QtWidgets.QWidget(self.groupBox)
        self.formLayoutWidget.setGeometry(QtCore.QRect(20, 30, 281, 161))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.comboBox_port = QtWidgets.QComboBox(self.formLayoutWidget)
        self.comboBox_port.setObjectName("comboBox_port")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.comboBox_port)
        self.label = QtWidgets.QLabel(self.formLayoutWidget)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.label_2 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.comboBox_bitRate = QtWidgets.QComboBox(self.formLayoutWidget)
        self.comboBox_bitRate.setObjectName("comboBox_bitRate")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.comboBox_bitRate)
        self.label_3 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.comboBox_dataLength = QtWidgets.QComboBox(self.formLayoutWidget)
        self.comboBox_dataLength.setObjectName("comboBox_dataLength")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.comboBox_dataLength)
        self.label_4 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.comboBox_stopBit = QtWidgets.QComboBox(self.formLayoutWidget)
        self.comboBox_stopBit.setObjectName("comboBox_stopBit")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.comboBox_stopBit)
        self.label_5 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_5.setObjectName("label_5")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label_5)
        self.comboBox_paritySet = QtWidgets.QComboBox(self.formLayoutWidget)
        self.comboBox_paritySet.setObjectName("comboBox_paritySet")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.comboBox_paritySet)
        self.buttonBox = QtWidgets.QDialogButtonBox(self.groupBox)
        self.buttonBox.setGeometry(QtCore.QRect(340, 60, 131, 91))
        self.buttonBox.setOrientation(QtCore.Qt.Vertical)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")

        self.retranslateUi(Dialog_SerialConnect)
        QtCore.QMetaObject.connectSlotsByName(Dialog_SerialConnect)

    def retranslateUi(self, Dialog_SerialConnect):
        _translate = QtCore.QCoreApplication.translate
        Dialog_SerialConnect.setWindowTitle(_translate("Dialog_SerialConnect", "SerialConnect"))
        self.groupBox.setTitle(_translate("Dialog_SerialConnect", "Serial port setup"))
        self.label.setText(_translate("Dialog_SerialConnect", "Prot:"))
        self.label_2.setText(_translate("Dialog_SerialConnect", "Bit rate:"))
        self.label_3.setText(_translate("Dialog_SerialConnect", "Data length:"))
        self.label_4.setText(_translate("Dialog_SerialConnect", "Stop bit:"))
        self.label_5.setText(_translate("Dialog_SerialConnect", "Parity set:"))

