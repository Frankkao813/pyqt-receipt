from PyQt6.QtWidgets import (
    QDialog,
    QLineEdit,
    QDateEdit,
    QVBoxLayout,
    QFormLayout,
    QPushButton,
    QLabel,
    QMessageBox,
    
)

#from login import Login
from . import login
from . import window
from PyQt6.QtCore import QDate, Qt
from PyQt6.QtGui import QFont
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

        # set the properties of widgets
        registerTitle.setFont(QFont('Arial', 20, 900, True))
        registerTitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        RegisterLayout.addLayout(registerFormLayout)
        registerFormLayout.setFormAlignment(Qt.AlignmentFlag.AlignHCenter)

        RegisterLayout.addWidget(complete)
        RegisterLayout.addWidget(toLogin)
        # TODO: check whether there is empty blank
        complete.clicked.connect(self._checkInput)
        toLogin.clicked.connect(self._toLoginPage)
        
        self.setLayout(RegisterLayout)

    def _toWindowPage(self):
        # TODO: write to database

        # go to the window class
        window_Page = window.Window()
        widget.addWidget(window_Page)
        widget.setCurrentIndex(widget.currentIndex()+1)


    def _toLoginPage(self):
        login_page = login.Login()
        widget.addWidget(login_page)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def _checkInput(self):
        # TODO: whether any of the input is blank
        dateInput = self.setBirthday.date()
        dateToday = QDate.currentDate()
        #year, month, day = QCalendar.partsFromDate(date)
        errorMessage  = QMessageBox()
        if (len(self.realName.text()) == 0 or len(self.setUsername.text()) == 0 or len(self.setPassword.text()) == 0):
            errorMessage.critical(self, "error", "Please eneter text in each field.")
            errorMessage.setFixedSize(100,100)
        elif (dateInput > dateToday):
            errorMessage.critical(self, "error", "invalid date")
            errorMessage.setFixedSize(100,100)
        else:
            self._registerSubmit()
