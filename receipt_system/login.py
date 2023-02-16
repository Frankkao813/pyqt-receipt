
from receipt_system import widget, db1
from receipt_system.utility import returnInfo
from PyQt6.QtWidgets import (
    QDialog,
    QLabel,
    QLineEdit,
    QVBoxLayout,
    QFormLayout,
    QPushButton,
    QMessageBox
)
import bcrypt
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtSql import QSqlDatabase, QSqlQuery
from . import window
from . import register


class Login(QDialog):
    # tranfer the text between pages
    def __init__(self):
        super().__init__()
        loginTitle = QLabel("login")
        loginLayout = QVBoxLayout()
        loginLayout.addWidget(loginTitle)
        loginFormLayout = QFormLayout()
        self.loginName = QLineEdit()
        self.loginName.setFixedWidth(150)
        loginFormLayout.addRow("Name: ", self.loginName) 
        self.loginPassword = QLineEdit()
        self.loginPassword.setFixedWidth(150)
        # setEchoMode: prevent from showing the password text
        self.loginPassword.setEchoMode(QLineEdit.EchoMode.Password) 
        loginFormLayout.addRow("Password: ", self.loginPassword) 
        loginLayout.addLayout(loginFormLayout)

        # set the attribute of the widget layout
        loginTitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        loginTitle.setFont(QFont('Arial', 20, 900, True))
        loginFormLayout.setFormAlignment(Qt.AlignmentFlag.AlignHCenter)  # Question: addLayout then setFormAlignment 

        # login button and its related function
        loginButton = QPushButton("login")
        registerButton = QPushButton("register")
        
        loginLayout.addWidget(loginButton)
        loginLayout.addWidget(registerButton)
        loginButton.clicked.connect(self._checkInput)
        registerButton.clicked.connect(self._toRegisterPage)
        self.setLayout(loginLayout)

    def _checkUser(self):
        # basic use of bcrypt
        password = "password"
        bytes = password.encode('utf-8')
        salt = bcrypt.gensalt()
        hash = bcrypt.hashpw(bytes, salt)
        check_password = bcrypt.checkpw(self.loginPassword.text().encode('utf-8'), hash) # userInput, hash
        #TODO: database check
        #TODO: fetch from database
        inputCheck = self._checkUsernameAndPassword(self.loginName.text(), self.loginPassword.text())
        if (inputCheck):
            count, time = returnInfo() # ??
            window_page = window.Window()
            
            widget.addWidget(window_page)
            widget.setCurrentIndex(widget.currentIndex()+1)
        
        
    def _toRegisterPage(self):
        register_page = register.Register()
        widget.addWidget(register_page)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def _checkInput(self):
        if (len(self.loginName.text()) == 0 or len(self.loginPassword.text()) == 0):
            # TODO: show informative text that field should not be blank
            errorMessage  = QMessageBox()
            errorMessage.critical(self, "error", "Please eneter text in each blank");
            errorMessage.setFixedSize(100,100)
        else:
            self._checkUser()

    @staticmethod
    def _checkUsernameAndPassword(user, passwordField) -> bool:
        findPassword = QSqlQuery(db1)
        findPassword.prepare(
            '''
            SELECT password from users WHERE username = :name
            '''
        )
        findPassword.bindValue(":name", user)
        findPassword.exec()
        findPassword.next()
        passwordDb = findPassword.value(0)
        # the user does not exist
        if(len(passwordDb) == 0):
            return False
    
        check_password = bcrypt.checkpw(passwordField.encode('utf-8'), passwordDb.encode('utf-8')) # userInput, hash
        return check_password
