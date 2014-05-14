# -*- coding: utf-8 -*-

#
# Created: Mon Apr 28 11:12:08 2014
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

class Ui_webConnectorDialog(object):
    def setupUi(self, webservicesDialog):
        webservicesDialog.setObjectName(_fromUtf8("webservicesDialog"))
        webservicesDialog.resize(600, 385)
        self.Webview = QtWebKit.QWebView(webservicesDialog)
        self.Webview.setGeometry(QtCore.QRect(0, 30, 600, 360))
        self.Webview.setUrl(QtCore.QUrl(_fromUtf8("about:blank")))
        self.Webview.setObjectName(_fromUtf8("Webview"))
        self.openInBrowser = QtGui.QPushButton(webservicesDialog)
        self.openInBrowser.setGeometry(QtCore.QRect(509, 2, 90, 25))
        self.openInBrowser.setObjectName(_fromUtf8("openInBrowser"))
        self.zoomPlus = QtGui.QPushButton(webservicesDialog)
        self.zoomPlus.setGeometry(QtCore.QRect(556, 360, 20, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.zoomPlus.setFont(font)
        self.zoomPlus.setObjectName(_fromUtf8("zoomPlus"))
        self.comboBox = QtGui.QComboBox(webservicesDialog)
        self.comboBox.setGeometry(QtCore.QRect(2, 2, 120, 25))
        self.comboBox.setObjectName(_fromUtf8("comboBox"))
        self.urlLine = QtGui.QLineEdit(webservicesDialog)
        self.urlLine.setGeometry(QtCore.QRect(122, 2, 298, 25))
        self.urlLine.setObjectName(_fromUtf8("urlLine"))
        self.zoomMinus = QtGui.QPushButton(webservicesDialog)
        self.zoomMinus.setGeometry(QtCore.QRect(575, 360, 20, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.zoomMinus.setFont(font)
        self.zoomMinus.setObjectName(_fromUtf8("zoomMinus"))
        self.openGeoJSON = QtGui.QPushButton(webservicesDialog)
        self.openGeoJSON.setGeometry(QtCore.QRect(420, 2, 90, 25))
        self.openGeoJSON.setObjectName(_fromUtf8("openGeoJSON"))

        self.retranslateUi(webservicesDialog)
        QtCore.QMetaObject.connectSlotsByName(webservicesDialog)

    def retranslateUi(self, webservicesDialog):
        webservicesDialog.setWindowTitle(_translate("webservicesDialog", "Dialog", None))
        self.openInBrowser.setText(_translate("webservicesDialog", "open in browser", None))
        self.zoomPlus.setToolTip(_translate("webservicesDialog", "Zoom +", None))
        self.zoomPlus.setText(_translate("webservicesDialog", "+", None))
        self.zoomMinus.setToolTip(_translate("webservicesDialog", "Zoom -", None))
        self.zoomMinus.setText(_translate("webservicesDialog", "-", None))
        self.openGeoJSON.setText(_translate("webservicesDialog", "Open GeoJSON", None))

from PyQt4 import QtWebKit
