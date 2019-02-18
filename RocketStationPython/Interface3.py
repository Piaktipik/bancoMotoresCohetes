
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import (QWidget, QLCDNumber, QSlider, QVBoxLayout, QApplication)
import matplotlib as mpl
mpl.use('Agg')
import testdesigner
import time
import csv

class RocketInterface(QMainWindow, testdesigner.Ui_MainWindow):

    def __init__(self, parent = None):
        super(RocketInterface, self).__init__(parent)
        self.setupUi(self)

        self.Sampling_Time = '500'
        self.CountDown_Value = 10
        self.Save_Format = "txt"
        self.CountDownTimer = QTimer()
        self.Led.setStyleSheet('QLabel {background-color: #ef0e0e; color: red;}')
        #self.Feedback.setStyleSheet('QLabel {background-color: #ffffff; color: white;}')
        self.Feedback.setText('Bienvenido al banco de pruebas')

        #self.clicked.connect(self.Fire, SIGNAL("clicked()"), self.colorC)
        self.Fire.clicked.connect(self.colorC)
        #connect the button to the start method ...
        #self.connect(self.Fire, SIGNAL("clicked()"), self.CountDownDisplay)
        #self.connect(self.Stop, SIGNAL("clicked()"), self.Detener)
        self.Stop.clicked.connect(self.Detener)
        self.Fire.clicked.connect(self.CountDownDisplay)
        self.SampleTime.currentIndexChanged.connect(self.currentIndexChanged1)
        self.OutFormat.currentIndexChanged.connect(self.currentIndexChanged2)
        self.CountDown_Box.currentIndexChanged.connect(self.currentIndexChanged3)
        self.check_Temp.stateChanged.connect(self.state_changed1)
        self.check_Press.stateChanged.connect(self.state_changed2)
        self.check_Thr.stateChanged.connect(self.state_changed3)
        #self.connect(self.Communication, SIGNAL("clicked()"), self.CommunicationTest)
        self.Communication.clicked.connect(self.CommunicationTest)

        #... and the timer to the update method
        self.CountDownTimer.timeout.connect(self.updateTimerDisplay)

        self.testdato = 10

    def colorC(self):
        self.Led.setStyleSheet('QLabel {background-color: #0eef61 ; color: red;}')
        #        self.mpl_1.PlotData(1)0eef61

    def CommunicationTest(self):
        self.mpl_1.Data.CheckCommunication()
        self.Feedback.setText(self.mpl_1.Data.Message)

    def Detener(self):
        self.mpl_1.PlotData(1,0)
        self.mpl_1.PlotData(2,0)
        self.mpl_1.PlotData(3,0)
        self.Led.setStyleSheet('QLabel {background-color: #ef0e0e ; color: red;}')
        self.SaveData()

    def currentIndexChanged1(self, index):
        SampleTimes = ['300','400','500']
        self.Sampling_Time = SampleTimes[index]
        #self.lcdNumber.display(1)

    def currentIndexChanged2(self, index):
        SampleTimes = ['txt','csv']
        self.Save_Format = SampleTimes[index]

    def currentIndexChanged3(self, index):
        CountDownValue = [10,20,30]
        self.CountDown_Value = CountDownValue[index]

    def state_changed1(self, int):
        if self.check_Temp.isChecked():
            self.mpl_1.CheckData(1,1)
        else:
            self.mpl_1.CheckData(1,0)

    def state_changed2(self, int):
        if self.check_Press.isChecked():
            self.mpl_1.CheckData(2,1)
        else:
            self.mpl_1.CheckData(2,0)

    def state_changed3(self, int):
        if self.check_Thr.isChecked():
            self.mpl_1.CheckData(3,1)
        else:
            self.mpl_1.CheckData(3,0)


    def CountDownDisplay(self):
        self.CountDownTimer.start(1000)

    def updateTimerDisplay(self):
        self.CountDown_Value -= 1

        self.lcdNumber.display(self.CountDown_Value)
        if self.CountDown_Value == 0:
            self.CountDownTimer.stop()
            self.CountDown_Value=10
            self.CountDownEnd()

    def CountDownEnd(self):
        self.Feedback.setText('Midiendo...')
        self.mpl_1.Data.StartCommunication(self.Sampling_Time)
        self.mpl_1.PlotData(1,1)
        self.mpl_1.PlotData(2,1)
        self.mpl_1.PlotData(3,1)

    def SaveData(self):
        if (self.Save_Format == 'txt'):
            file = open('Datos-'+time.strftime("%d-%m-%Y")+'-'+time.strftime("%H-%M-%S")+'.txt','w')
            for index in range(len(self.mpl_1.Data.X_Press)):
                file.write(str(self.mpl_1.Data.X_Press[index]) + " " + str(self.mpl_1.Data.Y_Press[index]) + " " + str(self.mpl_1.Data.Y_Temp[index]) + " " + str(self.mpl_1.Data.Y_Thr[index]) + "\n")

            file.close()

        elif (self.Save_Format == 'csv'):
            with open('Datos-'+time.strftime("%d-%m-%Y")+'-'+time.strftime("%H-%M-%S")+'.csv', 'w') as f:
                writer = csv.writer(f, delimiter=',')
                writer.writerows(list(zip(self.mpl_1.Data.X_Press, self.mpl_1.Data.Y_Press, self.mpl_1.Data.Y_Temp, self.mpl_1.Data.Y_Thr)))

            f.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    frame = RocketInterface()
    frame.show()
    sys.exit(app.exec_())
