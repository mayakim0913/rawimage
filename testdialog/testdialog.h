#ifndef TESTDIALOG_H
#define TESTDIALOG_H

#include <QDialog>
#include "ui_testdialog.h"

class QButtonGroup;

class TestDialog : public QDialog {
	Q_OBJECT
public:
	enum Color {RGB = 0, CMYK, YUV};
	TestDialog();
private slots:
	void setColorChecked(int id);
private:
	Ui::TestDialog ui;
	QButtonGroup *buttons;
};

#endif
