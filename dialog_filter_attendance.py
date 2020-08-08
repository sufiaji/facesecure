# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dialog_filter_attendance.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!

# Pradhono R Aji @ merkaba.co.id
# 22/05/2020


from PyQt5 import QtCore, QtGui, QtWidgets
from date_picker import Ui_Dialog_Calendar
from datetime import datetime

class Ui_Dialog_Attendance(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setWindowModality(QtCore.Qt.ApplicationModal)
        Dialog.resize(476, 115)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(380, 10, 81, 241))
        self.buttonBox.setOrientation(QtCore.Qt.Vertical)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(10, 20, 47, 13))
        self.label.setObjectName("label")
        self.lineEdit = QtWidgets.QLineEdit(Dialog)
        self.lineEdit.setGeometry(QtCore.QRect(60, 20, 113, 20))
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit.setMaxLength(8)
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(10, 50, 31, 16))
        self.label_2.setObjectName("label_2")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("assets/calendar.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(171, 49, 31, 23))
        self.pushButton.setText("")
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setIcon(icon)
        self.pushButton_2 = QtWidgets.QPushButton(Dialog)
        self.pushButton_2.setGeometry(QtCore.QRect(333, 49, 31, 23))
        self.pushButton_2.setText("")
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.setIcon(icon)
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(10, 83, 47, 13))
        self.label_3.setObjectName("label_3")
        self.lineEdit_4 = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_4.setGeometry(QtCore.QRect(60, 80, 113, 20))
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.dateEdit = QtWidgets.QDateEdit(Dialog)
        self.dateEdit.setDate(datetime.now())
        self.dateEdit.setGeometry(QtCore.QRect(60, 50, 110, 22))
        self.dateEdit.setObjectName("dateEdit")
        self.dateEdit_2 = QtWidgets.QDateEdit(Dialog)
        self.dateEdit_2.setDate(datetime.now())
        self.dateEdit_2.setGeometry(QtCore.QRect(220, 50, 110, 22))
        self.dateEdit_2.setObjectName("dateEdit_2")
        self.pushButton.clicked.connect(self.dateFrom)
        self.pushButton_2.clicked.connect(self.dateTo)
        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Filter Attendance Data"))
        self.label.setText(_translate("Dialog", "NIK"))
        self.label_2.setText(_translate("Dialog", "Date"))
        self.label_3.setText(_translate("Dialog", "Location"))
    
    def initWidgets(self, nik, date_from, date_to, location):
        self.lineEdit.setText(nik) 
        self.lineEdit_4.setText(location)
        self.dateEdit.setDate(date_from)
        self.dateEdit_2.setDate(date_to)
    
    def dateFrom(self):
        Dialog = QtWidgets.QDialog()
        ui_cal = Ui_Dialog_Calendar()
        ui_cal.setupUi(Dialog)
        Dialog.show()
        okcode = Dialog.exec_()
        if okcode == QtWidgets.QDialog.Accepted:
            date = ui_cal.calendarWidget.selectedDate()
            self.dateEdit.setDate(date)
        # else:
        #     print('Cancelled')

    def dateTo(self):
        Dialog = QtWidgets.QDialog()
        ui_cal = Ui_Dialog_Calendar()
        ui_cal.setupUi(Dialog)
        Dialog.show()
        okcode = Dialog.exec_()
        if okcode == QtWidgets.QDialog.Accepted:
            date = ui_cal.calendarWidget.selectedDate()
            self.dateEdit_2.setDate(date)
        # else:
        #     print('Cancelled')


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog_Attendance()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
