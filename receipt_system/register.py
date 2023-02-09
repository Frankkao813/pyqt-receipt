from PyQt6.QtWidgets import (
    QDialog,
    QLineEdit,
    QDateEdit,
    QVBoxLayout,
    QFormLayout,
    QPushButton,
    QLabel,
)

#from login import Login
from . import login
from receipt_system import widget

class Register(QDialog):
    def __init__(self):
        super().__init__()
        RegisterLayout = QVBoxLayout()

        # create register form
        registerTitle = QLabel("Register")
        registerFormLayout = QFormLayout()
        self.realName = QLineEdit()
        self.setUsername = QLineEdit()
        self.setBirthday = QDateEdit()
        self.setPassword = QLineEdit()
        registerFormLayout.addRow("real name", self.realName)
        registerFormLayout.addRow("Birthday", self.setBirthday)
        registerFormLayout.addRow("Username: ", self.setUsername) 
        registerFormLayout.addRow("password", self.setPassword)
        complete = QPushButton("complete")
        toLogin = QPushButton("back")
        RegisterLayout.addWidget(registerTitle)
        RegisterLayout.addLayout(registerFormLayout)
        RegisterLayout.addWidget(complete)
        RegisterLayout.addWidget(toLogin)
        # TODO: check whether there is empty blank
        complete.clicked.connect(self._registerSubmit)
        toLogin.clicked.connect(self._toLoginPage)
        

        self.setLayout(RegisterLayout)

    def _registerSubmit(self):
        # TODO: write to database
        pass

    def _toLoginPage(self):
        login_page = login.Login()
        widget.addWidget(login_page)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def _checkInput(self):
        # TODO: whether any of the input is blank
        pass
