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

    def histTabsInit(self):
        print "Initializing Layer"
        initQuery = "SELECT * FROM "
        # self.cur.execute()

    def histTabsVersion(self):
        pass

    def histTabsUpdate(self):
        pass
