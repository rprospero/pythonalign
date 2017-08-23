""" This module calculates the alignment of the sample images"""
import json
import numpy as np
from PyQt5.QtCore import pyqtProperty, pyqtSignal, pyqtSlot, QPointF
from PyQt5.QtGui import QPixmap
from PyQt5.QtQml import qmlRegisterType
from PyQt5.QtQuick import QQuickItem


class AlignData(QQuickItem):
    """This class models the alignment of an image"""
    def __init__(self, parent=None):
        super(AlignData, self).__init__(parent)
        self.setFlag(QQuickItem.ItemHasContents, True)
        self._p1 = QPointF(0.1, 0.1)
        self._p2 = QPointF(100, 0.1)
        self._p3 = QPointF(100, 100)
        self._p4 = QPointF(0.1, 100)
        self._slope = 1.0+0.0j
        self._intercept = 0.0+0.0j
        self._width = 1
        self._height = 1
        self._newsize = 1

        self._pixmap = QPixmap("img.jpg")

    @pyqtSlot(float, float)
    def select(self, x, y):
        """Find the point closest to a coordinate and move that point to the
        new coordinate"""
        distance1 = (self._p1.x()-x)**2+(self._p1.y()-y)**2
        distance2 = (self._p2.x()-x)**2+(self._p2.y()-y)**2
        distance3 = (self._p3.x()-x)**2+(self._p3.y()-y)**2
        distance4 = (self._p4.x()-x)**2+(self._p4.y()-y)**2
        if distance1 < distance2 and \
           distance1 < distance3 and \
           distance1 < distance4:
            self._p1.setX(x)
            self._p1.setY(y)
        elif distance2 < distance3 and distance2 < distance4:
            self._p2.setX(x)
            self._p2.setY(y)
        elif distance3 < distance4:
            self._p3.setX(x)
            self._p3.setY(y)
        else:
            self._p4.setX(x)
            self._p4.setY(y)
        self.linreg()

    realigned = pyqtSignal()

    def linreg(self):
        """Use a linear regression to find the desired transformation between
        the control points and the corners of the reference image"""
        ys = [0, self._newsize, self._newsize+self._newsize*1.0j,
              self._newsize*1.0j]
        xs = [self.toComplex(p) for p in
              [self._p1, self._p2, self._p3, self._p4]]
        xmean = np.mean(xs)
        ymean = np.mean(ys)
        self._slope = np.sum((xs-xmean)*np.conj(ys-ymean)) / \
            np.sum(np.abs(xs-xmean)**2)
        self._intercept = ymean - self._slope*xmean
        self.realigned.emit()

    @staticmethod
    def toComplex(v):
        """Turn a Qt QPoint into a complex number"""
        return v.x()+1j*v.y()

    @pyqtProperty('qreal', notify=realigned)
    def width(self):
        """The width of the photorgaph"""
        return self._width

    @width.setter
    def width(self, p):
        self._width = p
        self.linreg()

    @pyqtProperty('qreal', notify=realigned)
    def height(self):
        """The height of the photograph"""
        return self._height

    @height.setter
    def height(self, p):
        self._height = p
        self.linreg()

    @pyqtProperty('qreal', notify=realigned)
    def newsize(self):
        """The width and height of the cropped reference image"""
        return self._newsize

    @newsize.setter
    def newsize(self, p):
        self._newsize = p
        self.linreg()

    @pyqtProperty('QPointF', notify=realigned)
    def p1(self):
        """The control point for the top left corner"""
        return self._p1

    @p1.setter
    def p1(self, p):
        self._p1 = p
        self.linreg()

    @pyqtProperty('QPointF')
    def p2(self):
        """The control point for the top right corner"""
        return self._p2

    @p2.setter
    def p2(self, p):
        self._p2 = p
        self.linreg()

    @pyqtProperty('QPointF')
    def p3(self):
        """The control point for the bottom right corner"""
        return self._p3

    @p3.setter
    def p3(self, p):
        self._p3 = p
        self.linreg()

    @pyqtProperty('QPointF')
    def p4(self):
        """The control point for the bottom left corner"""
        return self._p4

    @p4.setter
    def p4(self, p):
        self._p4 = p
        self.linreg()

    @pyqtProperty(str)
    def jsonString(self):
        """A JSON serialisation of the object's current state"""
        value = {"p1": {"x": self._p1.x(), "y": self._p1.y()},
                 "p2": {"x": self._p2.x(), "y": self._p2.y()},
                 "p3": {"x": self._p3.x(), "y": self._p3.y()},
                 "p4": {"x": self._p4.x(), "y": self._p4.y()}}
        return json.dumps(value)

    @jsonString.setter
    def jsonString(self, value):
        value = json.loads(value)
        self._p1 = QPointF(value["p1"]["x"], value["p1"]["y"])
        self._p2 = QPointF(value["p2"]["x"], value["p2"]["y"])
        self._p3 = QPointF(value["p3"]["x"], value["p3"]["y"])
        self._p4 = QPointF(value["p4"]["x"], value["p4"]["y"])
        self.linreg()

    @pyqtProperty('qreal', notify=realigned)
    def angle(self):
        """The rotation correction angle for the reference image"""
        return np.angle(self._slope)*180/np.pi

    @pyqtProperty('qreal', notify=realigned)
    def scale(self):
        """The appropriate magnification for the reference image"""
        return np.abs(self._slope)

    @pyqtProperty('QPointF', notify=realigned)
    def translate(self):
        """The position offset for the reference image"""
        old_center = self._newsize * (0.5 + 0.5j)
        center = (old_center-self._intercept)/self._slope
        offset = (self._width/2 + self._height/2*1.0j) - center

        return QPointF(np.real(offset), np.imag(offset))


qmlRegisterType(AlignData, "PythonAlign", 1, 0, "AlignData")
