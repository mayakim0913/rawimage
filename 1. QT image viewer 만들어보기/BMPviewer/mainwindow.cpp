#include "mainwindow.h"
#include "ui_mainwindow.h"

MainWindow::MainWindow(QWidget *parent) :
QMainWindow(parent),
    ui(new Ui::MainWindow)
{
    ui->setupUi(this);
}

MainWindow::~MainWindow()
{
    delete ui;
}

void MainWindow::on_openButton_pressed()
{
    QString imagepath = QFileDialog::getOpenFileName
            (
                this,
                tr("Open Images"),
                "",
                tr("Images (*.jpg *.jpeg *.png *.bmp *tif)")
                );
    imageObject = new QImage();
    imageObject->load(imagepath);
    image = QPixmap::fromImage(*imageObject);

    scene = new QGraphicsScene(this);
    scene->addPixmap(image);
    scene->setSceneRect(image.rect());
    ui->graphicsView->setScene(scene);
}

void MainWindow::on_saveButton_pressed()
{
    QString imagepath = QFileDialog::getSaveFileName
            (
                this,
                tr("Saves Images"),
                "",
                tr("Images ()") //[Optional ]*.jpg *.jpeg *.png *.bmp *tif
                );
    *imageObject = image.toImage();
    imageObject->save(imagepath);

}

void MainWindow::on_openButton_2_clicked()
{
    QString imagepath2 = QFileDialog::getOpenFileName
            (
                this,
                tr("Open Images"),
                "",
                tr("Images (*.jpg *.jpeg *.png *.bmp *tif)")
                );
    QImage imageobject2(imagepath2);
    QPixmap image2 = QPixmap::fromImage(imageobject2);
    ui->label_img->setPixmap(image2.scaled(150,150,Qt::KeepAspectRatio));
}
