
# - This script function launch the GUI to select the serial port settings and return these
# in order to start a serial communication.

import sys
from os import getcwd, path
from PyQt5 import uic, QtWidgets, QtCore
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QMessageBox, QApplication, QStyle
from PyQt5.QtCore import pyqtSignal

import platform
import serial
from serial.tools import list_ports

if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
    # High DPI Scaling
if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)
    # High DPI Icons



"""
cwd = getcwd()  # Current working directory
GuiFilePathGuiSerial = path.join(cwd, "SerialConfigWindowHighDPI.ui")  # Find Ui file
# Load the file with the GUI layout, buttons and widgets.
Ui_MainWindow, QtBaseClass = uic.loadUiType(GuiFilePathGuiSerial)
"""

class SerialConfigWindow(QtWidgets.QMainWindow):
    Status = QtCore.pyqtSignal(bool)
    SelectedParameters = QtCore.pyqtSignal(list)
        
    def __init__(self):
        

        #QtWidgets.QMainWindow.__init__(self)
        #Ui_MainWindow.__init__(self)
        # self.setupUi(self)
        super(SerialConfigWindow, self).__init__()
        loadUi('SerialConfigWindowHighDPI.ui', self)
        self.setWindowModality(QtCore.Qt.ApplicationModal)  # Any window can be edited if this is open
        
        self.setWindowIcon(self.style().standardIcon(getattr(QStyle, 'SP_ComputerIcon')))
        self.setFixedSize(self.size())
        
        OS = platform.system() + ' ' + platform.release()
        self.OSlabel.setText(OS)
        
        self.Brate = 0
        self.port = ''
        
        
        self.RetryButton.setEnabled(False)
        self.RetryButton.setVisible(False)
        
        Lp = self.portsavailable()
        if len(Lp)>0:
            self.AvaPortlbl.setText('Select an available port:')
            self.ListPort.addItems(Lp)
            self.RetryButton.setEnabled(False)
            self.RetryButton.setVisible(False)
        else:
            self.AvaPortlbl.setText('There aren\'t available ports:')
            self.OkButton.setEnabled(False)
            self.RetryButton.setEnabled(True)
            self.RetryButton.setVisible(True)
            
        # Connections to functions.            
        self.ListPort.itemSelectionChanged.connect(self.selectionChanged)
        self.OkButton.clicked.connect(self.on_Okclick)
        self.CancellButtom.clicked.connect(self.on_Cancellclick)
        self.RetryButton.clicked.connect(self.on_Retryclick)

        
    def portsavailable(self):
        Ports = serial.tools.list_ports.comports()
        Lp = []  # Listport
        for element in Ports:
            Lp.append(element.device)
        return Lp
        
    def selectionChanged(self):
        self.port = self.ListPort.currentItem().text()
        self.OkButton.setEnabled(True)
        self.OkButton.setFocus(True)
        self.OkButton.setDefault(True)

    def on_Okclick(self):

        if self.B9600.isChecked():
            self.Brate = 9600
        elif self.B14400.isChecked():
            self.Brate = 14400
        elif self.B19200.isChecked():
            self.Brate = 19200
        elif self.B38400.isChecked():
            self.Brate = 38400
        elif self.B57600.isChecked():
            self.Brate = 57600
        else:  # if (self.B115200.isChecked()):
            self.Brate = 115200
        #print(self.port, self.Brate)
        self.close()
        self.Status.emit(True)
        self.SelectedParameters.emit([self.port, self.Brate])
        
    def on_Cancellclick(self):
        self.Brate = 0
        self.port = ''
        self.close()
        print('The serial parameters were not configured')
        self.Status.emit(False)

    def on_Retryclick(self):
        Answer = QMessageBox.question(self, "Scan ports.", "Do you want to scan ports again?",
                                      QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if Answer == QMessageBox.Yes: 
            Lp = self.portsavailable()
            if len(Lp) > 0:
                self.AvaPortlbl.setText('Select an available port:')
                self.ListPort.addItems(Lp)
                self.RetryButton.setEnabled(False)
                self.RetryButton.setVisible(False)
            else:
                self.AvaPortlbl.setText('There aren\'t available ports:')
                self.OkButton.setEnabled(False)
                self.RetryButton.setEnabled(True)
                self.RetryButton.setVisible(True)
        else: 
            self.close()
            print('The serial parameters were not configured')

def main():
    app = QApplication(sys.argv)
    window = SerialConfigWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
