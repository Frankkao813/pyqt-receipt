from PyQt6.QtSql import QSqlDatabase, QSqlQuery
import sys

def connectDb(databaseName, connectionName):
    db = QSqlDatabase.addDatabase("QSQLITE", connectionName)
    db.setDatabaseName(databaseName)
    if not db.open():
        print(f"Database Error {db.lastError().databaseText()}")
        sys.exit(1)
    print(f"The connection for {databaseName} is {db.open()}")
    return db