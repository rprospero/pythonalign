import json
import numpy as np
from PyQt5.QtCore import pyqtProperty, pyqtSignal, pyqtSlot, QPointF
from PyQt5.QtGui import QColor, QPixmap
from PyQt5.QtQml import qmlRegisterType
from PyQt5.QtQuick import QQuickItem, QSGGeometryNode, QSGGeometry, QSGNode, \
    QSGFlatColorMaterial, QSGSimpleTextureNode


class AlignData(QQuickItem):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFlag(QQuickItem.ItemHasContents, True)
        self._p1 = QPointF(0.1, 0.1)
        self._p2 = QPointF(0.9, 0.1)
        self._p3 = QPointF(0.9, 0.9)
        self._p4 = QPointF(0.1, 0.9)

        self._pixmap = QPixmap("img.jpg")

    @pyqtSlot(float, float)
    def select(self, x, y):
        d1 = (self._p1.x()-x)**2+(self._p1.y()-y)**2
        d2 = (self._p2.x()-x)**2+(self._p2.y()-y)**2
        d3 = (self._p3.x()-x)**2+(self._p3.y()-y)**2
        d4 = (self._p4.x()-x)**2+(self._p4.y()-y)**2
        if d1<d2 and d1<d3 and d1<d4:
            self._p1.setX(x)
            self._p1.setY(y)
        elif d2<d3 and d2<d4:
            self._p2.setX(x)
            self._p2.setY(y)
        elif d3<d4:
            self._p3.setX(x)
            self._p3.setY(y)
        else:
            self._p4.setX(x)
            self._p4.setY(y)
        self.realigned.emit()
        self.update()

    realigned = pyqtSignal()

    @pyqtProperty('QPointF', notify=realigned)
    def p1(self): return self._p1
    @p1.setter
    def p1(self, p): self._p1 = p; self.update()
    @pyqtProperty('QPointF')
    def p2(self): return self._p2
    @p2.setter
    def p2(self, p): self._p2 = p; self.update()
    @pyqtProperty('QPointF')
    def p3(self): return self._p3
    @p3.setter
    def p3(self, p): self._p3 = p; self.update()
    @pyqtProperty('QPointF')
    def p4(self): return self._p4
    @p4.setter
    def p4(self, p): self._p4 = p; self.update()

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
        self.realigned.emit()
        self.update()

    def _hangle(self, b, a):
        dx = b.x() - a.x()
        dy = b.y() - a.y()
        return 180*np.arctan2(dy, dx)/np.pi

    @pyqtProperty('qreal', notify=realigned)
    def angle(self):
        a = self._hangle(self._p2, self._p1)
        b = self._hangle(self._p3, self._p4)
        c = self._hangle(self._p3, self._p2)-90
        d = 90+self._hangle(self._p1, self._p4)
        return -(a+b+c+d)/4

    @pyqtProperty('QPointF', notify=realigned)
    def scale(self):
        x = (np.sqrt((self._p2.x()-self._p1.x())**2 +
               (self._p2.y()-self._p1.y())**2) +
             np.sqrt((self._p4.x()-self._p3.x())**2 +
               (self._p4.y()-self._p3.y())**2))/2
        y = (np.sqrt((self._p2.x()-self._p3.x())**2 +
               (self._p2.y()-self._p3.y())**2) +
             np.sqrt((self._p4.x()-self._p1.x())**2 +
               (self._p4.y()-self._p1.y())**2))/2
        return QPointF(1.0/x, 1.0/y)


    @pyqtProperty('QPointF', notify=realigned)
    def translate(self):
        base = self._p1+self._p2+self._p3+self._p4
        base /= 4
        return QPointF(0.5, 0.5) - base

qmlRegisterType(AlignData, "PythonAlign", 1, 0, "AlignData")
