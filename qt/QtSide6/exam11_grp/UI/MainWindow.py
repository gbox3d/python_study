# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MainWindow.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QMainWindow, QMenu, QMenuBar,
    QSizePolicy, QStatusBar, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(530, 462)
        self.actionclear = QAction(MainWindow)
        self.actionclear.setObjectName(u"actionclear")
        self.actionload = QAction(MainWindow)
        self.actionload.setObjectName(u"actionload")
        self.actionsave = QAction(MainWindow)
        self.actionsave.setObjectName(u"actionsave")
        self.actionitem1 = QAction(MainWindow)
        self.actionitem1.setObjectName(u"actionitem1")
        self.actionline = QAction(MainWindow)
        self.actionline.setObjectName(u"actionline")
        self.actionrect = QAction(MainWindow)
        self.actionrect.setObjectName(u"actionrect")
        self.actionimage = QAction(MainWindow)
        self.actionimage.setObjectName(u"actionimage")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 530, 24))
        self.menuhome = QMenu(self.menubar)
        self.menuhome.setObjectName(u"menuhome")
        self.menucommand = QMenu(self.menubar)
        self.menucommand.setObjectName(u"menucommand")
        self.menugrapics = QMenu(self.menubar)
        self.menugrapics.setObjectName(u"menugrapics")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuhome.menuAction())
        self.menubar.addAction(self.menucommand.menuAction())
        self.menubar.addAction(self.menugrapics.menuAction())
        self.menuhome.addAction(self.actionitem1)
        self.menucommand.addAction(self.actionclear)
        self.menucommand.addAction(self.actionload)
        self.menucommand.addAction(self.actionsave)
        self.menugrapics.addAction(self.actionline)
        self.menugrapics.addAction(self.actionrect)
        self.menugrapics.addAction(self.actionimage)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionclear.setText(QCoreApplication.translate("MainWindow", u"clear", None))
        self.actionload.setText(QCoreApplication.translate("MainWindow", u"load", None))
        self.actionsave.setText(QCoreApplication.translate("MainWindow", u"save", None))
        self.actionitem1.setText(QCoreApplication.translate("MainWindow", u"item1", None))
        self.actionline.setText(QCoreApplication.translate("MainWindow", u"line", None))
        self.actionrect.setText(QCoreApplication.translate("MainWindow", u"rect", None))
        self.actionimage.setText(QCoreApplication.translate("MainWindow", u"image", None))
        self.menuhome.setTitle(QCoreApplication.translate("MainWindow", u"home", None))
        self.menucommand.setTitle(QCoreApplication.translate("MainWindow", u"command", None))
        self.menugrapics.setTitle(QCoreApplication.translate("MainWindow", u"grapics", None))
    # retranslateUi

