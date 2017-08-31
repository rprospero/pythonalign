import json
from PyQt5.QtCore import pyqtProperty, pyqtSignal, pyqtSlot, Qt, QModelIndex, \
    QAbstractListModel, QVariant, QObject
from PyQt5.QtQml import qmlRegisterType

class SinglePosition(QObject):
    def __init__(self, parent):
        super(SinglePosition, self).__init__(parent)
        self._parent = parent
        self._title = ""
        self._top = 0
        self._left = 0

    titleChanged = pyqtSignal(str)

    @pyqtProperty(str, notify=titleChanged)
    def title(self):
        """What to name this position"""
        return self._title

    @title.setter
    def title(self, value):
        if self._title == value:
            return
        self._title = value
        self.titleChanged.emit()

    topChanged = pyqtSignal(str)

    @pyqtProperty(float, notify=topChanged)
    def top(self):
        """The coordinate of the frame's top"""
        return self._top

    @top.setter
    def top(self, value):
        if self._top == value:
            return
        self._top = value
        self.topChanged.emit()

    leftChanged = pyqtSignal(str)

    @pyqtProperty(float, notify=leftChanged)
    def left(self):
        """The coordinate of the frame's left"""
        return self._left

    @left.setter
    def left(self, value):
        if self._left == value:
            return
        self._left = value
        self.leftChanged.emit()

class PositionModel(QAbstractListModel):

    _roles = {
        Qt.UserRole: b"position",
        Qt.DisplayRole: b"display"
    }

    def roleNames(self):
        """The names of the roles performed by the model.

        This is required by QtQuick"""
        return self._roles

    def __init__(self, parent=None):
        super(PositionModel, self).__init__(parent)
        self._pos = [SinglePosition(self), SinglePosition(self)]
        self._pos[0]._title = "Foo"
        self._pos[1]._title = "Quux"
        self._pos[1]._top = 15
        self._pos[1]._left = 10

    @pyqtSlot(int)
    def remove(self, i):
        """Delete a position"""
        if i >= len(self._pos):
            return False
        self.beginRemoveRows(QModelIndex(), i, i)
        del self._pos[i]
        self.endRemoveRows()
        return True

    @pyqtSlot()
    def append(self):
        """Add a new position"""
        pos = SinglePosition(self)
        self.beginInsertRows(QModelIndex(),
                             len(self._pos),
                             len(self._pos))
        self._pos.append(pos)
        self.endInsertRows()

    def rowCount(self, index=QModelIndex()):
        """The current number of positions.  This is required by QtQuick"""
        return len(self._pos)

    def data(self, index, role=Qt.DisplayRole):
        """Access the position at a given index.  This is required by QtQuick"""
        if not index.isValid():
            return QVariant()
        pos = self._pos[index.row()]
        if role == Qt.UserRole:
            return pos
        elif role == Qt.DisplayRole:
            return pos.title

        return QVariant()

    def setData(self, index, value, role=Qt.EditRole):
        """Update the data at a given index.  This is required by QtQuick"""
        if not index.isValid():
            return False

        if role == Qt.Edit:
            self._pos[index.row()] = value
            return True

        return False

    def flags(self, index):
        """A description of the model properties required by QtQuick"""
        if not index.isValid():
            return Qt.ItemIsEditable
        return Qt.ItemIsEnabled | Qt.ItemIsEditable

qmlRegisterType(PositionModel, "PythonAlign", 1, 0, "PositionModel")
qmlRegisterType(PositionModel, "PythonAlign", 1, 0, "SinglePosition")
