from datetime import datetime


from PySide6.QtCore import (QCoreApplication, QDate, QMetaObject, QRect, QSize, Qt)
from PySide6.QtGui import (QCursor, QFont)
from PySide6.QtWidgets import (QComboBox,
    QDateEdit, QDialogButtonBox, QHBoxLayout, QTextEdit, QVBoxLayout, QWidget, QFrame, QLabel)

import mysql.connector
from user_manager import User, get_user_list, get_username_from_id, change_user_password
from functools import partial

import log


#connect to db
taskmng = mysql.connector.connect(
  host="localhost",
  user="root",
  password="aD0106##",
  database="taskmanager"
)
taskmng_cursor = taskmng.cursor()

######################## list of possible statuses ###########################
status_list = ("New", "In Progress", "Complete")

####################### list of possible priorities ##########################
priority_list = ("Low", "Medium", "High", "Urgent")

taskList = []
userList = get_user_list()

currentUser = User(0, '', '')
       
class Task:
    def __init__(self, title, desc, assigned_to, status, priority, created_by, due_date, id = -1):
        self.title = title
        self.desc = desc
        self.assigned_to = assigned_to
        self.status = status
        self.creation_time = datetime.now()
        self.priority = priority
        self.created_by = created_by
        self.due_date = due_date
        self.id = id

    def __getDesc__(self):
        return self.desc


def print_task_list(user_id, sort_type):
    tasks_cursor = taskmng.cursor()
    if sort_type == 0:
        tasks_cursor.execute("SELECT * FROM tasks WHERE tasks.assigned_to = '" + str(user_id) + 
                             "' OR tasks.created_by = '" + str(user_id) + "' ORDER BY tasks.priority")
    else:
        tasks_cursor.execute("SELECT * FROM tasks WHERE tasks.assigned_to = '" + str(user_id) + 
                             "' OR tasks.created_by = '" + str(user_id) + "' ORDER BY tasks.due_date")
    
    tasks = tasks_cursor.fetchall()
    taskList = []

    for x in tasks:
        y = str(x)
        y = y[1:len(y)-1]
        y = y.split(', ')

        id = y[0]
        created_by = y[1]
        y[3] += '-' + y[4]
        y[3] += '-' + y[5] 
        y[3] += ';' + y[6]  
        y[3] += ':' + y[7]  
        y[3] += ':' + y[8] 
      
        assigned_to = y[2]
        creation_time = y[3]
        description = y[9]
        status = y[10]
        priority = y[11]
        title = y[12]
        due_date = y[13] + '-' + y[len(y)-2] + '-' + y[len(y)-1]
        due_date = due_date[14:-1]
    
        newTask = Task(title, description, assigned_to, status, priority, created_by, due_date, id)
        taskList.append(newTask)

    return taskList


# this function will save the task in the database
def add_task(new_task):
    sql = "INSERT INTO tasks (created_by, assigned_to, creation_time, descr, status, priority, title, due_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    val = (new_task.created_by, new_task.assigned_to, new_task.creation_time, new_task.desc, new_task.status, new_task.priority, new_task.title, new_task.due_date)
    taskmng_cursor.execute(sql, val)
    taskmng.commit()

    log_text = "added the task " + new_task.title + ", which is due on " + str(new_task.due_date.strftime("%Y-%m-%d")) + "\n"
    log.log(userList[int(new_task.created_by)].username, log_text)
    #refresh_tasks()

def update_task(task):
    sql = "UPDATE tasks set assigned_to = %s, descr = %s, status = %s, priority = %s, title = %s, due_date = %s WHERE tasks.id = %s"
    val = (task.assigned_to, task.desc, task.status, task.priority, task.title, task.due_date, task.id)
    taskmng_cursor.execute(sql, val)
    taskmng.commit()

    log_text = "changed task " + task.title + ", which is due on " + str(task.due_date) + "\n"
    log.log(userList[int(task.created_by)].username, log_text)


def del_task(task):
    print("deleting task with id: " + task.id)
    sql = "DELETE FROM tasks WHERE id = %s"
    val = (str(task.id), )
    taskmng_cursor.execute(sql, val)
    taskmng.commit()
    #refresh_tasks()
    log_text = "deleted task " + task.title + "\n"
    log.log(userList[int(task.created_by)].username, log_text)


class TaskWindow(QWidget):
     def __init__(self, currentUser, task = 0):
        super().__init__()
        self.resize(570, 287)
        self.verticalLayoutWidget = QWidget(self)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(0, 0, 561, 271))
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.item_title = QTextEdit(self.verticalLayoutWidget)
        self.item_title.setObjectName(u"textEdit")
        self.item_title.setMaximumSize(QSize(16777215, 75))
        font = QFont()
        font.setPointSize(25)
        font.setBold(True)
        font.setItalic(True)
        self.item_title.setFont(font)
        self.item_title.viewport().setProperty("cursor", QCursor(Qt.IBeamCursor))
        self.item_title.setFrameShape(QFrame.NoFrame)

        if task:
            self.item_title.setText(QCoreApplication.translate("Dialog", task.title[1:-1], None))
        else:
            self.item_title.setPlaceholderText(QCoreApplication.translate("Dialog", u"Enter title", None))
            
        self.verticalLayout.addWidget(self.item_title)
        self.item_desc = QTextEdit(self.verticalLayoutWidget)
        self.item_desc.setObjectName(u"textEdit_2")
        self.item_desc.setFrameShape(QFrame.NoFrame)

        if task:
            self.item_desc.setText(QCoreApplication.translate("Dialog", task.desc[1:-1], None))
        else:
            self.item_desc.setPlaceholderText(QCoreApplication.translate("Dialog", u"Enter task description", None))

        self.verticalLayout.addWidget(self.item_desc)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.created_by_h_layout = QHBoxLayout()
        if task:
            created_by_label = QLabel("Created by: " + get_username_from_id(task.created_by))
            self.created_by_h_layout.addWidget(created_by_label)
        self.assign_to = QComboBox(self.verticalLayoutWidget)
        self.assign_to.setObjectName(u"comboBox")
        nrOfItems = self.assign_to.count()
        if  nrOfItems < 1:
            for x in userList:
                self.assign_to.addItem(x.username, x.id)
        if task:           
            self.assign_to.setCurrentText(task.assigned_to)

        self.horizontalLayout.addWidget(self.assign_to)

        self.item_priority = QComboBox(self.verticalLayoutWidget)
        self.item_priority.setObjectName(u"comboBox_2")
        self.item_priority.addItems(priority_list)

        if task:
            self.item_priority.setCurrentIndex(priority_list.index(task.priority[1:-1]))

        self.horizontalLayout.addWidget(self.item_priority)

        self.item_status = QComboBox(self.verticalLayoutWidget)
        self.item_status.setObjectName(u"comboBox_2")
        self.item_status.addItems(status_list)

        if task:
            self.item_status.setCurrentIndex(status_list.index(task.status[1:-1]))

        self.horizontalLayout.addWidget(self.item_status)
        self.item_due_date = QDateEdit(self.verticalLayoutWidget)
        self.item_due_date.setObjectName(u"dateEdit")
        font1 = QFont()
        font1.setKerning(True)
        self.item_due_date.setFont(font1)
        self.item_due_date.setCursor(QCursor(Qt.PointingHandCursor))
        self.item_due_date.setFocusPolicy(Qt.NoFocus)
        self.item_due_date.setFrame(True)
        self.item_due_date.setKeyboardTracking(True)
        self.item_due_date.setProperty("showGroupSeparator", False)
        self.item_due_date.setCalendarPopup(True)
        self.item_due_date.setTimeSpec(Qt.UTC)

        if task:
            date = task.due_date
            self.item_due_date.setDate(QDate(datetime.strptime(task.due_date, '%Y-%m-%d')))
        else:
            self.item_due_date.setDate(datetime.now())

        self.lables_h_layout = QHBoxLayout()
        self.lables_h_layout.addWidget(QLabel("Assigned to:"))
        self.lables_h_layout.addWidget(QLabel("Priority:"))
        self.lables_h_layout.addWidget(QLabel("Status:"))
        self.lables_h_layout.addWidget(QLabel("Due date:"))
        self.lables_h_layout.setContentsMargins(25, 20, 10, 0)

        self.horizontalLayout.addWidget(self.item_due_date)
        self.verticalLayout.addLayout(self.created_by_h_layout)
        self.verticalLayout.addLayout(self.lables_h_layout)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.buttonBox = QDialogButtonBox(self.verticalLayoutWidget)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(self)
        self.buttonBox.accepted.connect(partial(self.accept, task))
        self.buttonBox.rejected.connect(self.reject)

        if task:
            self.setWindowTitle(u"Edit Task")
        else:
            self.setWindowTitle(u"Add New Task")

        QMetaObject.connectSlotsByName(self)


     def retranslateUi(self, Dialog):
        self.assign_to.setPlaceholderText(QCoreApplication.translate("Dialog", u"Assigned to", None))
        self.item_priority.setPlaceholderText(QCoreApplication.translate("Dialog", u"Priority", None))
        self.item_due_date.setSpecialValueText("")

     def accept(self, task):
        #from user_interface import refresh_tasks
        self.close()
        
        print("task created. assigned to: " + str(self.assign_to.currentData()) + " " + str(self.assign_to.currentText()))
        new_item_due_date = datetime.date(self.item_due_date.dateTime().toPython())

        new = Task(self.item_title.toPlainText(), self.item_desc.toPlainText(),self.assign_to.currentData(), 
                   status_list[0], self.item_priority.currentText(), currentUser.id, new_item_due_date)
        if task:
            new.id = task.id
            update_task(new)
        else:
            add_task(new)

        #refresh_tasks(currentUser)

     def reject(self):
        self.close()