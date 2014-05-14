# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Documents and Settings\ferregutie\.qgis2\python\plugins\go2webservices\EditWebServices.ui'
#
# Created: Mon Apr 28 11:12:56 2014
#      by: PyQt4 UI code generator 4.10.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_EditWSDialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(480, 172)
        self.WSName = QtGui.QLineEdit(Dialog)
        self.WSName.setGeometry(QtCore.QRect(150, 10, 131, 25))
        self.WSName.setObjectName(_fromUtf8("WSName"))
        self.listWS = QtGui.QListView(Dialog)
        self.listWS.setGeometry(QtCore.QRect(10, 10, 131, 154))
        self.listWS.setObjectName(_fromUtf8("listWS"))
        self.UpdateNewWS = QtGui.QPushButton(Dialog)
        self.UpdateNewWS.setGeometry(QtCore.QRect(290, 10, 91, 25))
        self.UpdateNewWS.setObjectName(_fromUtf8("UpdateNewWS"))
        self.DeleteWS = QtGui.QPushButton(Dialog)
        self.DeleteWS.setGeometry(QtCore.QRect(390, 10, 77, 25))
        self.DeleteWS.setObjectName(_fromUtf8("DeleteWS"))
        self.WSUrl = QtGui.QTextEdit(Dialog)
        self.WSUrl.setGeometry(QtCore.QRect(150, 40, 320, 71))
        self.WSUrl.setObjectName(_fromUtf8("WSUrl"))
        self.VariablesList = QtGui.QComboBox(Dialog)
        self.VariablesList.setGeometry(QtCore.QRect(150, 140, 221, 23))
        self.VariablesList.setObjectName(_fromUtf8("VariablesList"))
        self.insertVar = QtGui.QPushButton(Dialog)
        self.insertVar.setGeometry(QtCore.QRect(380, 140, 91, 23))
        self.insertVar.setObjectName(_fromUtf8("insertVar"))
        self.helper = QtGui.QLabel(Dialog)
        self.helper.setGeometry(QtCore.QRect(150, 120, 321, 16))
        self.helper.setText(_fromUtf8(""))
        self.helper.setObjectName(_fromUtf8("helper"))

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Edit Geo Web Services", None))
        self.UpdateNewWS.setText(_translate("Dialog", "Update/New", None))
        self.DeleteWS.setText(_translate("Dialog", "Delete", None))
        self.insertVar.setText(_translate("Dialog", "Insert variable", None))

