from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QComboBox, QDialog, QHBoxLayout, QLabel, QPushButton, QRadioButton, QSizePolicy, QSlider, \
    QVBoxLayout

from book_tools import get_book_size


class PreparePage(QDialog):
    def __init__(self, welcome_frame, target_num_setter='slider'):
        super(PreparePage, self).__init__()
        self.setFixedSize(700, 350)
        self.setWindowTitle('准备开始')
        self.setWindowIcon(QIcon('assets/icon.png'))
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)

        self.chosen_book = ''
        self.chosen_book_size = 0
        self.target_num_setter = target_num_setter
        self.target_num = min(self.chosen_book_size, 200)
        self.mode_factor = 4
        self.revision_factor = 25
        self.ok = False

        self.question1 = QLabel('要背哪个词库？', self)
        self.books_combo_box = QComboBox(self)
        self.books_combo_box.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.books_combo_box.currentTextChanged.connect(self.choose_book_func)
        self.chosen_book_info = QLabel(self)

        self.image = QLabel(self)
        self.image.setPixmap(QPixmap('assets/icon3.png'))
        if self.target_num_setter == 'slider':
            self.question2 = QLabel('打算背多少个单词？%05d' % self.target_num, self)
            self.target_num_slider = QSlider(Qt.Horizontal)
            self.target_num_slider.setRange(1, self.chosen_book_size)
            self.target_num_slider.setValue(self.target_num)
            self.target_num_slider.valueChanged.connect(self.set_target_num_func)
        else:
            self.question2 = QLabel('打算背多少个单词？', self)
            self.radio_button_20 = QRadioButton('20', self)
            self.radio_button_50 = QRadioButton('50', self)
            self.radio_button_100 = QRadioButton('100', self)
            self.radio_button_200 = QRadioButton('200', self)
            self.radio_button_max = QRadioButton('有多少来多少！', self)
            self.radio_buttons = [self.radio_button_20, self.radio_button_50, self.radio_button_100,
                                  self.radio_button_200, self.radio_button_max]
            for button in self.radio_buttons:
                button.clicked.connect(self.set_target_num_func)

        self.question3 = QLabel('每个单词的记忆次数：%d' % self.mode_factor, self)
        self.mode_factor_slider = QSlider(Qt.Horizontal)
        self.mode_factor_slider.setRange(1, 6)
        self.mode_factor_slider.setValue(4)
        self.mode_factor_slider.valueChanged.connect(self.set_mode_factor_func)

        self.question4 = QLabel('历史高错单词的比例：%d%%' % self.revision_factor, self)
        self.revision_factor_slider = QSlider(Qt.Horizontal)
        self.revision_factor_slider.setRange(0, 100)
        self.revision_factor_slider.setValue(25)
        self.revision_factor_slider.valueChanged.connect(self.set_revision_factor_func)

        self.ok_button = QPushButton('确定', self)
        self.ok_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.ok_button.clicked.connect(self.ok_func)
        self.cancel_button = QPushButton('取消', self)
        self.cancel_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.cancel_button.clicked.connect(self.cancel_func)

        self.layout = QHBoxLayout()
        self.layout.setAlignment(Qt.AlignCenter)
        self.choose_book_v_layout = QVBoxLayout()
        self.chosen_book_info.setAlignment(Qt.AlignCenter)
        self.choose_book_v_layout.addWidget(self.question1)
        self.choose_book_v_layout.addWidget(self.books_combo_box)
        self.choose_book_v_layout.addStretch(1)
        self.choose_book_v_layout.addWidget(self.chosen_book_info)
        self.choose_book_v_layout.addStretch(1)
        self.choose_book_v_layout.addWidget(self.ok_button)

        self.set_task_v_layout = QVBoxLayout()
        self.question2_h_layout = QHBoxLayout()
        self.question2_h_layout.addWidget(self.image)
        self.question2_h_layout.addWidget(self.question2)
        if self.target_num_setter == 'slider':
            self.target_num_slider_h_layout = QHBoxLayout()
            self.target_num_slider_h_layout.setAlignment(Qt.AlignCenter)
            self.target_num_slider_h_layout.addWidget(self.target_num_slider)
        else:
            self.radio_button_h_layout = QHBoxLayout()
            for button in self.radio_buttons[:-1]:
                self.radio_button_h_layout.addWidget(button)
        self.mode_factor_slider_h_layout = QHBoxLayout()
        self.mode_factor_slider_h_layout.setAlignment(Qt.AlignCenter)
        self.mode_factor_slider_h_layout.addWidget(self.mode_factor_slider)
        self.revision_factor_slider_h_layout = QHBoxLayout()
        self.revision_factor_slider_h_layout.setAlignment(Qt.AlignCenter)
        self.revision_factor_slider_h_layout.addWidget(self.revision_factor_slider)

        self.set_task_v_layout.addLayout(self.question2_h_layout)
        if self.target_num_setter == 'slider':
            self.set_task_v_layout.addLayout(self.target_num_slider_h_layout)
        else:
            self.set_task_v_layout.addLayout(self.radio_button_h_layout)
            self.set_task_v_layout.addWidget(self.radio_button_max)
        self.set_task_v_layout.addStretch(1)
        self.set_task_v_layout.addWidget(self.question3)
        self.set_task_v_layout.addLayout(self.mode_factor_slider_h_layout)
        self.set_task_v_layout.addStretch(1)
        self.set_task_v_layout.addWidget(self.question4)
        self.set_task_v_layout.addLayout(self.revision_factor_slider_h_layout)
        self.set_task_v_layout.addStretch(1)
        self.set_task_v_layout.addWidget(self.cancel_button)
        self.layout.addLayout(self.choose_book_v_layout)
        self.layout.addSpacing(50)
        self.layout.addLayout(self.set_task_v_layout)
        self.setLayout(self.layout)

    def choose_book_func(self):
        self.chosen_book = self.books_combo_box.currentText()
        self.chosen_book_size = get_book_size(self.chosen_book)
        self.target_num = min(self.chosen_book_size, 200)
        self.chosen_book_info.setText('选中的词库：\n「%s」\n单词量：%d'
                                      % (self.chosen_book, self.chosen_book_size))
        self.set_target_num_setter()

    def set_target_num_func(self):
        if self.target_num_setter == 'slider':
            self.target_num = self.target_num_slider.value()
            self.question2.setText('打算背多少个单词？%05d' % self.target_num)
        else:
            button = self.sender()
            self.target_num = self.chosen_book_size if button.text() == '有多少来多少！' else int(button.text())

    def set_mode_factor_func(self):
        self.mode_factor = self.mode_factor_slider.value()
        self.question3.setText('每个单词的记忆次数：%d' % self.mode_factor)

    def set_revision_factor_func(self):
        self.revision_factor = self.revision_factor_slider.value()
        self.question4.setText('历史高错单词的比例：%d%%' % self.revision_factor)

    def ok_func(self):
        self.ok = True
        self.close()

    def cancel_func(self):
        self.close()

    def set_target_num_setter(self):
        if self.target_num_setter == 'slider':
            self.target_num_slider.setRange(1, self.chosen_book_size)
            self.target_num_slider.setValue(self.target_num)
            self.question2.setText('打算背多少个单词？%05d' % self.target_num)
        else:
            for button in self.radio_buttons[:-1]:
                if int(button.text()) <= self.chosen_book_size:
                    button.setEnabled(True)
                else:
                    button.setEnabled(False)
            for button in self.radio_buttons:
                if button.isEnabled():
                    button.setChecked(True)
                    self.target_num = self.chosen_book_size if button.text() == '有多少来多少！' else int(button.text())
                    break

    def set_books(self, books):
        self.chosen_book = books[0]
        self.chosen_book_size = get_book_size(self.chosen_book)
        self.target_num = min(self.chosen_book_size, 200)
        self.books_combo_box.addItems(books)
        self.chosen_book_info.setText('选中的词库：\n「%s」\n单词量：%d'
                                      % (self.chosen_book, self.chosen_book_size))
        self.set_target_num_setter()

    def get_result(self):
        return (self.chosen_book, self.target_num, self.mode_factor, self.revision_factor) if self.ok else ('', 0, 0, 0)
