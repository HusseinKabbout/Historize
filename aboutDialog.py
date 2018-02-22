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
from PyQt4.QtCore import QUrl, pyqtSignature
from PyQt4.QtGui import QDialog

import os

from ui_about import Ui_About


class AboutDialog(QDialog, Ui_About):
    """
    Class for displaying the user manual
    """
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.load_html()

    def load_html(self):
        htmlPath = os.path.dirname(os.path.realpath(
            __file__)) + '/doc/html/about.html'
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
