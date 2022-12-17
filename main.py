from sys import argv
from PyQt5.QtWidgets import QApplication
from gui import ApplicationForm

def main():
    app = QApplication(argv)
    form = ApplicationForm()

    form.on_date_changed()
    form.on_refresh_btn_clicked()

    form.show()
    app.exec_()


if __name__ == '__main__':
    main()
    