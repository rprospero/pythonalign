import numpy as np
from PyQt5.QtCore import pyqtProperty, pyqtSignal, pyqtSlot, QPointF, Qt, QModelIndex, QObject, QAbstractListModel, QVariant
from PyQt5.QtGui import QColor, QPixmap
from PyQt5.QtQml import qmlRegisterType, QQmlListProperty
from PyQt5.QtQuick import QQuickItem, QSGGeometryNode, QSGGeometry, QSGNode, \
    QSGFlatColorMaterial, QSGSimpleTextureNode


class SingleRun(QObject):
    def __init__(self, parent, startx=0, starty=0):
        super(SingleRun, self).__init__(parent)
        self._x = startx
        self._y = starty
        self._vertical = False
        self._length = 0
        self._selected = False

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

    @starty.setter
    def starty(self, y):
        self._y = y
        if not self._vertical:
            self.stopxChanged.emit(y)
        else:
            self.stopxChanged.emit(y+self._length)

    @selected.setter
    def selected(self, v):
        self._selected = v


class RunModel(QAbstractListModel):

    _roles = {Qt.DisplayRole: b"run"}

    def roleNames(self):
        return self._roles

    def __init__(self, parent=None):
        super(RunModel, self).__init__(parent)
        self._runs = []

    @pyqtProperty(int)
    def count(self):
        return len(self._runs)

    def rowCount(self, index=QModelIndex()):
        return len(self._runs)

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return QVariant()
        run = self._runs[index.row()]
        if role == Qt.DisplayRole:
            return run

        return QVariant()

    def setData(self, index, value, role=Qt.EditRole):
        if not index.isValid():
            return False

        if role == Qt.Edit:
            self._runs[index.row()] = value
            return True

        return False

    def flags(self, index):
        if not index.isValid():
            return Qt.ItemIsEditable
        return Qt.ItemIsEnabled | Qt.ItemIsEditable

    @pyqtSlot(float, float)
    def append(self, startx, starty):
        r = SingleRun(self, startx, starty)
        self.beginInsertRows(QModelIndex(),
                             len(self._runs),
                             len(self._runs))
        self._runs.append(r)
        self.endInsertRows()

    @pyqtSlot(float, float)
    def update(self, x, y):
        dx = x-self._runs[-1]._x
        dy = y-self._runs[-1]._y
        if abs(dx)>abs(dy):
            self._runs[-1]._vertical = False
            self._runs[-1]._length = dx
        else:
            self._runs[-1]._vertical = True
            self._runs[-1]._length = dy
        i = len(self._runs) - 1
        self.dataChanged.emit(self.index(i, 0), self.index(i, 0))

    @pyqtSlot(int)
    def remove(self, i):
        if i >= len(self._runs):
            return False
        self.beginRemoveRows(QModelIndex(), i, i)
        del self._runs[i]
        self.endRemoveRows()
        return True

    @pyqtSlot(int, result=SingleRun)
    def get(self, i):
        return self._runs[i]


qmlRegisterType(SingleRun, "PythonAlign", 1, 0, "SingleRun")
qmlRegisterType(RunModel, "PythonAlign", 1, 0, "RunModel")
