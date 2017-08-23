import json
import numpy as np
from PyQt5.QtCore import pyqtProperty, pyqtSignal, pyqtSlot, QPointF
from PyQt5.QtGui import QPixmap
from PyQt5.QtQml import qmlRegisterType
from PyQt5.QtQuick import QQuickItem


class AlignData(QQuickItem):
    def __init__(self, parent=None):
        super().__init__(parent)
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
        d1 = (self._p1.x()-x)**2+(self._p1.y()-y)**2
        d2 = (self._p2.x()-x)**2+(self._p2.y()-y)**2
        d3 = (self._p3.x()-x)**2+(self._p3.y()-y)**2
        d4 = (self._p4.x()-x)**2+(self._p4.y()-y)**2
        if d1 < d2 and d1 < d3 and d1 < d4:
            self._p1.setX(x)
            self._p1.setY(y)
        elif d2 < d3 and d2 < d4:
            self._p2.setX(x)
            self._p2.setY(y)
        elif d3 < d4:
            self._p3.setX(x)
            self._p3.setY(y)
        else:
            self._p4.setX(x)
            self._p4.setY(y)
        self.linreg()

    realigned = pyqtSignal()

    def linreg(self):
        ys = [0, self._newsize, self._newsize+self._newsize*1.0j,
              self._newsize*1.0j]
        xs = [self.toComplex(p) for p in
              [self._p1, self._p2, self._p3, self._p4]]
        xmean = np.mean(xs)
        ymean = np.mean(ys)
        self._slope = np.sum((xs-xmean)*np.conj(ys-ymean)) / \
            np.sum(np.abs(xs-xmean)**2)
        self._intercept = ymean - self._slope*xmean
        print(np.abs(self._slope))
        print(np.angle(self._slope))
        print(self._intercept)
        self.realigned.emit()

    @staticmethod
    def toComplex(v):
        return v.x()+1j*v.y()

    @pyqtProperty('qreal', notify=realigned)
    def width(self): return self._width

    @width.setter
    def width(self, p):
        self._width = p
        self.linreg()

    @pyqtProperty('qreal', notify=realigned)
    def height(self): return self._height

    @height.setter
    def height(self, p):
        self._height = p
        self.linreg()

    @pyqtProperty('qreal', notify=realigned)
    def newsize(self): return self._newsize

    @newsize.setter
    def newsize(self, p):
        self._newsize = p
        self.linreg()

    @pyqtProperty('QPointF', notify=realigned)
    def p1(self): return self._p1

    @p1.setter
    def p1(self, p):
        self._p1 = p
        self.linreg()

    @pyqtProperty('QPointF')
    def p2(self): return self._p2

    @p2.setter
    def p2(self, p):
        self._p2 = p
        self.linreg()

    @pyqtProperty('QPointF')
    def p3(self): return self._p3

    @p3.setter
    def p3(self, p):
        self._p3 = p
        self.linreg()

    @pyqtProperty('QPointF')
    def p4(self): return self._p4

    @p4.setter
    def p4(self, p):
        self._p4 = p
        self.linreg()

    @pyqtProperty(str)
    def jsonString(self):
        d = {"p1": {"x": self._p1.x(), "y": self._p1.y()},
             "p2": {"x": self._p2.x(), "y": self._p2.y()},
             "p3": {"x": self._p3.x(), "y": self._p3.y()},
             "p4": {"x": self._p4.x(), "y": self._p4.y()}}
        return json.dumps(d)

    @jsonString.setter
    def jsonString(self, v):
        d = json.loads(v)
        self._p1 = QPointF(d["p1"]["x"], d["p1"]["y"])
        self._p2 = QPointF(d["p2"]["x"], d["p2"]["y"])
        self._p3 = QPointF(d["p3"]["x"], d["p3"]["y"])
        self._p4 = QPointF(d["p4"]["x"], d["p4"]["y"])
        self.linreg()

    def _hangle(self, b, a):
        dx = b.x() - a.x()
        dy = b.y() - a.y()
        return 180*np.arctan2(dy, dx)/np.pi

    @pyqtProperty('qreal', notify=realigned)
    def angle(self):
        print(np.angle(self._slope)*180/np.pi)
        return np.angle(self._slope)*180/np.pi

    @pyqtProperty('qreal', notify=realigned)
    def scale(self):
        print("Scale:", np.abs(self._slope))
        return np.abs(self._slope)

    @pyqtProperty('QPointF', notify=realigned)
    def translate(self):
        old_center = self._newsize * (0.5 + 0.5j)
        center = (old_center-self._intercept)/self._slope
        offset = (self._width/2 + self._height/2*1.0j) - center
        print("Offset: ", offset)

        return QPointF(np.real(offset), np.imag(offset))


qmlRegisterType(AlignData, "PythonAlign", 1, 0, "AlignData")
