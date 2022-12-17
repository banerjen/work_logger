import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from constants import Constants
from daily_log import DailyLog
from todo_and_misc import TodoAndMisc

import datetime


class ApplicationForm(QMainWindow):
    def __init__(self, parent=None):
        self.load_data()
        QMainWindow.__init__(self, parent)
        self.setWindowTitle(Constants.PROGRAM_NAME)
        self.main_frame = QWidget()
        self.populate_main_frame()
        self.setCentralWidget(self.main_frame)

    def load_data(self):
        self.daily_log = DailyLog()
        self.todo_and_misc = TodoAndMisc()
        self.daily_log.load_daily_log_from_file()
        self.todo_and_misc.load_todo_from_file()
        self.todo_and_misc.load_misc_from_file()
        self.prev_date = None

    def populate_main_frame(self):
        self.main_frame.setMinimumHeight(800)
        self.main_frame.setMinimumWidth(1300)

        self.create_update_and_refresh_buttons()
        self.create_calendar()
        self.create_daily_log_box()
        self.create_todo_box()
        self.create_misc_box()

        vwidget_1 = QWidget()
        vbox_1 = QVBoxLayout(vwidget_1)
        vbox_1.addWidget(self.update_refresh_widget)
        vbox_1.addWidget(self.calendar_widget)
        vbox_1.addWidget(self.daily_log_group_box)

        vwidget_2 = QWidget()
        vbox_2 = QVBoxLayout(vwidget_2)
        vbox_2.addWidget(self.todo_group_box)
        vbox_2.addWidget(self.misc_group_box)

        hwidget = QWidget()
        hbox = QHBoxLayout(hwidget)
        hbox.addWidget(vwidget_1)
        hbox.addWidget(vwidget_2)

        vbox = QVBoxLayout()
        vbox.addWidget(hwidget)
        self.notification_label = QLabel(Constants.PROGRAM_NAME)
        self.notification_label.setFixedHeight(40)
        self.notification_label.setStyleSheet('font-size: 24px;')
        vbox.addWidget(self.notification_label)

        self.main_frame.setLayout(vbox)

    ################## CALLBACKS ##################
    def on_date_changed(self):
        # PyDate format : yyyy-mm-dd
        if self.prev_date:
            self.daily_log.set_log(self.prev_date, self.daily_log_text_edit.toPlainText())

        selected_date = self.calendar_widget.selectedDate().toString()
        self.prev_date = selected_date
        self.daily_log_text_edit.setText(self.daily_log.get_log(selected_date))

    def on_update_btn_clicked(self):
        selected_date = self.calendar_widget.selectedDate().toString()
        self.daily_log.set_log(selected_date, self.daily_log_text_edit.toPlainText())
        self.daily_log.save_daily_log_to_file()

        self.todo_and_misc.set_todo(self.todo_text_edit.toPlainText())
        self.todo_and_misc.set_misc(self.misc_text_edit.toPlainText())
        self.todo_and_misc.save_todo_to_file()
        self.todo_and_misc.save_misc_to_file()

        self.notification_label.setText(Constants.PROGRAM_NAME + ' : ' \
            + str(Constants.UPDATE_NOTIFICATION_LBL) + datetime.datetime.now().strftime("%m/%d/%Y, %I:%M %p") + '.')

    def on_refresh_btn_clicked(self):
        self.daily_log.load_daily_log_from_file()
        self.todo_and_misc.load_todo_from_file()
        self.todo_and_misc.load_misc_from_file()

        self.prev_date = None
        self.on_date_changed()
        self.todo_text_edit.setText(self.todo_and_misc.get_todo())
        self.misc_text_edit.setText(self.todo_and_misc.get_misc())

        self.notification_label.setText(Constants.PROGRAM_NAME + ' : ' +\
            str(Constants.REFRESH_NOTIFICATION_LBL) +  datetime.datetime.now().strftime("%m/%d/%Y, %I:%M %p") + '.')

    ################## CREATE OBJECTS ##################
    def create_update_and_refresh_buttons(self):
        self.refresh_btn = QPushButton(Constants.REFRESH_BTN_LBL)
        self.update_btn = QPushButton(Constants.UPDATE_BTN_LBL)
        self.refresh_btn.clicked.connect(self.on_refresh_btn_clicked)
        self.update_btn.clicked.connect(self.on_update_btn_clicked)

        self.update_refresh_widget = QWidget()
        hbox = QHBoxLayout(self.update_refresh_widget)
        hbox.addWidget(self.refresh_btn)
        hbox.addWidget(self.update_btn)
        self.update_refresh_widget.setFixedHeight(50)

    def create_calendar(self):
        self.calendar_widget = QCalendarWidget()
        self.calendar_widget.showToday()
        self.calendar_widget.selectionChanged.connect(self.on_date_changed)
        self.calendar_widget.setMinimumHeight(200)
        self.calendar_widget.setMinimumWidth(400)

    def create_daily_log_box(self):
        self.daily_log_group_box = QGroupBox(Constants.DAILY_LOG_LBL)
        daily_log_layout = QVBoxLayout()

        self.daily_log_text_edit = QTextEdit()
        self.daily_log_text_edit.setTabChangesFocus(True)

        daily_log_layout.addWidget(self.daily_log_text_edit)

        self.daily_log_group_box.setLayout(daily_log_layout)
        self.daily_log_group_box.setMinimumHeight(300)
        self.daily_log_group_box.setMinimumWidth(600)

    def create_todo_box(self):
        self.todo_group_box = QGroupBox(Constants.TODO_LBL)
        todo_layout = QVBoxLayout()

        self.todo_text_edit = QTextEdit()
        self.todo_text_edit.setTabChangesFocus(True)

        todo_layout.addWidget(self.todo_text_edit)

        self.todo_group_box.setLayout(todo_layout)
        self.todo_group_box.setMinimumHeight(300)
        self.todo_group_box.setMinimumWidth(600)

    def create_misc_box(self):
        self.misc_group_box = QGroupBox(Constants.MISC_LBL)
        misc_layout = QVBoxLayout()

        self.misc_text_edit = QTextEdit()
        self.misc_text_edit.setTabChangesFocus(True)

        misc_layout.addWidget(self.misc_text_edit)

        self.misc_group_box.setLayout(misc_layout)
        self.misc_group_box.setMinimumHeight(300)
        self.misc_group_box.setMinimumWidth(600)


