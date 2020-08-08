# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dialog_dates.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!

# Pradhono R Aji @ merkaba.co.id
# 25/01/2020


from PyQt5 import QtCore, QtGui, QtWidgets
from date_picker import Ui_Dialog_Calendar
from datetime import datetime

class Ui_Dialog_Dates(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setWindowModality(QtCore.Qt.ApplicationModal)
        Dialog.resize(357, 92)
        Dialog.setModal(True)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("assets/calendar.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(250, 20, 81, 241))
        self.buttonBox.setOrientation(QtCore.Qt.Vertical)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.date_edit_from = QtWidgets.QDateEdit(Dialog)
        self.date_edit_from.setGeometry(QtCore.QRect(60, 20, 110, 22))
        self.date_edit_from.setObjectName("date_edit_from")
        self.date_edit_from.setDate(datetime.now())
        self.label_from = QtWidgets.QLabel(Dialog)
        self.label_from.setGeometry(QtCore.QRect(20, 20, 41, 16))
        self.label_from.setObjectName("label_from")
        self.label_to = QtWidgets.QLabel(Dialog)
        self.label_to.setGeometry(QtCore.QRect(20, 50, 41, 16))
        self.label_to.setObjectName("label_to")
        self.date_edit_to = QtWidgets.QDateEdit(Dialog)
        self.date_edit_to.setGeometry(QtCore.QRect(60, 50, 110, 22))
        self.date_edit_to.setObjectName("date_edit_to")
        self.date_edit_to.setDate(datetime.now())
        self.button_from = QtWidgets.QPushButton(Dialog)
        self.button_from.setIcon(icon)
        self.button_from.setGeometry(QtCore.QRect(180, 20, 31, 23))
        self.button_from.setText("")
        self.button_from.setObjectName("button_from")
        self.button_from.clicked.connect(self.dateFrom)
        self.button_to = QtWidgets.QPushButton(Dialog)
        self.button_to.setIcon(icon)
        self.button_to.setGeometry(QtCore.QRect(180, 50, 31, 23))
        self.button_to.setText("")
        self.button_to.setObjectName("button_to")
        self.button_to.clicked.connect(self.dateTo)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
    
    def dateFrom(self):
        Dialog = QtWidgets.QDialog()
        ui_cal = Ui_Dialog_Calendar()
        ui_cal.setupUi(Dialog)
        Dialog.show()
        okcode = Dialog.exec_()
        if okcode == QtWidgets.QDialog.Accepted:
            date = ui_cal.calendarWidget.selectedDate()
            self.date_edit_from.setDate(date)
        else:
            print('Cancelled')

    def dateTo(self):
        Dialog = QtWidgets.QDialog()
        ui_cal = Ui_Dialog_Calendar()
        ui_cal.setupUi(Dialog)
        Dialog.show()
        okcode = Dialog.exec_()
        if okcode == QtWidgets.QDialog.Accepted:
            date = ui_cal.calendarWidget.selectedDate()
            self.date_edit_to.setDate(date)
        else:
            print('Cancelled')

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Select Dates"))
        self.label_from.setText(_translate("Dialog", "From:"))
        self.label_to.setText(_translate("Dialog", "To:"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui_this = Ui_Dialog_Dates()
    ui_this.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
