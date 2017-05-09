from PyQt4.QtCore import *
from PyQt4.QtGui import *

from qgis.utils import *
from qgis.core import *
from qgis.gui import *
from ui_selectDate import Ui_SelectDate


class SelectDateDialog(QDialog, Ui_SelectDate):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)

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
