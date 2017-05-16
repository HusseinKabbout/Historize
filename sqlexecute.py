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
from datetime import datetime
from qgis.core import QgsVectorLayer, QgsMapLayerRegistry, QgsDataSourceURI


class SQLExecute:
    """Class receives a connection object, creates a cursor for it and runs the SQL commands."""

    def __init__(self, conn=None, layer=None):
        self.conn = conn
        self.cur = conn.cursor()
        self.layer = layer
        self.success = False

    def histTabsInit(self, hasGeometry, schema, table):
        initQuery = "SELECT * FROM hist_tabs._table_init('%s.%s')" % (schema, table)
        try:
            self.cur.execute(initQuery)
            self.conn.commit()
            self.success = True
        except:
            self.conn.rollback()
        self.conn.close()
        return self.success

    def histTabsVersion(self, schema, layer, date, uri):
        paramDate = datetime.strptime(date, '%Y-%m-%d %H:%M:%S.%f').date()
        versionQuery = "SELECT * FROM hist_tabs.version(NULL::%s.%s, '%s')" % (schema, layer, date)
        try:
            uri.setDataSource("", u"(%s\n)" % versionQuery, "wkb_geometry", "", "fid")
            vlayer = QgsVectorLayer(uri.uri(), "%s_%s_(Historised)" % (paramDate, layer), "postgres")
            if vlayer.isValid():
                QgsMapLayerRegistry.instance().addMapLayers([vlayer], True)
        except:
            QMessageBox.warning(self.iface.mainWindow(), self.tr(u"Error"), self.tr(u"Unable to load layer to map reigstry."))
        self.conn.close()

    def histTabsUpdate(self, importSchema, importTable, prodSchema, prodTable, hasGeometry, exclList):
        exclString = ', '.join(exclList)
        updateQuery = "SELECT * FROM hist_tabs.update( \
                       '%s.%s', \
                       '%s.%s', \
                       %s, \
                       '%s')" % (importSchema, importTable, prodSchema, prodTable, hasGeometry, exclString)
        #try:
        self.cur.execute(updateQuery)
        #    self.conn.commit()
        #except:
        #    self.conn.rollback()
        self.conn.close()

    def retrieveHistVersions(self, layer, schema):
        """Returns a list of historized dates or False"""
        getHistorizedDatesQuery = "SELECT DISTINCT valid_from FROM hist_tabs.%s" % schema+"_"+layer
        try:
            self.cur.execute(getHistorizedDatesQuery)
            self.conn.commit()
            dateList = self.cur.fetchall()
        except:
            self.conn.rollback()
            dateList = False
        return dateList

    def retrieveImportableTables(self):
        """Returns all table names and schemas eglible for an import"""

        importableQuery = "SELECT table_schema, table_name FROM information_schema.columns \
                           WHERE table_schema != 'information_schema' \
                           AND table_schema != 'pg_catalog' \
                           AND NOT table_name IN ('spatial_ref_sys', 'geography_columns', 'geometry_columns', 'raster_columns')"

        self.cur.execute(importableQuery)
        return self.cur.fetchall()

    def checkIfHistorised(self, schema, layer):
        self.success = False
        isHistorisedQuery = "SELECT hist_id FROM hist_tabs.%s" % schema+"_"+layer
        try:
            self.cur.execute(isHistorisedQuery)
            self.success = True
        except:
            pass
        self.conn.close()
        return self.success
