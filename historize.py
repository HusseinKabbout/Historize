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
from PyQt4.QtCore import (QSettings, QTranslator, QCoreApplication,
                          qVersion, QObject)
from PyQt4.QtGui import QAction, QMenu, QMessageBox

from qgis.core import QgsDataSourceURI

import os
import psycopg2

from importUpdateDialog import ImportUpdateDialog
from selectDateDialog import SelectDateDialog
from aboutDialog import AboutDialog
from dbconn import DBConn
from sqlexecute import SQLExecute


class Historize(QObject):
    """This class handles the initialization and calls of the menus"""

    def __init__(self, iface):
        QObject.__init__(self)

        self.iface = iface
        self.dbconn = DBConn(iface)
        plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            plugin_dir,
            'i18n',
            'Historize_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            translator = QTranslator()
            translator.load(locale_path)
            QCoreApplication.installTranslator(translator)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(translator)

    def initGui(self):
        self.menu = QMenu()
        self.menu.setTitle("Historize")

        self.layerMenu = QMenu()
        self.layerMenu.setTitle("Layer")

        # Create menu actions
        self.actionInitDB = QAction(self.tr(u"Initialize Database"),
                                    self.iface.mainWindow())
        self.actionInitLayer = QAction(self.tr(u"Initialize Layer"),
                                       self.iface.mainWindow())
        self.actionLayerUpdate = QAction(self.tr(u"Update Layer"),
                                         self.iface.mainWindow())
        self.actionLayerLoad = QAction(self.tr(u"Load Layer"),
                                       self.iface.mainWindow())
        self.actionAbout = QAction(self.tr(u"About"), self.iface.mainWindow())

        # Connect menu actions
        self.actionInitDB.triggered.connect(self.initialize_database)
        self.actionInitLayer.triggered.connect(self.initialize_layer)
        self.actionLayerLoad.triggered.connect(self.show_load_layer_dialog)
        self.actionLayerUpdate.triggered.connect(self.show_update_layer_dialog)
        self.actionAbout.triggered.connect(self.show_about_dialog)

        self.iface.legendInterface().currentLayerChanged.connect(
            self.enable_disable_gui)

        # Add actions to menu
        self.layerMenu.addActions(
            [self.actionInitLayer,
             self.actionLayerLoad, self.actionLayerUpdate])
        self.menu.addAction(self.actionInitDB)
        self.menu.addMenu(self.layerMenu)
        self.menu.addAction(self.actionAbout)
        self.menu.insertSeparator(self.actionAbout)
        menuBar = self.iface.mainWindow().menuBar()
        menuBar.addMenu(self.menu)

        # Disable unusable actions
        self.actionInitDB.setEnabled(False)
        self.actionInitLayer.setEnabled(False)
        self.actionLayerUpdate.setEnabled(False)
        self.actionLayerLoad.setEnabled(False)

    def unload(self):
        self.menu.deleteLater()

    def initialize_database(self):
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
        conn = self.dbconn.connect_to_DB(uri)
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
            try:
                # Ignore first three characters
                # which invalidate the SQL command
                cur.execute(open(sqlPath, "r").read())
                conn.commit()
                QMessageBox.warning(
                    self.iface.mainWindow(),
                    self.tr(u"Success"),
                    self.tr(u"Database initialized successfully!"))
            except psycopg2.Error as e:
                conn.rollback()
                QMessageBox.warning(
                    self.iface.mainWindow(),
                    self.tr(u"Error"),
                    self.tr(u"Couldn't initialize Database.\n" + e.message))
            conn.close()
            self.enable_disable_gui(selectedLayer)
        else:
            return

    def initialize_layer(self):
        """Use Layer info and run init() .sql query"""
        selectedLayer = self.iface.activeLayer()
        provider = selectedLayer.dataProvider()
        uri = QgsDataSourceURI(provider.dataSourceUri())
        conn = self.dbconn.connect_to_DB(uri)

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

            execute = SQLExecute(self.iface, self.iface.mainWindow(), uri)
            success, msg = execute.Init_hist_tabs(hasGeometry, schema, table)
            if success:
                QMessageBox.warning(
                    self.iface.mainWindow(),
                    self.tr(u"Success"),
                    self.tr(u"Layer successfully initialized!"))
            else:
                QMessageBox.warning(
                    self.iface.mainWindow(),
                    self.tr(u"Error"),
                    self.tr(u"Initialization failed!\n" + msg))
            self.enable_disable_gui(selectedLayer)
        else:
            return

    def show_update_layer_dialog(self):
        """Open ImportUpdate dialog"""
        self.updateDialog = ImportUpdateDialog(self.iface)
        self.updateDialog.show()

    def show_load_layer_dialog(self):
        """Open selectDate dialog"""
        self.dateDialog = SelectDateDialog(self.iface)
        self.dateDialog.show()

    def show_about_dialog(self):
        """Show About dialog"""
        self.aboutDialog = AboutDialog()
        self.aboutDialog.show()

    def enable_disable_gui(self, layer):
        """Enable/Disable menu options based on selected layer"""
        self.actionInitDB.setEnabled(False)
        self.layerMenu.setEnabled(False)
        self.actionInitLayer.setEnabled(False)
        self.actionLayerUpdate.setEnabled(False)
        self.actionLayerLoad.setEnabled(False)

        selectedLayer = self.iface.activeLayer()
        if selectedLayer:
            provider = layer.dataProvider()

            if provider.name() == "postgres":
                self.actionInitDB.setEnabled(True)
                uri = QgsDataSourceURI(provider.dataSourceUri())
                execute = SQLExecute(self.iface, self.iface.mainWindow(), uri)
                historised = execute.check_if_historised(
                    uri.schema(), self.iface.activeLayer().name())
                db_initialized = execute.db_initialize_check(uri.schema())

                if db_initialized:
                    self.actionInitDB.setEnabled(False)
                    self.layerMenu.setEnabled(True)
                else:
                    self.layerMenu.setEnabled(False)

                if historised:
                    self.actionLayerUpdate.setEnabled(True)
                    self.actionLayerLoad.setEnabled(True)
                else:
                    self.actionInitLayer.setEnabled(True)
