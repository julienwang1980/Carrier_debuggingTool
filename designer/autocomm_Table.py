# -*- coding: utf-8 -*-

import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import modbus_tk.defines as cst
from PyQt5.QtCore import QTimer
import struct
from openpyxl import Workbook, load_workbook
from openpyxl.utils import get_column_letter, column_index_from_string
from openpyxl.styles import Alignment

class AutocommTableSubwindow(QMdiSubWindow, ):
    wb = None
    modbus = None
    scanRate = 5000
    widgetSize = {"width": 250, "height": 150}
    odus = []
    idus = []
    err_code = {'100101': '配置率超上限', '100102': '配置率超下限', '100201': '环境温度超上限', '100202': '环境温度超下限',
                '100301': '外机风机异常', '100401': '压缩机启动异常', '100501': '手阀未开启', '100601': '主阀动作异常',
                '100701': '四通阀动作异常', '200101': '内机EXV异常', '200102': '内机风机异常', '200103': '内机风机过半异常',
                '300101': '系统高压报警', '300102': '系统低压报警', '300103':'排气温度过高', '300104': '驱动器温度过高'}


    def __init__(self):
        super(AutocommTableSubwindow, self).__init__()
        self.resize(self.widgetSize["width"], self.widgetSize["height"])
        self.SubWinWidget = QWidget()
        self.setWidget(self.SubWinWidget)
        layout = QVBoxLayout(self.SubWinWidget)
        self.tablewidget = QTableWidget()
        self.tablewidget.setRowCount(1)
        self.tablewidget.setColumnCount(1)
        layout.addWidget(self.tablewidget)
        self.setWindowTitle("autocommisioning")
        self.tablewidget.setHorizontalHeaderLabels(['autocommi_timer'])
        self.tablewidget.resizeColumnsToContents()
        self.tablewidget.resizeRowsToContents()
        self.setLayout(layout)
        self.mTimer = QTimer()
        self.mTimer.timeout.connect(self.ReceiverPortData)
        self.mTimer.start(self.scanRate)

        # f = 0
        # z0=hex(65535)[2:]
        # z1=hex(65535)[2:]
        # z = z0+z1
        # print(z0+z1)
        # f = struct.unpack('!f', bytes.fromhex(z))[0]
        # print(f)

        # self.wb = load_workbook("../多联机调试记录表-自动调试.xlsx")
        #
        # self.wb.save("../多联机调试记录表_temp.xlsx")


        # col = column_index_from_string('bb')



    def close(self):
        self.deleteLater()


    def ReceiverPortData(self):
        # print("程序执行到文件：{}，第{}行".format(sys._getframe().f_code.co_filename, str(sys._getframe().f_lineno)))
        # print(self.wb.sheetnames)
        # odu = {'addr':0, 'HP':0, 'T3':0, 'T4':0, 'T7':0, 'T8':0, 'Pdis':0, 'Psur':0, 'Comp1':0, 'Comp2':0, 'Fan1':0, 'Fan2':0, 'MainEXV':0, 'RV':0, 'err_code':0}
        # idu = {'addr':0, 'T1':0, 'T2':0, 'T2B':0, 'IDFan_speed':0, 'ID_EXV':0, 'COMM_lost':0, 'err_code':0}
        if self.modbus:
            try:
                # Connect to the slave
                self.modbus['master'].set_timeout(1)
                self.modbus['master'].set_verbose(True)
                data = []
                for i in range(8):
                    # 读取下位机1的寄存器值，采用cst.READ_INPUT_REGISTERS，地址40000开始，长度100，数据格式为short
                    x = self.modbus['master'].execute(1, cst.READ_INPUT_REGISTERS, 40000+100*i, 100, data_format=">{}".format(100*'h'))
                    data.extend(x)
                    # print(x)
                newItem = QTableWidgetItem(str(data[0]))
                self.tablewidget.setItem(0, 0, newItem)
                # 写入excel表内
                if len(self.odus) == 0:
                    if data[0] >= 360-10:
                        for i in range(20, 100, 20):
                            if data[i] != 0:
                                odu = {}
                                odu['addr'] = int(i/20-1)
                                odu['HP'] = data[i]
                                odu['T3'] = data[i+1]/10
                                odu['T4'] = data[i+2]/10
                                odu['T7'] = data[i+3]/10
                                odu['T8'] = data[i+4]/10
                                odu['Pdis'] = data[i+5]
                                odu['Psur'] = data[i+6]
                                odu['Comp1'] = data[i+7]
                                odu['Comp2'] = data[i+8]
                                odu['Fan1'] = data[i+9]
                                odu['Fan2'] = data[i+10]
                                odu['MainEXV'] = data[i+11]
                                odu['RV'] = data[i+12]
                                odu['err_code'] = data[i+13]%1000 + data[i+13]//1000*100000
                                self.odus.append(odu)
                        for i in range(100, 800, 7):
                            if (data[i] != 0 or data[i+1] != 0 or data[i+2] != 0):
                                idu = {}
                                idu['addr'] = int((i-100)/7)
                                idu['T1'] = data[i]/10
                                idu['T2'] = data[i+1]/10
                                idu['T2B'] = data[i+2]/10
                                idu['IDFan_speed'] = data[i+3]
                                idu['ID_EXV'] = data[i+4]
                                idu['COMM_lost'] = data[i+5]
                                idu['err_code'] = data[i+6]%1000 + data[i+6]//1000*100000
                                self.idus.append(idu)
                        align = Alignment(horizontal='center', vertical='center', wrap_text=False, shrink_to_fit=False) # 居中样式
                        # 表格<详细数据-外机>表头
                        row = self.wb["详细数据-外机"]['2']
                        for i in range(1, len(self.odus)):
                            col_index = 2 + 12 * i
                            col_lett = get_column_letter(col_index)
                            self.wb["详细数据-外机"]['{}1'.format(col_lett)] = "{}#外机".format(self.odus[i]["addr"])
                            self.wb["详细数据-外机"]['{}1'.format(col_lett)].alignment = align
                            self.wb["详细数据-外机"].merge_cells(start_row=1, start_column=col_index, end_row=1, end_column=col_index+11)
                            for j in range(12):
                                col_lett = get_column_letter(col_index + j)
                                self.wb["详细数据-外机"]['{}2'.format(col_lett)] = row[j + 1].value
                                self.wb["详细数据-外机"]['{}2'.format(col_lett)].alignment = align
                        # 表格<详细数据-内机>表头
                        row = self.wb["详细数据-内机"]['2']
                        for i in range(len(self.idus)):
                            col_index = 2 + 6 * i
                            col_lett = get_column_letter(col_index)
                            self.wb["详细数据-内机"]['{}1'.format(col_lett)] = "{}#内机".format(self.idus[i]["addr"])
                            self.wb["详细数据-内机"]['{}1'.format(col_lett)].alignment = align
                            self.wb["详细数据-内机"].merge_cells(start_row=1, start_column=col_index, end_row=1, end_column=col_index+5)
                            for j in range(6):
                                col_lett = get_column_letter(col_index + j)
                                self.wb["详细数据-内机"]['{}2'.format(col_lett)] = row[j + 1].value
                                self.wb["详细数据-内机"]['{}2'.format(col_lett)].alignment = align
                    else:
                        pass


                print(self.odus)
                print(self.idus)

            except:
                print('unknown')
                print("run")

        # data1 = []
        # data1.append(-1)
        # newItem = QTableWidgetItem(str(data1[0]))
        # self.tablewidget.setItem(0, 0, newItem)
        # self.wb["调试记录表"]
        # data = []
        # for row in ws.iter_rows(min_row=3, max_row=3, min_col=2):
        #     for cell in row:
        #         data.append(cell.value)
        # wb.close()
        # self.table1.modbus = self.modbus_conn






if __name__ == '__main__':
    # 创建QApplication类的实例
    app = QApplication(sys.argv)
    # 创建一个窗口
    MainDesk = AutocommTableSubwindow()
    # 显示窗口
    MainDesk.show()
    sys.exit(app.exec_())

