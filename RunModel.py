import numpy as np
from PyQt5.QtCore import pyqtProperty, pyqtSignal, pyqtSlot, QPointF, Qt, QModelIndex, QObject, QAbstractListModel, QVariant
from PyQt5.QtGui import QColor, QPixmap
from PyQt5.QtQml import qmlRegisterType, QQmlListProperty
from PyQt5.QtQuick import QQuickItem, QSGGeometryNode, QSGGeometry, QSGNode, \
    QSGFlatColorMaterial, QSGSimpleTextureNode


class SingleRun(QObject):
    def __init__(self, parent=None, startx=0, starty=0, stopx=1, stopy=1):
        super(SingleRun, self).__init__(parent)
        self._startx = startx
        self._starty = starty
        self._stopx = stopx
        self._stopy = stopy

    def __repr__(self):
        return "SingleRun({}, {}, {}, {})".format(
            self.startx, self.starty, self.stopx, self.stopy)

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


class RunModel(QAbstractListModel):
    def __init__(self, parent=None):
        super(RunModel, self).__init__(parent)
        self._runs = [SingleRun(self, 0, 0, 1, 1),
                      SingleRun(self, 0.1, 0.9, 0.9, 0.1)]

    def rowCount(self, index=QModelIndex()):
        print("Row Count")
        return len(self._runs)

    def data(self, index, role):
        print("Data")
        if not index.idValid():
            return QVariant()
        return QVariant(self._runs[index.row()])

    def setData(self, index, value, role=Qt.EditRole):
        if index.isValid():
            self._runs[index.row()] = value
            return True
        return False

    def flags(self, index):
        if not index.isValid():
            return Qt.ItemIsEditable
        return Qt.ItemIsEnabled | Qt.ItemIsEditable

    @pyqtSlot(float, float, float, float)
    def append(self, startx, starty, stopx, stopy):
        r = SingleRun(self, startx, starty, stopx, stopy)
        self.beginInsertRows(QModelIndex(),
                             len(self._runs),
                             len(self._runs))
        self._runs.append(r)
        self.endInsertRows()
        print(self._runs)

    @pyqtSlot(float, float)
    def update(self, x, y):
        self._runs[-1]._stopx = x
        self._runs[-1]._stopy = y

    @pyqtSlot(int)
    def remove(self, i):
        if i >= len(self._runs):
            print(i)
            print(self._runs)
            return False
        self.beginRemoveRows(QModelIndex(), i, i)
        del self._runs[i]
        self.endRemoveRows()
        return True


qmlRegisterType(SingleRun, "PythonAlign", 1, 0, "SingleRun")
qmlRegisterType(RunModel, "PythonAlign", 1, 0, "RunModel")
