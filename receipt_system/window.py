from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QFormLayout,
    QLineEdit,
    QPlainTextEdit,
    QPushButton,
    QDialogButtonBox,
    QMessageBox,
    QTabWidget,
    QLabel,
    QWidget

)

#from .login import Login
from . import login
from .pdfFile import pdfFile
from receipt_system import widget
from datetime import datetime
from receipt_system import queryDb2


class Window(QDialog):
    loginUser = ""
    def __init__(self):
        super().__init__() # parent = None??
        
        tabWidget = QTabWidget()
        self.appLayout = QVBoxLayout() # main layout
        dataFormLayout = QFormLayout()

        # the data input page
        windowPage = QWidget(self)
        windowPage.setLayout(dataFormLayout)
        self.name = QLineEdit()
        dataFormLayout.addRow("Name: ", self.name)
        self.classPricing = QPlainTextEdit()
        dataFormLayout.addRow("item,pricing: ", self.classPricing)
        self.note = QLineEdit()
        dataFormLayout.addRow("note", self.note)

        # the account info page
        accountInfoPage = QWidget(self)
        infoLayout = QFormLayout()
        accountInfoPage.setLayout(infoLayout)
        infoLayout.addRow("First row", QLabel("Widget in Tab2."))
        
        tabWidget.addTab(windowPage, "data input")
        tabWidget.addTab(accountInfoPage, "account info")
        self.appLayout.addWidget(tabWidget)
        #self.appLayout.addLayout(formLayout)
        #self.appLayout.addWidget(tabWidget)
        
        self.buttons = QDialogButtonBox()
        self.buttons.setStandardButtons(
            QDialogButtonBox.StandardButton.Cancel|
            QDialogButtonBox.StandardButton.Ok
        )
        self.logoutButton = QPushButton("Logout")
        # https://stackoverflow.com/questions/33547821/execute-function-after-click-ok-qdialogbuttonbox
        # try-except case
        self.buttons.accepted.connect(self._checkInput)
        self.buttons.rejected.connect(self._reject)
        self.logoutButton.clicked.connect(self._logout)
        
        self.appLayout.addWidget(self.buttons)
        self.appLayout.addWidget(self.logoutButton)
        
        self.setLayout(self.appLayout)

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
    
    def _checkInput(self):
        completeStatus =  QMessageBox()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        userIssue = self.loginUser # the person who issues the receipt, pass value between pages
        nameInput = self.name.text()
        classPricingInput = self.classPricing.toPlainText()
        noteInput = self.note.text()
        # TODO: some check conditions

        result = self._writeToDatabase(timestamp, userIssue, nameInput, classPricingInput, noteInput)
        if result:
            completeStatus.information(self, "info", "sucessfully write to database")
            completeStatus.setFixedSize(100,100)
            pdfFile(nameInput, classPricingInput, noteInput)

    @staticmethod
    def _writeToDatabase(time, userIssue, name, classPrice, note):
        queryDb2.addBindValue(time)
        queryDb2.addBindValue(userIssue)
        queryDb2.addBindValue(name)
        queryDb2.addBindValue(classPrice)
        queryDb2.addBindValue(note)
        result = queryDb2.exec()
        return result


