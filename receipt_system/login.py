
from receipt_system import widget
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
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
from . import window
from . import register
#from .window import Window
#from register import Register

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

        if (self.loginName.text() == "testUser" and check_password):
            window_page = window.Window()
            window_page.loginUser = self.loginName.text()
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

