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
from qgis.core import QgsFeature,  QgsMapLayerRegistry
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *
from dbconn import DBConn
from historizeDialog import HistorizeDialog


class Historize:
    """Class documentation goes here"""

    def __init__(self, iface):
        self.iface = iface
        self.dbconn = DBConn(iface)

    def initGui(self):
        self.action = QAction("Historize", self.iface.mainWindow())
        self.iface.addPluginToMenu("Historize", self.action)
        self.histoDialog = HistorizeDialog()
        QObject.connect(self.action, SIGNAL("activated()"), self.histoDialog.show)

    def unload(self):
        self.iface.removePluginMenu("Historize", self.action)
