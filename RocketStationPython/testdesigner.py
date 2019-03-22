from PyQt5 import QtWidgets, QtCore, QtWidgets

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtWidgets.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtWidgets.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtWidgets.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):

        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(1200, 600)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))

        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_6.setObjectName(_fromUtf8("verticalLayout_6"))

        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))

        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setEnabled(True)

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())

        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setMinimumSize(QtCore.QSize(215, 500))
        self.groupBox.setMaximumSize(QtCore.QSize(16777215, 500))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))

        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_5.setObjectName(_fromUtf8("verticalLayout_5"))
        
        '''self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setSpacing(6)
        self.verticalLayout_2.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))

        self.label_SampleTime = QtWidgets.QLabel(self.groupBox)
        self.label_SampleTime.setMaximumSize(QtCore.QSize(16777215, 20))
        self.label_SampleTime.setObjectName(_fromUtf8("label_SampleTime"))

        self.verticalLayout_2.addWidget(self.label_SampleTime)
        self.SampleTime = QtWidgets.QComboBox(self.groupBox)
        self.SampleTime.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.SampleTime.setObjectName(_fromUtf8("SampleTime"))
        self.SampleTime.addItem(_fromUtf8(""))
        self.SampleTime.addItem(_fromUtf8(""))
        self.SampleTime.addItem(_fromUtf8(""))
        self.verticalLayout_2.addWidget(self.SampleTime)
        
        self.verticalLayout_5.addLayout(self.verticalLayout_2)
        spacerItem = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_5.addItem(spacerItem)
        '''

        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label_Sensor = QtWidgets.QLabel(self.groupBox)
        self.label_Sensor.setObjectName(_fromUtf8("label_Sensor"))
        self.verticalLayout.addWidget(self.label_Sensor)
        self.check_Temp = QtWidgets.QCheckBox(self.groupBox)
        self.check_Temp.setObjectName(_fromUtf8("check_Temp"))
        self.check_Temp.setChecked(True)
        self.verticalLayout.addWidget(self.check_Temp)
        self.check_Press = QtWidgets.QCheckBox(self.groupBox)
        self.check_Press.setObjectName(_fromUtf8("check_Press"))
        self.check_Press.setChecked(True)
        self.verticalLayout.addWidget(self.check_Press)
        self.check_Thr = QtWidgets.QCheckBox(self.groupBox)
        self.check_Thr.setObjectName(_fromUtf8("check_Thr"))
        self.check_Thr.setChecked(True)
        self.verticalLayout.addWidget(self.check_Thr)
        
        self.verticalLayout_5.addLayout(self.verticalLayout)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_5.addItem(spacerItem1)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.label_SaveDataFormat = QtWidgets.QLabel(self.groupBox)
        
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_SaveDataFormat.sizePolicy().hasHeightForWidth())
        
        self.label_SaveDataFormat.setSizePolicy(sizePolicy)
        self.label_SaveDataFormat.setObjectName(_fromUtf8("label_SaveDataFormat"))
        self.verticalLayout_3.addWidget(self.label_SaveDataFormat)
        self.OutFormat = QtWidgets.QComboBox(self.groupBox)
        self.OutFormat.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.OutFormat.setObjectName(_fromUtf8("OutFormat"))
        self.OutFormat.addItem(_fromUtf8(""))
        self.OutFormat.addItem(_fromUtf8(""))
        self.verticalLayout_3.addWidget(self.OutFormat)
        self.verticalLayout_5.addLayout(self.verticalLayout_3)
        
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_5.addItem(spacerItem2)

        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))

        self.label_CountDown = QtWidgets.QLabel(self.groupBox)
        self.label_CountDown.setObjectName(_fromUtf8("label_CountDown"))
        self.verticalLayout_4.addWidget(self.label_CountDown)

        self.CountDown_Box = QtWidgets.QComboBox(self.groupBox)
        self.CountDown_Box.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.CountDown_Box.setObjectName(_fromUtf8("CountDown_Box"))
        self.CountDown_Box.addItem(_fromUtf8(""))
        self.CountDown_Box.addItem(_fromUtf8(""))
        self.CountDown_Box.addItem(_fromUtf8(""))
        self.verticalLayout_4.addWidget(self.CountDown_Box)
        self.verticalLayout_5.addLayout(self.verticalLayout_4)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_5.addItem(spacerItem3)
        self.Communication = QtWidgets.QPushButton(self.groupBox)
        self.Communication.setObjectName(_fromUtf8("Communication"))
        self.verticalLayout_5.addWidget(self.Communication)
        self.horizontalLayout_2.addWidget(self.groupBox)
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.groupBox_2)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.mpl_1 = MplWidget(self.groupBox_2)
        self.mpl_1.setObjectName(_fromUtf8("mpl_1"))
        self.horizontalLayout_3.addWidget(self.mpl_1)
        self.horizontalLayout_2.addWidget(self.groupBox_2)
        self.verticalLayout_6.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.groupBox_3 = QtWidgets.QGroupBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_3.sizePolicy().hasHeightForWidth())
        self.groupBox_3.setSizePolicy(sizePolicy)
        self.groupBox_3.setObjectName(_fromUtf8("groupBox_3"))
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.groupBox_3)
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.Feedback = QtWidgets.QLabel(self.groupBox_3)
        self.Feedback.setFrameShape(QtWidgets.QFrame.Panel)
        self.Feedback.setFrameShadow(QtWidgets.QFrame.Plain)
        self.Feedback.setLineWidth(3)
        self.Feedback.setMidLineWidth(0)
        self.Feedback.setTextFormat(QtCore.Qt.AutoText)
        self.Feedback.setObjectName(_fromUtf8("Feedback"))
        self.horizontalLayout_5.addWidget(self.Feedback)
        self.horizontalLayout.addWidget(self.groupBox_3)
        self.groupBox_4 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_4.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_4.sizePolicy().hasHeightForWidth())
        self.groupBox_4.setSizePolicy(sizePolicy)
        self.groupBox_4.setMinimumSize(QtCore.QSize(350, 80))
        self.groupBox_4.setBaseSize(QtCore.QSize(0, 0))
        self.groupBox_4.setObjectName(_fromUtf8("groupBox_4"))
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.groupBox_4)
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.Fire = QtWidgets.QPushButton(self.groupBox_4)
        self.Fire.setObjectName(_fromUtf8("Fire"))
        self.horizontalLayout_4.addWidget(self.Fire)
        self.Stop = QtWidgets.QPushButton(self.groupBox_4)
        self.Stop.setObjectName(_fromUtf8("Stop"))
        self.horizontalLayout_4.addWidget(self.Stop)
        self.verticalLayout_7 = QtWidgets.QVBoxLayout()
        self.verticalLayout_7.setObjectName(_fromUtf8("verticalLayout_7"))
        self.label_D1 = QtWidgets.QLabel(self.groupBox_4)
        self.label_D1.setObjectName(_fromUtf8("label_D1"))
        self.verticalLayout_7.addWidget(self.label_D1)
        self.Led = QtWidgets.QLabel(self.groupBox_4)
        self.Led.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.Led.setFrameShadow(QtWidgets.QFrame.Raised)
        self.Led.setText(_fromUtf8(""))
        self.Led.setObjectName(_fromUtf8("Led"))
        self.verticalLayout_7.addWidget(self.Led)
        self.horizontalLayout_4.addLayout(self.verticalLayout_7)
        self.verticalLayout_8 = QtWidgets.QVBoxLayout()
        self.verticalLayout_8.setObjectName(_fromUtf8("verticalLayout_8"))
        self.label_D2 = QtWidgets.QLabel(self.groupBox_4)
        self.label_D2.setObjectName(_fromUtf8("label_D2"))
        self.verticalLayout_8.addWidget(self.label_D2)
        self.lcdNumber = QtWidgets.QLCDNumber(self.groupBox_4)
        self.lcdNumber.setFrameShape(QtWidgets.QFrame.Box)
        self.lcdNumber.setLineWidth(1)
        self.lcdNumber.setMidLineWidth(1)
        self.lcdNumber.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.lcdNumber.setObjectName(_fromUtf8("lcdNumber"))
        self.verticalLayout_8.addWidget(self.lcdNumber)
        self.horizontalLayout_4.addLayout(self.verticalLayout_8)
        self.horizontalLayout.addWidget(self.groupBox_4)
        self.verticalLayout_6.addLayout(self.horizontalLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1015, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):

        MainWindow.setWindowTitle(_translate("MainWindow", _fromUtf8("Estación de Medición"), None))
        self.groupBox.setTitle(_translate("MainWindow", "Parámetros de entrada", None))

        '''self.label_SampleTime.setText(_translate("MainWindow", "Tiempo de muestreo (ms):", None))
        self.SampleTime.setItemText(0, _translate("MainWindow", "300", None))
        self.SampleTime.setItemText(1, _translate("MainWindow", "400", None))
        self.SampleTime.setItemText(2, _translate("MainWindow", "500", None))'''

        self.label_Sensor.setText(_translate("MainWindow", "Sensores", None))
        self.check_Temp.setText(_translate("MainWindow", "Temperatura", None))
        self.check_Press.setText(_translate("MainWindow", "Presión", None))
        self.check_Thr.setText(_translate("MainWindow", "Empuje", None))

        self.label_SaveDataFormat.setText(_translate("MainWindow", "Formato de salida:", None))
        self.OutFormat.setItemText(0, _translate("MainWindow", "Excel (.csv)", None))
        self.OutFormat.setItemText(1, _translate("MainWindow", "Text (.txt)", None))

        self.label_CountDown.setText(_translate("MainWindow", "Tiempo cuenta regresiva (s):", None))
        self.CountDown_Box.setItemText(0, _translate("MainWindow", "10", None))
        self.CountDown_Box.setItemText(1, _translate("MainWindow", "20", None))
        self.CountDown_Box.setItemText(2, _translate("MainWindow", "30", None))

        self.Communication.setText(_translate("MainWindow", "Inicio de comunicación", None))

        self.groupBox_2.setTitle(_translate("MainWindow", "Gráficas", None))

        self.groupBox_3.setTitle(_translate("MainWindow", "Visualización de estado", None))
        self.Feedback.setText(_translate("MainWindow", "Bienvenido al banco de pruebas", None))
        
        self.groupBox_4.setTitle(_translate("MainWindow", "Control de ignición", None))
        self.Fire.setText(_translate("MainWindow", "Ignición", None))
        self.Stop.setText(_translate("MainWindow", "Stop", None))

        self.label_D1.setText(_translate("MainWindow", "Midiendo", None))
        self.label_D2.setText(_translate("MainWindow", "Cuenta regresiva", None))

from mplwidget import MplWidget

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
