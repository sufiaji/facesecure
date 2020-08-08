# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'admin.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!

# Pradhono R Aji @ merkaba.co.id
# 22/05/2020

from PyQt5 import QtCore, QtGui, QtWidgets
# from pickle5 import pickle
import sqlalchemy as alchemy
from dialog_dates import Ui_Dialog_Dates
from dialog_filter_user import Ui_Dialog_User
from dialog_filter_attendance import Ui_Dialog_Attendance
from dialog_about import Ui_Dialog_About
from dialog_db_credential import Ui_Dialog_DBCredential
from PyQt5.QtWidgets import QFileDialog
from dialog_confirm import Ui_Dialog_Confirm
import face_recognition
import utils
import csv
import os
import datetime

KEY_CSV_DOWNLOAD_PATH = utils.KEY_CSV_DOWNLOAD_PATH
DB_NAME = 'facesecure'

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(820, 537)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setFixedSize(820, 537)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(10, 10, 611, 451))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(630, 11, 181, 211))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("assets/noPhotoAvailable.png"))
        self.label.setScaledContents(True)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")        
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("assets/mag_glass.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(10, 470, 75, 23))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(139, 470, 101, 23))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(85, 470, 31, 23))
        self.pushButton_3.setText("")
        self.pushButton_3.setIcon(icon)
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(240, 470, 31, 23))
        self.pushButton_4.setText("")
        self.pushButton_4.setIcon(icon)
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_5 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_5.setGeometry(QtCore.QRect(491, 470, 131, 23))
        self.pushButton_5.setObjectName("pushButton_5")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 820, 21))
        self.menubar.setObjectName("menubar")
        self.menuMenu = QtWidgets.QMenu(self.menubar)
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")        
        MainWindow.setStatusBar(self.statusbar)
        self.actionDownload_CSV = QtWidgets.QAction(MainWindow)
        self.actionDownload_CSV.triggered.connect(self.downloadCSV)
        self.actionDownload_CSV.setObjectName("actionDownload_CSV")
        self.actionShow_Encoding = QtWidgets.QAction(MainWindow)
        self.actionShow_Encoding.setObjectName("actionShow_Encoding")
        self.actionAbout = QtWidgets.QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.actionAbout.triggered.connect(self.showAbout)
        self.actionGuidance = QtWidgets.QAction(MainWindow)
        self.actionGuidance.setObjectName("actionGuidance")
        self.actionGuidance.triggered.connect(self.openGuide)
        self.actionSet_Download_Path = QtWidgets.QAction(MainWindow)
        self.actionSet_Download_Path.triggered.connect(self.setDownloadPath)
        self.actionSet_Download_Path.setObjectName("actionSet_Download_Path")
        self.actionSave_DB_Credential = QtWidgets.QAction(MainWindow)
        self.actionSave_DB_Credential.setObjectName("actionSave_DB_Credential")
        self.actionSave_DB_Credential.triggered.connect(self.saveDBCredential)
        self.actionDelete_record = QtWidgets.QAction(MainWindow)
        self.actionDelete_record.setObjectName("actionDelete_record")
        self.actionDelete_record.triggered.connect(self.delete)
        self.menuMenu.addAction(self.actionDownload_CSV)
        self.menuMenu.addAction(self.actionSet_Download_Path)
        self.menuMenu.addAction(self.actionSave_DB_Credential)
        self.menuAbout = QtWidgets.QMenu(self.menubar)
        self.menuAbout.setObjectName("menuAbout")
        self.menuAbout.addAction(self.actionAbout)
        self.menuAbout.addAction(self.actionGuidance)
        self.menuMenu.addAction(self.actionDelete_record)
        self.menubar.addAction(self.menuMenu.menuAction())
        self.menubar.addAction(self.menuAbout.menuAction())        

        self.pushButton.clicked.connect(self.showUser)
        self.pushButton_2.clicked.connect(self.showAttendance)
        self.pushButton_3.clicked.connect(self.filterUser)
        self.pushButton_4.clicked.connect(self.filterAttendance)
        self.pushButton_5.clicked.connect(self.register)
        self.tableWidget.itemSelectionChanged.connect(self.onItemSelected)
        self.statusbar.showMessage("Connecting to database...")

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Alpharai: Admin Program (Demo Version)"))
        self.pushButton.setText(_translate("MainWindow", "User Data"))
        self.pushButton_2.setText(_translate("MainWindow", "Attendance Data"))
        self.pushButton_5.setText(_translate("MainWindow", "Register New Person"))
        self.menuMenu.setTitle(_translate("MainWindow", "Menu"))
        self.menuAbout.setTitle(_translate("MainWindow", "Help"))
        self.actionDownload_CSV.setText(_translate("MainWindow", "Download CSV"))
        self.actionShow_Encoding.setText(_translate("MainWindow", "Show Encoding"))
        self.actionAbout.setText(_translate("MainWindow", "About"))
        self.actionGuidance.setText(_translate("MainWindow", "Guidance"))
        self.actionSet_Download_Path.setText(_translate("MainWindow", "Set CSV Download Path"))
        self.actionSave_DB_Credential.setText(_translate("MainWindow", "Save DB Credential"))
        self.actionDelete_record.setText(_translate("MainWindow", "Delete record"))
    
    def openGuide(self):
        try:
            os.startfile('Guide.pdf')
        except Exception as ex:
            self.showMessagebar(str(ex))
    
    def delete(self):
        b = self.tableWidget.selectedItems()
        if len(b)==0:
            self.showMessagebar("Please load data and/or select item you want to delete")
            return
        Dialog = QtWidgets.QDialog()
        ui = Ui_Dialog_Confirm()
        ui.setupUi(Dialog)
        Dialog.show()
        okcode = Dialog.exec_()
        if okcode == QtWidgets.QDialog.Accepted:
            self.deleteRow()
    
    def deleteRow(self):
        if self.show=="user":            
            try:
                for index in self.tableWidget.selectedIndexes():
                    d = index.row()              
                    selected_user_data = self.user_data[d]
                    nik = selected_user_data[0]
                    okcode, engine = utils.getEngine()
                    if okcode==utils.OK_CODE:
                        with engine.connect() as connection:
                            delete_statement = "delete from public." + utils.TABLE_USER + " where user_id='" + nik + "'"
                            sql_statement = alchemy.text(delete_statement)
                            connection.execute(sql_statement)
                self.showUser()
                self.showMessagebar('record deleted successfully')
            except Exception as ex:
                self.showMessagebar(str(ex))
        elif self.show=="attendance":
            try:
                for index in self.tableWidget.selectedIndexes():
                    d = index.row()
                    selected_att_data = self.att_data[d]
                    id = selected_att_data[0]
                    ok, engine = utils.getEngine()
                    if ok==utils.OK_CODE:
                        with engine.connect() as connection:
                            delete_statement = "delete from public." + utils.TABLE_ATTENDANCE + " where id='" + str(id) + "'"
                            sql_query = alchemy.text(delete_statement)
                            connection.execute(sql_query)
                self.showAttendance()
                self.showMessagebar('record deleted successfully')
            except Exception as ex:
                self.showMessagebar(str(ex))

    def register(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        filename, _ = QFileDialog.getOpenFileName(None,"Select a photo", "","JPG Files (*.jpg);;JPEG Files (*.jpeg)", options=options)
        if filename:
            Dialog = QtWidgets.QDialog()
            ui = Ui_Dialog_User()
            ui.setupUi(Dialog, "Please input ID and name")
            ui.initWidgets('', '')
            Dialog.show()
            okcode = Dialog.exec_()
            if okcode == QtWidgets.QDialog.Accepted:
                loadfile = face_recognition.load_image_file(filename)
                encoding = face_recognition.face_encodings(loadfile)[0]
                if(len(encoding)==128):
                    nik = ui.lineEdit.text().strip()
                    name = ui.lineEdit_2.text().strip()
                    if(nik!=''):
                        okcode,_,_,_ = utils.saveNewUser(nik, name)
                        if okcode==utils.OK_CODE:
                            okcode,_ = utils.saveNewEncoding(userId=nik, encoding_array=encoding)
                            utils.saveImageUser2('photos/', nik, filename)
                            self.showMessagebar("New user successfully registered")

    def showAbout(self):
        Dialog = QtWidgets.QDialog()
        ui = Ui_Dialog_About()
        ui.setupUi(Dialog)
        Dialog.show()
        Dialog.exec_()        
    
    def downloadCSV(self):        
        Dialog = QtWidgets.QDialog()
        ui = Ui_Dialog_Dates()
        ui.setupUi(Dialog)
        Dialog.show()
        okcode = Dialog.exec_()
        if okcode == QtWidgets.QDialog.Accepted:
            date_from = ui.date_edit_from.dateTime().toPyDateTime()
            date_to = ui.date_edit_to.dateTime().toPyDateTime()
            att_data = self.loadDbAttendance(nik="", dateFrom=date_from, dateTo=date_to, loc="")
            if att_data:
                try:
                    filename = 'attendance'
                    if date_to is None:
                        filename = filename + '_' + date_from.strftime("%d-%m-%Y")
                    else:
                        filename = filename + '_' + date_from.strftime("%d-%m-%Y") + '_to_' + date_to.strftime("%d-%m-%Y")
                    filename = filename + '.csv'
                    with open(os.path.join(self.download_path, filename), 'w', newline='') as csvfile:
                        writer = csv.writer(csvfile)
                        writer.writerow(['NIK', 'Date', 'Time', 'Status', 'Location'])                        
                        for data in att_data:
                            writer.writerow([data[1], (data[2]).strftime("%d-%m-%Y"), (data[3]).strftime("%H:%M:%S"), data[4], data[5]])  
                    self.showMessagebar('Successfully download attendance data into csv file')
                except Exception as ex:
                    self.showMessagebar(str(ex))
    
    def setDownloadPath(self):
        dialog = QtWidgets.QFileDialog()
        download_path = dialog.getExistingDirectory(None, "Select Folder to save CSV file", self.download_path)
        if download_path!='':
            self.download_path = download_path
            self.updateConfig(KEY_CSV_DOWNLOAD_PATH, download_path)
            self.showMessagebar('Download path saved successfully.')
    
    def updateConfig(self, key, value):
        sql_statement = "UPDATE public.config SET value='" + value + "' WHERE key='" + key + "'" 
        okcode, engine = utils.getEngine()
        if okcode==utils.OK_CODE:
            with engine.connect() as connection:
                sql_query = alchemy.text(sql_statement)
                connection.execute(sql_query)
        else:
            self.showMessagebar(okcode)
    
    def saveDBCredential(self):
        Dialog = QtWidgets.QDialog()
        ui = Ui_Dialog_DBCredential()
        ui.setupUi(Dialog)
        Dialog.show()
        okcode = Dialog.exec_()
        if okcode == QtWidgets.QDialog.Accepted:
            utils.saveCredentialPickle(dbuser=ui.lineEdit.text(), dbpass=ui.lineEdit_2.text())
            self.showMessagebar("DB Credential changed successfully")
        else:
            self.showMessagebar("DB Credential unchanged")

    def filterUser(self):
        Dialog = QtWidgets.QDialog()
        ui = Ui_Dialog_User()
        ui.setupUi(Dialog, "Filter User records")
        ui.initWidgets(self.filter_user_nik, self.filter_user_name)
        Dialog.show()
        okcode = Dialog.exec_()
        if okcode == QtWidgets.QDialog.Accepted:
            self.filter_user_nik = ui.lineEdit.text()
            self.filter_user_name = ui.lineEdit_2.text()
            self.user_data = self.loadDbUser(self.filter_user_nik, self.filter_user_name)
            self.showTableUser(self.user_data)
            self.showMessagebar('User data filtered')
        else:
            self.showMessagebar('User data filter cancelled')

    def filterAttendance(self):
        Dialog = QtWidgets.QDialog()
        ui = Ui_Dialog_Attendance()
        ui.setupUi(Dialog)
        ui.initWidgets(self.filter_att_nik, self.filter_att_datefrom, self.filter_att_dateto, self.filter_att_location)
        Dialog.show()
        okcode = Dialog.exec_()
        if okcode == QtWidgets.QDialog.Accepted:
            self.filter_att_nik = ui.lineEdit.text()
            self.filter_att_datefrom = ui.dateEdit.dateTime().toPyDateTime()
            self.filter_att_dateto = ui.dateEdit_2.dateTime().toPyDateTime()
            self.filter_att_location = ui.lineEdit_4.text()
            self.att_data = self.loadDbAttendance(self.filter_att_nik , self.filter_att_datefrom, self.filter_att_dateto, self.filter_att_location)
            self.showTableAttendance(self.att_data)
            self.showMessagebar('Attendance data filtered')
        else:
            self.showMessagebar('Attendance data filter cancelled')

    def onItemSelected(self):       
        if self.show=="user":            
            try:
                d = set(index.row() for index in self.tableWidget.selectedIndexes())
                d = d.pop()
                selected_user_data = self.user_data[d]
                nik = selected_user_data[0]
                # self.selectedItem = self.tableWidget.selectedItems()
                image = 'photos/' + nik + '.jpg'
                self.label.setPixmap(QtGui.QPixmap(image))
                self.showMessagebar('NIK: '+nik+', Name: '+selected_user_data[2]+'] selected')
            except Exception as ex:
                self.label.setPixmap(QtGui.QPixmap("assets/noPhotoAvailable.png"))
                self.showMessagebar(str(ex))
        elif self.show=="attendance":
            try:
                d = set(index.row() for index in self.tableWidget.selectedIndexes())
                d = d.pop()
                selected_att_data = self.att_data[d]
                nik = selected_att_data[1]
                date = (selected_att_data[2]).strftime("%d-%m-%Y")
                time = (selected_att_data[3]).strftime("%H-%M-%S")
                image = 'attendances/'+ nik + '_' + date + ',' + time + '.jpg'
                self.label.setPixmap(QtGui.QPixmap(image))
                ok, engine = utils.getEngine()
                if ok==utils.OK_CODE:
                    with engine.connect() as connection:
                        select_statement = "select name from public.euser where user_id='" + nik + "'"
                        sql_query = alchemy.text(select_statement)
                        result = connection.execute(sql_query)
                        result_as_list = result.fetchall()
                        msg = 'Attendance data for NIK: '+nik+', Name: '+result_as_list[0][0]+' selected'
                        self.showMessagebar(msg)
            except Exception as ex:
                self.label.setPixmap(QtGui.QPixmap("assets/noPhotoAvailable.png"))
                self.showMessagebar(str(ex))
    
    def showUser(self):
        self.show = "user"
        self.user_data = []
        self.user_data = self.loadDbUser("","")
        if self.user_data:
            self.showTableUser(self.user_data)
            self.pushButton_3.setEnabled(True)
            self.pushButton_4.setEnabled(False)
        else:
            self.showMessagebar('Data not found')
    
    def showTableUser(self, user_data):
        self.label.setPixmap(QtGui.QPixmap("assets/noPhotoAvailable.png"))
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setRowCount(0)
        self.tableWidget.setHorizontalHeaderLabels(['NIK', 'Time', 'Name'])
        for i, data in enumerate(user_data):
            nik = data[0]
            createdAt = (data[1]).strftime("%d/%m/%Y, %H:%M:%S")
            name = data[2]
            self.tableWidget.insertRow(i)
            self.tableWidget.setItem(i, 0, QtWidgets.QTableWidgetItem(nik))
            self.tableWidget.setItem(i, 1, QtWidgets.QTableWidgetItem(createdAt))
            self.tableWidget.setItem(i, 2, QtWidgets.QTableWidgetItem(name))

    def showAttendance(self):
        self.show = "attendance"
        self.att_data = []
        self.att_data = self.loadDbAttendance("","","","")
        if self.att_data:
            self.showTableAttendance(self.att_data)
            self.pushButton_3.setEnabled(False)
            self.pushButton_4.setEnabled(True)
        else:
            self.showMessagebar('Data not found')

    def showTableAttendance(self, att_data):
        self.label.setPixmap(QtGui.QPixmap("assets/noPhotoAvailable.png"))
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setRowCount(0)
        self.tableWidget.setHorizontalHeaderLabels(['ID', 'NIK', 'Date', 'Time', 'Status', 'Location'])
        for i, data in enumerate(att_data):
            id = data[0]
            nik = data[1]
            date = (data[2]).strftime("%d/%m/%Y")
            time = (data[3]).strftime("%H:%M:%S")
            status = data[4]
            location = data[5]
            self.tableWidget.insertRow(i)            
            self.tableWidget.setItem(i, 0, QtWidgets.QTableWidgetItem(nik))
            self.tableWidget.setItem(i, 1, QtWidgets.QTableWidgetItem(date))
            self.tableWidget.setItem(i, 2, QtWidgets.QTableWidgetItem(time))
            self.tableWidget.setItem(i, 3, QtWidgets.QTableWidgetItem(status))
            self.tableWidget.setItem(i, 4, QtWidgets.QTableWidgetItem(location))
            # self.tableWidget.setItem(i, 5, QtWidgets.QTableWidgetItem(id))
    
    def loadDbUser(self, nik, name):
        nik = nik.strip()
        nik = "%"+nik+"%"
        name = name.strip()
        name = "%"+name+"%"
        select_statement = "select * from public.euser where user_id like '" + nik \
            + "' and name like '" + name + "'"
        
        okcode, engine = utils.getEngine()
        if okcode==utils.OK_CODE:            
            with engine.connect() as connection:                
                sql_query = alchemy.text(select_statement)
                result = connection.execute(sql_query)
                result_as_list = result.fetchall()
                return result_as_list
        else:
            self.showMessagebar(okcode)

    def loadDbAttendance(self, nik, dateFrom, dateTo, loc):
        # nik
        nik = nik.strip()
        nik = "%" +nik+ "%"
        # location
        loc = loc.strip()
        loc = "%"+ loc
        # date_from
        date_from = "1970-01-01"
        if dateFrom!="":            
            date_from = dateFrom.strftime("%Y-%m-%d")
        # date_to
        date_to = "2100-01-01"
        if dateTo!="":
            date_to = dateTo.strftime("%Y-%m-%d")
        select_statement = "select * from public.attendance where user_id like '" + nik \
            + "' and created_at >= '" + date_from + "' and created_at <= '" + date_to \
            + "' and location like '" + loc + "'" + " order by created_at asc, created_on asc"
        okcode, engine = utils.getEngine()
        if okcode==utils.OK_CODE:
            with engine.connect() as connection:                
                sql_query = alchemy.text(select_statement)
                result = connection.execute(sql_query)
                result_as_list = result.fetchall()
                return result_as_list
        else:
            self.showMessagebar(okcode)
    
    def showMessagebar(self, message):
        self.statusbar.showMessage(message)
    
    def init(self):
        self.dbname = DB_NAME
        self.filter_user_nik = ''
        self.filter_user_name = ''
        self.filter_att_nik = ''
        self.filter_att_datefrom = datetime.datetime.now()
        self.filter_att_dateto = datetime.datetime.now()
        self.filter_att_location = ''
        self.user_data = []
        self.att_data = []
        okcode, _ = utils.getEngine()
        if okcode==utils.OK_CODE:
            self.showMessagebar('Ready.')
        else:
            self.showMessagebar(okcode)

        self.pushButton_3.setEnabled(False)
        self.pushButton_4.setEnabled(False)
        self.download_path = os.getcwd()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    ui.init()
    MainWindow.show()
    sys.exit(app.exec_())