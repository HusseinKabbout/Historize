"""
 /***************************************************************************
   QGIS Historize Plugin
  -------------------------------------------------------------------
 Date                 : 09 Mai 2017
 Copyright            : (C) 2017 by William Habelt
 email                : wha@sourcepole.ch

  ***************************************************************************
  *                                                                         *
  *   This program is free software; you can redistribute it and/or modify  *
  *   it under the terms of the GNU General Public License as published by  *
  *   the Free Software Foundation; either version 2 of the License, or     *
  *   (at your option) any later version.                                   *
  *                                                                         *
  ***************************************************************************/
"""
from PyQt4.QtCore import pyqtSignature
from PyQt4.QtGui import QDialog, QStandardItemModel, QStandardItem

from qgis.core import QgsDataSourceURI

from sqlexecute import SQLExecute

from ui_importUpdate import Ui_ImportUpdate
from dbconn import DBConn


class ImportUpdateDialog(QDialog, Ui_ImportUpdate):
    """
    Class responsible for handling the update() function.
    """
    def __init__(self, iface, parent=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.iface = iface
        self.dbconn = DBConn(iface)
        self.getAttributes()
        self.setImportableTables()

    def getAttributes(self):
        """Place excludable attributes in model list"""
        # Model Structure used from Tutorial at
        # http://pythoncentral.io/pyside-pyqt-tutorial-qlistview-and-qstandarditemmodel/

        self.model = QStandardItemModel(self.listTblAttrib)
        self.hasGeometry = self.iface.activeLayer().hasGeometryType()
        self.provider = self.iface.activeLayer().dataProvider()
        fields = self.iface.activeLayer().pendingFields()

        for field in fields:
            item = QStandardItem(field.name())
            item.setCheckable(True)
            self.model.appendRow(item)
        self.listTblAttrib.setModel(self.model)

    def getCheckedAttributes(self):
        """Creates a list of checked elements to be excluded"""
        i = 0
        exclList = list()
        while self.model.item(i):
            if self.model.item(i).checkState():
                exclList.append(self.model.item(i).text())
            i += 1
        return exclList

    def setImportableTables(self):
        """Populates combobox with importable tables

           Name Structure <schema.tablename>"""
        self.uri = QgsDataSourceURI(self.provider.dataSourceUri())
        conn = self.dbconn.connectToDb(self.uri)
        self.execute = SQLExecute(self.iface.mainWindow(), conn,
                                  self.iface.activeLayer())

        # Returns Result to be parsed
        schemaTableList = self.execute.retrieveImportableTables()
        cmbList = list()
        if schemaTableList:
            for entry in schemaTableList:
                cmbEntry = entry[0] + '.' + entry[1]
                cmbList.append(cmbEntry)
        self.cmbImportTable.addItems(cmbList)

    @pyqtSignature("")
    def on_buttonBox_accepted(self):
        """
        Run hist_tabs.update() SQL function with given parameters
        """
        select = self.cmbImportTable.currentText()
        exclList = self.getCheckedAttributes()
        # Split the user selection for querying
        splitString = select.split('.')
        importSchema = splitString[0]
        importTable = splitString[1]
        self.execute.histTabsUpdate(
            importSchema,
            importTable,
            self.uri.schema(),
            self.iface.activeLayer().name(),
            self.hasGeometry, exclList)

    @pyqtSignature("")
    def on_buttonBox_rejected(self):
        """
        Slot documentation goes here.
        """
        self.close()
