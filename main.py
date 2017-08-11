#!/usr/bin/python

import numpy as np
import sys
import AlignData
from PyQt5.QtWidgets import QApplication
from PyQt5.QtQml import QQmlApplicationEngine



if __name__ == "__main__":
    app = QApplication(sys.argv)
    engine = QQmlApplicationEngine("main.qml")
    engine.rootObjects()[0].show()

    sys.exit(app.exec_())
