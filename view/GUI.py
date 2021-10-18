import os

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QFrame

from view.QuitPage import QuitPage
from view.TangoFrame import TangoFrame
from view.TaskFrame import TaskFrame
from view.WelcomeFrame import WelcomeFrame


class GUI(QFrame):
    def __init__(self):
        super(GUI, self).__init__()
        self.setFixedSize(1280, 720)
        self.setWindowTitle('DangoTango')
        self.setWindowIcon(QIcon('assets/icon.png'))
        self.center()

        self.welcome_frame = WelcomeFrame(self)
        self.task_frame = TaskFrame(self)
        self.tango_frame = TangoFrame(self)
        self.frames = [self.welcome_frame, self.task_frame, self.tango_frame]
        self.quit_page = QuitPage()

    def closeEvent(self, e):
        self.quit_page.exec_()
        if self.quit_page.quit:
            e.accept()
        else:
            e.ignore()

    def center(self):
        desktop = QApplication.desktop()
        width_d, height_d = desktop.width(), desktop.height()
        pos_x = width_d / 2 - self.frameGeometry().width() / 2
        pos_y = height_d / 2 - self.frameGeometry().height() / 2
        self.move(int(pos_x), int(pos_y))

    def set_visible_frame(self, visible_frame):
        for frame in self.frames:
            if frame == visible_frame:
                frame.setVisible(True)
            else:
                frame.setVisible(False)
