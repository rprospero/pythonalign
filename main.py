#!/usr/bin/python

import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFontDatabase
from PyQt5.QtCore import QUrl, pyqtProperty, pyqtSignal, pyqtSlot, QObject
from PyQt5.QtQml import qmlRegisterType, QQmlApplicationEngine
from PyQt5.QtQuick import QQuickView


if __name__ == "__main__":
    app = QApplication(sys.argv)
    engine = QQmlApplicationEngine("main.qml")
    engine.rootObjects()[0].showFullScreen()

    sys.exit(app.exec_())
