# import pyqt module
import sys
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import(
    QApplication,
    QFormLayout,
    QLineEdit,
    QPlainTextEdit,
    QWidget,
    QDialog,
    QDialogButtonBox,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
)
from PyQt6.QtCore import Qt
from pdfFile import pdfFile
import bcrypt

class Login(QDialog):
    def __init__(self):
        super().__init__()
        loginLayout = QVBoxLayout()
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
        loginFormLayout.setFormAlignment(Qt.AlignmentFlag.AlignCenter)  # Question: addLayout then setFormAlignment 

        # login button and its related function
        loginButton = QPushButton("login")
        registerButton = QPushButton("register")
        loginLayout.addWidget(loginButton)
        loginLayout.addWidget(registerButton)
        loginButton.clicked.connect(self._checkUser)
        registerButton.clicked.connect(self._toRegisterPage)
        self.setLayout(loginLayout)

    def _checkUser(self):
        # basic use of bcrypt
        password = "password"
        bytes = password.encode('utf-8')
        # invalid salt ?
        salt = bcrypt.gensalt()
        hash = bcrypt.hashpw(bytes, salt)
        check_password = bcrypt.checkpw(self.loginPassword.text().encode('utf-8'), hash) # userInput, hash

        if (self.loginName.text() == "testUser" and check_password):
            window = Window()
            widget.addWidget(window)
            widget.setCurrentIndex(widget.currentIndex()+1)
    
    def _toRegisterPage(self):
        register = Register()
        widget.addWidget(register)
        widget.setCurrentIndex(widget.currentIndex()+1)

class Register(QDialog):
    def __init__(self):
        super().__init__()
        RegisterLayout = QVBoxLayout()
        complete = QPushButton("complete")
        RegisterLayout.addWidget(complete)
        self.setLayout(RegisterLayout)


class Window(QDialog):
    def __init__(self):
        super().__init__() # parent = None??
        self.setWindowTitle("receipt system")
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
        login = Login()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex()+1)


        
if __name__ == "__main__":
    app = QApplication([])

    # https://www.youtube.com/watch?v=82v2ZR-g6wY
    widget = QtWidgets.QStackedWidget()
    login = Login()
    window = Window()
    widget.addWidget(login)
    #widget.addWidget(window)

    widget.setFixedHeight(400)
    widget.setFixedWidth(400)
    widget.setWindowTitle("receipt app")
    widget.show()
    sys.exit(app.exec())
