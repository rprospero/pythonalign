import numpy as np
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
        self._selected = False
        self._title = ""

    titleChanged = pyqtSignal(str)
    @pyqtProperty(str, notify=titleChanged)
    def title(self):
        return self._title

    @title.setter
    def title(self, v):
        self._title = v
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
                len=self._length*length_scale)
        except KeyError:
            result = "!!!!" + skeleton + "!!!! Missing Key"
        except ValueError:
            result = "!!!!" + skeleton + "!!!! Bad format specifier"

        return result


class RunModel(QAbstractListModel):

    _roles = {Qt.DisplayRole: b"run"}

    def roleNames(self):
        return self._roles

    def __init__(self, parent=None):
        super(RunModel, self).__init__(parent)
        self._runs = []
        self._horizontal_command = ""
        self._vertical_command = ""
        self._frame_width=1
        self._frame_height=1

    frameWidthChanged = pyqtSignal(float)
    @pyqtProperty(float, notify=frameWidthChanged)
    def frameWidth(self):
        return self._frame_width

    @frameWidth.setter
    def frameWidth(self, x):
        self._frame_width = x
        self.scriptChanged.emit()

    frameHeightChanged = pyqtSignal(float)
    @pyqtProperty(float, notify=frameHeightChanged)
    def frameHeight(self):
        return self._frame_height

    @frameHeight.setter
    def frameHeight(self, x):
        self._frame_height = x
        self.scriptChanged.emit()

    @pyqtProperty(str)
    def horizontalCommand(self):
        return self._horizontal_command

    @horizontalCommand.setter
    def horizontalCommand(self, value):
        self._horizontal_command = value
        self.scriptChanged.emit()

    @pyqtProperty(str)
    def verticalCommand(self):
        return self._vertical_command

    @verticalCommand.setter
    def verticalCommand(self, value):
        self._vertical_command = value
        self.scriptChanged.emit()

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
        self.scriptChanged.emit()

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
        self.scriptChanged.emit()

    @pyqtSlot(int)
    def remove(self, i):
        if i >= len(self._runs):
            return False
        self.beginRemoveRows(QModelIndex(), i, i)
        del self._runs[i]
        self.endRemoveRows()
        self.scriptChanged.emit()
        return True

    @pyqtSlot(int, result=SingleRun)
    def get(self, i):
        return self._runs[i]

    scriptChanged = pyqtSignal()
    @pyqtProperty(str, notify=scriptChanged)
    def script(self):
        temp = "\n".join([r.script_line(self._horizontal_command, self._vertical_command,
                                        self._frame_width, self._frame_height)
                          for r in self._runs])
        return temp


qmlRegisterType(SingleRun, "PythonAlign", 1, 0, "SingleRun")
qmlRegisterType(RunModel, "PythonAlign", 1, 0, "RunModel")
