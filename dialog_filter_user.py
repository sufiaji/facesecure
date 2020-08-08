# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dialog_filter_user.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!

# Pradhono R Aji @ merkaba.co.id
# 22/05/2020


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog_User(object):
    def setupUi(self, Dialog, Title):
        Dialog.setObjectName("Dialog")
        Dialog.setWindowModality(QtCore.Qt.ApplicationModal)
        Dialog.resize(386, 96)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(290, 20, 81, 241))
        self.buttonBox.setOrientation(QtCore.Qt.Vertical)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.lineEdit = QtWidgets.QLineEdit(Dialog)
        self.lineEdit.setGeometry(QtCore.QRect(50, 20, 113, 20))
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit.setMaxLength(8)
        self.lineEdit_2 = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_2.setGeometry(QtCore.QRect(50, 50, 201, 20))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(10, 20, 47, 13))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(10, 50, 47, 13))
        self.label_2.setObjectName("label_2")

        self.retranslateUi(Dialog, Title)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog, Title):
        _translate = QtCore.QCoreApplication.translate
        # Dialog.setWindowTitle(_translate("Dialog", "Filter User"))
        Dialog.setWindowTitle(_translate("Dialog", Title))
        self.label.setText(_translate("Dialog", "NIK"))
        self.label_2.setText(_translate("Dialog", "Name"))
    
    def initWidgets(self, nik, name):
        self.lineEdit.setText(nik)
        self.lineEdit_2.setText(name)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog_User()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
