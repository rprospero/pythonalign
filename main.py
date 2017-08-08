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
        self._segment_count = 256
        self._p1 = QPointF(0, 0)
        self._p2 = QPointF(1, 0)
        self._p3 = QPointF(0, 1)
        self._p4 = QPointF(1, 1)

        self._pixmap = QPixmap("img.jpg")

    def updatePaintNode(self, oldNode, _):
        if not oldNode:
            node3 = QSGGeometryNode()

            node2 = QSGSimpleTextureNode()
            node = QSGNode()
            texture = self.window().createTextureFromImage(self._pixmap.toImage())
            node2.setTexture(texture)
            # node3.appendChildNode(node2)
            node.appendChildNode(node3)

            geometry = QSGGeometry(QSGGeometry.defaultAttributes_Point2D(),
                                   self._segment_count)
            geometry.setLineWidth(2)
            geometry.setDrawingMode(QSGGeometry.DrawLineStrip)
            node3.setGeometry(geometry)
            node3.setFlag(QSGNode.OwnsGeometry)
            material = QSGFlatColorMaterial()
            material.setColor(QColor(255, 0, 0))
            node3.setMaterial(material)
            node3.setFlag(QSGNode.OwnsMaterial)
            print("New node!")
        else:
            node = oldNode
            geometry = node.firstChild().geometry()
            geometry.allocate(self._segment_count)
            print("Old Node!")

        vertices = geometry.vertexDataAsPoint2D()

        for i in range(self._segment_count):
            t = float(i)/(self._segment_count-1)
            invt = 1-t

            pos = invt * invt * invt * self._p1 \
                  + 3 * invt * invt * t * self._p2 \
                  + 3 * invt * t * t * self._p3 \
                  + t * t * t * self._p4 \


            x = pos.x() * self.width()
            y = pos.y() * self.height()

            vertices[i].set(x, y)

        node.firstChild().markDirty(QSGNode.DirtyGeometry)

        return node


qmlRegisterType(AlignData, "PythonAlign", 1, 0, "AlignData")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    engine = QQmlApplicationEngine("main.qml")
    engine.rootObjects()[0].show()

    sys.exit(app.exec_())
