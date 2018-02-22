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

from qgis.core import QgsVectorLayer, QgsMapLayerRegistry

from dbconn import DBConn

from datetime import datetime
import psycopg2


class SQLExecute(DBConn):
    """Class receives a connection object,
    creates a cursor for it and runs the SQL commands."""

    def __init__(self, iface, mainWindow, uri):
        DBConn.__init__(self, iface)

        self.mainWindow = mainWindow
        self.uri = uri

    def Init_hist_tabs(self, hasGeometry, schema, table):
        initQuery = "SELECT * FROM hist_tabs._table_init('%s.%s')" % (
            schema, table)
        success = False
        msg = ''
        conn = self.connect_to_DB(self.uri)
        cur = conn.cursor()
        try:
            cur.execute(initQuery)
            conn.commit()
            success = True
        except psycopg2.Error as e:
            conn.rollback()
            msg = e.message.split('\n')[0]
        conn.close()
        return success, msg

    def get_older_table_version(self, schema, layer, date, uri):
        paramDate = datetime.strptime(date, '%Y-%m-%d %H:%M:%S.%f').date()
        versionQuery = "SELECT * FROM hist_tabs.version(NULL::%s.%s, '%s')" % (
            schema, layer, date)
        conn = self.connect_to_DB(self.uri)
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
        conn.close()

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
        conn = self.connect_to_DB(self.uri)
        cur = conn.cursor()
        try:
            cur.execute(updateQuery)
            conn.commit()
        except psycopg2.Error as e:
            conn.rollback()
            QMessageBox.warning(
                self.mainWindow,
                self.tr(u"Error"),
                self.tr(e.message.split('\n')[0]))
        conn.close()

    def retrieve_all_table_versions(self, layer, schema):
        """Returns a list of historized dates or False"""
        getHistorizedDatesQuery = "SELECT DISTINCT valid_from \
        FROM hist_tabs.%s" % schema+"_"+layer
        conn = self.connect_to_DB(self.uri)
        cur = conn.cursor()
        try:
            cur.execute(getHistorizedDatesQuery)
            conn.commit()
            dateList = cur.fetchall()
        except psycopg2.Error as e:
            conn.rollback()
            dateList = False
        return dateList

    def retrieve_all_importable_tables(self):
        """Returns all table names and schemas eglible for an import"""

        importableLayersQuery = "SELECT table_schema, table_name \
        FROM information_schema.tables \
        WHERE table_schema != 'information_schema' \
        AND table_schema != 'pg_catalog' \
        AND NOT table_name IN \
        ('spatial_ref_sys', 'geography_columns', \
        'geometry_columns', 'raster_columns')"
        conn = self.connect_to_DB(self.uri)
        cur = conn.cursor()

        cur.execute(importableLayersQuery)
        return cur.fetchall()

    def check_if_historised(self, schema, layer):
        isHistorisedQuery = "SELECT hist_id \
        FROM hist_tabs.%s" % schema+"_" + layer
        conn = self.connect_to_DB(self.uri)
        cur = conn.cursor()
        try:
            cur.execute(isHistorisedQuery)
            self.success = True
        except psycopg2.Error as e:
            self.success = False
        conn.close()
        return self.success

    def get_geometry(self, layer):
        conn = self.connect_to_DB(self.uri)
        cur = conn.cursor()
        cur.execute("SELECT f_geometry_column FROM (\
                         SELECT * FROM geometry_columns \
                         WHERE f_table_name='%s') as f" % (layer))
        return cur.fetchall()[0][0]
        conn.close()

    def get_id(self, layer):
        conn = self.connect_to_DB(self.uri)
        cur = conn.cursor()
        cur.execute("SELECT a.attname FROM pg_index i \
                         JOIN pg_attribute a ON a.attrelid=i.indrelid \
                         AND a.attnum=ANY(i.indkey) \
                         WHERE i.indrelid='%s'::regclass \
                         AND i.indisprimary;" % (layer))
        return cur.fetchall()[0][0]
        conn.close()

    def db_initialize_check(self, schema):
        isInitializedQuery = "SELECT TRUE FROM information_schema.schemata \
        WHERE schema_name = 'hist_tabs';"
        conn = self.connect_to_DB(self.uri)
        cur = conn.cursor()

        cur.execute(isInitializedQuery)
        success = bool(cur.rowcount)
        conn.close()
        return success
