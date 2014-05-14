"""
/***************************************************************************
qgis web connector
                                 A QGIS plugin

                             -------------------
        begin                : 
        copyright            : 
        email                : 
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

from PyQt4 import QtCore, QtGui
from ui_qwebconnector import Ui_webConnectorDialog
from EditWebServices import Ui_EditWSDialog

# create the view dialog
class qWebConnectorDialog(QtGui.QDialog, Ui_webConnectorDialog):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        # Set up the user interface from Designer.
        #self.ui = Ui_Dialog()
        self.setupUi(self)
# create the settings dialog
class webservicesSettingDialog(QtGui.QDialog, Ui_EditWSDialog):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        # Set up the user interface from Designer.
        #self.ui = Ui_Dialog()
        self.setupUi(self)