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
from PyQt4.QtGui import QMessageBox
from PyQt4.QtCore import QObject

from qgis.core import QgsCredentials

import psycopg2


class DBConn(QObject):
    """Class for establishing a DB-connection"""

    def __init__(self, iface):
        QObject.__init__(self)

        self.iface = iface

    def connect_to_DB(self, uri):
        """Create a connection object from a uri and return it."""
        conn = None
        ok = False
        while not conn:
            try:
                conn = psycopg2.connect(uri.connectionInfo())
            except psycopg2.OperationalError as e:
                (ok, user, passwd) = QgsCredentials.instance().get(
                    uri.connectionInfo(), uri.username(), uri.password())
                if not ok:
                    break
        if not conn:
            QMessageBox.warning(self.iface.mainWindow(), self.tr(
                u"Connection Error"), self.tr(
                    u"Could not connect to PostgreSQL database"))

        if ok:
            QgsCredentials.instance().put(uri.connectionInfo(), user, passwd)

        return conn
