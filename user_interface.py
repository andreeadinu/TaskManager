from PySide6.QtCore import (QCoreApplication, QMetaObject, QRect, QSize, Qt)
from PySide6.QtGui import (QAction, QColor)
from PySide6.QtWidgets import (QApplication, QFormLayout, QGridLayout,
    QLabel, QLineEdit, QMainWindow, QMenu,
    QMenuBar, QPushButton, QSizePolicy, QStatusBar,
    QTabWidget, QTableWidget, QTableWidgetItem, QVBoxLayout,
    QWidget, QComboBox)
import PySide6.QtCore

from functools import partial
import user_manager
import task_manager
import error_handling
import sys
from task_manager import print_task_list
from user_manager import get_user_list, role_list, change_user_password
import datetime

colors = {
        "Urgent": "#FF0000",
        "Low": "#00FF00",
        "Medium": "#F6FF00",
        "High": "#FF8400"
}

def get_rgb_from_hex(code):
    code_hex = code.replace("#", "")
    rgb = tuple(int(code_hex[i:i+2], 16) for i in (0, 2, 4))
    return QColor.fromRgb(rgb[0], rgb[1], rgb[2])

order_by = ("Priority", "Due date")

uList = get_user_list()



class MainWindow(QMainWindow): #was QMainWindow

    def __init__(self, currentUser):
        super().__init__()

        userList = get_user_list()
        self.changed_users = dict()
        self.current_user = currentUser

        tasklist = task_manager.print_task_list(self.current_user.id, 0)
        userList = task_manager.get_user_list()
        tasklist = task_manager.print_task_list(self.current_user.id, 0)

        self.button = QPushButton("Add new user")
        #self.button.clicked.connect(self.show_user_manager)
        self.setCentralWidget(self.button)
        self.setWindowFlag(PySide6.QtCore.Qt.WindowStaysOnTopHint, False)

        self.resize(753, 425)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.actionLog_out = QAction(self)
        self.actionLog_out.setObjectName(u"actionLog_out")
        self.actionDELETE_USER = QAction(self)
        self.actionDELETE_USER.setObjectName(u"actionDELETE_USER")
        
        self.centralwidget = QWidget(self)
        self.centralwidget.setObjectName(u"centralwidget")
        
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setGeometry(QRect(0, 0, 751, 501))
        self.tabWidget.setLayoutDirection(Qt.LeftToRight)
        self.tabWidget.setElideMode(Qt.ElideMiddle)
        
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        
        self.gridLayoutWidget = QWidget(self.tab)
        self.gridLayoutWidget.setObjectName(u"gridLayoutWidget")
        self.gridLayoutWidget.setGeometry(QRect(-3, 3, 751, 371))
        
        self.gridLayout = QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        
        self.tasksTable = QTableWidget(self.gridLayoutWidget)
        self.tasksTable.setObjectName(u"tasksTable")
        self.tasksTable.setFixedWidth(753)
        self.tasksTable.setColumnCount(6)
        self.tasksTable.setColumnWidth(0,250)
        self.tasksTable.setColumnWidth(2,125)
        self.tasksTable.setColumnWidth(5,55)
        self.tasksTable.setHorizontalHeaderLabels(["Title", "Status", "Priority", "Due date", "", ""])
        
        self.populateTaskTable(0)

        self.newTask_Button = QPushButton(self.gridLayoutWidget)
        self.newTask_Button.setObjectName(u"newTask_Button")
        self.newTask_Button.clicked.connect(self.cr_task)

        self.refreshTasks_Button = QPushButton(self.gridLayoutWidget)
        self.refreshTasks_Button.setObjectName(u"refreshTasks_Button")
        self.order_list = QComboBox()
        self.order_list.addItems(order_by)
        self.order_list.setFixedWidth(100)
        self.order_label = QLabel("Order by:")
        
        self.order_list.currentIndexChanged.connect(partial(self.populateTaskTable, ))
        self.refreshTasks_Button.clicked.connect(partial(self.refresh_tasks, self.current_user))
        
        self.gridLayout.addWidget(self.order_label, 0, 0, Qt.AlignRight)
        self.gridLayout.addWidget(self.order_list, 0, 1, Qt.AlignRight)
        self.gridLayout.addWidget(self.refreshTasks_Button, 0, 2, Qt.AlignLeft)

        self.gridLayout.addWidget(self.tasksTable, 2, 0, 1, 1)
        
        self.gridLayout.addWidget(self.newTask_Button, 3, 2, Qt.AlignLeft)
        

        ###########################
        ## USERS TAB
        ###########################

        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.verticalLayoutWidget_2 = QWidget(self.tab_2)
        self.verticalLayoutWidget_2.setObjectName(u"verticalLayoutWidget_2")
        self.verticalLayoutWidget_2.setGeometry(QRect(-1, 10, 751, 364))
        self.verticalLayout_2 = QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self.verticalLayoutWidget_2)
        self.label.setObjectName(u"label")
        self.label.setText("Logged in as: " + self.current_user.username + "; Role: " + self.current_user.role)

        self.verticalLayout_2.addWidget(self.label)

        self.usersTable = QTableWidget(self.verticalLayoutWidget_2)
        self.usersTable.setObjectName(u"tableWidget")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.usersTable.sizePolicy().hasHeightForWidth())
        self.usersTable.setSizePolicy(sizePolicy1)
        self.usersTable.setMinimumSize(QSize(0, 150))

        ###########################
        # populate user tablewidget
        ###########################

        
        self.usersTable.setColumnCount(4)
        self.usersTable.setColumnWidth(0,360)
        self.usersTable.setColumnWidth(1,165)
        self.usersTable.setHorizontalHeaderLabels(["Username", "Role", "Change", ""])
        '''i = 0
        flg = PySide6.QtCore.Qt.ItemIsEditable  
        for u in userList:
            username = QTableWidgetItem(u.username)
            username.setFlags(~flg)

            role = QTableWidgetItem(u.role)
            role.setFlags(~flg)

            b_change_role = QPushButton("Change")
            b_change_role.clicked.connect(partial(user_manager.ch_perm, u.id))

            #item_status.setCurrentIndex(status_list.index(task.status[1:-1]))
            combo_role = QComboBox()
            combo_role.addItems(user_manager.role_list)
            combo_role.setCurrentIndex(user_manager.role_list.index(str(u.role).capitalize()))
            combo_role.currentTextChanged.connect(partial(self.edt_roles, u.id))

            if str(self.current_user.role).capitalize() != role_list[2]:
                combo_role.setDisabled(1)

            self.usersTable.setItem(i, 0, username)
            self.usersTable.setItem(i, 1, role)
            self.usersTable.setCellWidget(i, 2, combo_role)

            i += 1'''
        self.populateUsersTable()
        self.gridLayout.addWidget(self.usersTable, 0, 0, 1, 1)

        self.verticalLayout_2.addWidget(self.usersTable)

        self.label_4 = QLabel(self.verticalLayoutWidget_2)
        self.label_4.setObjectName(u"label_4")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy2)
        self.label_4.setMaximumSize(QSize(16777215, 25))

        #self.verticalLayout_2.addWidget(self.label_4)

        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.label_2 = QLabel(self.verticalLayoutWidget_2)
        self.label_2.setObjectName(u"label_2")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label_4)

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_2)

        self.lineEdit = QLineEdit(self.verticalLayoutWidget_2)
        self.lineEdit.setObjectName(u"lineEdit")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.lineEdit)

        self.label_3 = QLabel(self.verticalLayoutWidget_2)
        self.label_3.setObjectName(u"label_3")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.label_3)

        self.lineEdit_2 = QLineEdit(self.verticalLayoutWidget_2)
        self.lineEdit_2.setObjectName(u"lineEdit_2")

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.lineEdit_2)

        self.label_5 = QLabel(self.verticalLayoutWidget_2)
        self.label_5.setObjectName(u"label_5")

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.label_5)

        self.lineEdit_3 = QLineEdit(self.verticalLayoutWidget_2)
        self.lineEdit_3.setObjectName(u"lineEdit_3")

        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.lineEdit_3)

        #self.saveUserP_Button = QPushButton(self.verticalLayoutWidget_2)
        #self.saveUserP_Button.setObjectName(u"saveUserP_Button")

        #self.formLayout.setWidget(4, QFormLayout.FieldRole, self.saveUserP_Button)


        self.verticalLayout_2.addLayout(self.formLayout)

        self.newUser_Button = QPushButton(self.verticalLayoutWidget_2)
        self.newUser_Button.setObjectName(u"newUser_Button")
        self.newUser_Button.clicked.connect(self.cr_user)

        if str(self.current_user.role).capitalize() != role_list[2]:
                self.newUser_Button.setDisabled(1)

        self.applyChanges_Button = QPushButton()
        self.applyChanges_Button.setText("Apply changes")
        self.applyChanges_Button.clicked.connect(self.apply_changes)

        self.verticalLayout_2.addWidget(self.newUser_Button)
        self.verticalLayout_2.addWidget(self.applyChanges_Button)

        self.tabWidget.addTab(self.tab_2, "")
        self.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(self)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 753, 24))
        self.menuUsername = QMenu(self.menubar)
        self.menuUsername.setObjectName(u"menuUsername")
        self.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(self)
        self.statusbar.setObjectName(u"statusbar")
        self.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuUsername.menuAction())
        self.menuUsername.addAction(self.actionLog_out)
        self.menuUsername.addAction(self.actionDELETE_USER)

        self.retranslateUi(self)

        self.tabWidget.setCurrentIndex(0)

        QMetaObject.connectSlotsByName(self)

    def get_order_index(self):
        return self.order_list.currentIndex()

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionLog_out.setText(QCoreApplication.translate("MainWindow", u"Log out", None))
        self.actionDELETE_USER.setText(QCoreApplication.translate("MainWindow", u"DELETE USER", None))
        self.newTask_Button.setText(QCoreApplication.translate("MainWindow", u"Add New task", None))
        self.refreshTasks_Button.setText(QCoreApplication.translate("MainWindow", u"Refresh tasks", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("MainWindow", u"Tasks", None))
        #self.label.setText(QCoreApplication.translate("MainWindow", u"User list:", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Change your password:", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Old Password:", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"New Password:", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Re-enter New Password:", None))
        #self.saveUserP_Button.setText(QCoreApplication.translate("MainWindow", u"Save changes", None))
        self.newUser_Button.setText(QCoreApplication.translate("MainWindow", u"Add new user", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("MainWindow", u"User management", None))
        self.menuUsername.setTitle(QCoreApplication.translate("MainWindow", u"Username", None))

    def populateUsersTable(self):
        userList = user_manager.get_user_list()
        self.usersTable.setRowCount(len(userList)-1)
        i = 0
        flg = PySide6.QtCore.Qt.ItemIsEditable  
        for u in userList:
            if u.id != self.current_user.id:
                username = QTableWidgetItem(u.username)
                username.setFlags(~flg)

                role = QTableWidgetItem(str(u.role).capitalize())
                role.setFlags(~flg)

                b_change_role = QPushButton("Change")
                b_change_role.clicked.connect(partial(user_manager.ch_perm, u.id))

                #item_status.setCurrentIndex(status_list.index(task.status[1:-1]))
                combo_role = QComboBox()
                combo_role.addItems(user_manager.role_list)
                combo_role.setCurrentIndex(user_manager.role_list.index(str(u.role).capitalize()))
                combo_role.currentTextChanged.connect(partial(self.edt_roles, u.id))

                if str(self.current_user.role).capitalize() != role_list[2]:
                    combo_role.setDisabled(1)

                user_delete = QPushButton("x")
                user_delete.clicked.connect(partial(user_manager.delete_user, u.id))

                if str(self.current_user.role).capitalize() != role_list[2]:
                    user_delete.setDisabled(1)

                self.usersTable.setItem(i, 0, username)
                self.usersTable.setItem(i, 1, role)
                self.usersTable.setCellWidget(i, 2, combo_role)

                self.usersTable.setCellWidget(i, 3, user_delete)

                i += 1
        


    def populateTaskTable(self, order):
        i = 0
        self.tasklist = task_manager.print_task_list(self.current_user.id, order)
        print("total tasks: " + str(len(self.tasklist) ))
        flg = PySide6.QtCore.Qt.ItemIsEditable  
        self.tasksTable.setRowCount(len(self.tasklist))
        for t in self.tasklist:
            task_desc = QTableWidgetItem(t.title[1:-1])
            task_desc.setFlags(~flg)

            task_priority = QTableWidgetItem(t.priority[1:-1])
            task_priority.setFlags(~flg)

            task_status = QTableWidgetItem(t.status[1:-1])
            task_status.setFlags(~flg)

            task_delete = QPushButton("x")
            task_delete.clicked.connect(partial(task_manager.del_task, t))

            task_edit = QPushButton("View/Edit")
            task_edit.clicked.connect(partial(self.edt_task, t))
            
            task_priority.setBackground(get_rgb_from_hex(colors[t.priority[1:-1]]))

            task_due_date = QTableWidgetItem(t.due_date)
            date_format = '%Y-%m-%d'

            if datetime.datetime.strptime(t.due_date, date_format) < datetime.datetime.now():
                task_due_date.setBackground(get_rgb_from_hex(colors["Urgent"]))
            elif datetime.datetime.strptime(t.due_date, date_format) == datetime.datetime.now():
                task_due_date.setBackground(get_rgb_from_hex(colors["High"]))
            task_due_date.setFlags(~flg)
            
            self.tasksTable.setItem(i, 0, task_desc)
            self.tasksTable.setItem(i, 1, task_status)
            self.tasksTable.setItem(i, 2, task_priority)
            self.tasksTable.setItem(i, 3, task_due_date)
            self.tasksTable.setCellWidget(i, 4, task_edit)
            self.tasksTable.setCellWidget(i, 5, task_delete)

            i += 1
    
    def refresh_tasks(self, currentUser):
        self.tasklist = []
        ordering = self.get_order_index()
        self.tasklist = task_manager.print_task_list(currentUser.id, ordering)
        self.populateTaskTable(ordering)

    def cr_user(self, checked):
        self.w = user_manager.UserWindow()
        self.w.show()
        self.w.setFocus()
        print("f")

    def cr_task(self):
        self.w = task_manager.TaskWindow(self.current_user)
        self.w.show()
        self.w.setFocus()
        print("hhh")

    def edt_task(self, task):
        self.w = task_manager.TaskWindow(self.current_user, task)
        self.w.show()
        self.w.setFocus()
        print("hhh")

    def edt_roles(self, user_id, role):
        self.changed_users[user_id] = role
    

    def apply_changes(self):
        if self.lineEdit.text() != "" and self.lineEdit_2.text() != "":
            if self.lineEdit_2.text() == self.lineEdit_3.text():
                change_user_password(self.current_user, self.lineEdit.text(), self.lineEdit_2.text())
            else:
                er = error_handling.ErrorWindow()
                er.setErrorText(12)
                er.show()

        if self.changed_users:
            for new_permission in self.changed_users:
                user_manager.ch_perm(new_permission, self.changed_users[new_permission])
        self.populateUsersTable()
        
        

        
#change_user_password(3, "pass", "")
    '''
app = QApplication(sys.argv)
main_window = MainWindow(uList[0])
main_window.show()
app.exec()
'''