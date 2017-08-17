import numpy as np
from PyQt5.QtCore import pyqtProperty, pyqtSignal, pyqtSlot, QPointF, Qt, QModelIndex, QObject
from PyQt5.QtGui import QColor, QPixmap
from PyQt5.QtQml import qmlRegisterType, QQmlListProperty
from PyQt5.QtQuick import QQuickItem, QSGGeometryNode, QSGGeometry, QSGNode, \
    QSGFlatColorMaterial, QSGSimpleTextureNode


class SingleRun(QObject):
    def __init__(self, parent=None, startx=0, starty=0, stopx=1, stopy=1):
        super().__init__(parent)
        self._startx = startx
        self._starty = starty
        self._stopx = stopx
        self._stopy = stopy

    startxChanged = pyqtSignal(float)
    @pyqtProperty(float, notify=startxChanged)
    def startx(self):
        return self._startx

    startyChanged = pyqtSignal(float)
    @pyqtProperty(float, notify=startyChanged)
    def starty(self):
        return self._starty

    stopxChanged = pyqtSignal(float)
    @pyqtProperty(float, notify=stopxChanged)
    def stopx(self):
        return self._stopx

    stopyChanged = pyqtSignal(float)
    @pyqtProperty(float, notify=stopyChanged)
    def stopy(self):
        return self._stopy

    @startx.setter
    def startx(self, x):
        self._startx = x

    @starty.setter
    def starty(self, y):
        self._starty = y

    @stopx.setter
    def stopx(self, x):
        self._stopx = x

    @stopy.setter
    def stopy(self, y):
        self._stopy = y


class RunModel(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._runs = []

    runsChanged = pyqtSignal(QQmlListProperty)
    @pyqtProperty(QQmlListProperty)
    def runs(self):
        return QQmlListProperty(SingleRun, self, self._runs)


qmlRegisterType(SingleRun, "PythonAlign", 1, 0, "SingleRun")
qmlRegisterType(RunModel, "PythonAlign", 1, 0, "RunModel")
