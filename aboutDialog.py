from PyQt4.QtCore import *
from PyQt4.QtGui import *

from qgis.utils import *
from qgis.core import *
from qgis.gui import *
from ui_about import Ui_About


class AboutDialog(QDialog, Ui_About):
    """
    Class for displaying the user manual
    """
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.loadHtml()

    def loadHtml(self):
        htmlPath = os.path.dirname(os.path.realpath(__file__)) + '/doc/html/about.html'
        self.aboutView.load(QUrl(htmlPath))

    @pyqtSignature("")
    def on_buttonBox_accepted(self):
        """
        Slot documentation goes here.
        """

    @pyqtSignature("")
    def on_buttonBox_rejected(self):
        """
        Slot documentation goes here.
        """
        self.close()
