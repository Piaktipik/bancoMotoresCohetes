
# Librerias
import numpy as np
import serial
import time
import re

 # Clase Graficar Datos puerto serial
class PlotData():

    def __init__(self, parent = None):
        # Se inicia puerto de comunicaciones
        self.ser = serial.Serial('COM4', 115200, timeout=1)  # serial prueba

        # Se inicializan los vectores de datos (Tiempo y Variables)
        self.Time = np.array([0])
        # Variables
        self.Temp = np.array([0.])
        self.Press = np.array([0.])
        self.Thr = np.array([0.])
        # Mensajes 
        self.Message = ''

    # Funcion Captura dato serial
    def Medir(self):
        mida = 2

        while (mida>1):
            print("Lectura Dato...")

            Dato = self.ser.readline()
            print(Dato)
            print("Tam: " + str(len(Dato)))

            if (Dato.decode('utf-8')!=''):
                print('No Vacio')
                
                if(len(Dato)<20 and len(Dato)>2):
                    # Señales
                    p = self.ser.readline()
                    print("Llego.....................:")
                    print(p)
                    # Cuenta regresiva iniciada -> valor conteo
                    Dato = Dato.decode('utf-8')
                    if(Dato[0] == 'A'):
                        print("Cuenta regresiva inicidada")
                    # Cuenta regresiva abortada


                if(len(Dato)>=20):
                    try:
                        Dato = Dato.decode('utf-8')
                        Dato1 = Dato.split(',')
                        Dato2 = Dato1[1:5]
                        
                        self.Time = np.append(self.Time, int(Dato2[0]))

                        self.Press = np.append(self.Press, (float(Dato2[1])/1000))
                        self.Temp = np.append(self.Temp, (float(Dato2[2])/100))
                        self.Thr = np.append(self.Thr, (float(Dato2[3])/1000))

                        print(len(self.Time))
                    except:
                        mida=mida+1
                    mida=mida-1

                    


    def CheckCommunication(self):
        #ser = serial.Serial('COM9', 9600, timeout=0)
        time.sleep(2)
        var='1'.encode('utf-8');
        # ser.write(var)
        Wait = 1
        #time.sleep(5)
        self.ser.write(var)

        while (Wait==1):
            try:
                time.sleep(2)
                print("Lectura linea...")
                p = self.ser.readline()
                print(p)
                Wait=0
                '''
                if (p.decode('utf-8')==''):
                    #Wait=1
                    print('')
                elif (p.decode('utf-8')=='1'):
                    self.Message = 'Comunicación exitosa'
                    print(p)
                    print('exito')
                    Wait=0
                    #ser.close()
                else:
                    self.Message = 'Error en la comunicación'
                    print(p)
                    print('Noexito')
                    #Wait=0
                    #ser.close()
                    '''
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

    def StartCount(self):
        # Enviamos comando inicion conteo 10 segundos
        print("Enviando comando inicio cuenta regresiva")
        self.ser.write(b'S')  
        #p = self.ser.readline();
        #print(p)
        # ser.close()

