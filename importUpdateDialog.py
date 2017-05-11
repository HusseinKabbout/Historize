from PyQt4.QtCore import *
from PyQt4.QtGui import *

from qgis.utils import *
from qgis.core import *
from qgis.gui import *
from ui_importUpdate import Ui_ImportUpdate
from sqlexecute import SQLExecute
from dbconn import DBConn


class ImportUpdateDialog(QDialog, Ui_ImportUpdate):
    """
    Class documentation goes here.
    """
    def __init__(self, iface, parent=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.iface = iface
        self.dbconn = DBConn(iface)
        self.getAttributes()
        self.setImportableTables()

    def getAttributes(self):
        # Model Structure used from Tutorial at
        # http://pythoncentral.io/pyside-pyqt-tutorial-qlistview-and-qstandarditemmodel/
        self.model = QStandardItemModel(self.listTblAttrib)

        self.selectedLayer = self.iface.activeLayer()

        if not self.selectedLayer:
            QMessageBox.warning(self.iface.mainWindow(), "Select Layer", "Please select a layer!")
            return

        self.hasGeometry = self.selectedLayer.hasGeometryType()
        self.provider = self.selectedLayer.dataProvider()

        if self.provider.name() != 'postgres':
            QMessageBox.warning(self.iface.mainWindow(), "Invalid Layer", "Layer must be provided by postgres!")
            return

        fields = self.selectedLayer.pendingFields()

        # http://pythoncentral.io/pyside-pyqt-tutorial-qlistview-and-qstandarditemmodel/
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
                print self.model.item(i).text()
                exclList.append(self.model.item(i).text())
            i += 1
        return exclList

    def setImportableTables(self):
        """Populates combobox with importable tables

           Name Structure <schema.tablename>"""
        self.uri = QgsDataSourceURI(self.provider.dataSourceUri())
        cur = self.dbconn.connectToDb(self.uri)
        self.execute = SQLExecute(cur)

        # Returns Result to be parsed
        schemaTableList = self.execute.retrieveImportableTables()
        if schemaTableList:
            for entry in schemaTableList:
                print entry[0]

    @pyqtSignature("")
    def on_buttonBox_accepted(self):
        """
        Slot documentation goes here.
        """
        exclList = self.getCheckedAttributes()
        # Split the user selection for querying
        select = self.cmbImportTable.currentText()
        if select == "":
            QMessageBox.warning(self.iface.mainWindow(), "Invalid Selection", "Please select an import table.")
            self.show()
        else:
            splitString = select.split('.')
            importSchema = splitString[0]
            importTable = splitString[1]
            self.execute.histTabsUpdate(importSchema, importTable, self.uri.schema(), self.selectedLayer, self.hasGeometry, exclList)
        print "Accepted"

    @pyqtSignature("")
    def on_buttonBox_rejected(self):
        """
        Slot documentation goes here.
        """
        print "Close"
        self.close()
