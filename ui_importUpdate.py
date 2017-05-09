# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'importUpdate.ui'
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
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(438, 348)
        self.verticalLayout = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.groupBox = QtGui.QGroupBox(Dialog)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.gridLayout = QtGui.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.splitter = QtGui.QSplitter(self.groupBox)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.tableLabel = QtGui.QLabel(self.splitter)
        self.tableLabel.setObjectName(_fromUtf8("tableLabel"))
        self.cmbImportTable = QtGui.QComboBox(self.splitter)
        self.cmbImportTable.setObjectName(_fromUtf8("cmbImportTable"))
        self.gridLayout.addWidget(self.splitter, 0, 0, 1, 1)
        self.checkBox = QtGui.QCheckBox(self.groupBox)
        self.checkBox.setObjectName(_fromUtf8("checkBox"))
        self.gridLayout.addWidget(self.checkBox, 1, 0, 1, 1, QtCore.Qt.AlignRight)
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.attribLabel = QtGui.QLabel(self.groupBox)
        self.attribLabel.setObjectName(_fromUtf8("attribLabel"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.attribLabel)
        self.listTblAttrib = QtGui.QListView(self.groupBox)
        self.listTblAttrib.setObjectName(_fromUtf8("listTblAttrib"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.listTblAttrib)
        self.gridLayout.addLayout(self.formLayout, 2, 0, 1, 1)
        self.verticalLayout.addWidget(self.groupBox)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.groupBox.setTitle(_translate("Dialog", "Import Table Data", None))
        self.tableLabel.setText(_translate("Dialog", "Table:", None))
        self.checkBox.setText(_translate("Dialog", "Has Geometry", None))
        self.attribLabel.setText(_translate("Dialog", "Exclude Attributes:", None))
