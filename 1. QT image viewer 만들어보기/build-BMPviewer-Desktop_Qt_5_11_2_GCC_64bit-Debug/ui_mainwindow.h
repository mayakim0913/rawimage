/********************************************************************************
** Form generated from reading UI file 'mainwindow.ui'
**
** Created by: Qt User Interface Compiler version 5.11.2
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_MAINWINDOW_H
#define UI_MAINWINDOW_H

#include <QtCore/QVariant>
#include <QtWidgets/QApplication>
#include <QtWidgets/QGraphicsView>
#include <QtWidgets/QLabel>
#include <QtWidgets/QMainWindow>
#include <QtWidgets/QMenuBar>
#include <QtWidgets/QPushButton>
#include <QtWidgets/QSplitter>
#include <QtWidgets/QStatusBar>
#include <QtWidgets/QToolBar>
#include <QtWidgets/QWidget>

QT_BEGIN_NAMESPACE

class Ui_MainWindow
{
public:
    QWidget *centralWidget;
    QGraphicsView *graphicsView;
    QLabel *label_img;
    QLabel *label_name1;
    QLabel *label_name2;
    QPushButton *openButton_2;
    QSplitter *splitter;
    QPushButton *openButton;
    QPushButton *saveButton;
    QMenuBar *menuBar;
    QToolBar *mainToolBar;
    QStatusBar *statusBar;

    void setupUi(QMainWindow *MainWindow)
    {
        if (MainWindow->objectName().isEmpty())
            MainWindow->setObjectName(QStringLiteral("MainWindow"));
        MainWindow->resize(400, 300);
        centralWidget = new QWidget(MainWindow);
        centralWidget->setObjectName(QStringLiteral("centralWidget"));
        graphicsView = new QGraphicsView(centralWidget);
        graphicsView->setObjectName(QStringLiteral("graphicsView"));
        graphicsView->setGeometry(QRect(31, 11, 159, 111));
        label_img = new QLabel(centralWidget);
        label_img->setObjectName(QStringLiteral("label_img"));
        label_img->setGeometry(QRect(31, 145, 159, 81));
        label_name1 = new QLabel(centralWidget);
        label_name1->setObjectName(QStringLiteral("label_name1"));
        label_name1->setGeometry(QRect(200, 10, 111, 20));
        label_name2 = new QLabel(centralWidget);
        label_name2->setObjectName(QStringLiteral("label_name2"));
        label_name2->setGeometry(QRect(200, 140, 111, 20));
        openButton_2 = new QPushButton(centralWidget);
        openButton_2->setObjectName(QStringLiteral("openButton_2"));
        openButton_2->setGeometry(QRect(260, 170, 89, 25));
        splitter = new QSplitter(centralWidget);
        splitter->setObjectName(QStringLiteral("splitter"));
        splitter->setGeometry(QRect(260, 40, 89, 50));
        splitter->setOrientation(Qt::Vertical);
        openButton = new QPushButton(splitter);
        openButton->setObjectName(QStringLiteral("openButton"));
        splitter->addWidget(openButton);
        saveButton = new QPushButton(splitter);
        saveButton->setObjectName(QStringLiteral("saveButton"));
        splitter->addWidget(saveButton);
        MainWindow->setCentralWidget(centralWidget);
        menuBar = new QMenuBar(MainWindow);
        menuBar->setObjectName(QStringLiteral("menuBar"));
        menuBar->setGeometry(QRect(0, 0, 400, 22));
        MainWindow->setMenuBar(menuBar);
        mainToolBar = new QToolBar(MainWindow);
        mainToolBar->setObjectName(QStringLiteral("mainToolBar"));
        MainWindow->addToolBar(Qt::TopToolBarArea, mainToolBar);
        statusBar = new QStatusBar(MainWindow);
        statusBar->setObjectName(QStringLiteral("statusBar"));
        MainWindow->setStatusBar(statusBar);

        retranslateUi(MainWindow);

        QMetaObject::connectSlotsByName(MainWindow);
    } // setupUi

    void retranslateUi(QMainWindow *MainWindow)
    {
        MainWindow->setWindowTitle(QApplication::translate("MainWindow", "MainWindow", nullptr));
        label_img->setText(QString());
        label_name1->setText(QApplication::translate("MainWindow", "<1. QGraphics>", nullptr));
        label_name2->setText(QApplication::translate("MainWindow", "<2. QPixmap>", nullptr));
        openButton_2->setText(QApplication::translate("MainWindow", "Open", nullptr));
        openButton->setText(QApplication::translate("MainWindow", "Open", nullptr));
        saveButton->setText(QApplication::translate("MainWindow", "Save", nullptr));
    } // retranslateUi

};

namespace Ui {
    class MainWindow: public Ui_MainWindow {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_MAINWINDOW_H
