import numpy as np
from os.path import join
from pathlib import Path
from PyQt5.QtCore import pyqtProperty, pyqtSignal, pyqtSlot, QPointF, Qt, QModelIndex, QObject, QAbstractListModel, QVariant
from PyQt5.QtGui import QColor, QPixmap
from PyQt5.QtQml import qmlRegisterType, QQmlListProperty
from PyQt5.QtQuick import QQuickItem, QSGGeometryNode, QSGGeometry, QSGNode, \
    QSGFlatColorMaterial, QSGSimpleTextureNode

class SingleRun(QObject):
    def __init__(self, parent, startx=0, starty=0):
        super(SingleRun, self).__init__(parent)
        self._parent = parent
        self._x = startx
        self._y = starty
        self._vertical = False
        self._length = 0
        self._step_size = 0.1
        self._selected = False
        self._title = ""
        self._valid = False

    @staticmethod
    def fromJson(parent, d):
        self = SingleRun(parent)
        self._x = d["startx"]
        self._y = d["starty"]
        self._vertical = d["vertical"]
        self._length = d["length"]
        self._step_size = d["step_size"]
        self._title = d["title"]
        self._valid = d["valid"]
        return self

    def toJson(self):
        d = {"startx": self._x,
             "starty": self._y,
             "vertical": self._vertical,
             "length": self._length,
             "step_size": self._step_size,
             "title": self._title,
             "valid": self._valid}
        return d

    validChanged = pyqtSignal()
    @pyqtProperty(bool, notify=validChanged)
    def valid(self):
        if not self.title or " " in self.title:
            return False
        return True

    titleChanged = pyqtSignal(str)
    @pyqtProperty(str, notify=titleChanged)
    def title(self):
        return self._title

    @title.setter
    def title(self, v):
        self._title = v
        self._parent.scriptChanged.emit()
        self.validChanged.emit()
        self._parent.validChanged.emit()

    stepSizeChanged = pyqtSignal(float)
    @pyqtProperty(float, notify=stepSizeChanged)
    def stepSize(self):
        return self._step_size

    @stepSize.setter
    def stepSize(self, x):
        self._step_size = x
        self._parent.scriptChanged.emit()

    startxChanged = pyqtSignal(float)
    @pyqtProperty(float, notify=startxChanged)
    def startx(self):
        return self._x

    startyChanged = pyqtSignal(float)
    @pyqtProperty(float, notify=startyChanged)
    def starty(self):
        return self._y

    stopxChanged = pyqtSignal(float)
    @pyqtProperty(float, notify=stopxChanged)
    def stopx(self):
        if self._vertical:
            return self._x
        return self._x+self._length

    stopyChanged = pyqtSignal(float)
    @pyqtProperty(float, notify=stopyChanged)
    def stopy(self):
        if self._vertical:
            return self._y+self._length
        return self._y

    @pyqtProperty(bool)
    def selected(self):
        return self._selected

    @startx.setter
    def startx(self, x):
        self._x = x
        if self._vertical:
            self.stopxChanged.emit(x)
        else:
            self.stopxChanged.emit(x+self._length)
        self._parent.scriptChanged.emit()

    @starty.setter
    def starty(self, y):
        self._y = y
        if not self._vertical:
            self.stopyChanged.emit(y)
        else:
            self.stopyChanged.emit(y+self._length)
        self._parent.scriptChanged.emit()

    @stopx.setter
    def stopx(self, x):
        if self._vertical:
            self._x = x
            self.startxChanged.emit(x)
        else:
            self._length = x-self._x
        self._parent.scriptChanged.emit()

    @stopy.setter
    def stopy(self, y):
        if not self._vertical:
            self._y = y
            self.startyChanged.emit(y)
        else:
            self._length = y-self._y
        self._parent.scriptChanged.emit()

    def selected(self, v):
        self._selected = v

    def script_line(self, hor, ver, width, height):
        if self._vertical:
            skeleton = ver
            length_scale = height
        else:
            skeleton = hor
            length_scale = width

        try:
            result = skeleton.format(
                startx=self.startx*width,
                starty=self.starty*height,
                stopx=self.stopx*width,
                stopy=self.stopy*height,
                title=self._title,
                ndark=1,
                time=0.04,
                stepSize=self._step_size,
                frameCount= round(self._length*length_scale/self._step_size),
                sleep=0,
                len=self._length*length_scale)
        except KeyError as e:
            result = "!!!!" + skeleton + "!!!! Missing Key: " + str(e)
        except ValueError as e:
            result = "!!!!" + skeleton + "!!!! Bad format specifier: " + str(e)

        return result


qmlRegisterType(SingleRun, "PythonAlign", 1, 0, "SingleRun")
