from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QFormLayout,
    QLineEdit,
    QPlainTextEdit,
    QPushButton,
    QDialogButtonBox

)

#from .login import Login
from . import login
from .pdfFile import pdfFile
import sys
from receipt_system import widget

class Window(QDialog):
    def __init__(self):
        super().__init__() # parent = None??
        self.appLayout = QVBoxLayout() #
        formLayout = QFormLayout()

        self.name = QLineEdit()
        formLayout.addRow("Name: ", self.name)
        self.class_pricing = QPlainTextEdit()
        formLayout.addRow("class,pricing: ", self.class_pricing)
        self.note = QLineEdit()
        formLayout.addRow("note", self.note)

        self.appLayout.addLayout(formLayout)
        
        self.buttons = QDialogButtonBox()
        self.buttons.setStandardButtons(
            QDialogButtonBox.StandardButton.Cancel|
            QDialogButtonBox.StandardButton.Ok
        )
        self.logoutButton = QPushButton("Logout")
        # https://stackoverflow.com/questions/33547821/execute-function-after-click-ok-qdialogbuttonbox
        # try-except case
        self.buttons.accepted.connect(self._accept)
        self.buttons.rejected.connect(self._reject)
        self.logoutButton.clicked.connect(self._logout)
        
        self.appLayout.addWidget(self.buttons)
        self.appLayout.addWidget(self.logoutButton)
        self.setLayout(self.appLayout)

    def _accept(self):
        # Q: how to extract the information in input box of formlayout?
        name_data = self.name.text()
        # http://www.learningaboutelectronics.com/Articles/How-to-retrieve-data-from-plain-text-edit-qt-widget-c++.php
        class_pricing_data = self.class_pricing.toPlainText()
        note_data = self.note.text()
        # generating pdf file
        pdfFile(name_data, class_pricing_data, note_data)

        sys.exit()

    def _reject(self):
        # TODO: clear the dialog box
        self.name.setText("")
        self.class_pricing.clear()
        self.note.setText("")
        print("request declined.")
        # sys.exit()
    
    def _logout(self):
        login_page = login.Login()
        widget.addWidget(login_page)
        widget.setCurrentIndex(widget.currentIndex()+1)

