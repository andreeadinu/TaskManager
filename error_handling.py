from PySide6.QtCore import (QCoreApplication, QMetaObject, QRect, QSize, Qt)
from PySide6.QtGui import (QFont, QIcon)
from PySide6.QtWidgets import (QDialogButtonBox, QLabel, QSizePolicy, QWidget)


###########################################################################
### implement the error handling window
###########################################################################
class ErrorWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(400, 143)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setMaximumSize(QSize(400, 143))
        icon = QIcon(QIcon.fromTheme(u"dialog-error"))
        self.setWindowIcon(icon)
        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setGeometry(QRect(20, 100, 341, 32))
        sizePolicy.setHeightForWidth(self.buttonBox.sizePolicy().hasHeightForWidth())
        self.buttonBox.setSizePolicy(sizePolicy)
        self.buttonBox.setMaximumSize(QSize(16777215, 200))
        self.buttonBox.setLayoutDirection(Qt.LeftToRight)
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(True)
        self.label = QLabel(self)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(20, 30, 341, 41))
        self.label.setWordWrap(True)
        font = QFont()
        font.setPointSize(15)
        self.label.setFont(font)
        self.label.setLayoutDirection(Qt.LeftToRight)
        self.label.setAlignment(Qt.AlignCenter)

        self.retranslateUi()
        self.buttonBox.accepted.connect(self.accept)
        
        QMetaObject.connectSlotsByName(self)
    
    def retranslateUi(self):
        self.setWindowTitle(QCoreApplication.translate("Dialog", u"Error", None))

###########################################################################
### the error info text is set using this function called with an error code
### possible codes:
###     10: the two fields of password do not match when creating a user
###     11: the username is less than 7 characters long when creating a user
###     12: wrong password
###########################################################################
    def setErrorText(self, error_code):
        match error_code:
            case 1:
                self.label.setText(QCoreApplication.translate("Dialog", u"error 1", None))
            case 10:
                self.label.setText(QCoreApplication.translate("Dialog", u"Error creating user. Passwords do not match! Please write the same password in both text lines", None))
            case 11:
                self.label.setText(QCoreApplication.translate("Dialog", u"Username must be at least 7 character long", None))
            case 12:
                self.label.setText(QCoreApplication.translate("Dialog", u"The password is wrong", None))
            case 13:
                self.label.setText(QCoreApplication.translate("Dialog", u"Please enter a username and a password", None))
            case 14:
                self.label.setText(QCoreApplication.translate("Dialog", u"Wrong username or password", None))
            case _:
                self.label.setText(QCoreApplication.translate("Dialog", u"unknown error", None))

    def accept(self):
        self.close()