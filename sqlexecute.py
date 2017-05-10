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

    def __init__(self, cur=None):
        self.cur = cur

    def histTabsInit(self, hasGeometry, schema, table):
        print hasGeometry
        print schema
        print table
        initQuery = "SELECT * FROM hist_tabs.init('%s.%s', %s)" % (schema, table, hasGeometry)
        self.cur.execute(initQuery)

    def histTabsVersion(self):
        pass

    def histTabsUpdate(self):
        pass
