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
# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'selectDate.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_SelectDate(object):
    def setupUi(self, SelectDate):
        SelectDate.setObjectName(_fromUtf8("SelectDate"))
        SelectDate.resize(393, 131)
        self.gridLayout_2 = QtGui.QGridLayout(SelectDate)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.dateBox = QtGui.QGroupBox(SelectDate)
        self.dateBox.setObjectName(_fromUtf8("dateBox"))
        self.gridLayout = QtGui.QGridLayout(self.dateBox)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.cmbDate = QtGui.QComboBox(self.dateBox)
        self.cmbDate.setObjectName(_fromUtf8("cmbDate"))
        self.gridLayout.addWidget(self.cmbDate, 0, 0, 1, 1)
        self.gridLayout_2.addWidget(self.dateBox, 0, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(SelectDate)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout_2.addWidget(self.buttonBox, 1, 0, 1, 1)
        self.dateBox.raise_()
        self.buttonBox.raise_()

        self.retranslateUi(SelectDate)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), SelectDate.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), SelectDate.reject)
        QtCore.QMetaObject.connectSlotsByName(SelectDate)

    def retranslateUi(self, SelectDate):
        SelectDate.setWindowTitle(_translate("SelectDate", "Load", None))
        self.dateBox.setTitle(_translate("SelectDate", "Select Date", None))
