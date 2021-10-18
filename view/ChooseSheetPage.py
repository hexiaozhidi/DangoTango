from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QComboBox, QDialog, QHBoxLayout, QLabel, QPushButton, QSizePolicy, QVBoxLayout


class ChooseSheetPage(QDialog):
    def __init__(self, welcome_frame):
        super(ChooseSheetPage, self).__init__()
        self.welcome_frame = welcome_frame
        self.setFixedSize(350, 200)
        self.setWindowTitle('选择工作表')
        self.setWindowIcon(QIcon('assets/icon.png'))
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)

        self.chosen_sheet = ''
        self.ok = False
        self.info = QLabel('要用哪个工作表创建/更新词库？', self)
        self.sheets = QComboBox(self)
        self.sheets.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.sheets.currentTextChanged.connect(self.choose_sheet_func)
        self.ok_button = QPushButton('确定', self)
        self.ok_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.ok_button.clicked.connect(self.ok_func)
        self.cancel_button = QPushButton('取消', self)
        self.cancel_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.cancel_button.clicked.connect(self.close)

        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignCenter)
        self.button_h_layout = QHBoxLayout()
        self.button_h_layout.setAlignment(Qt.AlignCenter)
        self.button_h_layout.addWidget(self.ok_button)
        self.button_h_layout.addWidget(self.cancel_button)
        self.layout.addWidget(self.info)
        self.layout.addWidget(self.sheets)
        self.layout.addSpacing(50)
        self.layout.addLayout(self.button_h_layout)
        self.setLayout(self.layout)

    def choose_sheet_func(self):
        self.chosen_sheet = self.sheets.currentText()

    def ok_func(self):
        self.ok = True
        self.close()

    def set_sheets(self, sheets):
        self.chosen_sheet = sheets[0]
        self.sheets.addItems(sheets)

    def get_chosen_sheet(self):
        return self.chosen_sheet if self.ok else ''
