from PyQt6 import QtWidgets
from PyQt6.QtSql import QSqlDatabase, QSqlQuery
import sys
from PyQt6.QtWidgets import (
    QApplication
)
import bcrypt
import datetime

# about the database
con = QSqlDatabase.addDatabase("QSQLITE")
con.setDatabaseName(r"users.sqlite")
if not con.open():
    print(f"Database Error {con.lastError().databaseText()}")
    sys.exit(1)
print(f"The connection is {con.open()}")


if "users" not in con.tables():
    createTableQuery = QSqlQuery()
    createTableQuery.exec(
        '''
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
            timestamp INTEGER NOT NULL,
            realname VARCHAR(40) NOT NULL,
            birthday INTEGER NOT NULL,
            username VARCHAR(100) UNIQUE NOT NULL,
            password VARCHAR(100) NOT NULL
        )
        
        '''
    )
print(con.tables())

# creating dynamic queries
insertDataQuery = QSqlQuery()
insertDataQuery.prepare(
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


# about the app
app = QApplication([])
widget = QtWidgets.QStackedWidget()

