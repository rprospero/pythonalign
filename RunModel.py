import json
from PyQt5.QtCore import pyqtProperty, pyqtSignal, pyqtSlot, Qt, QModelIndex, \
    QAbstractListModel, QVariant
from PyQt5.QtQml import qmlRegisterType
from SingleRun import SingleRun


class RunModel(QAbstractListModel):

    _roles = {Qt.DisplayRole: b"run"}

    def roleNames(self):
        return self._roles

    def __init__(self, parent=None):
        super(RunModel, self).__init__(parent)
        self._runs = []
        self._horizontal_command = ""
        self._vertical_command = ""
        self._frame_width = 1
        self._frame_height = 1

    @pyqtSlot(str)
    def export(self, path):
        with open(path[7:], "w") as outfile:
            outfile.write(self.script)

    @pyqtProperty(str)
    def alignmentJson(self):
        return self._alignmentJson

    @pyqtSlot(str, str)
    def save(self, path, alignmentJson):
        path = path[7:]
        if path[-5:] != ".json":
            path += ".json"
        print(path)
        with open(path, "w") as outfile:
            d = {
                "horizontalCommand": self._horizontal_command,
                "verticalCommand": self._vertical_command,
                "frameWidth": self._frame_width,
                "frameHeight": self._frame_height,
                "runs": [r.toJson() for r in self._runs],
                "alignment": json.loads(alignmentJson)
            }
            json.dump(d, outfile)

    @pyqtSlot(str)
    def load(self, path):
        path = path[7:]
        if path[-5:] != ".json":
            path += ".json"
        print(path)
        with open(path, "r") as infile:
            d = json.load(infile)
        self._horizontal_command = d["horizontalCommand"]
        self._vertical_command = d["verticalCommand"]
        self._frame_width = d["frameWidth"]
        self.frameWidthChanged.emit()
        self._frame_height = d["frameHeight"]
        self._runs = [SingleRun.fromJson(self, r)
                      for r in d["runs"]]
        self._alignmentJson = json.dumps(d["alignment"])

        self.frameHeightChanged.emit()
        self.validChanged.emit()
        self.scriptChanged.emit()

    frameWidthChanged = pyqtSignal()

    @pyqtProperty(float, notify=frameWidthChanged)
    def frameWidth(self):
        return self._frame_width

    @frameWidth.setter
    def frameWidth(self, x):
        self._frame_width = x
        self.scriptChanged.emit()

    frameHeightChanged = pyqtSignal()

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
        self.validChanged.emit()

    @pyqtSlot(float, float)
    def update(self, x, y):
        dx = x-self._runs[-1]._x
        dy = y-self._runs[-1]._y
        if abs(dx) > abs(dy):
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
        temp = "\n\n".join([r.script_line(self._horizontal_command,
                                          self._vertical_command,
                                          self._frame_width,
                                          self._frame_height)
                            for r in self._runs])
        return temp

    validChanged = pyqtSignal()

    @pyqtProperty(bool, notify=validChanged)
    def valid(self):
        if not self._runs:
            return False
        return all([r.valid for r in self._runs])


qmlRegisterType(RunModel, "PythonAlign", 1, 0, "RunModel")
