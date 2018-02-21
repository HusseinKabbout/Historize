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

from qgis.core import QgsVectorLayer, QgsMapLayerRegistry

from datetime import datetime


class SQLExecute(QObject):
    """Class receives a connection object,
    creates a cursor for it and runs the SQL commands."""

    def __init__(self, mainWindow, conn, layer):
        QObject.__init__(self)

        self.mainWindow = mainWindow
        self.conn = conn
        self.cur = conn.cursor()
        self.layer = layer
        self.success = False

    def histTabsInit(self, hasGeometry, schema, table):
        initQuery = "SELECT * FROM hist_tabs._table_init('%s.%s')" % (
            schema, table)
        try:
            self.cur.execute(initQuery)
            self.conn.commit()
            self.success = True
        except Exception:
            self.conn.rollback()
        self.conn.close()
        return self.success

    def histTabsVersion(self, schema, layer, date, uri):
        paramDate = datetime.strptime(date, '%Y-%m-%d %H:%M:%S.%f').date()
        versionQuery = "SELECT * FROM hist_tabs.version(NULL::%s.%s, '%s')" % (
            schema, layer, date)
        try:
            uri.setDataSource(
                "", u"(%s\n)" % versionQuery, "wkb_geometry", "", "fid")
            vlayer = QgsVectorLayer(uri.uri(), "%s_%s_(Historised)" % (
                paramDate, layer), "postgres")
            if vlayer.isValid():
                QgsMapLayerRegistry.instance().addMapLayers([vlayer], True)
        except Exception:
            QMessageBox.warning(
                self.mainWindow,
                self.tr(u"Error"),
                self.tr(u"Unable to load layer to map reigstry."))
        self.conn.close()

    def histTabsUpdate(self, importSchema, importTable,
                       prodSchema, prodTable, hasGeometry, exclList):
        exclString = ', '.join(exclList)
        updateQuery = "SELECT * FROM hist_tabs.update( \
                       '%s.%s', \
                       '%s.%s', \
                       %s, \
                       '%s')" % (
                           importSchema, importTable, prodSchema,
                           prodTable, hasGeometry, exclString)
        try:
            self.cur.execute(updateQuery)
            self.conn.commit()
        except Exception:
            self.conn.rollback()
            QMessageBox.warning(
                self.mainWindow,
                self.tr(u"Error"),
                self.tr(u"Unable to update layer attributes."))
        self.conn.close()

    def retrieveHistVersions(self, layer, schema):
        """Returns a list of historized dates or False"""
        getHistorizedDatesQuery = "SELECT DISTINCT valid_from FROM hist_tabs.%s" % schema+"_"+layer
        try:
            self.cur.execute(getHistorizedDatesQuery)
            self.conn.commit()
            dateList = self.cur.fetchall()
        except Exception:
            self.conn.rollback()
            dateList = False
        return dateList

    def retrieveImportableTables(self):
        """Returns all table names and schemas eglible for an import"""

        importableLayersQuery = "SELECT table_schema, table_name FROM information_schema.columns WHERE table_schema != 'information_schema' AND table_schema != 'pg_catalog' AND NOT table_name IN ('spatial_ref_sys', 'geography_columns', 'geometry_columns', 'raster_columns')"

        self.cur.execute(importableLayersQuery)
        return self.cur.fetchall()

    def checkIfHistorised(self, schema, layer):
        self.success = False
        isHistorisedQuery = "SELECT hist_id FROM hist_tabs.%s" % schema+"_" + layer
        try:
            self.cur.execute(isHistorisedQuery)
            self.success = True
        except Exception:
            pass
        self.conn.close()
        return self.success
