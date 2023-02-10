from PyQt6 import QtWidgets
from PyQt6.QtSql import QSqlDatabase, QSqlQuery
import sys
from PyQt6.QtWidgets import (
    QApplication
)

# about the database
con = QSqlDatabase.addDatabase("QSQLITE")
con.setDatabaseName("../user.sqlite")
if not con.open():
    print(f"Database Error {con.lastError().databaseText()}")
    sys.exit(1)
print(f"The connection is {con.open()}")

createTableQuery = QSqlQuery()
createTableQuery.exec(
    '''
    CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
        name VARCHAR(40) NOT NULL,
        birthday INTEGER NOT NULL,
        password VARCHAR(40) NOT NULL
    )
    
    '''
)
print(con.tables())

# about the app
app = QApplication([])
widget = QtWidgets.QStackedWidget()

