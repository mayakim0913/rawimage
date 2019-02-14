#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>

#include <QFileDialog>
#include <QLabel>
#include <QImage>
#include <QPixmap>
#include <QApplication>

#include <QGraphicsScene>
#include <QGraphicsView>


namespace Ui {
class MainWindow;
}

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    explicit MainWindow(QWidget *parent = nullptr);
    ~MainWindow();

private slots:
    void on_openButton_pressed();
    void on_saveButton_pressed();
    void on_openButton_2_clicked();

private:
    Ui::MainWindow *ui;
    QPixmap image;
    QImage *imageObject;
    QGraphicsScene *scene;
};

#endif // MAINWINDOW_H
