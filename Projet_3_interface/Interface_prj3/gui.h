#ifndef GUI_H
#define GUI_H

#include <QDialog>

namespace Ui {
class GUI;
}

class GUI : public QDialog
{
    Q_OBJECT

public:
    explicit GUI(QWidget *parent = 0);
    ~GUI();

private:
    Ui::GUI *ui;
};

#endif // GUI_H
