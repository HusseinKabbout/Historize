from PyQt4.QtCore import *
from PyQt4.QtGui import *

from qgis.utils import *
from qgis.core import *
from qgis.gui import *
from ui_selectDate import Ui_SelectDate
from sqlexecute import SQLExecute
from dbconn import DBConn


class SelectDateDialog(QDialog, Ui_SelectDate):
    """
    Class responsible for handling the date selection.
    """
    def __init__(self, iface, parent=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.iface = iface
        self.dbconn = DBConn(iface)
        self.cmbDate.clear()
        self.getDates()

    def getDates(self):
        """Get all historized dates from layer"""
        provider = self.iface.activeLayer().dataProvider()
        self.uri = QgsDataSourceURI(provider.dataSourceUri())
        self.conn = self.dbconn.connectToDb(self.uri)
        self.schema = self.uri.schema()
        self.execute = SQLExecute(self.conn, self.iface.activeLayer())
        self.dateList = self.execute.retrieveHistVersions(self.iface.activeLayer().name(), self.schema)

        if not self.dateList:
            self.records = False
            QMessageBox.warning(self.iface.mainWindow(), "Error", "No historized versions found!")
        else:
            for date in self.dateList:
                self.cmbDate.addItem(str(date[0]))
                self.records = True

    @pyqtSignature("")
    def on_buttonBox_accepted(self):
        """
        Run hist_tabs.version() SQL-function
        """
        if self.records:
            self.execute.histTabsVersion(self.schema, self.iface.activeLayer().name(), self.cmbDate.currentText(), self.uri)

    @pyqtSignature("")
    def on_buttonBox_rejected(self):
        """
        Close Window and DB-Connection
        """
        self.conn.close()
        self.close()
