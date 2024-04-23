import mysql.connector
from PySide6.QtWidgets import (QSizePolicy, QVBoxLayout, QLabel, QWidget)
from PySide6.QtCore import (QCoreApplication, QMetaObject, QRect, QSize, Qt)
from PySide6.QtWidgets import (QComboBox, QDialogButtonBox, QHBoxLayout, QLineEdit)

import error_handling

taskmng = mysql.connector.connect(
  host="localhost",
  user="root",
  password="aD0106##",
  database="taskmanager"
)

user_cursor = taskmng.cursor()
user_cursor.execute("SELECT * FROM users")
users = user_cursor.fetchall()

######################## list of possible roles ###########################
role_list = ("Viewer", "Editor", "Admin")

###########################################################################
### define User class
### a user will have an id, a username and role
###########################################################################
class User:
    def __init__(self, id, username, role):
        self.id = id
        self.username = username
        self.role = role

############# the function will insert in users db a new user #############
def add_user(username, role, password):
    sql = "INSERT INTO users (name, permission, passwd) VALUES (%s, %s, %s)"
    val = (username, role, password)
    user_cursor.execute(sql, val)
    taskmng.commit()  

###########################################################################
### the function will process the result of select * from users 
### and return a list of objects of type User
########################################################################### 
def get_user_list():
    user_cursor.execute("SELECT * FROM users")
    users = user_cursor.fetchall()
    userList = []
    for x in users:
        userList.append(User(x[0], x[1], x[2]))
        print(str(x[0]) + " " + x[1] + " " + x[2])
    return userList

def try_login(username, password):
    user_cursor.execute("SELECT * FROM users WHERE name = '" + username + "' AND passwd = '" + password + "'")
    returned_user = user_cursor.fetchall()
    for x in returned_user:
        return User(x[0], x[1], x[2])
    return 0


def get_username_from_id(user_id):
    tasks_cursor = taskmng.cursor()
    tasks_cursor.execute("SELECT name FROM users WHERE id = '" + str(user_id) +"'")
    username = tasks_cursor.fetchall()
    username = str(username[0]).split("'")
    return str(username[1])

def change_user_password(user_id, old_password, new_password):
    cursor = taskmng.cursor()
    cursor.execute("SELECT passwd FROM users WHERE id = '" + str(user_id) +"'")
    passwd = cursor.fetchone()[0]
    if old_password == passwd:
        print("ok")
    else:
        #error_window = error_handling.ErrorWindow()
        #error_window.setErrorText(12)
        #error_window.show()
        print()

def ch_perm(user_id, role):
        user_cursor.execute("UPDATE users SET permission = '" + role + "' WHERE id = " + str(user_id))
        taskmng.commit()  
        
def delete_user(user_id):
    sql = "DELETE FROM users WHERE id = %s"
    val = (user_id, )
    user_cursor.execute(sql, val)
    taskmng.commit()  


###########################################################################
### implement the user window for adding a new user
### this will have user, password and role fields
###########################################################################
class UserWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(383, 282)
        sizePolicyy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicyy.setHorizontalStretch(0)
        sizePolicyy.setVerticalStretch(0)
        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setGeometry(QRect(30, 240, 341, 32))
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.verticalLayoutWidget = QWidget(self)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(10, 10, 363, 211))
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(self.verticalLayoutWidget)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)

        self.lineUsername = QLineEdit(self.verticalLayoutWidget)
        self.lineUsername.setObjectName(u"lineUsername")
        sizePolicyy.setHeightForWidth(self.lineUsername.sizePolicy().hasHeightForWidth())
        self.lineUsername.setSizePolicy(sizePolicyy)
        self.lineUsername.setMinimumSize(QSize(237, 0))

        self.horizontalLayout.addWidget(self.lineUsername)

        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_2 = QLabel(self.verticalLayoutWidget)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_2.addWidget(self.label_2)

        self.linePass1 = QLineEdit(self.verticalLayoutWidget)
        self.linePass1.setObjectName(u"linePass1")
        sizePolicyy.setHeightForWidth(self.linePass1.sizePolicy().hasHeightForWidth())
        self.linePass1.setSizePolicy(sizePolicyy)
        self.linePass1.setEchoMode(QLineEdit.Password)
        self.linePass1.setMinimumSize(QSize(237, 0))

        self.horizontalLayout_2.addWidget(self.linePass1)

        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.label_6 = QLabel(self.verticalLayoutWidget)
        self.label_6.setObjectName(u"label_6")

        self.horizontalLayout_6.addWidget(self.label_6)

        self.linePass2 = QLineEdit(self.verticalLayoutWidget)
        self.linePass2.setObjectName(u"linePass2")
        sizePolicyy.setHeightForWidth(self.linePass2.sizePolicy().hasHeightForWidth())
        self.linePass2.setSizePolicy(sizePolicyy)
        self.linePass2.setMinimumSize(QSize(237, 0))
        self.linePass2.setEchoMode(QLineEdit.Password)

        self.horizontalLayout_6.addWidget(self.linePass2)

        self.verticalLayout.addLayout(self.horizontalLayout_6)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.label_7 = QLabel(self.verticalLayoutWidget)
        self.label_7.setObjectName(u"label_7")

        self.horizontalLayout_7.addWidget(self.label_7)

        self.comboRoles = QComboBox(self.verticalLayoutWidget)
        self.comboRoles.setObjectName(u"comboRoles")
        self.comboRoles.addItems(role_list)

        self.horizontalLayout_7.addWidget(self.comboRoles)

        self.verticalLayout.addLayout(self.horizontalLayout_7)

        self.retranslateUi(self)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        QMetaObject.connectSlotsByName(self)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Add new user", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Username", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"Password", None))
        self.label_6.setText(QCoreApplication.translate("Dialog", u"Re-enter password", None))
        self.label_7.setText(QCoreApplication.translate("Dialog", u"Role", None))

###########################################################################
### after accepting the add user dialog we check if the following 
### requirements are met: 
### - matching passwords 
### - username at least 7 characters long
### if yes then the user is created
### if no then an error is raised using error_handling module
########################################################################### 
    def accept(self):
        username = self.lineUsername.text()
        password = self.linePass1.text()
        password2 = self.linePass2.text()
        role = self.comboRoles.currentText().lower()

        if password != password2:
            self.error_window = error_handling.ErrorWindow()
            self.error_window.setErrorText(10)
            self.error_window.show()

        elif len(username) < 7:
            self.error_window = error_handling.ErrorWindow()
            self.error_window.setErrorText(11)
            self.error_window.show()
        
        else:
            add_user(username, role, password)
            self.close()

############ when rejecting the dialog the window will be closed ###########
    def reject(self):
        self.close()




