import sys

from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication

from view.GUI import GUI

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setFont(QFont('Microsoft YaHei UI'))
    gui = GUI()
    gui.show()
    sys.exit(app.exec_())
