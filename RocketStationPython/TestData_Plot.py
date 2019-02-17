
import numpy as np
import serial
import time
import re

class PlotData():

    def __init__(self, parent = None):
        #super(PlotData, self).__init__(parent)

    #    self.ser = serial.Serial('/dev/tty.usbmodem1421', 115200, timeout=0)
        self.ser = serial.Serial('/dev/cu.usbserial-DN018IQ4', 38400, timeout=0)

        self.X_Temp = np.array([0.])
        self.X_Press = np.array([0.])
        self.X_Thr = np.array([0.])
        self.Y_Temp = np.array([0.])
        self.Y_Press = np.array([0.])
        self.Y_Thr = np.array([0.])
        self.Message = ''

    def Medir(self):

#        ser = serial.Serial('COM9', 9600, timeout=1)
        mida = 2

        while (mida>1):

#            time.sleep(0.1)
            Dato=self.ser.readline()
            print(Dato)
#            print('Popo')
            if (Dato.decode('utf-8')!=''):
                print('No')
                print(Dato)

                if(len(Dato)==23):
                    Dato = Dato.decode('utf-8')
                    Dato1 = re.split('P|T|E|F\r\n',Dato)
                    Dato2 = Dato1[1:4]

    #                print(Dato2[3])
                    self.Y_Press = np.append(self.Y_Press, float(Dato2[0]))
                    self.X_Press = np.append(self.X_Press, self.X_Press[len(self.X_Press)-1]+1*0.2)
                    self.Y_Temp = np.append(self.Y_Temp, float(Dato2[1]))
                    self.X_Temp = np.append(self.X_Temp, self.X_Temp[len(self.X_Temp)-1]+1*0.2)
                    self.Y_Thr = np.append(self.Y_Thr, float(Dato2[2]))
                    self.X_Thr = np.append(self.X_Thr, self.X_Thr[len(self.X_Thr)-1]+1*0.2)

                    if (len(self.X_Press)>len(self.Y_Press)):
                        self.X_Press = np.delete(self.X_Press, len(self.X_Press)-1)
                    if (len(self.X_Temp)>len(self.Y_Temp)):
                        self.X_Temp = np.delete(self.X_Temp, len(self.X_Temp)-1)
                    if (len(self.X_Thr)>len(self.Y_Thr)):
                        self.X_Thr = np.delete(self.X_Thr, len(self.X_Thr)-1)
                    print(len(self.X_Temp))
                    print(len(self.Y_Press))
                    print(len(self.Y_Temp))
                    print(len(self.Y_Thr))
                    mida=mida-1

    def CheckCommunication(self):

#        ser = serial.Serial('COM9', 9600, timeout=0)
        time.sleep(2)
        var='1'.encode('utf-8');
#        ser.write(var)
        Wait = 1
#        time.sleep(5)
        self.ser.write(var)

        while (Wait==1):

            try:
                time.sleep(2)
                p=self.ser.readline()
                if (p.decode('utf-8')==''):
#                    Wait=1
                    print('')
                elif (p.decode('utf-8')=='1'):
                    self.Message = 'Comunicación exitosa'
                    print(p)
                    print('exito')
                    Wait=0
#                    ser.close()
                else:
                    self.Message = 'Error en la comunicación'
                    print(p)
                    print('Noexito')
    #                    Wait=0
#                    ser.close()
            except:
                pass



#        time.sleep(1)

#        while (Wait==1):
#            try:
#                p=ser.readline()
##                if (p.decode('utf-8')=='')
#                print(p)
#                if (float(p.decode('utf-8'))==1):
#                    self.Message = 'Comunicación exitosa'
#                else:
#                    self.Message = 'Error en la comunicación'
#
#                Wait=0
#                ser.close()
#
#
#            except:
#                pass

    def StartCommunication(self, sampletime):
#        ser = serial.Serial('COM9', 9600, timeout=0)
#        time.sleep(1)
        var=sampletime.encode('utf-8');
        self.ser.write(var)
        p = self.ser.readline();
        print(p)
#        ser.close()
