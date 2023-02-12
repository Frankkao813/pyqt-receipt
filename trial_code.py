from PyQt6.QtSql import QSqlDatabase, QSqlQuery
from PyQt6.QtCore import QDate
import sys
from os import path
import bcrypt
import datetime




# tday = datetime.date.today()
# print(tday)

# tdayTime = datetime.datetime.now()
# currTime = tdayTime.strftime("%Y-%m-%d %H:%M:%S")
# print(tdayTime)
# print(type(tdayTime))

# print(currTime)
# print(type(currTime))


# # about the sqlite database
# # about the database
# con = QSqlDatabase.addDatabase("QSQLITE")
# con.setDatabaseName(r"trial_users.sqlite")
# if not con.open():
#     print(f"Database Error {con.lastError().databaseText()}")
#     sys.exit(1)
# print(f"The connection is {con.open()}")

# if "users" not in con.tables():
#     createTableQuery = QSqlQuery()
#     createTableQuery.exec(
#         '''
#         CREATE TABLE users (
#             id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
#             timestamp INTEGER NOT NULL,
#             realname VARCHAR(40) NOT NULL,
#             birthday INTEGER NOT NULL,
#             username VARCHAR(100) UNIQUE NOT NULL,
#             password VARCHAR(100) NOT NULL
#         )
        
#         '''
#     )
# print(con.tables())

# # creating dynamic queries
# insertDataQuery = QSqlQuery()
# insertDataQuery.prepare(
#     '''
#     INSERT INTO users (
#         timestamp,
#         realname,
#         birthday,
#         username,
#         password
#     )
#     VALUES (?, ?, ?, ?, ?)
    
#     '''
# )

# password_ = "password"
# bytes = password_.encode('utf-8')
# salt = bcrypt.gensalt()
# hash = bcrypt.hashpw(bytes, salt)
# print(type(hash))
# currTime = datetime.datetime.now()
# currTimeStr = currTime.strftime("%Y-%m-%d %H:%M:%S")

# birthday - tranform QTime to python format
bday = QDate(2000, 7, 7)
bdayStr = bday.toPyDate().strftime("%Y-%m-%d")
print(bday.toPyDate())
print(type(bday.toPyDate()))
print(type(bdayStr))



# insertDataQuery.addBindValue(currTimeStr)
# insertDataQuery.addBindValue("王大明")
# insertDataQuery.addBindValue("2000-07-07")
# insertDataQuery.addBindValue("testUser")
# insertDataQuery.addBindValue(hash.decode("utf-8"))
# result = insertDataQuery.exec()

# print("this line successful?", result)

# newQuery = QSqlQuery()
# newQuery.exec("SELECT timestamp, realname, birthday, username, password FROM users")
# newQuery.first()
# timestamp, realname, birthday, username, password = range(5)
# print(newQuery.value(timestamp))
# print(newQuery.value(realname))
# print(newQuery.value(birthday))
# print(newQuery.value(username))
# print(newQuery.value(password))

#print("the result is ...", result)
