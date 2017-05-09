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

class Ui_Load(object):
    def setupUi(self, Load):
        Load.setObjectName(_fromUtf8("Load"))
        Load.resize(388, 139)
        self.buttonBox = QtGui.QDialogButtonBox(Load)
        self.buttonBox.setGeometry(QtCore.QRect(40, 100, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.dateBox = QtGui.QGroupBox(Load)
        self.dateBox.setGeometry(QtCore.QRect(10, 10, 371, 91))
        self.dateBox.setObjectName(_fromUtf8("dateBox"))
        self.gridLayout = QtGui.QGridLayout(self.dateBox)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.cmbDate = QtGui.QComboBox(self.dateBox)
        self.cmbDate.setObjectName(_fromUtf8("cmbDate"))
        self.gridLayout.addWidget(self.cmbDate, 0, 0, 1, 1)
        self.dateBox.raise_()
        self.buttonBox.raise_()

        self.retranslateUi(Load)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Load.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Load.reject)
        QtCore.QMetaObject.connectSlotsByName(Load)

    def retranslateUi(self, Load):
        Load.setWindowTitle(_translate("Load", "Load", None))
        self.dateBox.setTitle(_translate("Load", "Select Date", None))

