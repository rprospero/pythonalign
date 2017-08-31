#!/usr/bin/python

import sys
import AlignData
import RunModel
from PyQt5.QtWidgets import QApplication
from PyQt5.QtQml import QQmlApplicationEngine


if __name__ == "__main__":
    app = QApplication(sys.argv)
    engine = QQmlApplicationEngine("main.qml")
    engine.rootObjects()[0].show()

    sys.exit(app.exec_())
