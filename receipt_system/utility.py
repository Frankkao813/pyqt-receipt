from PyQt6.QtSql import QSqlDatabase, QSqlQuery
import sys
from receipt_system import db1, db2

def connectDb(databaseName, connectionName):
    db = QSqlDatabase.addDatabase("QSQLITE", connectionName)
    db.setDatabaseName(databaseName)
    if not db.open():
        print(f"Database Error {db.lastError().databaseText()}")
        sys.exit(1)
    print(f"The connection for {databaseName} is {db.open()}")
    return db

def returnInfo(realname, username):
    
        # find number of receipt issued
        numReceiptIssuedQuery = QSqlQuery(db2)
        numReceiptIssuedQuery.exec("SELECT userissue FROM log WHERE userissue = :realName ")
        numReceiptIssuedQuery.bindValue(":realName", realname)
        numReceiptIssuedQuery.last()
        count = numReceiptIssuedQuery.at() + 1 # first parameter passed

        # find time account created
        findTimeQuery = QSqlQuery(db1)
        findTimeQuery.prepare("SELECT timestamp FROM users WHERE username = :loginUser")
        findTimeQuery.bindValue(":loginUser", username)
        findTimeQuery.exec()
        findTimeQuery.next()
        time = findTimeQuery.value(0)
        print(type(time))
        return count, time # not completed