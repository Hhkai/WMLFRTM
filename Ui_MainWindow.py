# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Ui_MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1298, 550)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setTabPosition(QtWidgets.QTabWidget.North)
        self.tabWidget.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.tabWidget.setIconSize(QtCore.QSize(80, 20))
        self.tabWidget.setUsesScrollButtons(True)
        self.tabWidget.setDocumentMode(False)
        self.tabWidget.setTabsClosable(True)
        self.tabWidget.setMovable(False)
        self.tabWidget.setTabBarAutoHide(True)
        self.tabWidget.setObjectName("tabWidget")
        self.widget = QtWidgets.QWidget()
        self.widget.setObjectName("widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.splitter_3 = QtWidgets.QSplitter(self.widget)
        self.splitter_3.setOrientation(QtCore.Qt.Vertical)
        self.splitter_3.setObjectName("splitter_3")
        self.splitter = QtWidgets.QSplitter(self.splitter_3)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.label = QtWidgets.QLabel(self.splitter)
        font = QtGui.QFont()
        font.setFamily("Adobe Devanagari")
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.lineEdit_initLF = QtWidgets.QLineEdit(self.splitter)
        self.lineEdit_initLF.setObjectName("lineEdit_initLF")
        self.chooseButton = QtWidgets.QPushButton(self.splitter)
        self.chooseButton.setObjectName("chooseButton")
        self.searchButton_actions = QtWidgets.QPushButton(self.splitter)
        self.searchButton_actions.setObjectName("searchButton_actions")
        self.searchButton_actions_one_step = QtWidgets.QPushButton(self.splitter)
        self.searchButton_actions_one_step.setObjectName("searchButton_actions_one_step")
        self.textEdit_display_actions = QtWidgets.QTextEdit(self.splitter_3)
        self.textEdit_display_actions.setObjectName("textEdit_display_actions")
        self.verticalLayout.addWidget(self.splitter_3)
        self.tabWidget.addTab(self.widget, "")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.tab)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.splitter_6 = QtWidgets.QSplitter(self.tab)
        self.splitter_6.setOrientation(QtCore.Qt.Vertical)
        self.splitter_6.setObjectName("splitter_6")
        self.splitter_5 = QtWidgets.QSplitter(self.splitter_6)
        self.splitter_5.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_5.setObjectName("splitter_5")
        self.label_4 = QtWidgets.QLabel(self.splitter_5)
        font = QtGui.QFont()
        font.setFamily("Adobe Devanagari")
        font.setPointSize(10)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.lineEdit_input_knowledge = QtWidgets.QLineEdit(self.splitter_5)
        self.lineEdit_input_knowledge.setObjectName("lineEdit_input_knowledge")
        self.searchButton_knowledge = QtWidgets.QPushButton(self.splitter_5)
        self.searchButton_knowledge.setObjectName("searchButton_knowledge")
        self.deleteButton_knowledge = QtWidgets.QPushButton(self.splitter_5)
        self.deleteButton_knowledge.setObjectName("deleteButton_knowledge")
        self.textEdit_display_knowledge = QtWidgets.QTextBrowser(self.splitter_6)
        self.textEdit_display_knowledge.setObjectName("textEdit_display_knowledge")
        self.verticalLayout_2.addWidget(self.splitter_6)
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.tab_2)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.splitter_11 = QtWidgets.QSplitter(self.tab_2)
        self.splitter_11.setOrientation(QtCore.Qt.Vertical)
        self.splitter_11.setObjectName("splitter_11")
        self.frame = QtWidgets.QFrame(self.splitter_11)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.splitter_7 = QtWidgets.QSplitter(self.frame)
        self.splitter_7.setOrientation(QtCore.Qt.Vertical)
        self.splitter_7.setObjectName("splitter_7")
        self.splitter_8 = QtWidgets.QSplitter(self.splitter_7)
        self.splitter_8.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_8.setObjectName("splitter_8")
        self.label_5 = QtWidgets.QLabel(self.splitter_8)
        font = QtGui.QFont()
        font.setFamily("Adobe Devanagari")
        font.setPointSize(10)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.splitter_8)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.splitter_9 = QtWidgets.QSplitter(self.splitter_7)
        self.splitter_9.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_9.setObjectName("splitter_9")
        self.label_6 = QtWidgets.QLabel(self.splitter_9)
        font = QtGui.QFont()
        font.setFamily("Adobe Devanagari")
        font.setPointSize(10)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.lineEdit_3 = QtWidgets.QLineEdit(self.splitter_9)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.splitter_10 = QtWidgets.QSplitter(self.splitter_7)
        self.splitter_10.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_10.setObjectName("splitter_10")
        self.label_7 = QtWidgets.QLabel(self.splitter_10)
        font = QtGui.QFont()
        font.setFamily("Adobe Devanagari")
        font.setPointSize(10)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.lineEdit_4 = QtWidgets.QLineEdit(self.splitter_10)
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.horizontalLayout_2.addWidget(self.splitter_7)
        self.AddButton_knowledge = QtWidgets.QPushButton(self.frame)
        self.AddButton_knowledge.setObjectName("AddButton_knowledge")
        self.horizontalLayout_2.addWidget(self.AddButton_knowledge)
        self.horizontalLayout_2.setStretch(0, 5)
        self.horizontalLayout_2.setStretch(1, 1)
        self.textEdit = QtWidgets.QTextEdit(self.splitter_11)
        self.textEdit.setObjectName("textEdit")
        self.verticalLayout_3.addWidget(self.splitter_11)
        self.tabWidget.addTab(self.tab_2, "")
        self.horizontalLayout.addWidget(self.tabWidget)
        self.splitter_4 = QtWidgets.QSplitter(self.centralwidget)
        self.splitter_4.setOrientation(QtCore.Qt.Vertical)
        self.splitter_4.setObjectName("splitter_4")
        self.label_graph = QtWidgets.QLabel(self.splitter_4)
        self.label_graph.setText("")
        self.label_graph.setObjectName("label_graph")
        self.splitter_2 = QtWidgets.QSplitter(self.splitter_4)
        self.splitter_2.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_2.setObjectName("splitter_2")
        self.pushButton = QtWidgets.QPushButton(self.splitter_2)
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.splitter_2)
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(self.splitter_2)
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_4 = QtWidgets.QPushButton(self.splitter_2)
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_5 = QtWidgets.QPushButton(self.splitter_2)
        self.pushButton_5.setObjectName("pushButton_5")
        self.horizontalLayout.addWidget(self.splitter_4)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(2)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">潮流初始状态：</p></body></html>"))
        self.chooseButton.setText(_translate("MainWindow", "选择文件夹"))
        self.searchButton_actions.setText(_translate("MainWindow", "多步调整"))
        self.searchButton_actions_one_step.setText(_translate("MainWindow", "单步调整"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.widget), _translate("MainWindow", "潮流收敛调整"))
        self.label_4.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">输入知识：</p></body></html>"))
        self.searchButton_knowledge.setText(_translate("MainWindow", "查询"))
        self.deleteButton_knowledge.setText(_translate("MainWindow", "删除"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "查询知识"))
        self.label_5.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">状态1\\实体1：</p></body></html>"))
        self.label_6.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">操作 \\关系 ：</p></body></html>"))
        self.label_7.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">状态2\\实体2：</p></body></html>"))
        self.AddButton_knowledge.setText(_translate("MainWindow", "\n"
"添加\n"
""))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "添加知识"))
        self.pushButton.setText(_translate("MainWindow", ""))
        self.pushButton_2.setText(_translate("MainWindow", ""))
        self.pushButton_3.setText(_translate("MainWindow", ""))
        self.pushButton_4.setText(_translate("MainWindow", ""))
        self.pushButton_5.setText(_translate("MainWindow", ""))
