# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/importUpdate.ui'
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

class Ui_ImportUpdate(object):
    def setupUi(self, ImportUpdate):
        ImportUpdate.setObjectName(_fromUtf8("ImportUpdate"))
        ImportUpdate.resize(416, 354)
        self.gridLayout_2 = QtGui.QGridLayout(ImportUpdate)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.groupBox = QtGui.QGroupBox(ImportUpdate)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.gridLayout = QtGui.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.splitter = QtGui.QSplitter(self.groupBox)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.tableLabel = QtGui.QLabel(self.splitter)
        self.tableLabel.setObjectName(_fromUtf8("tableLabel"))
        self.cmbImportTable = QtGui.QComboBox(self.splitter)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cmbImportTable.sizePolicy().hasHeightForWidth())
        self.cmbImportTable.setSizePolicy(sizePolicy)
        self.cmbImportTable.setObjectName(_fromUtf8("cmbImportTable"))
        self.gridLayout.addWidget(self.splitter, 0, 0, 1, 1)
        self.gridLayout_3 = QtGui.QGridLayout()
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.attribLabel = QtGui.QLabel(self.groupBox)
        self.attribLabel.setObjectName(_fromUtf8("attribLabel"))
        self.gridLayout_3.addWidget(self.attribLabel, 0, 0, 1, 1, QtCore.Qt.AlignTop)
        self.listTblAttrib = QtGui.QListView(self.groupBox)
        self.listTblAttrib.setObjectName(_fromUtf8("listTblAttrib"))
        self.gridLayout_3.addWidget(self.listTblAttrib, 0, 1, 1, 1)
        self.gridLayout.addLayout(self.gridLayout_3, 1, 0, 1, 1)
        self.gridLayout_2.addWidget(self.groupBox, 0, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(ImportUpdate)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout_2.addWidget(self.buttonBox, 1, 0, 1, 1)

        self.retranslateUi(ImportUpdate)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), ImportUpdate.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), ImportUpdate.reject)
        QtCore.QMetaObject.connectSlotsByName(ImportUpdate)

    def retranslateUi(self, ImportUpdate):
        ImportUpdate.setWindowTitle(_translate("ImportUpdate", "Update Table", None))
        self.groupBox.setTitle(_translate("ImportUpdate", "Import Table Data", None))
        self.tableLabel.setText(_translate("ImportUpdate", "Table:", None))
        self.attribLabel.setText(_translate("ImportUpdate", "Exclude Attributes:", None))

