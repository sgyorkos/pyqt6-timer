import sys

from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QFont, QMouseEvent
from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow


MINUTES = 90


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.timer = QTimer(self)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.update_time_display)
        self.iterator = 60 * MINUTES

        self.setAutoFillBackground(True)
        self.setStyleSheet("background-color: black")

        f = QFont(["monospace"], 450)
        f.setStyleHint(QFont.StyleHint.Monospace)

        qr = self.frameGeometry()
        cp = self.screen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        self.cx, self.cy = qr.center().x(), qr.center().y()

        self.time_display = QLabel("{:02d}:{:02d}".format(self.iterator//60, self.iterator%60), self)
        self.time_display.setFont(f)
        self.time_display.setStyleSheet("color: white")
        self.time_display.adjustSize()
        self.time_display.move(self.cx - self.time_display.width()//2, self.cy - self.time_display.height()//2)

    def start_timer(self):
        if self.iterator > 0:
            self.time_display.setStyleSheet("color: green")
            self.timer.start()

    def pause_timer(self):
        self.time_display.setStyleSheet("color: white")
        self.timer.stop()

    def restart_timer(self):
        self.pause_timer()
        self.iterator = 60 * MINUTES + 1
        self.update_time_display()

    def update_time_display(self):
        self.iterator -= 1
        self.time_display.setText("{:02d}:{:02d}".format(self.iterator//60, self.iterator%60))
        self.time_display.adjustSize()
        if self.iterator == 0:
            self.timer.stop()
            self.time_display.setStyleSheet("color: red")

    def mousePressEvent(self, _: QMouseEvent):
        if self.timer.isActive():
            self.pause_timer()
        else:
            self.start_timer()

    def mouseDoubleClickEvent(self, _: QMouseEvent):
        self.restart_timer()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.showFullScreen()
    sys.exit(app.exec())

