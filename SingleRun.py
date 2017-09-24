"""This module houses the SingleRun class, which manages
an individual scan on a sample
"""
from PyQt5.QtCore import pyqtProperty, pyqtSignal, QObject
from PyQt5.QtQml import qmlRegisterType
import PositionModel
from math import pi, cos

def xadjust(pos, origin, angle):
    return origin + (pos-origin)*cos(angle*pi/180)

class SingleRun(QObject):
    """The class describes a single scan to be performed on the sample."""
    def __init__(self, parent, startx=0, starty=0, angles=[0], position=None):
        super(SingleRun, self).__init__(parent)
        if not position:
            position = PositionModel.SinglePosition(parent)
        self._parent = parent
        self._x = startx
        self._y = starty
        self._vertical = False
        self._length = 0
        self._step_size = 0.5
        self._selected = False
        self._title = ""
        self._valid = False
        self._angles = angles
        self._position = position

    @staticmethod
    def from_json(parent, x):
        """Creates an object from a json string that describes the object"""
        self = SingleRun(parent)
        self._x = x["startx"]  # pylint: disable=W0212
        self._y = x["starty"]  # pylint: disable=W0212
        self._vertical = x["vertical"]  # pylint: disable=W0212
        self._length = x["length"]  # pylint: disable=W0212
        self._step_size = x["step_size"]  # pylint: disable=W0212
        self._title = x["title"]  # pylint: disable=W0212
        self._valid = x["valid"]  # pylint: disable=W0212
        self._angles = x["angles"]  # pylint: disable=W0212
        self._position = SinglePosition.from_dict(x["position"])  # pylint: disable=W0212
        return self

    def to_json(self):
        """Serializes a SingleRun object into a json string"""
        return {"startx": self._x,
                "starty": self._y,
                "vertical": self._vertical,
                "length": self._length,
                "step_size": self._step_size,
                "title": self._title,
                "angles": self._angles,
                "position": self._position.to_dict(),
                "valid": self._valid}

    validChanged = pyqtSignal()

    @pyqtProperty(bool, notify=validChanged)
    def valid(self):
        """A boolean describing if the run is valid for writing to a file"""
        if not self.title or " " in self.title:
            return False
        return True

    titleChanged = pyqtSignal(str)

    @pyqtProperty(str, notify=titleChanged)
    def title(self):
        """The title for the run"""
        return self._title

    @title.setter
    def title(self, value):
        self._title = value
        self._parent.scriptChanged.emit()
        self.validChanged.emit()
        self._parent.validChanged.emit()

    anglesChanged = pyqtSignal()

    @pyqtProperty(str, notify=anglesChanged)
    def angles(self):
        """A comma delimited string of angles"""
        return ",".join(map(str, self._angles))

    @angles.setter
    def angles(self, x):
        try:
            self._angles = [float(angle) for angle in x.split(",")]
            self._parent.scriptChanged.emit()
        except ValueError:
            pass

    positionChanged = pyqtSignal()

    @pyqtProperty(QObject, notify=positionChanged)
    def position(self):
        """Which frame position the sample is in"""
        return self._position

    @position.setter
    def position(self, value):
        if self._position == value:
            return
        self._position = value
        self.positionChanged.emit()
        self._parent.scriptChanged.emit()

    stepSizeChanged = pyqtSignal(float)

    @pyqtProperty(float, notify=stepSizeChanged)
    def stepSize(self):
        """The spacing between measurements, in mm"""
        return self._step_size

    @stepSize.setter
    def stepSize(self, x):
        self._step_size = x
        self._parent.scriptChanged.emit()

    startxChanged = pyqtSignal(float)

    @pyqtProperty(float, notify=startxChanged)
    def startx(self):
        """The initial horizontal position for the scan"""
        return self._x

    startyChanged = pyqtSignal(float)

    @pyqtProperty(float, notify=startyChanged)
    def starty(self):
        """The initial vertical position for the scan"""
        return self._y

    stopxChanged = pyqtSignal(float)

    @pyqtProperty(float, notify=stopxChanged)
    def stopx(self):
        """The final horizontal position for the scan"""
        if self._vertical:
            return self._x
        return self._x+self._length

    stopyChanged = pyqtSignal(float)

    @pyqtProperty(float, notify=stopyChanged)
    def stopy(self):
        """The final vertical position for the scan"""
        if self._vertical:
            return self._y+self._length
        return self._y

    @pyqtProperty(bool)
    def selected(self):
        """A boolean indicating whether this run is currently being examined"""
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

    @selected.setter
    def selected(self, value):
        self._selected = value

    def script_line(self, angle, hor, ver, origin, width, height):
        """Turn the run into a command for the script file.
        Parameters
        ----------
        hor: string
          The format string that describes how to write a horizontal scan
        ver: string
          The format string that describes how to write a vertical scan
        width: float
          The width of the selected image region in mm
        height: float
          The height of the selected image region in mm

        Returns
        -------
        A string containing the scripting commands for the instrument

        """
        if self._vertical:
            skeleton = ver
            length_scale = height
        else:
            skeleton = hor
            length_scale = width

        skeleton = angle + "\n\n" + skeleton

        result = []
        for angle in self._angles:
            try:
                result.append(skeleton.format(
                    startx=xadjust(self.startx*width, origin, angle),
                    starty=self.starty*height,
                    stopx=xadjust(self.stopx*width, origin, angle),
                    stopy=self.stopy*height,
                    title=self._title,
                    angle=angle,
                    top=self._position._top,
                    left=self._position._left,
                    ndark=1,
                    time=0.04,
                    stepSize=self._step_size * cos(angle*pi/180),
                    frameCount=round(self._length*length_scale/self._step_size),
                    sleep=0,
                    len=self._length*length_scale))
            except IndexError:
                result.append("!!!!" + skeleton + "!!!! Missing Key")
            except KeyError as error:
                result.append("!!!!" + skeleton + "!!!! Missing Key: " + str(error))
            except ValueError as error:
                result.append( "!!!!" + skeleton + "!!!! Bad format specifier: " \
                               + str(error))

        return "\n\n".join(result)


qmlRegisterType(SingleRun, "PythonAlign", 1, 0, "SingleRun")
