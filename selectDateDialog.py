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
from PyQt4.QtGui import QDialog, QMessageBox


from qgis.core import QgsDataSourceURI

from sqlexecute import SQLExecute

from ui_selectDate import Ui_SelectDate
from dbconn import DBConn


class SelectDateDialog(QDialog, Ui_SelectDate):
    """
    Class responsible for handling the date selection.
    """
    def __init__(self, iface):
        QDialog.__init__(self)
        self.setupUi(self)
        self.iface = iface
        self.dbconn = DBConn(iface)
        self.cmbDate.clear()
        self.get_dates()

    def get_dates(self):
        """Get all historized dates from layer"""
        provider = self.iface.activeLayer().dataProvider()
        self.uri = QgsDataSourceURI(provider.dataSourceUri())
        self.conn = self.dbconn.connect_to_DB(self.uri)
        # self.schema = self.uri.schema()
        self.execute = SQLExecute(
            self.iface, self.iface.mainWindow(), self.uri)
        dateList = self.execute.retrieve_all_table_versions(
            self.iface.activeLayer().name(), self.uri.schema())

        if not dateList:
            self.records = False
            QMessageBox.warning(
                self.iface.mainWindow(),
                self.tr(u"Error"),
                self.tr(u"No historized versions found!"))
        else:
            for date in dateList:
                self.cmbDate.addItem(str(date[0]))
                self.records = True

    @pyqtSignature("")
    def on_buttonBox_accepted(self):
        """
        Run hist_tabs.version() SQL-function
        """
        if self.records:
            self.execute.get_older_table_version(
                self.uri.schema(),
                self.iface.activeLayer().name(),
                self.cmbDate.currentText(),
                self.uri)

    @pyqtSignature("")
    def on_buttonBox_rejected(self):
        """
        Close Window and DB-Connection
        """
        self.conn.close()
        self.close()
