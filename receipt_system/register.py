
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
from datetime import datetime
from PyQt6.QtSql import QSqlDatabase, QSqlQuery
#from login import Login
from . import login
from . import window
from PyQt6.QtCore import QDate, Qt
from PyQt6.QtGui import QFont
from receipt_system import widget, db1, db2
import bcrypt
from receipt_system.utility import returnInfo

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

    def _toWindowPage(self, count, time):
        # show sucessfully entered message
        # pass info from register to window page
        window_Page = window.Window(self.setUsername.text(), count, time)
        widget.addWidget(window_Page)
        widget.setCurrentIndex(widget.currentIndex()+1)


    def _toLoginPage(self):
        login_page = login.Login()
        widget.addWidget(login_page)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def _checkInput(self):
        # TODO: whether any of the input is blank
        bdayInput = self.setBirthday.date()
        bdayInputStr = self.setBirthday.date().toPyDate().strftime("%Y-%m-%d")
        dateToday = QDate.currentDate()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        realnameInput = self.realName.text()
        usernameInput = self.setUsername.text()
        passwordInput = self.setPassword.text()
        
        errorMessage  = QMessageBox()
        if (len(realnameInput) == 0 or len(usernameInput) == 0 or len(passwordInput) == 0):
            errorMessage.critical(self, "error", "Please eneter text in each field.")
            errorMessage.setFixedSize(100,100)
        elif (bdayInput > dateToday):
            errorMessage.critical(self, "error", "invalid date")
            errorMessage.setFixedSize(100,100)
        else: # check repetitive username - more simplistic method?
            hashedPassword = self._hash(passwordInput)
            result = self._writeToDataBase(timestamp, realnameInput, bdayInputStr, usernameInput, hashedPassword)
            if(not result):
                # already set the unique attribute in username field
                errorMessage.critical(self, "error", "repetitve username")
                errorMessage.setFixedSize(100,100)
            else:
                count, time = returnInfo(realnameInput, usernameInput)
                self._toWindowPage(count, time)
    
    @staticmethod
    def _hash(password):
        bytes = password.encode('utf-8')
        salt = bcrypt.gensalt()
        hash = bcrypt.hashpw(bytes, salt)
        return hash.decode('utf-8') # save to database

    @staticmethod
    def _writeToDataBase(timestamp, realname, birthday, username, password):
        insertUserDataQuery = QSqlQuery(db1)
        insertUserDataQuery.prepare(
            '''
            INSERT INTO users (
                timestamp,
                realname,
                birthday,
                username,
                password
            )
            VALUES (?, ?, ?, ?, ?)
            
            '''
        )
        insertUserDataQuery.addBindValue(timestamp)
        insertUserDataQuery.addBindValue(realname)
        insertUserDataQuery.addBindValue(birthday)
        insertUserDataQuery.addBindValue(username)
        insertUserDataQuery.addBindValue(password)
        result = insertUserDataQuery.exec()
        return result

