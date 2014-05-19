"""
/***************************************************************************
qgis Web Connector
                                 A QGIS plugin
 Click to connect to geo web services
                              -------------------
        begin                : 2014-05-01
        copyright            : (C) 2014 enrico ferreguti
        email                : enricofer@gmail.com
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
# Import the PyQt and QGIS libraries

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *
from PyQt4 import QtGui, QtCore
from PyQt4 import uic
from qgis.core import *
from qgis.utils import *
from qgis.gui import *
from PyQt4.QtNetwork import *
from string import digits
from qwebconnectorDialog import qWebConnectorDialog, webservicesSettingDialog

import resources
import webbrowser
import urllib2
import string 
import os
import math
import json

class qWebConnector(QgsMapTool):

    def __init__(self, iface):
       
       # Save reference to the QGIS interface
        self.iface = iface
        # reference to the canvas
        self.canvas = self.iface.mapCanvas()
        QgsMapTool.__init__(self, self.canvas)

    def initGui(self):
        # Create actions that will start plugin configuration
        self.webServicesAction = QAction(QIcon(":/plugins/qgisWebConnector/icoWebConnector.png"), \
            "Click to open Geo Web Services", self.iface.mainWindow())
        QObject.connect(self.webServicesAction, SIGNAL("triggered()"), self.webServicesRun)
        # Add toolbar button and menu item
        self.iface.addToolBarIcon(self.webServicesAction)
        self.iface.addPluginToMenu("&Qgis Web Connector", self.webServicesAction)
        self.path = os.path.dirname( os.path.abspath( __file__ ) )
        #self.view = uic.loadUi( os.path.join( self.path, "qwebconnector.ui" ) )
        self.view = qWebConnectorDialog()
        self.view.zoomPlus.clicked.connect(self.zoomPlus)
        self.view.zoomMinus.clicked.connect(self.zoomMinus)
        self.view.openInBrowser.clicked.connect(self.openInBrowser)
        self.view.openGeoJSON.clicked.connect(self.openGeoJSON)
        self.view.comboBox.activated.connect(self.changeWebService)
        self.view.comboBox.setMaxVisibleItems(20)
        self.view.urlLine.returnPressed.connect(self.updateWebView)
        #self.view.urlLine.clicked.connect(self.highlightUrlLine) non funziona, bisogna reimplementare l'evento
        self.loadWebservicesFromFile()
        self.pressed=None
        #self.editWS = uic.loadUi( os.path.join( self.path, "EditWebServices.ui" ) )
        self.editWS = webservicesSettingDialog()
        #self.param={'VIEWLEFT':"",'VIEWBOTTOM':"",'VIEWRIGHT':"",'VIEWTOP':"",'SCALE':"",'LAT':"",'LON':"",'X':"",'Y':"",'HEADING':"",'BOXLEFT':"",'BOXRIGHT':"",'BOXBOTTOM':"",'BOXTOP':"",'PREVLAT':"",'PREVLON':"",'DRAGLAT':"",'DRAGLON':""}
        self.paramHelper={'VIEWLEFT':"Left side longitude of current map view",\
                        'VIEWBOTTOM':"Bottom side latitude of current map view",\
                        'VIEWRIGHT':"Right side longitude of current map view",\
                        'VIEWTOP':"Top side latitude of current map view",\
                        'SCALE':"Scale of the current map view",\
                        'LAT':"Latitude WGS84 of last click on map",\
                        'LON':"Longitude WGS84 of last click on map",\
                        'X':"Coordinate x in current SRS",\
                        'Y':"Coordinate y in current SRS",\
                        'HEADING':"Dragged direction Heading",\
                        'BOXLEFT':"Left side longitude of dragged box",\
                        'BOXRIGHT':"Right side longitude of dragged box",\
                        'BOXBOTTOM':"Bottom side latitude of dragged box",\
                        'BOXTOP':"Top side latitude of dragged box",\
                        'PREVLAT':"Latitude WGS84 of previous click on map",\
                        'PREVLON':"Longitude WGS84 of previous click on map",\
                        'DRAGLAT':"Latitude WGS84 of dragged point when cursor released",\
                        'DRAGLON':"Longitude WGS84 of dragged point when cursor released",
                        'OSMZOOMFACTOR':"Openstreetmap zoom factor",
                        'GMAPSZOOMFACTOR':"Google maps zoom factor",
                        'RADIUS': "distance in meters from click point and release point"}
        self.param = {}
        for (key,value) in self.paramHelper.iteritems():
            self.param[key]=""
        self.initEditWS()
        # procedure to set proxy if needed
        s = QSettings() #getting proxy from qgis options settings
        proxyEnabled = s.value("proxy/proxyEnabled", "")
        proxyType = s.value("proxy/proxyType", "" )
        proxyHost = s.value("proxy/proxyHost", "" )
        proxyPort = s.value("proxy/proxyPort", "" )
        proxyUser = s.value("proxy/proxyUser", "" )
        proxyPassword = s.value("proxy/proxyPassword", "" )
        print proxyEnabled+"; "+proxyType+"; "+proxyHost+"; " + proxyPort+"; " + proxyUser+"; " +"*********; "
        
        if proxyEnabled == "true": # test if there are proxy settings
           proxy = QNetworkProxy()
           if proxyType == "DefaultProxy":
               proxy.setType(QNetworkProxy.DefaultProxy)
           elif proxyType == "Socks5Proxy":
               proxy.setType(QNetworkProxy.Socks5Proxy)
           elif proxyType == "HttpProxy":
               proxy.setType(QNetworkProxy.HttpProxy)
           elif proxyType == "HttpCachingProxy":
               proxy.setType(QNetworkProxy.HttpCachingProxy)
           elif proxyType == "FtpCachingProxy":
               proxy.setType(QNetworkProxy.FtpCachingProxy)
           proxy.setHostName(proxyHost)
           proxy.setPort(int(proxyPort))
           proxy.setUser(proxyUser)
           proxy.setPassword(proxyPassword)
           QNetworkProxy.setApplicationProxy(proxy)

    def initEditWS(self):
        # Method to setup Settings editor window
        self.updateEditWS()
        model=QStandardItemModel(self.editWS.VariablesList)
        # populate qcombobox
        for key,value in self.param.iteritems():
            item = QStandardItem(key)
            model.appendRow(item)
            #self.editWS.VariablesList.addItem(key)
        model.sort(0)
        #set window to stay on top
        self.editWS.setWindowFlags(self.editWS.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)
        self.editWS.VariablesList.setModel(model)
        #catch selection of items in qlistview 
        self.editWS.listWS.clicked.connect(self.listWSelectedItem)
        self.editWS.UpdateNewWS.clicked.connect(self.updateNewWS)
        self.editWS.DeleteWS.clicked.connect(self.deleteWS)
        self.editWS.insertVar.clicked.connect(self.insertVariable)
        self.editWS.VariablesList.activated.connect(self.printHelper)

    def updateEditWS(self):
        #method to update qlistview with current webservices list
        model=QStandardItemModel(self.editWS.listWS)
        for key,value in self.webservicesList.iteritems():
            item = QStandardItem(key)
            model.appendRow(item)
        model.sort(0)
        self.editWS.listWS.setModel(model)

    def listWSelectedItem(self,id):
        # landing method from selected item in qlistview event
        print "selected item in listWS"
        print id.row()
        print id.data()
        self.editWS.WSName.setText(id.data())
        self.editWS.WSUrl.setText(self.webservicesList[id.data()])
        pass

    def updateNewWS(self):
        #method to update webservices list called by button click
        print "update item clicked"
        self.webservicesList[self.editWS.WSName.text()]=self.editWS.WSUrl.toPlainText()
        self.updateEditWS()
        self.editWS.WSName.clear()
        self.editWS.WSUrl.clear()
        self.updateComboWebservices()
        self.writeWebservicesToFile()

    def updateComboWebservices(self):
        #method to update qcombobox in main windows 
        self.view.comboBox.clear()
        model=QStandardItemModel(self.view.comboBox)
        for key,value in self.webservicesList.iteritems():
            item = QStandardItem(key)
            model.appendRow(item)
        model.sort(0)
        self.view.comboBox.setModel(model)
        self.view.comboBox.addItem("Edit Webservices")
        self.view.comboBox.insertItem(0,"Select a Webservice")
        self.view.comboBox.setCurrentIndex(0)

    def zoomPlus(self):
        #zooming qwebview
        self.view.Webview.setZoomFactor(self.view.Webview.zoomFactor()+0.1)

    def zoomMinus(self):
        #zooming qwebview
        self.view.Webview.setZoomFactor(self.view.Webview.zoomFactor()-0.1)

    def deleteWS(self):
        #method to delete current item from webservices list called by button click
        print "delete item clicked"
        del self.webservicesList[self.editWS.WSName.text()]
        self.updateEditWS()
        self.editWS.WSName.clear()
        self.editWS.WSUrl.clear()
        self.updateComboWebservices()
        self.writeWebservicesToFile()

    def insertVariable(self):
        #landing method to insert in qeditview the variable selected in qcombobox
        print "insert variable clicked"
        self.editWS.WSUrl.insertPlainText("[%"+self.editWS.VariablesList.currentText()+"%]")

    def printHelper(self,var):
        self.editWS.helper.setText(self.paramHelper[self.editWS.VariablesList.currentText()])

    def unload(self):
        # Remove the plugin menu item and icon 
        self.iface.removePluginMenu("&Qgis Web Connector",self.webServicesAction)
        self.iface.removeToolBarIcon(self.webServicesAction)

    def loadWebservicesFromFile(self):
        #method for loading webservices list from file in plugin directory in json format
        path = os.path.dirname( os.path.abspath( __file__ ) )
        #webservicesListFile = open(os.path.join(path,'webservices.txt'),'r')
        self.webservicesList = json.load(open(os.path.join(path,'webservices.txt')))
        self.updateComboWebservices()

    def writeWebservicesToFile(self):
        #method for saving webservices list to file in plugin directory in json format
        path = os.path.dirname( os.path.abspath( __file__ ) )
        json.dump(self.webservicesList, open(os.path.join(path,'webservices.txt'),'w'))

    def openInBrowser(self):
        # open the current url in external browser
        webbrowser.open_new(self.view.urlLine.text())

    def openGeoJSON(self):
        vlayer = QgsVectorLayer(self.view.urlLine.text(), "Imported_GeoJSON", "ogr")
        QgsMapLayerRegistry.instance().addMapLayer(vlayer)

    def changeWebService(self,line):
        #landing method called when user click on qcombobox in main window
        print line
        #print self.webservicesList[self.view.comboBox.itemText(line)]
        if self.view.comboBox.itemText(line) == "Edit Webservices":
            self.updateComboWebservices()
            self.addWebService()
        else:
            self.view.urlLine.setText(self.parseUrl(self.webservicesList[self.view.comboBox.itemText(line)]))
            self.updateWebView()
            
    def addWebService(self):
        #called by clicking "edit webservices" on qcombobox
        self.editWS.show()
        pass
        

    def parseUrl(self,urlToParse):
        #procedure to replace variables string with variable contents
        urlToParse = urlToParse.replace("[%","%(")
        urlToParse = urlToParse.replace("%]",")s")
        #print urlToParse
        #print self.param
        return urlToParse % self.param


    def transformToWGS84(self, pPoint):
        # transformation from the current SRS to WGS84
        crcMappaCorrente = iface.mapCanvas().mapRenderer().destinationCrs() # get current crs
        crsSrc = crcMappaCorrente
        crsDest = QgsCoordinateReferenceSystem(4326)  # WGS 84
        xform = QgsCoordinateTransform(crsSrc, crsDest)
        return xform.transform(pPoint) # forward transformation: src -> dest

    def canvasPressEvent(self, event):
        # Press event handler inherited from QgsMapTool used to store the given location in WGS84 long/lat
        self.pressed=True
        self.pressx = event.pos().x()
        self.pressy = event.pos().y()
        self.movex = event.pos().x()
        self.movey = event.pos().y()
        self.highlight=QgsRubberBand(iface.mapCanvas(),QGis.Line )
        self.highlight.setColor(Qt.yellow)
        self.highlight.setWidth(5)
        self.box=QgsRubberBand(iface.mapCanvas(),QGis.Line )
        self.box.setColor(Qt.yellow)
        self.box.setWidth(1)
        #print "x:",self.pressx," y:",self.pressy
        self.pressedPoint = self.canvas.getCoordinateTransform().toMapCoordinates(self.pressx, self.pressy)
        self.pointWgs84 = self.transformToWGS84(self.pressedPoint)
        self.param['PREVLON'] = self.param['LON']
        self.param['PREVLAT'] = self.param['LAT']
        self.param['LON'] = str(self.pointWgs84.x())
        self.param['LAT'] = str(self.pointWgs84.y())
        self.param['X'] = str(self.pressx)
        self.param['Y'] = str(self.pressy)

    def canvasMoveEvent(self, event):
        # Moved event handler inherited from QgsMapTool needed to highlight the direction that is giving by the user
        if self.pressed:
            #print "canvasMoveEvent"
            x = event.pos().x()
            y = event.pos().y()
            movedPoint = self.canvas.getCoordinateTransform().toMapCoordinates(x, y)
            self.highlight.reset()
            self.highlight.addPoint(self.pressedPoint)
            self.highlight.addPoint(movedPoint)
            self.box.reset()
            self.box.addPoint(self.pressedPoint)
            self.box.addPoint(QgsPoint(self.pressedPoint.x(),movedPoint.y()))
            self.box.addPoint(movedPoint)
            self.box.addPoint(QgsPoint(movedPoint.x(),self.pressedPoint.y()))
            self.box.addPoint(self.pressedPoint)
            

    def canvasReleaseEvent(self, event):
        # Release event handler inherited from QgsMapTool needed to calculate heading
        self.pressed=None
        self.highlight.reset()
        self.box.reset()
        self.releasedx = event.pos().x()
        self.releasedy = event.pos().y()
        self.releasedPoint = self.canvas.getCoordinateTransform().toMapCoordinates(self.releasedx, self.releasedy)
        self.dragBox = QgsRectangle(self.pressedPoint,self.releasedPoint)
        self.releasedPoint = self.transformToWGS84(self.releasedPoint)
        self.param['DRAGLON'] = str(self.releasedPoint.x())
        self.param['DRAGLAT'] = str(self.releasedPoint.x())
        self.param['RADIUS'] = str(math.sqrt( (self.releasedx - self.pressx)**2 + (self.releasedy - self.pressy)**2 ))
        #print "x:",self.releasedx," y:",self.releasedy
        if (self.releasedx==self.pressx)&(self.releasedy==self.pressy):
            heading=0
            result=0
        else:
            result = math.atan2((self.releasedPoint.x() - self.pressedPoint.x()),(self.releasedPoint.y() - self.pressedPoint.y()))
            result = math.degrees(result)
            if result > 0:
                heading =  180 - result
            else:
                heading = 360 - (180 + result)      
        self.openSVDialog(heading)
        
    def openSVDialog(self,heading):
        # procedure for compiling streetview and bing url with the given location and heading
        heading = math.trunc(heading)
        self.param['HEADING'] = str(heading)
        viewExt = self.iface.mapCanvas().extent()
        topRight = self.transformToWGS84(QgsPoint(viewExt.xMaximum(),viewExt.yMaximum()))
        bottomLeft = self.transformToWGS84(QgsPoint(viewExt.xMinimum(),viewExt.yMinimum() ))
        #saving limits in lat/log of screen bounding box
        self.param['VIEWLEFT'] = str(bottomLeft.x())
        self.param['VIEWBOTTOM'] = str(bottomLeft.y())
        self.param['VIEWRIGHT'] = str(topRight.x())
        self.param['VIEWTOP'] = str(topRight.y())
        topRight = self.transformToWGS84(QgsPoint(self.dragBox.xMaximum(),self.dragBox.yMaximum()))
        bottomLeft = self.transformToWGS84(QgsPoint(self.dragBox.xMinimum(),self.dragBox.yMinimum() ))
        #saving bounding box set by the userf
        self.param['BOXLEFT'] = str(bottomLeft.x())
        self.param['BOXBOTTOM'] = str(bottomLeft.y())
        self.param['BOXRIGHT'] = str(topRight.x())
        self.param['BOXTOP'] = str(topRight.y())
        self.param['SCALE'] = str(self.iface.mapCanvas().scale())
        OSMzf={0:500000000.0,1:250000000.0,2:150000000.0,3:70000000.0,4:35000000.0,\
        5:15000000.0,6:10000000.0,7:4000000.0,8:2000000.0,\
        9:1000000.0,10:500000.0,11:250000.0,12:150000.0,\
        13:70000.0,14:35000.0,15:15000.0,16:8000.0,\
        17:4000.0,18:2000.0,19:1000.0}
        print OSMzf
        print "OSM"
        for (key,value) in OSMzf.iteritems():
            if self.iface.mapCanvas().scale()>value:
                self.param['OSMZOOMFACTOR']=str(key)
                break
        GMzf={1:591657550.500000,2:295828775.300000,3:147914387.600000,4:73957193.820000,\
        5:36978596.910000,6:18489298.450000,7:9244649.227000,8:4622324.614000,\
        9:2311162.307000,10:1155581.153000,11:577790.576700,12:288895.288400,\
        13:144447.644200,14:72223.822090,15:36111.911040,16:18055.955520,\
        17:9027.977761,18:4513.988880,19:2256.994440,20:1128.497220}
        for (key,value) in GMzf.iteritems():
            if self.iface.mapCanvas().scale()>value:
                self.param['GMAPSZOOMFACTOR']=str(key)
                break
        self.view.setWindowTitle("Qgis Web Connector")
        self.view.show()
        self.view.raise_()
        self.view.activateWindow()
        self.view.Webview.hide()
        if (self.view.comboBox.currentText() != "Select a Webservice")and(self.view.comboBox.currentText() != "Edit Webservices"):
            self.view.urlLine.setText(self.parseUrl(self.webservicesList[self.view.comboBox.currentText()]))
            self.updateWebView()
        #self.view.Webview.load(QUrl(self.WSUrl))
        self.view.Webview.show()

    def updateWebView(self):
        self.view.Webview.setZoomFactor(0.7)
        self.view.urlLine.setCursorPosition(0)
        self.view.Webview.load(QUrl(self.view.urlLine.text()))
        #self.param['PREVLAT']=""
        #self.param['PREVLON']=""

#    def updateWebView(highlightUrlLine):
#        self.view.urlLine.selectAll()
#        self.view.urlLine.copy()

    def webServicesRun(self):
        # called by click on toolbar icon
        gsvMessage="Pick a point and select a geo web service to open in browser window"
        iface.mainWindow().statusBar().showMessage(gsvMessage)
        self.canvas.setMapTool(self)
