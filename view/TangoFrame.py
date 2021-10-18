from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtWidgets import QFrame, QHBoxLayout, QLabel, QPushButton, QSizePolicy, QVBoxLayout

from view.ReturnPage import ReturnPage


class TangoFrame(QFrame):
    def __init__(self, gui):
        super(TangoFrame, self).__init__(gui)
        self.gui = gui
        self.resize(self.gui.size())
        self.setVisible(False)

        self.task = None
        self.questions = []
        self.question_id = -1
        self.tango = None
        self.return_page = ReturnPage()

        self.word = QLabel('', self)
        self.word.setAlignment(Qt.AlignCenter)
        self.word.setFont(QFont('MS Gothic', 80))
        self.kana_english = QLabel('', self)
        self.kana_english.setAlignment(Qt.AlignCenter)
        self.kana_english.setFont(QFont('Yu Gothic', 48))
        self.tone_part = QLabel('', self)
        self.tone_part.setAlignment(Qt.AlignCenter)
        self.tone_part.setStyleSheet('font-size:20pt')
        self.explanation = QLabel('', self)
        self.explanation.setAlignment(Qt.AlignCenter)
        self.explanation.setStyleSheet('font-size:24pt')

        self.image = QLabel(self)
        self.image.setPixmap(QPixmap('assets/icon2.png'))
        self.image.setAlignment(Qt.AlignCenter)
        self.prev_button = QPushButton('上一个', self)
        self.prev_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.prev_button.clicked.connect(lambda: self.refresh_history(self.question_id - 1))
        self.next_button = QPushButton('下一个', self)
        self.next_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.next_button.clicked.connect(lambda: self.refresh_history(self.question_id + 1))
        self.return_to_task_button = QPushButton('继续背', self)
        self.return_to_task_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.return_to_task_button.clicked.connect(self.return_to_task_func)
        self.return_to_welcome_button = QPushButton('不背了', self)
        self.return_to_welcome_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.return_to_welcome_button.clicked.connect(self.return_to_welcome_func)

        self.v_layout = QVBoxLayout()
        self.h_layout = QHBoxLayout()
        self.tango_v_layout = QVBoxLayout()
        self.tango_v_layout.addSpacing(100)
        self.tango_v_layout.addWidget(self.word)
        self.tango_v_layout.addStretch(2)
        self.tango_v_layout.addWidget(self.kana_english)
        self.tango_v_layout.addStretch(4)
        self.tango_v_layout.addWidget(self.tone_part)
        self.tango_v_layout.addStretch(1)
        self.tango_v_layout.addWidget(self.explanation)
        self.tango_v_layout.addSpacing(100)
        self.status_v_layout = QVBoxLayout()
        self.status_v_layout.addWidget(self.image)
        self.status_v_layout.addStretch(1)
        self.status_v_layout.addWidget(self.prev_button)
        self.status_v_layout.addWidget(self.next_button)
        self.status_v_layout.addWidget(self.return_to_task_button)
        self.status_v_layout.addWidget(self.return_to_welcome_button)
        self.h_layout.addSpacing(30)
        self.h_layout.addLayout(self.tango_v_layout)
        self.h_layout.addSpacing(30)
        self.h_layout.addLayout(self.status_v_layout)
        self.h_layout.addSpacing(30)
        self.h_layout.setStretch(1, 5)
        self.h_layout.setStretch(3, 1)
        self.v_layout.addSpacing(30)
        self.v_layout.addLayout(self.h_layout)
        self.v_layout.addSpacing(30)
        self.setLayout(self.v_layout)

    def return_to_task_func(self):
        self.gui.set_visible_frame(self.gui.task_frame)

    def return_to_welcome_func(self):
        if self.task.get_progress() == 1:
            self.gui.set_visible_frame(self.gui.welcome_frame)
        else:
            self.return_page.exec_()
            if self.return_page.return_:
                self.gui.set_visible_frame(self.gui.welcome_frame)

    def load_task(self, task):
        self.task = task
        self.questions = self.task.questions

    def refresh_history(self, question_id):
        self.question_id = question_id
        self.tango = self.questions[self.question_id].target
        self.refresh_tango()
        self.image.setPixmap(QPixmap('assets/icon.png'))
        self.prev_button.setVisible(True)
        self.next_button.setVisible(True)
        self.prev_button.setEnabled(self.question_id > 0)
        self.next_button.setEnabled(self.question_id < self.task.memory_counter - 1)

    def refresh_mistake(self, tango):
        self.tango = tango
        self.refresh_tango()
        self.image.setPixmap(QPixmap('assets/icon2.png'))
        self.prev_button.setVisible(False)
        self.next_button.setVisible(False)

    def refresh_tango(self):
        self.word.setText('<b>%s</b>' % self.tango.word)
        if len(self.tango.word) <= 4:
            self.word.setFont(QFont('MS Gothic', 80))
        elif len(self.tango.word) <= 8:
            self.word.setFont(QFont('MS Gothic', 72))
        else:
            self.word.setFont(QFont('MS Gothic', 40))
        if self.tango.kana:
            self.kana_english.setText(self.tango.kana)
            self.kana_english.setFont(QFont('Yu Gothic', (48 if len(self.tango.kana) < 10 else 32)))
        else:
            self.kana_english.setText(self.tango.english)
            self.kana_english.setFont(QFont('Comic Sans MS', 48))
        self.tone_part.setText('<b>%s</b>' % (self.tango.tone + self.tango.part))
        self.explanation.setText(self.tango.explanation)
