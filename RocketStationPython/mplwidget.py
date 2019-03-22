#!/usr/bin/env python3


from PyQt5 import QtWidgets, QtCore, QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from  matplotlib.figure import *
from TestData_Plot import PlotData as TDP

__version__ = '1.0'


class MplCanvas(FigureCanvas):

    def __init__(self, parent=None):

        fig = Figure()
        self.axes = fig.add_subplot(111)

        self.compute_initial_figure()

        #Data=TDP()
        #self.Data=Data

        # Check
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

###################################### Graficas ###################################### 

class MplTemp(MplCanvas):

    def __init__(self,Data,*args, **kwargs):
        MplCanvas.__init__(self, *args, **kwargs)
        #self.PlotSignal = PlotSignalFlag
        self.PlotSignal = 0
        self.checkSignal = 1
        self.Data=Data
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.update_figure)
        timer.start(0)

    def compute_initial_figure(self):
        self.axes.plot([0],[0])
        self.axes.set_title('Temperatura')

    def update_figure(self):
        # Build a list of 4 random integers between 0 and 10 (both inclusive)
        #print(self.PlotSignal)
        if (self.checkSignal==0):
            self.axes.cla()
        else:

            if (self.PlotSignal==1):
                #l = [random.randint(0, 10) for i in range(50)]
                #self.axes.cla()
                #self.axes.plot(np.arange(50.0), l, 'r')
                #self.axes.set_title('Temperatura')
                #self.draw()
                self.Data.Medir()
                self.axes.cla()
                if (len(self.Data.Time)>50):
                    self.axes.plot(self.Data.Time[-50:], self.Data.Temp[-50:], 'r')
                else:
                    self.axes.plot(self.Data.Time[1:], self.Data.Temp[1:], 'r')
                self.axes.set_title('Temperatura')
                self.draw()

class MplPress(MplCanvas):

    def __init__(self,Data, *args, **kwargs):
        MplCanvas.__init__(self, *args, **kwargs)
        self.PlotSignal = 0
        self.checkSignal = 1
        self.Data=Data
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.update_figure)
        timer.start(0)

    def compute_initial_figure(self):
        self.axes.plot([0],[0])
        self.axes.set_title('Presión')

    def update_figure(self):
        # Build a list of 4 random integers between 0 and 10 (both inclusive)
        if (self.checkSignal==0):
            self.axes.cla()
        else:

            if (self.PlotSignal==1):
                self.Data.Medir()
                self.axes.cla()
                if (len(self.Data.Time)>50):
                    self.axes.plot(self.Data.Time[-50:], self.Data.Press[-50:], 'b')
                else:
                    self.axes.plot(self.Data.Time[1:], self.Data.Press[1:], 'b')
                self.axes.set_title('Presión')
                self.draw()

class MplThr(MplCanvas):

    def __init__(self,Data, *args, **kwargs):
        MplCanvas.__init__(self, *args, **kwargs)
        self.PlotSignal = 0
        self.checkSignal = 1
        self.Data=Data
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.update_figure)
        timer.start(0)

    def compute_initial_figure(self):
        self.axes.plot([0],[0])
        self.axes.set_title('Empuje')

    def update_figure(self):
        # Build a list of 4 random integers between 0 and 10 (both inclusive)
        if (self.checkSignal==0):
            self.axes.cla()
        else:

            if (self.PlotSignal==1):
                self.Data.Medir()
                self.axes.cla()
                if (len(self.Data.Time)>50):
                    self.axes.plot(self.Data.Time[-50:], self.Data.Thr[-50:], 'g')
                else:
                    self.axes.plot(self.Data.Time[1:], self.Data.Thr[1:], 'g')
                self.axes.set_title('Empuje')
                self.draw()

######################################  ###################################### 

class MplWidget(QtWidgets.QWidget):
    """Widget defined in Qt Designer"""
    def __init__(self, parent=None):
        # initialization of Qt MainWindow widget
        QtWidgets.QWidget.__init__(self, parent)
        Data=TDP()
        self.Data=Data

        # set the canvas to the Matplotlib widget
        self.canvasTemp = MplTemp(self.Data)
        self.canvasPress = MplPress(self.Data)
        self.canvasThr = MplThr(self.Data)
        #self.Signals = MplSignals()
        #self.canvas_2 = MplCanvas(figure=2)
        # create a vertical box layout
        #QSplitter(Qt.Horizontal, self)
        self.hbl = QtWidgets.QHBoxLayout()
        # add mpl widget to vertical box
        #self.hbl.addWidget(self.canvas_2, stretch=2)
        self.hbl.addWidget(self.canvasTemp, stretch=1)
        self.hbl.addWidget(self.canvasPress, stretch=1)
        self.hbl.addWidget(self.canvasThr, stretch=1)
        #self.hbl.addWidget(self.Signals.MplTemp, stretch=1)
        #self.hbl.addWidget(self.Signals.MplPress, stretch=1)
        #self.hbl.addWidget(self.Signals.MplThr, stretch=1)
        # set the layout to th vertical box
        self.setLayout(self.hbl)

    def PlotData(self,sensor,PlotSignalFlag):

        if (sensor==1):
            self.canvasTemp.PlotSignal=PlotSignalFlag
        elif (sensor==2):
            self.canvasPress.PlotSignal=PlotSignalFlag
        elif (sensor==3):
            self.canvasThr.PlotSignal=PlotSignalFlag
        else:
            print('Error, Check PlotSignal')

    def CheckData(self,sensor,PlotSignalFlag):

        if (sensor==1):
            self.canvasTemp.checkSignal=PlotSignalFlag
        elif (sensor==2):
            self.canvasPress.checkSignal=PlotSignalFlag
        elif (sensor==3):
            self.canvasThr.checkSignal=PlotSignalFlag
        else:
            print('Error, Check CheckSignal')

###################################### Comentarios ###################################### 

'''
#class MplSignals(MplCanvas):
#
#    def __init__(self,*args, **kwargs):
#        self.MplTemp = MplCanvas.__init__(self, *args, **kwargs)
#        self.MplPress = MplCanvas.__init__(self, *args, **kwargs)
#        self.MplThr = MplCanvas.__init__(self, *args, **kwargs)
#        self.PlotSignal = 0
#        timer = QtCore.QTimer(self)
#        timer.timeout.connect(self.update_figure)
#        timer.start(0)
#
#    def compute_initial_figure(self):
#        self.MplTemp.axes.plot([0, 1],[1, 2])
#        self.MplPress.axes.plot([0, 1],[1, 2])
#        self.MplThr.axes.plot([0, 1],[1, 2])
#
#    def update_figure(self):
#        # Build a list of 4 random integers between 0 and 10 (both inclusive)
#        #print(self.PlotSignal)
#        if (self.PlotSignal==1):
##            l = [random.randint(0, 10) for i in range(50)]
##            self.axes.cla()
##            self.axes.plot(np.arange(50.0), l, 'r')
##            self.axes.set_title('Temperatura')
##            self.draw()
#            self.Data.Medir()
#            self.axes.cla()
#            self.axes.plot(self.Data.X, self.Data.Y, 'r')
#            self.axes.set_title('Temperatura')
#            self.draw()


#    def CheckCommunication(self):
#
#        self.Data.CheckCommunication()

#def rotate(element, theta):
#    """Applies a rotation operation on any polarizing element given
#    its Jones matrix representation and a angle of rotation.
#    The angle is to be given in radians."""
#
#    #Pending to import only the most elevant numpy functions for improving speed
#    import numpy as np
#    assert isinstance(element, np.matrix)
#    assert element.shape == (2, 2)
#    rotator = np.matrix([[np.cos(theta), np.sin(theta)],\
#                         [-np.sin(theta), np.cos(theta)]])
#    return rotator.transpose()*element*rotator
#
#
#class MplCanvas(FigureCanvas):
#    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""
#    def __init__(self, polAngle=-3*pi/8, qwpAngle=-pi/4, figure=1, Jones=0):
#        """ Draws the polarization ellipse that results from propagating
#             a linear polarized field alligned with angle polAngle trough
#             a qwp aligned along qwpAngle"""
#        from matplotlib.pylab import close
#        close('all')
#        if isinstance(Jones,np.matrix):
#            fig_1, fig_2 = plot_ellipse(Jones,show=False, retrieve=True)
#        else:
#
#            self.QWP = np.matrix([[np.exp(1.j*pi/4), 0],\
#                                  [0, np.exp(-1.j*pi/4)]])
#            fig_1, fig_2 = plot_ellipse(rotate(self.QWP, qwpAngle)*\
#                                        np.matrix([[np.cos(polAngle)],\
#                                                   [np.sin(polAngle)]],\
#                                                   dtype='complex'), \
#                                                  show=False, retrieve=True)
#
#        if figure == 1:
#            self.fig = fig_1
#        elif figure == 2:
#            self.fig = fig_2
#        else:
#            raise ValueError("Oops!  That was no valid number.  Try again...")
#
#        self.fig.hold(False)
#        FigureCanvas.__init__(self, self.fig)
#        FigureCanvas.setSizePolicy(self,
#                                   QtWidgets.QSizePolicy.Expanding,
#                                   QtWidgets.QSizePolicy.Expanding)
#        FigureCanvas.updateGeometry(self)
#
##class MplCanvas(FigureCanvas):
##
##    def __init__(self):
##
#
#
#class MplWidget(QtWidgets.QWidget):
#    """Widget defined in Qt Designer"""
#    def __init__(self, parent=None):
#        # initialization of Qt MainWindow widget
#        QtWidgets.QWidget.__init__(self, parent)
#        # set the canvas to the Matplotlib widget
#        self.canvas_1 = MplCanvas(figure=1)
#        #self.canvas_2 = MplCanvas(figure=2)
#        # create a vertical box layout
#        #QSplitter(Qt.Horizontal, self)
#        self.hbl = QtWidgets.QHBoxLayout()
#        # add mpl widget to vertical box
#        #self.hbl.addWidget(self.canvas_2, stretch=2)
#        self.hbl.addWidget(self.canvas_1, stretch=1)
#        # set the layout to th vertical box
#        self.setLayout(self.hbl)
#
##    def plot_ellipses(self, polAngle, qwpAngle,Jones = 0):
##        """ Draws the polarization ellipse that results from propagating
##         a linear polarized field alligned with angle polAngle trough
##         a qwp aligned along qwpAngle"""
##
##        self.canvas_1.setParent(None)
##        self.canvas_2.setParent(None)
##        if isinstance(Jones,np.matrix):
##            self.canvas_1 = MplCanvas(polAngle, qwpAngle, figure=1, Jones = Jones)
##            self.canvas_2 = MplCanvas(polAngle, qwpAngle, figure=2, Jones = Jones)
##
##        else:
##            self.canvas_1 = MplCanvas(polAngle, qwpAngle, figure=1)
##            self.canvas_2 = MplCanvas(polAngle, qwpAngle, figure=2)
##
##        self.hbl.addWidget(self.canvas_2, stretch=2)
##        self.hbl.addWidget(self.canvas_1, stretch=1)
##        self.setLayout(self.hbl)
'''