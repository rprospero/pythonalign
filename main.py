#!/usr/bin/python

import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QUrl, pyqtProperty, pyqtSignal, pyqtSlot, QObject, QPointF
from PyQt5.QtGui import QColor
from PyQt5.QtQml import qmlRegisterType, QQmlApplicationEngine
from PyQt5.QtQuick import QQuickItem, QSGGeometryNode, QSGGeometry, QSGNode, \
    QSGFlatColorMaterial


class AlignData(QQuickItem):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFlag(QQuickItem.ItemHasContents, True)
        self._segment_count = 32
        self._p1 = QPointF(0, 0)
        self._p2 = QPointF(1, 0)
        self._p3 = QPointF(0, 1)
        self._p4 = QPointF(1, 1)

    def updatePaintNode(self, oldNode, _):
        if not oldNode:
            node = QSGGeometryNode()
            geometry = QSGGeometry(QSGGeometry.defaultAttributes_Point2D(), 32)
            geometry.setLineWidth(2)
            geometry.setDrawingMode(QSGGeometry.DrawLineStrip)
            node.setGeometry(geometry)
            node.setFlag(QSGNode.OwnsGeometry)
            material = QSGFlatColorMaterial()
            material.setColor(QColor(255, 0, 0))
            node.setMaterial(material)
            node.setFlag(QSGNode.OwnsMaterial)
        else:
            node = oldNode
            geometry = node.geometry()

        # bounds = self.boundingRect()
        vertices = geometry.vertexDataAsPoint2D()

        for i in range(self._segment_count):
            t = float(i)/(self._segment_count-1)
            invt = 1-t

            pos = invt * invt * invt * self._p1 \
                  + 3 * invt * invt * t * self._p2 \
                  + 3 * invt * t * t * self._p3 \
                  + t * t * t * self._p4 \


            x = 0 + pos.x() * 400 # bounds.width()
            y = 0 + pos.y() * 400 # bounds.height()

            vertices[i].set(x, y)

        return node


qmlRegisterType(AlignData, "PythonAlign", 1, 0, "AlignData")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    engine = QQmlApplicationEngine("main.qml")
    engine.rootObjects()[0].showFullScreen()

    sys.exit(app.exec_())
