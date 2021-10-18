from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtWidgets import QFileDialog, QFrame, QHBoxLayout, QLabel, QMessageBox, QPushButton, QSizePolicy, QVBoxLayout

from book_tools import *
from view.ChooseSheetPage import ChooseSheetPage
from view.PreparePage import PreparePage


class WelcomeFrame(QFrame):
    def __init__(self, gui):
        super(WelcomeFrame, self).__init__(gui)
        self.gui = gui
        self.resize(self.gui.size())
        self.books = get_books()
        self.target_num_setter = 'slider'  # prepare_page 中的 target_num_setter 使用 'slider' 还是 'radio_button'
        self.choose_sheet_page = ChooseSheetPage(self)
        self.prepare_page = PreparePage(self, target_num_setter=self.target_num_setter)

        self.title_d = QLabel('だんご', self)
        self.title_d.setFont(QFont('MS Gothic', 75))
        self.title_t = QLabel('単語', self)
        self.title_t.setFont(QFont('Yu Gothic', 60))
        self.image = QLabel(self)
        self.image.setPixmap(QPixmap('assets/icon.png'))
        self.update_button = QPushButton('创建/更新词库', self)
        self.update_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.update_button.clicked.connect(self.update_func)
        self.start_button = QPushButton('开始背单词！', self)
        self.start_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.start_button.setEnabled(bool(self.books))
        self.start_button.clicked.connect(self.start_func)
        self.quit_button = QPushButton('溜了溜了', self)
        self.quit_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.quit_button.clicked.connect(self.gui.close)

        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignCenter)
        self.title_h_layout = QHBoxLayout()
        self.title_h_layout.setAlignment(Qt.AlignCenter)
        self.title_h_layout.addWidget(self.title_d)
        self.title_h_layout.addWidget(self.title_t)
        self.image.setAlignment(Qt.AlignCenter)
        self.button_h_layout = QHBoxLayout()
        self.button_h_layout.setAlignment(Qt.AlignCenter)
        self.button_h_layout.addSpacing(50)
        self.button_h_layout.addWidget(self.update_button)
        self.button_h_layout.addSpacing(50)
        self.button_h_layout.addWidget(self.start_button)
        self.button_h_layout.addSpacing(50)
        self.button_h_layout.addWidget(self.quit_button)
        self.button_h_layout.addSpacing(50)
        self.layout.addLayout(self.title_h_layout)
        self.layout.addWidget(self.image)
        self.layout.addSpacing(100)
        self.layout.addLayout(self.button_h_layout)
        self.layout.setAlignment(Qt.AlignCenter)
        self.setLayout(self.layout)

    def update_func(self):
        path = QFileDialog.getOpenFileName(self, directory='Open file', filter='Microsoft Excel 工作表 (*.xlsx)')[0]
        if not path:
            return
        sheet_names = get_xlsx_sheets(path)
        if len(sheet_names) == 1:
            sheet_name = sheet_names[0]
        else:
            self.choose_sheet_page.set_sheets(sheet_names)
            self.choose_sheet_page.exec_()
            sheet_name = self.choose_sheet_page.get_chosen_sheet()
            self.choose_sheet_page = ChooseSheetPage(self)
        if not sheet_name:
            return
        title, mode = update_book_by_xlsx_sheet(path, sheet_name)
        if mode == '单词量过少':
            QMessageBox.critical(self, '啧', '词库单词量少得都不够出一道题的，背个毛？')
            return
        self.start_button.setEnabled(True)
        self.refresh_books()
        QMessageBox.information(self, '提示', '词库「%s」%s完成。' % (title, mode))

    def start_func(self):
        self.prepare_page.set_books(self.books)
        self.prepare_page.exec_()
        chosen_book, target_num, mode_factor, revision_factor = self.prepare_page.get_result()
        self.prepare_page = PreparePage(self, target_num_setter=self.target_num_setter)
        if chosen_book:
            self.gui.task_frame.load_task(chosen_book, target_num, mode_factor, revision_factor)
            self.gui.set_visible_frame(self.gui.task_frame)

    def refresh_books(self):
        self.books = get_books()
