#!/usr/bin/python

import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QUrl, pyqtProperty, pyqtSignal, pyqtSlot, QObject, QPointF
from PyQt5.QtGui import QColor, QPixmap
from PyQt5.QtQml import qmlRegisterType, QQmlApplicationEngine
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

    @pyqtProperty('QPointF')
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

    def updatePaintNode(self, oldNode, _):
        if not oldNode:
            node3 = QSGGeometryNode()

            node2 = QSGSimpleTextureNode()
            node = QSGNode()
            texture = self.window().createTextureFromImage(self._pixmap.toImage())
            node2.setTexture(texture)
            node.appendChildNode(node3)

            geometry = QSGGeometry(QSGGeometry.defaultAttributes_Point2D(), 5)
            geometry.setLineWidth(2)
            geometry.setDrawingMode(QSGGeometry.DrawLineStrip)
            node3.setGeometry(geometry)
            node3.setFlag(QSGNode.OwnsGeometry)
            material = QSGFlatColorMaterial()
            material.setColor(QColor(255, 0, 0))
            node3.setMaterial(material)
            node3.setFlag(QSGNode.OwnsMaterial)
        else:
            node = oldNode
            geometry = node.firstChild().geometry()
            geometry.allocate(5)

        vertices = geometry.vertexDataAsPoint2D()

        vertices[0].set(self._p1.x() * self.width(),
                        self._p1.y() * self.height())
        vertices[1].set(self._p2.x() * self.width(),
                        self._p2.y() * self.height())
        vertices[2].set(self._p3.x() * self.width(),
                        self._p3.y() * self.height())
        vertices[3].set(self._p4.x() * self.width(),
                        self._p4.y() * self.height())
        vertices[4].set(self._p1.x() * self.width(),
                        self._p1.y() * self.height())

        node.firstChild().markDirty(QSGNode.DirtyGeometry)

        return node


qmlRegisterType(AlignData, "PythonAlign", 1, 0, "AlignData")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    engine = QQmlApplicationEngine("main.qml")
    engine.rootObjects()[0].show()

    sys.exit(app.exec_())
