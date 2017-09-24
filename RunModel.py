"""This module holds the QML type for managing a set of runs"""
import json
from PyQt5.QtCore import pyqtProperty, pyqtSignal, pyqtSlot, Qt, QModelIndex, \
    QAbstractListModel, QVariant, QObject
from PyQt5.QtQml import qmlRegisterType
from SingleRun import SingleRun


class RunModel(QAbstractListModel):
    """A representation of all of the runs to be added to the script"""

    _roles = {Qt.DisplayRole: b"run"}

    def roleNames(self):
        """The names of the roles performed by the model.

        This is required by QtQuick"""
        return self._roles

    def __init__(self, parent=None):
        super(RunModel, self).__init__(parent)
        self._runs = []
        self._angle_command = ""
        self._horizontal_command = ""
        self._vertical_command = ""
        self._origin = 0
        self._frame_width = 1
        self._frame_height = 1
        self._alignment_json = ""

    @pyqtSlot(str)
    def export(self, path):
        """Save the instrument script to a file"""
        if path[0] == "/" and path[2] == ":":
            path = path[1:] # Windows fix
        with open(path[7:], "w") as outfile:
            outfile.write(self.script)

    @pyqtSlot(str, QObject, QObject)
    def save(self, path, alignment, positions):
        """Save the current state to a file"""
        path = path[7:]
        if path[-5:] != ".json":
            path += ".json"
        if path[0] == "/" and path[2] == ":":
            path = path[1:] # Windows fix
        with open(path, "w") as outfile:
            value = {
                "angleCommand": self._angle_command,
                "horizontalCommand": self._horizontal_command,
                "verticalCommand": self._vertical_command,
                "origin": self._origin,
                "frameWidth": self._frame_width,
                "frameHeight": self._frame_height,
                "runs": [r.to_json() for r in self._runs],
                "alignment": alignment.to_dict(),
                "positions": positions.to_dict()
            }
            json.dump(value, outfile)

    @pyqtSlot(str, QObject, QObject)
    def load(self, path, alignment, positions):
        """Read the state from a file"""
        path = path[7:]
        if path[-5:] != ".json":
            path += ".json"
        if path[0] == "/" and path[2] == ":":
            path = path[1:] # Windows fix
        with open(path, "r") as infile:
            value = json.load(infile)
        self._angle_command = value["angleCommand"]
        self._horizontal_command = value["horizontalCommand"]
        self._vertical_command = value["verticalCommand"]
        self._frame_width = value["frameWidth"]
        self.frameWidthChanged.emit()
        self._frame_height = value["frameHeight"]
        self._origin = value["origin"]

        self.beginRemoveRows(QModelIndex(),0,len(self._runs)-1)
        self.endRemoveRows()

        if value["runs"]:
            self.beginInsertRows(QModelIndex(), 0, len(value["runs"])-1)
            self._runs = [SingleRun.from_json(self, r)
                          for r in value["runs"]]
            self.endInsertRows()

        alignment.from_dict(value["alignment"])
        positions.from_dict(value["positions"])

        self.frameHeightChanged.emit()
        self.validChanged.emit()
        self.scriptChanged.emit()

    originChanged = pyqtSignal()

    @pyqtProperty(float, notify=originChanged)
    def origin(self):
        """The horizontal center of rotation."""
        return self._origin

    @origin.setter
    def origin(self, x):
        if x != x:
            return
        self._origin = x
        self.scriptChanged.emit()

    frameWidthChanged = pyqtSignal()

    @pyqtProperty(float, notify=frameWidthChanged)
    def frameWidth(self):
        """The physical width in mm of the reference frame in the photograph"""
        return self._frame_width

    @frameWidth.setter
    def frameWidth(self, x):
        self._frame_width = x
        self.scriptChanged.emit()

    frameHeightChanged = pyqtSignal()

    @pyqtProperty(float, notify=frameHeightChanged)
    def frameHeight(self):
        """The physical height in mm of the reference in the photograph"""
        return self._frame_height

    @frameHeight.setter
    def frameHeight(self, x):
        self._frame_height = x
        self.scriptChanged.emit()

    scriptChanged = pyqtSignal()

    @pyqtProperty(str, notify=scriptChanged)
    def angleCommand(self):
        """The outline of the command used to perform a angle run"""
        return self._angle_command

    @angleCommand.setter
    def angleCommand(self, value):
        print("Set angle command")
        if value == self._angle_command:
            return
        self._angle_command = value
        self.scriptChanged.emit()

    @pyqtProperty(str, notify=scriptChanged)
    def horizontalCommand(self):
        """The outline of the command used to perform a horizontal run"""
        return self._horizontal_command

    @horizontalCommand.setter
    def horizontalCommand(self, value):
        if value == self._horizontal_command:
            return
        self._horizontal_command = value
        self.scriptChanged.emit()

    @pyqtProperty(str, notify=scriptChanged)
    def verticalCommand(self):
        """The outline of the command used to perform a vertical run"""
        return self._vertical_command

    @verticalCommand.setter
    def verticalCommand(self, value):
        if value == self._vertical_command:
            return
        self._vertical_command = value
        self.scriptChanged.emit()

    @pyqtProperty(int)
    def count(self):
        """The current number of runs"""
        return len(self._runs)

    def rowCount(self, index=QModelIndex()):
        """The current number of runs.  This is required by QtQuick"""
        return len(self._runs)

    def data(self, index, role=Qt.DisplayRole):
        """Access the run at a given index.  This is required by QtQuick"""
        if not index.isValid():
            return QVariant()
        run = self._runs[index.row()]
        if role == Qt.DisplayRole:
            return run

        return QVariant()

    def setData(self, index, value, role=Qt.EditRole):
        """Update the data at a given index.  This is required by QtQuick"""
        if not index.isValid():
            return False

        if role == Qt.Edit:
            self._runs[index.row()] = value
            return True

        return False

    def flags(self, index):
        """A description of the model properties required by QtQuick"""
        if not index.isValid():
            return Qt.ItemIsEditable
        return Qt.ItemIsEnabled | Qt.ItemIsEditable

    @pyqtSlot(float, float)
    def append(self, startx, starty):
        """Create a new run starting at the given coordinates"""
        if self._runs:
            angles = self._runs[-1]._angles
            pos = self._runs[-1]._position
        else:
            angles = [0]
            pos = None
        run = SingleRun(self, startx, starty, angles=angles, position=pos)
        self.beginInsertRows(QModelIndex(),
                             len(self._runs),
                             len(self._runs))
        self._runs.append(run)
        self.endInsertRows()
        self.scriptChanged.emit()
        self.validChanged.emit()

    @pyqtSlot(float, float)
    def update(self, x, y):
        """Change the ending coordinates of the most recent run"""
        delta_x = x-self._runs[-1]._x  # pylint: disable=W0212
        delta_y = y-self._runs[-1]._y  # pylint: disable=W0212
        if abs(delta_x) > abs(delta_y):
            self._runs[-1]._vertical = False  # pylint: disable=W0212
            self._runs[-1]._length = delta_x  # pylint: disable=W0212
        else:
            self._runs[-1]._vertical = True  # pylint: disable=W0212
            self._runs[-1]._length = delta_y  # pylint: disable=W0212
        i = len(self._runs) - 1
        self.dataChanged.emit(self.index(i, 0), self.index(i, 0))
        self.scriptChanged.emit()

    @pyqtSlot(int)
    def remove(self, i):
        """Delete a run"""
        if i >= len(self._runs):
            return False
        self.beginRemoveRows(QModelIndex(), i, i)
        del self._runs[i]
        self.endRemoveRows()
        self.scriptChanged.emit()
        return True

    @pyqtSlot(int, result=SingleRun)
    def get(self, i):
        """Access a single run."""
        return self._runs[i]

    @pyqtProperty(str, notify=scriptChanged)
    def script(self):
        """The instrument script the performs the requested runs"""
        temp = "\n\n".join([r.script_line(
            self._angle_command,
            self._horizontal_command,
            self._vertical_command,
            self._origin,
            self._frame_width,
            self._frame_height)
                            for r in self._runs])
        return temp

    validChanged = pyqtSignal()

    @pyqtProperty(bool, notify=validChanged)
    def valid(self):
        """Can the current model be exported into a usable script"""
        if not self._runs:
            return False
        return all([r.valid for r in self._runs])


qmlRegisterType(RunModel, "PythonAlign", 1, 0, "RunModel")
