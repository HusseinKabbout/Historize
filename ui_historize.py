# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'historize.ui'
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

class Ui_Historize(object):
    def setupUi(self, Historize):
        Historize.setObjectName(_fromUtf8("Historize"))
        Historize.setEnabled(True)
        Historize.resize(585, 338)
        self.gridLayout_4 = QtGui.QGridLayout(Historize)
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.gridLayout_4.addLayout(self.horizontalLayout_3, 0, 0, 1, 1)
        self.tabDoc = QtGui.QTabWidget(Historize)
        self.tabDoc.setObjectName(_fromUtf8("tabDoc"))
        self.lyrTab = QtGui.QWidget()
        self.lyrTab.setObjectName(_fromUtf8("lyrTab"))
        self.gridLayout_5 = QtGui.QGridLayout(self.lyrTab)
        self.gridLayout_5.setObjectName(_fromUtf8("gridLayout_5"))
        self.boxNonHistoLyr = QtGui.QGroupBox(self.lyrTab)
        self.boxNonHistoLyr.setObjectName(_fromUtf8("boxNonHistoLyr"))
        self.gridLayout_2 = QtGui.QGridLayout(self.boxNonHistoLyr)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.lyrLabel_1 = QtGui.QLabel(self.boxNonHistoLyr)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lyrLabel_1.sizePolicy().hasHeightForWidth())
        self.lyrLabel_1.setSizePolicy(sizePolicy)
        self.lyrLabel_1.setObjectName(_fromUtf8("lyrLabel_1"))
        self.gridLayout_2.addWidget(self.lyrLabel_1, 0, 0, 1, 1)
        self.checkNonHistoGeom = QtGui.QCheckBox(self.boxNonHistoLyr)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.checkNonHistoGeom.sizePolicy().hasHeightForWidth())
        self.checkNonHistoGeom.setSizePolicy(sizePolicy)
        self.checkNonHistoGeom.setObjectName(_fromUtf8("checkNonHistoGeom"))
        self.gridLayout_2.addWidget(self.checkNonHistoGeom, 1, 2, 1, 1, QtCore.Qt.AlignRight)
        self.cmbNonHistoLyr = QtGui.QComboBox(self.boxNonHistoLyr)
        self.cmbNonHistoLyr.setObjectName(_fromUtf8("cmbNonHistoLyr"))
        self.gridLayout_2.addWidget(self.cmbNonHistoLyr, 0, 1, 1, 2)
        self.btnHistoLyr = QtGui.QPushButton(self.boxNonHistoLyr)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnHistoLyr.sizePolicy().hasHeightForWidth())
        self.btnHistoLyr.setSizePolicy(sizePolicy)
        self.btnHistoLyr.setObjectName(_fromUtf8("btnHistoLyr"))
        self.gridLayout_2.addWidget(self.btnHistoLyr, 1, 1, 1, 1)
        self.lyrLabel_1.raise_()
        self.cmbNonHistoLyr.raise_()
        self.btnHistoLyr.raise_()
        self.checkNonHistoGeom.raise_()
        self.gridLayout_5.addWidget(self.boxNonHistoLyr, 0, 0, 1, 1)
        self.boxHistoLyr = QtGui.QGroupBox(self.lyrTab)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.boxHistoLyr.sizePolicy().hasHeightForWidth())
        self.boxHistoLyr.setSizePolicy(sizePolicy)
        self.boxHistoLyr.setObjectName(_fromUtf8("boxHistoLyr"))
        self.gridLayout_3 = QtGui.QGridLayout(self.boxHistoLyr)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.lyrLabel_2 = QtGui.QLabel(self.boxHistoLyr)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lyrLabel_2.sizePolicy().hasHeightForWidth())
        self.lyrLabel_2.setSizePolicy(sizePolicy)
        self.lyrLabel_2.setObjectName(_fromUtf8("lyrLabel_2"))
        self.gridLayout_3.addWidget(self.lyrLabel_2, 0, 0, 1, 1)
        self.btnLoadHistoLyr = QtGui.QPushButton(self.boxHistoLyr)
        self.btnLoadHistoLyr.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnLoadHistoLyr.sizePolicy().hasHeightForWidth())
        self.btnLoadHistoLyr.setSizePolicy(sizePolicy)
        self.btnLoadHistoLyr.setObjectName(_fromUtf8("btnLoadHistoLyr"))
        self.gridLayout_3.addWidget(self.btnLoadHistoLyr, 1, 1, 1, 1)
        self.btnUpdateHistoLyr = QtGui.QPushButton(self.boxHistoLyr)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnUpdateHistoLyr.sizePolicy().hasHeightForWidth())
        self.btnUpdateHistoLyr.setSizePolicy(sizePolicy)
        self.btnUpdateHistoLyr.setObjectName(_fromUtf8("btnUpdateHistoLyr"))
        self.gridLayout_3.addWidget(self.btnUpdateHistoLyr, 1, 2, 1, 1)
        self.checkHistoGeom = QtGui.QCheckBox(self.boxHistoLyr)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.checkHistoGeom.sizePolicy().hasHeightForWidth())
        self.checkHistoGeom.setSizePolicy(sizePolicy)
        self.checkHistoGeom.setObjectName(_fromUtf8("checkHistoGeom"))
        self.gridLayout_3.addWidget(self.checkHistoGeom, 1, 3, 1, 1, QtCore.Qt.AlignRight)
        self.cmbHistoLyr = QtGui.QComboBox(self.boxHistoLyr)
        self.cmbHistoLyr.setObjectName(_fromUtf8("cmbHistoLyr"))
        self.gridLayout_3.addWidget(self.cmbHistoLyr, 0, 1, 1, 3)
        self.gridLayout_5.addWidget(self.boxHistoLyr, 1, 0, 1, 1)
        self.tabDoc.addTab(self.lyrTab, _fromUtf8(""))
        self.dbTab = QtGui.QWidget()
        self.dbTab.setObjectName(_fromUtf8("dbTab"))
        self.gridLayout_6 = QtGui.QGridLayout(self.dbTab)
        self.gridLayout_6.setObjectName(_fromUtf8("gridLayout_6"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.dbLabel = QtGui.QLabel(self.dbTab)
        self.dbLabel.setObjectName(_fromUtf8("dbLabel"))
        self.gridLayout.addWidget(self.dbLabel, 0, 0, 1, 2)
        self.lneDatabase = QtGui.QLineEdit(self.dbTab)
        self.lneDatabase.setObjectName(_fromUtf8("lneDatabase"))
        self.gridLayout.addWidget(self.lneDatabase, 0, 3, 1, 1)
        self.hostLabel = QtGui.QLabel(self.dbTab)
        self.hostLabel.setObjectName(_fromUtf8("hostLabel"))
        self.gridLayout.addWidget(self.hostLabel, 1, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 1, 1, 1, 2)
        self.lneHost = QtGui.QLineEdit(self.dbTab)
        self.lneHost.setObjectName(_fromUtf8("lneHost"))
        self.gridLayout.addWidget(self.lneHost, 1, 3, 1, 1)
        self.portLabel = QtGui.QLabel(self.dbTab)
        self.portLabel.setObjectName(_fromUtf8("portLabel"))
        self.gridLayout.addWidget(self.portLabel, 2, 0, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 2, 1, 1, 2)
        self.lnePort = QtGui.QLineEdit(self.dbTab)
        self.lnePort.setObjectName(_fromUtf8("lnePort"))
        self.gridLayout.addWidget(self.lnePort, 2, 3, 1, 1)
        self.userLabel = QtGui.QLabel(self.dbTab)
        self.userLabel.setObjectName(_fromUtf8("userLabel"))
        self.gridLayout.addWidget(self.userLabel, 3, 0, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem2, 3, 1, 1, 2)
        self.lneUser = QtGui.QLineEdit(self.dbTab)
        self.lneUser.setObjectName(_fromUtf8("lneUser"))
        self.gridLayout.addWidget(self.lneUser, 3, 3, 1, 1)
        self.pswdLabel = QtGui.QLabel(self.dbTab)
        self.pswdLabel.setObjectName(_fromUtf8("pswdLabel"))
        self.gridLayout.addWidget(self.pswdLabel, 4, 0, 1, 2)
        self.lnePassword = QtGui.QLineEdit(self.dbTab)
        self.lnePassword.setObjectName(_fromUtf8("lnePassword"))
        self.gridLayout.addWidget(self.lnePassword, 4, 3, 1, 1)
        self.gridLayout_6.addLayout(self.gridLayout, 0, 0, 1, 3)
        self.btnHistoInstall = QtGui.QPushButton(self.dbTab)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnHistoInstall.sizePolicy().hasHeightForWidth())
        self.btnHistoInstall.setSizePolicy(sizePolicy)
        self.btnHistoInstall.setObjectName(_fromUtf8("btnHistoInstall"))
        self.gridLayout_6.addWidget(self.btnHistoInstall, 1, 0, 1, 1)
        self.btnTestConn = QtGui.QPushButton(self.dbTab)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnTestConn.sizePolicy().hasHeightForWidth())
        self.btnTestConn.setSizePolicy(sizePolicy)
        self.btnTestConn.setObjectName(_fromUtf8("btnTestConn"))
        self.gridLayout_6.addWidget(self.btnTestConn, 1, 2, 1, 1)
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_6.addItem(spacerItem3, 1, 1, 1, 1)
        self.tabDoc.addTab(self.dbTab, _fromUtf8(""))
        self.tabDoc1 = QtGui.QWidget()
        self.tabDoc1.setObjectName(_fromUtf8("tabDoc1"))
        self.gridLayout_7 = QtGui.QGridLayout(self.tabDoc1)
        self.gridLayout_7.setObjectName(_fromUtf8("gridLayout_7"))
        self.textBrowser = QtGui.QTextBrowser(self.tabDoc1)
        self.textBrowser.setObjectName(_fromUtf8("textBrowser"))
        self.gridLayout_7.addWidget(self.textBrowser, 0, 0, 1, 1)
        self.tabDoc.addTab(self.tabDoc1, _fromUtf8(""))
        self.gridLayout_4.addWidget(self.tabDoc, 1, 0, 1, 2)
        self.buttonBox = QtGui.QDialogButtonBox(Historize)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout_4.addWidget(self.buttonBox, 2, 1, 1, 1)
        self.layoutWidget = QtGui.QWidget(Historize)
        self.layoutWidget.setGeometry(QtCore.QRect(0, 0, 2, 2))
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.layoutWidget)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))

        self.retranslateUi(Historize)
        self.tabDoc.setCurrentIndex(0)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Historize.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Historize.reject)
        QtCore.QMetaObject.connectSlotsByName(Historize)

    def retranslateUi(self, Historize):
        Historize.setWindowTitle(_translate("Historize", "Historize", None))
        self.boxNonHistoLyr.setTitle(_translate("Historize", "Non-Historized Layers", None))
        self.lyrLabel_1.setText(_translate("Historize", "Select Layer:", None))
        self.checkNonHistoGeom.setText(_translate("Historize", "Has Geometry", None))
        self.btnHistoLyr.setText(_translate("Historize", "Historize", None))
        self.boxHistoLyr.setTitle(_translate("Historize", "Historized Layers", None))
        self.lyrLabel_2.setText(_translate("Historize", "Select Layer:", None))
        self.btnLoadHistoLyr.setText(_translate("Historize", "Load", None))
        self.btnUpdateHistoLyr.setText(_translate("Historize", "Update", None))
        self.checkHistoGeom.setText(_translate("Historize", "Has Geometry", None))
        self.tabDoc.setTabText(self.tabDoc.indexOf(self.lyrTab), _translate("Historize", "Layer", None))
        self.dbLabel.setText(_translate("Historize", "Database:", None))
        self.hostLabel.setText(_translate("Historize", "Host:", None))
        self.portLabel.setText(_translate("Historize", "Port:", None))
        self.userLabel.setText(_translate("Historize", "User:", None))
        self.pswdLabel.setText(_translate("Historize", "Password:", None))
        self.btnHistoInstall.setText(_translate("Historize", "Install Historisation", None))
        self.btnTestConn.setText(_translate("Historize", "Test Connection", None))
        self.tabDoc.setTabText(self.tabDoc.indexOf(self.dbTab), _translate("Historize", "Database", None))
        self.tabDoc.setTabText(self.tabDoc.indexOf(self.tabDoc1), _translate("Historize", "Documentation", None))

