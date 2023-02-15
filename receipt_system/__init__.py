from PyQt6 import QtWidgets
from PyQt6.QtSql import QSqlDatabase, QSqlQuery
import sys
from PyQt6.QtWidgets import (
    QApplication
)
import bcrypt
import datetime
from .connectDb import connectDb


#TODO: problems with multiple database connections
db1 = connectDb(r"users.sqlite", "con1")
db2 = connectDb(r"log.sqlite", "con2")
queryDb1 = QSqlQuery(db1)
queryDb2 = QSqlQuery(db2)

if "users" not in db1.tables():
    queryDb1.exec(
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

if "log" not in db2.tables():
    queryDb2.exec(
        '''
        CREATE TABLE log (
            id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
            timestamp INTEGER NOT NULL,
            userissue VARCHAR(40) NOT NULL,
            name VARCHAR(40) NOT NULL,
            item VARCHAR(100) NOT NULL,
            note VARCHAR(100) NOT NULL
        )
        '''
    ) 

print(db1.tables())
print(db2.tables())


# creating dynamic queries

insertUserDataQuery = queryDb1.prepare(
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

