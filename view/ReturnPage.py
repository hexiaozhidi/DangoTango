from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QDialog, QHBoxLayout, QLabel, QPushButton, QSizePolicy, QVBoxLayout


class ReturnPage(QDialog):
    def __init__(self):
        super(ReturnPage, self).__init__()
        self.setFixedSize(300, 180)
        self.setWindowTitle('啧')
        self.setWindowIcon(QIcon('assets/icon.png'))
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)

        self.return_ = False
        self.info = QLabel('溜了？', self)
        self.image = QLabel(self)
        self.image.setPixmap(QPixmap('assets/icon2.png'))
        self.ok_button = QPushButton('溜了', self)
        self.ok_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.ok_button.clicked.connect(self.quit_func)
        self.cancel_button = QPushButton('不溜', self)
        self.cancel_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.cancel_button.clicked.connect(self.cancel_func)

        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignCenter)
        self.info_h_layout = QHBoxLayout()
        self.info_h_layout.addWidget(self.image)
        self.info_h_layout.addWidget(self.info)
        self.button_h_layout = QHBoxLayout()
        self.button_h_layout.setAlignment(Qt.AlignCenter)
        self.button_h_layout.addWidget(self.ok_button)
        self.button_h_layout.addWidget(self.cancel_button)
        self.layout.addLayout(self.info_h_layout)
        self.layout.addStretch(1)
        self.layout.addLayout(self.button_h_layout)
        self.setLayout(self.layout)

    def quit_func(self):
        self.return_ = True
        self.close()

    def cancel_func(self):
        self.close()
