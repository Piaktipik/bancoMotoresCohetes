import sys
from os import makedirs, getcwd, path
import time
from datetime import datetime

from PyQt5 import uic, QtWidgets, QtCore
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QMessageBox, QApplication, QStyle
# librerias para plotear
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import *
import matplotlib.pyplot as plt

import numpy as np
import serial
from serial.tools import list_ports

from GuiSerialConfig import SerialConfigWindow


# Enable High DPI display with PyQt5
if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
    # High DPI Scaling

if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)
    # High DPI Icons

    # - Iniciar clase para el conteo regresivo (Multi Thread).

class UpdateConteo(QThread):
    Ignition = pyqtSignal(bool)
    Progreso = pyqtSignal(int)
    
    def __init__(self, parent=None):
        super(UpdateConteo, self).__init__(parent)
        self.Max = 100
    
    def run(self):
        #Max = RocketInterface.TiempoRestante
        for i in range (self.Max, 0, -1):
            time.sleep(1)
            self.Progreso.emit(i-1)
            #RocketInterface.lcdConteo.display(i)

        self.Ignition.emit(True)
        
class LeerDatos(QThread):
    LeerSerial = pyqtSignal(list)
  
    def __init__(self, parent=None):
        super(LeerDatos, self).__init__(parent)
        #self.GUI = RocketInterface()
        #self.ser = self.GUI.ser
        #self.Interface = RocketInterface()
        self.restartData()
    
    def restartData(self):
        self.Time = np.empty((0, 3), int)
        self.Press = np.empty((0, 3), dtype='float64')
        self.Temp = np.empty((0, 3), dtype='float64')
        self.Thr = np.empty((0, 3), dtype='float64')
        
    def run(self):
        while self.LeerDatosBool and self.ser.isOpen(): #self.ser.inWaiting() > 0:
            
            if self.ser.inWaiting() > 0:
                #print("Lectura Dato...")
                Dato = self.ser.readline()
                #print(Dato)
                #print("Tam: " + str(len(Dato)))
    
                if (Dato.decode('utf-8') != ''):
                    #print('No Vacio')
    
                    if (len(Dato) < 20 and len(Dato) > 2):
                        # Señales
                        p = self.ser.readline()
                        print("Llego.....................:")
                        print(p)
                        # Cuenta regresiva iniciada -> valor conteo
                        Dato = Dato.decode('utf-8')
                        if (Dato[0] == 'A'):
                            print("Cuenta regresiva iniciada")
                        # Cuenta regresiva abortada
    
                    if (len(Dato) >= 20):
                        try:
                            Dato = Dato.decode('utf-8')
                            Dato1 = Dato.split(',')
                            Dato2 = Dato1[1:5]
                            
                            Time = int(Dato2[0])
                            Press = float((float(Dato2[1]) / 1000))
                            Temp = (float(Dato2[2]) / 100)
                            Thr = float(float(Dato2[3]) / 1000)
                            
                            self.Time = np.append(self.Time, Time)
                            self.Press = np.append(self.Press, Press)
                            self.Temp = np.append(self.Temp, Temp)
                            self.Thr = np.append(self.Thr, Thr)

                            
                            #print(len(self.Time))
                        except:
                            print('error append', Dato2)
                            Dato2 = None
 
                # Actualizar datos cada que se completen 20 lecturas
                if len(self.Time) >= 20:
                    self.LeerSerial.emit([self.Time, self.Press, self.Temp, self.Thr])
                    
                    self.restartData()
                    
                time.sleep(0.01)

qtCreatorFile = "guiInterfaceQt.ui" # Aquí va el nombre del archivo .ui

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class RocketInterface(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        # - Set Window Parameters
        # Adjust Size Policy
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.centralwidget.setContentsMargins(0, 0, 0, 0)

        self.setWindowTitle('Rocket Station Interface')
        
        # Definir y ubicar los graficos.
        self.PlotData = MplCanvas(self)
        self.PlotData.move(110+200, 20+10)
        
        #  Thread para actualizar lectura de datos y plot
        self.ThreadDatos = LeerDatos(self)
        self.ser = serial.Serial() 
        

        # Definicion de Variables
        self.LeerDatosBool = False
        self.ConexionEstablecidaBool = False
        self.TiempoRestante = self.SPTiempoIgnicion.value()
        self.ThreadConteo = UpdateConteo()
        self.port = ''
        self.Brate = 0
        self.FormatosSalida = ['csv', 'txt']
        self.FormatoSalida = self.FormatosSalida[0]
        
        #  Configurar el estado inicial de los Widgets.
        self.BtnAbortar.setStyleSheet('background-color: red')
        self.BtnAbortar.setVisible(False)
        self.BtnIniciar.setEnabled(False)
        self.BtnDetener.setVisible(False)
        self.lcdConteo.display(self.SPTiempoIgnicion.value())


        # Conexiones con funciones
        self.SPTiempoIgnicion.valueChanged.connect(self.TiempoIgnicionCambio)
        self.BtnComunicacion.clicked.connect(self.IniciarComunicacion)
        self.BtnIniciar.clicked.connect(self.IniciarCuentaRegresiva)
        self.BtnAbortar.clicked.connect(self.AbortarIgnicion)
        self.ThreadConteo.Progreso.connect(self.ActualizarConteo)
        self.ThreadDatos.LeerSerial.connect(self.MedirSerial)
        self.BtnDetener.clicked.connect(self.DetenerComunicacion)
        self.CBFormatoSalida.currentIndexChanged.connect(self.CambioFormato)
        
        
        #  Definiendo la nueva ventana de configuracion serial.
        self.WindowSerial = QtWidgets.QMainWindow()
        self.windowUi = SerialConfigWindow()
        self.windowUi.Status.connect(self.EstadoSeleccionParametros)
        self.windowUi.SelectedParameters.connect(self.ParametrosSerial)
        
        
    # Aquí van las nuevas funciones

    def IniciarComunicacion(self):
        self.LblEstado.setText('Seleccionando parámetros para la conexión')
        #self.WindowSerial = QtWidgets.QMainWindow()
        #self.windowUi = SerialConfigWindow()
        self.windowUi.show()
        
    def EstadoSeleccionParametros(self, Status):
        if Status == True:
            self.LblEstado.setText('Verificando parámetros de la conexión')
        else:
            self.LblEstado.setText('Sin parámetros de conexión seleccionados')
            
    def ParametrosSerial(self, Parameters):
        self.port = Parameters[0]
        self.Brate = Parameters[1]
        print(self.port, self.Brate)
        self.BtnComunicacion.setEnabled(False)
       
        self.EstablecerComunicacion()
        self.LblRecepcion.setText('Conectado')
        self.LblEstado.setText('Recibiendo Datos')
        
    def EstablecerComunicacion(self):
        # Limpiar plot 
        self.PlotData.ax1.cla()
        self.PlotData.ax2.cla()
        self.PlotData.ax3.cla()
        # Se inicia puerto de comunicaciones
        try:
            self.ser.port=self.port
            self.ser.baudrate=self.Brate
            self.ser.timeout=1
            self.ser.open()
            self.BtnDetener.setVisible(True)        
        except:
            try:
                self.ser.close()
                self.ser.port=self.port
                self.ser.baudrate=self.Brate
                self.ser.timeout=1
                self.ser.open()
                self.BtnDetener.setVisible(True)
            except:
                self.LblRecepcion.setText('Sin Conexión')
                self.LblEstado.setText('Error de conexión al puerto')

        # Se inicializan los vectores de datos (Tiempo y Variables)
        self.Time = np.array([0])
        # Variables
        self.Temp = np.array([0.])
        self.Press = np.array([0.])
        self.Thr = np.array([0.])
        # Mensajes 
        self.Message = ''
        self.ThreadDatos.ser = self.ser
        self.ThreadDatos.restartData()
        self.ThreadDatos.LeerDatosBool = True
        self.ThreadDatos.start()
        self.BtnIniciar.setEnabled(True)
        

    def MedirSerial(self, Data):
        [Timei, Pressi, Tempi, Thri] = Data
        
        self.Time = np.append(self.Time, Timei)
        self.Press = np.append(self.Press, Pressi)
        self.Temp = np.append(self.Temp, Tempi)
        self.Thr = np.append(self.Thr, Thri)

         #  Update current values
        # Current
        self.P_Actual.setText(str(self.Press[-1]))
        self.T_Actual.setText(str(self.Temp[-1]))
        self.E_Actual.setText(str(self.Thr[-1]))
        # Max values
        self.P_Max.setText(str(np.amax(self.Press)))
        self.T_Max.setText(str(np.amax(self.Temp)))
        self.E_Max.setText(str(np.amax(self.Thr)))
        # Min values
        self.P_Min.setText(str(np.amin(self.Press)))
        self.T_Min.setText(str(np.amin(self.Temp)))
        self.E_Min.setText(str(np.amin(self.Thr)))
        # Mean values
        self.P_Avg.setText(str(np.mean(self.Press)))
        self.T_Avg.setText(str(np.mean(self.Temp)))
        self.E_Avg.setText(str(np.mean(self.Thr)))
        
        PlotEach = 21  # Actualizar plot cada "n" datos
        
        if len(self.Time) > PlotEach:
            self.PlotData.plotPress(time=self.Time[-PlotEach:], dataP=self.Press[-PlotEach:])
            self.PlotData.plotTemp(time=self.Time[-PlotEach:], dataT=self.Temp[-PlotEach:])
            self.PlotData.plotEmp(time=self.Time[-PlotEach:], dataE=self.Thr[-PlotEach:])
        else:
            self.PlotData.plotPress(time=self.Time, dataP=self.Press)
            self.PlotData.plotTemp(time=self.Time, dataT=self.Temp)
            self.PlotData.plotEmp(time=self.Time, dataE=self.Thr)

    def CambioFormato(self):
        self.FormatoSalida = self.FormatosSalida[self.CBFormatoSalida.currentIndex()]
        print(self.FormatoSalida)
        
    def TiempoIgnicionCambio(self):
        self.lcdConteo.display(self.SPTiempoIgnicion.value())
        self.TiempoRestante = self.SPTiempoIgnicion.value()

    def IniciarCuentaRegresiva(self):
        self.SPTiempoIgnicion.setEnabled(False)
        self.BtnAbortar.setVisible(True)
        self.ThreadConteo.Max = self.TiempoRestante
        self.ThreadConteo.start()
        self.LblEstado.setText('En cuenta regresiva para ignición')
        # Iniciar multithread para la cuenta regresiva y en caso de Stop
        # Enviar la se;al de stop

    def AbortarIgnicion(self):
        self.ThreadConteo.terminate()
        self.LblEstado.setText('Ignición Abortada, debe iniciar nuevamente el conteo')
        self.BtnAbortar.setVisible(False)
        self.SPTiempoIgnicion.setEnabled(True)
        self.TiempoIgnicionCambio()

    def ActualizarConteo(self, restante):
        self.lcdConteo.display(restante)
        if restante <= 0:
            self.ser.write(b'S') # Enviar se;al de Ignicion.
            self.LblEstado.setText('Señal de Ignición enviada')
            self.BtnAbortar.setVisible(False)
            self.BtnIniciar.setEnabled(False)
            self.ThreadConteo.terminate()
            
    def DetenerComunicacion(self):
        
        #self.ThreadDatos.wait()
        self.ThreadDatos.LeerDatosBool = False
        self.ThreadDatos.terminate()
        self.AbortarIgnicion()
        self.ser.close()
        
        self.BtnIniciar.setEnabled(False)
        self.LblEstado.setText('Deteniendo comunicación y guardando datos')
        self.ExportData()
        self.LblEstado.setText(str('Datos guardados en el directorio: '+ self.directory))
        self.BtnDetener.setVisible(False)
        self.BtnComunicacion.setEnabled(True)
        self.LblRecepcion.setText('Terminado')
        
    def closeEvent(self, event):
        self.DetenerComunicacion()
        
        
    def CreateFolder(self):
        try:
            if not path.exists(self.directory):
                makedirs(self.directory)
        except OSError:
            print('Error: Creating directory. ', self.directory)
    
    def ExportData(self):
        date = datetime.now().strftime('%Y-%m-%d %H-%M-%S')  # String with the current date and time.
        self.directory = str('./Data - ' + date + '/')
        self.CreateFolder()
        
        if path.exists(self.directory):
            # Save the plot.
            pathfolder = str(self.directory)
            pathfolderimg = pathfolder + ' Plot.png'
            self.PlotData.fig.savefig(pathfolderimg, dpi=300)
            
            # Save Data
            if len(self.Time) == len(self.Press) == len(self.Temp) == len(self.Thr):
                output = np.column_stack((self.Time.flatten(), self.Press.flatten(), self.Temp.flatten(), self.Thr.flatten()))
                np.savetxt(pathfolder + ' Datos Rocket.'+ self.FormatoSalida, output, delimiter=',', fmt='%f')
            else:
                print('Dimensions mismatch', len(self.Time), len(self.Press), len(self.Temp), len(self.Thr))
                np.savetxt(pathfolder + ' Datos Rocket Tiempo.'+ self.Time, output, delimiter=',', fmt='%f')
                np.savetxt(pathfolder + ' Datos Rocket Presion.'+ self.Press, output, delimiter=',', fmt='%f')
                np.savetxt(pathfolder + ' Datos Rocket Temperatura.'+ self.Temp, output, delimiter=',', fmt='%f')
                np.savetxt(pathfolder + ' Datos Rocket Empuje.'+ self.Thr, output, delimiter=',', fmt='%f')
                

    
class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=9.3, height=6.6, dpi=100):  # Dimentions by default
        #fig = Figure(figsize=(width, height), dpi=dpi)
        #self.axes = fig.add_subplot(3,1,1)
        #plt.ion()
        self.fig, (self.ax1, self.ax2, self.ax3) = plt.subplots(3, 1, sharex=True, figsize=(width, height), dpi=dpi)
        plt.tight_layout() #Reducir margenes pad=0


        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                QtWidgets.QSizePolicy.Expanding,
                QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
  
    def plotPress(self, time, dataP):
    
        self.pltPress, = self.ax1.plot(time, dataP, 'b-')
        self.pltPress.set_antialiased(False) # turn off antialising
        #self.ax1.set_title('Pressure')        
   
        self.draw()
        #self.flush_events()
        
    def plotTemp(self, time, dataT):
     
        self.pltTemp, = self.ax2.plot(time, dataT, 'r-')
        self.pltTemp.set_antialiased(False) # turn off antialising
        #self.ax2.set_title('Temperature')

        self.draw()
        
    def plotEmp(self, time, dataE):
    
        self.pltEmp, = self.ax3.plot(time, dataE, 'g-')
        self.pltEmp.set_antialiased(False) # turn off antialising
        #self.ax3.set_title('Empuje')
        
        self.draw()


if __name__ == "__main__":
    app =  QtWidgets.QApplication(sys.argv)
    window = RocketInterface()
    window.show()
    sys.exit(app.exec_())

