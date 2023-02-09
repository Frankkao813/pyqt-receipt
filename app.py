
import sys
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import (
    QApplication
)
from receipt_system.login import Login 
# https://stackoverflow.com/questions/1383239/can-i-use-init-py-to-define-global-variables
from receipt_system import app, widget # will it be working?

if __name__ == "__main__":

    # https://www.youtube.com/watch?v=82v2ZR-g6wY
    
    login = Login()
    widget.addWidget(login)

    widget.setFixedHeight(400)
    widget.setFixedWidth(400)
    widget.setWindowTitle("receipt app")
    widget.show()
    sys.exit(app.exec())