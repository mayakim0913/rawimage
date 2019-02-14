#include <QButtonGroup>
#include "testdialog.h"

TestDialog::TestDialog() {
	ui.setupUi(this);
	buttons = new QButtonGroup(this);
	buttons->addButton(ui.rgb_radio, RGB);
	buttons->addButton(ui.cmyk_radio, CMYK);
	buttons->addButton(ui.yuv_radio, YUV);
	connect(buttons, SIGNAL(buttonClicked(int)), ui.color_combo, SLOT(setCurrentIndex(int)));
	connect(ui.color_combo, SIGNAL(currentIndexChanged(int)), this, SLOT(setColorChecked(int)));
}

void TestDialog::setColorChecked(int id) {
	buttons->button(id)->setChecked(true);
}
