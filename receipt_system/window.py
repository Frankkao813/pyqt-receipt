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

    def __init__(self, username = "", count = "", time = ""):
        super().__init__() # parent = None??
        self.loginUser = username
        self.timeCreated = time
        self.numReceiptIssued = count
        
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

        # # the account info page
        # if len(self.loginUser) != 0:
        #     try:
        #         count, time = self._returnInfo()
        #     except TypeError:
        #         print("not executed.")

        #print("The info at this position", count, time)

        accountInfoPage = QWidget(self)
        infoLayout = QFormLayout()
        accountInfoPage.setLayout(infoLayout)

        # issue: the following three lines doesn;t show properly, why?
        infoLayout.addRow("username", QLabel(self.loginUser)) 
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
        
        dataFormLayout.addWidget(self.buttons)
        self.appLayout.addWidget(self.logoutButton)
        
        self.setLayout(self.appLayout)

    def _clear(self):
        # TODO: clear the dialog box
        self.name.setText("")
        self.classPricing.clear()
        self.note.setText("")
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
        classPricingFormat = self._checkclassPricingFormat(classPricingInput)
        # TODO: some check conditions
        if (len(nameInput) == 0 or len(classPricingInput) == 0 or len(noteInput) == 0):
            completeStatus.critical(self, "error", "repetitve username")
            completeStatus.setFixedSize(100,100)
        elif not classPricingFormat:
            completeStatus.critical(self, "error", "wrong format")
            completeStatus.setFixedSize(100,100)
        else:
            result = self._writeToDatabase(timestamp, userIssue, nameInput, classPricingInput, noteInput)
            if result:
                completeStatus.information(self, "info", "sucessfully write to database, generating pdf file...")
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
    
    @staticmethod
    def _checkclassPricingFormat(formatting):
        # strip all the '\n' elements, then the comma
        newlineStrip = formatting.split('\n')
        temp = ""
        commaStrip = []
        # strip the comma
        for idx, element in enumerate(newlineStrip):
            temp = element.split(",")
            commaStrip.append(temp)

        # check whether the element in the array can be converted
        for idx, element in enumerate(commaStrip):
            try:
                element[0] = str(element[0])
                element[1] = int(element[1])
            except TypeError:
                return False
        
        return True





    

        



