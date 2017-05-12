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


class SQLExecute:
    """Class documentation goes here"""

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

    def histTabsVersion(self, schema, table, date):
        versionQuery = "SELECT * FROM hist_tabs.version(NULL::%s.%s, %s)" % (schema, layer, date)
        try:
            self.cur.execute(versionQuery)
            self.conn.commit()
        except:
            self.conn.rollback()
        self.conn.close()

    def histTabsUpdate(self, importSchema, importTable, prodSchema, prodTable, hasGeometry, exclList):
        updateQuery = "SELECT * FROM hist_tabs.update( \
                       %s.%s, \
                       %s.%s, \
                       %s, \
                       %s)" % (importSchema, importTable, prodSchema, prodTable, hasGeometry, exclList)
        try:
            self.cur.execute(updateQuery)
            self.conn.commit()
        except:
            self.conn.rollback()
        self.conn.close()

    def retrieveHistVersions(self, selected_layer):
        """Returns a list of historized dates or False"""
        table = selected_layer.name()
        getHistorizedDatesQuery = "SELECT DISTINCT valid_from FROM hist_tabs.public_cities_max_pop_gr_4m_testsample"
        try:
            self.cur.execute(getHistorizedDatesQuery)
            self.conn.commit()
        except:
            self.conn.rollback()
        dateList = self.cur.fetchall()
        self.conn.close()
        return dateList

    def retrieveImportableTables(self):
        """Returns all table names and schemas eglible for an import"""

        importableQuery = "SELECT table_schema, table_name FROM information_schema.columns \
                           WHERE table_schema != 'information_schema' \
                           AND table_schema != 'pg_catalog' \
                           AND NOT table_name IN ('spatial_ref_sys', 'geography_columns', 'geometry_columns', 'raster_columns')"

        self.cur.execute(importableQuery)
        return self.cur.fetchall()
