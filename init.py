import mysql.connector
import sys
from user_interface import MainWindow
from user_manager import get_user_list, try_login
import error_handling
from datetime import datetime
from PySide6.QtCore import (QCoreApplication, QMetaObject, QRect, Qt)
from PySide6.QtWidgets import (QDialogButtonBox, QFormLayout, QLabel, QLineEdit, QWidget, QApplication)

taskmng = mysql.connector.connect(
  host="localhost",
  user="root",
  password="aD0106##",
  database="taskmanager"
)

mycursor = taskmng.cursor()

uList = get_user_list()

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(537, 217)
        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setGeometry(QRect(20, 170, 501, 32))
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.formLayoutWidget = QWidget(self)
        self.formLayoutWidget.setObjectName(u"formLayoutWidget")
        self.formLayoutWidget.setGeometry(QRect(50, 60, 431, 61))
        self.formLayout = QFormLayout(self.formLayoutWidget)
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self.formLayoutWidget)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label)

        self.lineEdit = QLineEdit(self.formLayoutWidget)
        self.lineEdit.setObjectName(u"lineEdit")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.lineEdit)

        self.label_2 = QLabel(self.formLayoutWidget)
        self.label_2.setObjectName(u"label_2")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_2)

        self.lineEdit_2 = QLineEdit(self.formLayoutWidget)
        self.lineEdit_2.setObjectName(u"lineEdit_2")
        self.lineEdit_2.setEchoMode(QLineEdit.Password)

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.lineEdit_2)


        self.retranslateUi(self)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        QMetaObject.connectSlotsByName(self)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Login", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Username:", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"Password:", None))
    # retranslateUi

    def accept(self):
      if self.lineEdit.text() == '' or self.lineEdit_2.text() == '':
        self.er = error_handling.ErrorWindow()
        self.er.setErrorText(13)
        self.er.show()
      else:
        loggedin_user = try_login(self.lineEdit.text(), self.lineEdit_2.text())
        if loggedin_user:
          main_window = MainWindow(uList[0])
          main_window.show()
          print()
          self.close()
        else:
          self.er = error_handling.ErrorWindow()
          self.er.setErrorText(14)
          self.er.show()

    def reject(self):
      self.close()

app = QApplication(sys.argv)
login_window = LoginWindow()
login_window.show()
app.exec()



#mycursor.execute("CREATE TABLE users (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), permission VARCHAR(255), passwd VARCHAR(255))")
#mycursor.execute("CREATE TABLE tasks (id INT AUTO_INCREMENT PRIMARY KEY, created_by INT, assigned_to INT, creation_time TIMESTAMP, descr VARCHAR(255), status VARCHAR(15), priority VARCHAR(15))")

#mycursor.execute("INSERT INTO users VALUES ('1', 'andreea', 'admin', 'pass')")
#taskmng.commit()
#now = str(datetime.now())

#print(now)

#sql = "INSERT INTO tasks (created_by, assigned_to, creation_time, descr, status, priority) VALUES ('1', '2', '" + now + "', 'send email to client', '" + task_manager.status_list[0] + "', '" + task_manager.priority_list[1] + "')"
#sql = "UPDATE tasks SET descr = 'update the timesheet' WHERE id = '2'"
#mycursor.execute(sql)
#taskmng.commit()

'''sql = "UPDATE tasks SET priority = 'Medium' WHERE id = 2"
#sql = "ALTER TABLE tasks ADD due_date DATE"
#sql = "SELECT * FROM tasks"
mycursor.execute(sql)
taskmng.commit()
myresult = mycursor.fetchall()

print(len(myresult))

for x in myresult:
  print(x)
'''
'''
sql = "UPDATE tasks SET created_by = 4 WHERE id = 12"
#sql = "ALTER TABLE tasks ADD due_date DATE"
'''
'''
sql = "SELECT * FROM users"
mycursor.execute(sql)
#taskmng.commit()
myresult = mycursor.fetchall()

print(len(myresult))

for x in myresult:
  print(x)
  '''