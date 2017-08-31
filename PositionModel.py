import json
from PyQt5.QtCore import pyqtProperty, pyqtSignal, pyqtSlot, Qt, QModelIndex, \
    QAbstractListModel, QVariant, QObject
from PyQt5.QtQml import qmlRegisterType

class SinglePosition(QObject):
    def __init__(self, parent):
        super(SinglePosition, self).__init__(parent)
        self._parent = parent
        self._title = ""

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


class PositionModel(QAbstractListModel):

    _roles = {Qt.UserRole: b"run"}

    def roleNames(self):
        """The names of the roles performed by the model.

        This is required by QtQuick"""
        return self._roles

    def __init__(self, parent=None):
        super(PositionModel, self).__init__(parent)
        self._pos = [SinglePosition(self)]
        self._pos[0]._title = "Foo"

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
