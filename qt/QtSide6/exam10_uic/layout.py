# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'layout.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QLabel, QPushButton, QSizePolicy,
    QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(610, 474)
        self.btnTest = QPushButton(Form)
        self.btnTest.setObjectName(u"btnTest")
        self.btnTest.setGeometry(QRect(90, 100, 100, 32))
        self.lbTest = QLabel(Form)
        self.lbTest.setObjectName(u"lbTest")
        self.lbTest.setGeometry(QRect(160, 30, 241, 21))

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.btnTest.setText(QCoreApplication.translate("Form", u"Test", None))
        self.lbTest.setText(QCoreApplication.translate("Form", u"TextLabel", None))
    # retranslateUi

