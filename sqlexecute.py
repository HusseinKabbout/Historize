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

    def Init_hist_tabs(self, hasGeometry, schema, table):
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

    def get_older_table_version(self, schema, layer, date, uri):
        paramDate = datetime.strptime(date, '%Y-%m-%d %H:%M:%S.%f').date()
        versionQuery = "SELECT * FROM hist_tabs.version(NULL::%s.%s, '%s')" % (
            schema, layer, date)
        try:
            uri.setDataSource(
                "", u"(%s\n)" % versionQuery, self.get_geometry(
                    layer), "", self.get_id(layer))
            vlayer = QgsVectorLayer(uri.uri(), "%s_%s_(Historised)" % (
                paramDate, layer), "postgres")
            if vlayer.isValid():
                QgsMapLayerRegistry.instance().addMapLayer(vlayer, True)
        except Exception:
            QMessageBox.warning(
                self.mainWindow,
                self.tr(u"Error"),
                self.tr(u"Unable to load layer to map reigstry."))
        self.conn.close()

    def update_table_entries(self, importSchema, importTable,
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
        except Exception as e:
            self.conn.rollback()
            QMessageBox.warning(
                self.mainWindow,
                self.tr(u"Error"),
                self.tr(e.message.split('\n')[0]))
        self.conn.close()

    def retrieve_all_table_versions(self, layer, schema):
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

    def retrieve_all_importable_tables(self):
        """Returns all table names and schemas eglible for an import"""

        importableLayersQuery = "SELECT table_schema, table_name FROM information_schema.tables WHERE table_schema != 'information_schema' AND table_schema != 'pg_catalog' AND NOT table_name IN ('spatial_ref_sys', 'geography_columns', 'geometry_columns', 'raster_columns')"

        self.cur.execute(importableLayersQuery)
        return self.cur.fetchall()

    def check_if_historised(self, schema, layer):
        self.success = False
        isHistorisedQuery = "SELECT hist_id FROM hist_tabs.%s" % schema+"_" + layer
        try:
            self.cur.execute(isHistorisedQuery)
            self.success = True
        except Exception:
            pass
        self.conn.close()
        return self.success

    def get_geometry(self, layer):
        self.cur.execute("SELECT f_geometry_column FROM (SELECT * FROM geometry_columns WHERE f_table_name='%s') as f" % (layer))
        return self.cur.fetchall()[0][0]

    def get_id(self, layer):
        self.cur.execute("SELECT a.attname FROM pg_index i JOIN pg_attribute a ON a.attrelid=i.indrelid AND a.attnum=ANY(i.indkey) WHERE i.indrelid='%s'::regclass AND i.indisprimary;" % (layer))
        return self.cur.fetchall()[0][0]
