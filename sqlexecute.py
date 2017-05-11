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

    def __init__(self, cur=None, layer=None):
        self.cur = cur
        self.layer = layer

    def histTabsInit(self, hasGeometry, schema, table):
        initQuery = "SELECT * FROM hist_tabs.init(%s.%s, %s)" % (schema, table, hasGeometry)
        self.cur.execute(initQuery)

    def histTabsVersion(self, schema, table, date):
        versionQuery = "SELECT * FROM hist_tabs.version(NULL::%s.%s, %s)" % (schema, layer, date)

    def histTabsUpdate(self, importSchema, importTable, prodSchema, prodTable, hasGeometry, exclList):
        updateQuery = "SELECT * FROM hist_tabs.update( \
                       %s.%s, \
                       %s.%s, \
                       %s, \
                       %s)" % (importSchema, importTable, prodSchema, prodTable, hasGeometry, exclList)

    def retrieveHistVersions(self, selected_layer):
        """Returns a list of historized dates or False"""
        # isHistorizedQuery = "SELECT * FROM hist_tabs WHERE myTable = %s" % selected_layer
        return False

    def retrieveImportableTables(self):
        """Returns all table names and schemas eglible for an import"""

        importableQuery = "SELECT table_schema, table_name FROM information_schema.columns \
                           WHERE table_schema != 'information_schema' \
                           AND table_schema != 'pg_catalog' \
                           AND NOT table_name IN ('spatial_ref_sys', 'geography_columns', 'geometry_columns', 'raster_columns')"

        self.cur.execute(importableQuery)
        return self.cur.fetchall()
