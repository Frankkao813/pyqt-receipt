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
from receipt_system import db1, db2
from PyQt6.QtSql import QSqlDatabase, QSqlQuery



class Window(QDialog):
    loginUser = ""
    timeCreated = ""
    numReceiptIssued = ""
    def __init__(self):
        super().__init__() # parent = None??
        
        tabWidget = QTabWidget()
        self.appLayout = QVBoxLayout() # main layout
        dataFormLayout = QFormLayout()

        # the data input page
        # TODO: change OK and cancel button...
        windowPage = QWidget(self)
        windowPage.setLayout(dataFormLayout)
        self.name = QLineEdit()
        dataFormLayout.addRow("Name: ", self.name)
        self.classPricing = QPlainTextEdit()
        dataFormLayout.addRow("item,pricing: ", self.classPricing)
        self.note = QLineEdit()
        dataFormLayout.addRow("note", self.note)

        # the account info page
        if (self.timeCreated == '' or self.numReceiptIssued == ''):
            count, time = self._returnInfo()
            self.timeCreated = time
            self.numReceiptIssued = count
        accountInfoPage = QWidget(self)
        infoLayout = QFormLayout()
        accountInfoPage.setLayout(infoLayout)
        infoLayout.addRow("username", QLabel(self.loginUser)) # why it doesn't show?
        infoLayout.addRow("created time", QLabel(self.timeCreated))
        infoLayout.addRow("num of receipt issued", QLabel(str(self.numReceiptIssued)))
        
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
        self.buttons.rejected.connect(self._clear)
        self.logoutButton.clicked.connect(self._logout)
        
        self.appLayout.addWidget(self.buttons)
        self.appLayout.addWidget(self.logoutButton)
        
        self.setLayout(self.appLayout)

    def _clear(self):
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
            # clean the cell input
            self._clear()

    @staticmethod
    def _writeToDatabase(time, userIssue, name, classPrice, note):
        insertLogDataQuery = QSqlQuery(db2)
        status = insertLogDataQuery.prepare (
            '''
            INSERT INTO log (
                timestamp,
                userissue,
                name,
                item,
                note
            )
            VALUES (?, ?, ?, ?, ?)
            '''
        )
        if (status):
            insertLogDataQuery.addBindValue(time)
            insertLogDataQuery.addBindValue(userIssue)
            insertLogDataQuery.addBindValue(name)
            insertLogDataQuery.addBindValue(classPrice)
            insertLogDataQuery.addBindValue(note)
            result = insertLogDataQuery.exec()
        return result
    
    def _returnInfo(self):
        # find number of receipt issued
        numReceiptIssuedQuery = QSqlQuery(db2)
        numReceiptIssuedQuery.exec("SELECT userissue FROM log WHERE userissue = '王大明' ")
        numReceiptIssuedQuery.last()
        count = numReceiptIssuedQuery.at() + 1 # first parameter passed

        # find the time the account is created
        findTimeQuery = QSqlQuery(db1)
        findTimeQuery.prepare("SELECT timestamp FROM users WHERE username == :loginUser")
        findTimeQuery.bindValue(":loginUser", self.loginUser)
        findTimeQuery.exec()
        findTimeQuery.next()
        time = findTimeQuery.value(0)

        return count, time # not completed
        

        



