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
from PyQt4.QtCore import QSettings, QTranslator, QCoreApplication, QObject
from PyQt4.QtGui import QAction, QMenu, QMessageBox

from qgis.core import QgsDataSourceURI

import os

from importUpdateDialog import ImportUpdateDialog
from selectDateDialog import SelectDateDialog
from aboutDialog import AboutDialog
from dbconn import DBConn
from sqlexecute import SQLExecute


class Historize:
    """This class handles the initialization and calls of the menus"""

    def __init__(self, iface):
        self.iface = iface
        self.dbconn = DBConn(iface)
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'Historize_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

    def tr(self, message):
        return QCoreApplication.translate('Historize', message)

    def initGui(self):
        self.menu = QMenu()
        self.menu.setTitle("Historize")

        self.lyrMenu = QMenu()
        self.lyrMenu.setTitle("Layer")

        # Create menu actions
        self.actionInit = QAction(self.tr(u"Initialize Database"),
                                  self.iface.mainWindow())
        self.actionLyrInit = QAction(self.tr(u"Initialize Layer"),
                                     self.iface.mainWindow())
        self.actionLyrUpdate = QAction(self.tr(u"Update Layer"),
                                       self.iface.mainWindow())
        self.actionLyrLoad = QAction(self.tr(u"Load Layer"),
                                     self.iface.mainWindow())
        self.actionAbout = QAction(self.tr(u"About"), self.iface.mainWindow())

        # Connect menu actions
        self.actionInit.triggered.connect(self.doInit)
        self.actionLyrInit.triggered.connect(self.doLyrInit)
        self.actionLyrLoad.triggered.connect(self.doLyrLoad)
        self.actionLyrUpdate.triggered.connect(self.doLyrUpdate)
        self.actionAbout.triggered.connect(self.doAbout)

        QObject.connect(self.iface.mapCanvas(), SIGNAL(
            "currentLayerChanged(QgsMapLayer *)"), self.setMenuOptions)

        # Add actions to menu
        self.lyrMenu.addActions(
            [self.actionLyrInit, self.actionLyrLoad, self.actionLyrUpdate])
        self.menu.addAction(self.actionInit)
        self.menu.addMenu(self.lyrMenu)
        self.menu.addAction(self.actionAbout)
        self.menu.insertSeparator(self.actionAbout)
        menuBar = self.iface.mainWindow().menuBar()
        menuBar.addMenu(self.menu)

        # Disable unusable actions
        self.actionInit.setEnabled(False)
        self.actionLyrInit.setEnabled(False)
        self.actionLyrUpdate.setEnabled(False)
        self.actionLyrLoad.setEnabled(False)

    def unload(self):
        self.menu.deleteLater()

    def doInit(self):
        """Use Database info from layer and run historisation.sql on it."""

        selectedLayer = self.iface.activeLayer()
        provider = selectedLayer.dataProvider()

        if provider.name() != 'postgres':
            QMessageBox.warning(
                self.iface.mainWindow(),
                self.tr(u"Invalid Layer"),
                self.tr(u"Layer must be provided by postgres!"))
            return

        uri = QgsDataSourceURI(provider.dataSourceUri())
        conn = self.dbconn.connectToDb(uri)
        cur = conn.cursor()
        if conn is False:
            return

        result = QMessageBox.warning(
            self.iface.mainWindow(),
            self.tr(u"Initialize Historisation"),
            self.tr(u"Initialize historisation on this layers database?"),
            QMessageBox.No | QMessageBox.Yes)
        if result == QMessageBox.Yes:
            sqlPath = os.path.dirname(
                os.path.realpath(__file__)) + '/sql/historisierung.sql'
            fd = open(sqlPath, 'r')
            sqlFile = fd.read()
            fd.close()
            try:
                # Ignore first three characters
                # which invalidate the SQL command
                cur.execute(sqlFile[3:])
                conn.commit()
                QMessageBox.warning(
                    self.iface.mainWindow(),
                    self.tr(u"Success"),
                    self.tr(u"Database initialized successfully!"))
            except Exception:
                conn.rollback()
                QMessageBox.warning(
                    self.iface.mainWindow(),
                    self.tr(u"Error"),
                    self.tr(u"Unable to initialize database!"))
            conn.close()
        else:
            return

    def doLyrInit(self):
        """Use Layer info and run init() .sql query"""
        selectedLayer = self.iface.activeLayer()
        provider = selectedLayer.dataProvider()
        uri = QgsDataSourceURI(provider.dataSourceUri())
        conn = self.dbconn.connectToDb(uri)
        cur = conn.cursor()

        if conn is False:
            return

        result = QMessageBox.warning(
            self.iface.mainWindow(),
            self.tr(u"Initialize Layer"),
            self.tr(u"Are you sure you wish to proceed?"),
            QMessageBox.No | QMessageBox.Yes)
        if result == QMessageBox.Yes:
            # Get SQL vars
            hasGeometry = selectedLayer.hasGeometryType()
            schema = uri.schema()
            table = uri.table()

            self.execute = SQLExecute(conn, selectedLayer)
            success = self.execute.histTabsInit(hasGeometry, schema, table)
            if success:
                QMessageBox.warning(
                    self.iface.mainWindow(),
                    self.tr(u"Success"),
                    self.tr(u"Layer successfully initialized!"))
            else:
                QMessageBox.warning(
                    self.iface.mainWindow(),
                    self.tr(u"Error"),
                    self.tr(u"Initialization failed!"))
        else:
            return

    def doLyrUpdate(self):
        """Open ImportUpdate dialog"""
        self.updateDialog = ImportUpdateDialog(self.iface)
        self.updateDialog.show()

    def doLyrLoad(self):
        """Open selectDate dialog"""
        self.dateDialog = SelectDateDialog(self.iface)
        self.dateDialog.show()

    def doAbout(self):
        """Show About dialog"""
        self.aboutDialog = AboutDialog()
        self.aboutDialog.show()

    def setMenuOptions(self, layer):
        """Enable/Disable menu options based on selected layer"""
        self.actionLyrInit.setEnabled(False)
        self.actionLyrUpdate.setEnabled(False)
        self.actionLyrLoad.setEnabled(False)
        self.actionInit.setEnabled(False)

        selectedLayer = self.iface.activeLayer()
        if selectedLayer:
            provider = layer.dataProvider()

            if provider.name() == "postgres":
                self.actionInit.setEnabled(True)
                uri = QgsDataSourceURI(provider.dataSourceUri())
                conn = self.dbconn.connectToDb(uri)
                cur = conn.cursor()
                self.execute = SQLExecute(conn)
                result = self.execute.checkIfHistorised(
                    uri.schema(), self.iface.activeLayer().name())

                if result:
                    self.actionLyrUpdate.setEnabled(True)
                    self.actionLyrLoad.setEnabled(True)
                else:
                    self.actionLyrInit.setEnabled(True)
