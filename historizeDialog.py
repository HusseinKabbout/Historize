
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from qgis.utils import *
from qgis.core import *
from qgis.gui import *
from ui_historize import Ui_Historize
from importUpdateDialog import ImportUpdateDialog
from selectDateDialog import SelectDateDialog


class HistorizeDialog(QDialog, Ui_Historize):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.updateDialog = ImportUpdateDialog()
        self.dateDialog = SelectDateDialog()

    @pyqtSignature("")
    def on_btnUpdateHistoLyr_clicked(self):
        """
        Slot documentation goes here.
        """
        print "open update dialog"
        self.updateDialog.show()

    @pyqtSignature("")
    def on_btnLoadHistoLyr_clicked(self):
        """
        Slot documentation goes here.
        """
        print "open update dialog"
        self.dateDialog.show()

    @pyqtSignature("")
    def on_buttonBox_accepted(self):
        """
        Slot documentation goes here.
        """
        print "Accepted"

    @pyqtSignature("")
    def on_buttonBox_rejected(self):
        """
        Slot documentation goes here.
        """
        print "Close"
        self.close()
