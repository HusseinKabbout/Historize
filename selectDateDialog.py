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
    Class documentation goes here.
    """
    def __init__(self, iface, parent=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.iface = iface
        self.dbconn = DBConn(iface)
        self.cmbDate.clear()
        self.getDates()

    def getDates(self):
        self.selectedLayer = self.iface.activeLayer()

        if not self.selectedLayer:
            QMessageBox.warning(self.iface.mainWindow(), "Select Layer", "Please select a layer!")
            return

        provider = self.selectedLayer.dataProvider()

        if provider.name() != 'postgres':
            QMessageBox.warning(self.iface.mainWindow(), "Invalid Layer", "Layer must be provided by postgres!")
            return

        uri = QgsDataSourceURI(provider.dataSourceUri())
        cur = self.dbconn.connectToDb(uri)

        self.schema = uri.schema()
        self.execute = SQLExecute(cur, self.selectedLayer)
        self.dateList = self.execute.retrieveHistVersions(self.selectedLayer)
        if not self.dateList:
            QMessageBox.warning(self.iface.mainWindow(), "Error", "No historized versions found!")
            self.noRecords = True
        else:
            self.cmbDate.addItems(self.dateList)

    @pyqtSignature("")
    def on_buttonBox_accepted(self):
        """
        Slot documentation goes here.
        """
        print "Accepted"
        if not self.noRecords:
            self.execute.histTabsVersion(self.schema, self.selectedLayer, self.cmbDate.currentText())

    @pyqtSignature("")
    def on_buttonBox_rejected(self):
        """
        Slot documentation goes here.
        """
        print "Close"
        self.close()
