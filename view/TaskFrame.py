from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QFrame, QHBoxLayout, QLabel, QProgressBar, \
    QPushButton, QSizePolicy, QVBoxLayout

from Task import Task
from view.ReturnPage import ReturnPage


class TaskFrame(QFrame):
    def __init__(self, gui):
        super(TaskFrame, self).__init__(gui)
        self.gui = gui
        self.resize(self.gui.size())
        self.setVisible(False)

        self.task = None
        self.return_page = ReturnPage()

        self.message = QLabel('', self)
        self.message.setWordWrap(True)
        self.message.setAlignment(Qt.AlignCenter)
        self.message.setStyleSheet('font-size:24pt')

        self.choice_button_0 = QPushButton('', self)
        self.choice_button_1 = QPushButton('', self)
        self.choice_button_2 = QPushButton('', self)
        self.choice_button_3 = QPushButton('', self)
        self.choice_buttons = [self.choice_button_0, self.choice_button_1,
                               self.choice_button_2, self.choice_button_3]
        for button in self.choice_buttons:
            button.setFixedSize(460, 200)
            button.setStyleSheet('font-size:20pt')
            button.clicked.connect(self.make_choice_func)

        self.image = QLabel(self)
        self.image.setPixmap(QPixmap('assets/icon.png'))
        self.image.setAlignment(Qt.AlignCenter)

        self.accuracy_bar = QProgressBar(self)
        self.accuracy_bar.setOrientation(Qt.Vertical)
        self.accuracy_bar.setRange(0, 10000)
        self.accuracy_bar.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        self.accuracy_info = QLabel('', self)
        self.accuracy_info.setAlignment(Qt.AlignCenter)

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setOrientation(Qt.Vertical)
        self.progress_bar.setRange(0, 10000)
        self.progress_bar.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        self.progress_info = QLabel('', self)
        self.progress_info.setAlignment(Qt.AlignCenter)

        self.history_button = QPushButton('回看', self)
        self.history_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.history_button.clicked.connect(self.history_func)

        self.return_button = QPushButton('不背了', self)
        self.return_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.return_button.clicked.connect(self.return_to_welcome_func)

        self.v_layout = QVBoxLayout()
        self.h_layout = QHBoxLayout()
        self.question_v_layout = QVBoxLayout()
        self.choice_v_layout = QVBoxLayout()
        self.choice_v_layout.setAlignment(Qt.AlignCenter)
        self.choice01_h_layout = QHBoxLayout()
        self.choice01_h_layout.setAlignment(Qt.AlignCenter)
        self.choice01_h_layout.addWidget(self.choice_button_0)
        self.choice01_h_layout.addSpacing(30)
        self.choice01_h_layout.addWidget(self.choice_button_1)
        self.choice23_h_layout = QHBoxLayout()
        self.choice23_h_layout.setAlignment(Qt.AlignCenter)
        self.choice23_h_layout.addWidget(self.choice_button_2)
        self.choice23_h_layout.addSpacing(30)
        self.choice23_h_layout.addWidget(self.choice_button_3)
        self.choice_v_layout.addLayout(self.choice01_h_layout)
        self.choice_v_layout.addSpacing(30)
        self.choice_v_layout.addLayout(self.choice23_h_layout)
        self.question_v_layout.addWidget(self.message, stretch=1)
        self.question_v_layout.addSpacing(30)
        self.question_v_layout.addLayout(self.choice_v_layout)
        self.status_v_layout = QVBoxLayout()
        self.status_v_layout.addWidget(self.image)
        self.status_v_layout.addSpacing(30)
        self.bar_h_layout = QHBoxLayout()
        self.accuracy_bar_v_layout = QVBoxLayout()
        self.accuracy_bar_v_layout.addWidget(self.accuracy_bar, stretch=4)
        self.accuracy_bar_v_layout.addWidget(self.accuracy_info, stretch=1, alignment=Qt.AlignCenter)
        self.progress_bar_v_layout = QVBoxLayout()
        self.progress_bar_v_layout.addWidget(self.progress_bar, stretch=4)
        self.progress_bar_v_layout.addWidget(self.progress_info, stretch=1, alignment=Qt.AlignCenter)
        self.bar_h_layout.addLayout(self.accuracy_bar_v_layout)
        self.bar_h_layout.addSpacing(30)
        self.bar_h_layout.addLayout(self.progress_bar_v_layout)
        self.status_v_layout.addLayout(self.bar_h_layout)
        self.status_v_layout.addSpacing(30)
        self.status_v_layout.addWidget(self.history_button)
        self.status_v_layout.addWidget(self.return_button)
        self.h_layout.addSpacing(30)
        self.h_layout.addLayout(self.question_v_layout)
        self.h_layout.addSpacing(30)
        self.h_layout.addLayout(self.status_v_layout)
        self.h_layout.addSpacing(30)
        self.h_layout.setStretch(1, 5)
        self.h_layout.setStretch(3, 1)
        self.v_layout.addSpacing(30)
        self.v_layout.addLayout(self.h_layout)
        self.v_layout.addSpacing(30)
        self.setLayout(self.v_layout)

    def make_choice_func(self):
        my_answer = str.join('', self.sender().text().split('\n'))
        self.task.current_question.make_choice(my_answer)
        result = self.task.current_question.check()
        self.task.finish_question(result)
        if not result:
            self.gui.tango_frame.refresh_mistake(self.task.current_question.target)
            self.gui.set_visible_frame(self.gui.tango_frame)
        if self.task.memory_counter == self.task.question_num:
            self.refresh_status()
            self.message.setText('还行吧。\n正确率：%.2f%%' % (self.task.get_accuracy() * 100))
            for button in self.choice_buttons:
                button.setText('')
                button.setIcon(QIcon('assets/icon4.png'))
                button.setIconSize(QSize(250, 250))
                button.setEnabled(False)
        else:
            self.task.start_question()
            self.refresh_question()
            self.refresh_status()

    def history_func(self):
        self.gui.tango_frame.refresh_history(self.task.memory_counter - 1)
        self.gui.set_visible_frame(self.gui.tango_frame)

    def return_to_welcome_func(self):
        if self.task.get_progress() == 1:
            self.gui.set_visible_frame(self.gui.welcome_frame)
        else:
            self.return_page.exec_()
            if self.return_page.return_:
                self.gui.set_visible_frame(self.gui.welcome_frame)

    def load_task(self, book_name, target_num, mode_factor, revision_factor):
        self.task = Task(book_name, target_num, mode_factor, revision_factor)
        self.return_page = ReturnPage()
        self.task.start_question()
        self.gui.tango_frame.load_task(self.task)
        self.refresh_question()
        self.refresh_status()

    def refresh_question(self):
        message_core = self.task.current_question.message_core
        message_remain = self.task.current_question.message.split(message_core)[1]
        self.message.setText('<b>%s</b>%s' % (message_core, message_remain))

        for i in range(4):
            choice = self.task.current_question.choices[i]
            choice_ = []
            for j in range(len(choice)):
                choice_.append(choice[j])
                if j % 12 == 11:
                    choice_.append('\n')
            if choice_[-1] == '\n':
                choice_.pop()
            choice = str.join('', choice_)
            self.choice_buttons[i].setText(choice)
            self.choice_buttons[i].setIcon(QIcon())
            self.choice_buttons[i].setEnabled(True)

    def refresh_status(self):
        self.accuracy_bar.setValue(int(self.task.get_accuracy() * 10000))
        self.accuracy_info.setText('正确率\n%.2f%%' % (self.task.get_accuracy() * 100))
        self.progress_bar.setValue(int(self.task.get_progress() * 10000))
        self.progress_info.setText('进度\n%.2f%%' % (self.task.get_progress() * 100))
        self.history_button.setEnabled(bool(self.task.memory_counter))
