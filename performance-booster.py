import sys
import random
import time
import math
import pyautogui
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton
from PyQt5.QtCore import QThread

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Mouse Hareket")
        self.setGeometry(200, 200, 300, 200)
        self.setStyleSheet("background-color: #FFC0CB;")

        self.stop_button = QPushButton("Durdur", self)
        self.stop_button.setGeometry(100, 150, 100, 40)
        self.stop_button.setEnabled(False)
        self.stop_button.clicked.connect(self.stop_mouse_movement)
       
        self.exit_button = QPushButton("Çıkış", self)
        self.exit_button.setGeometry(100, 100, 100, 40)
        self.exit_button.clicked.connect(self.exit_application)

        self.move_mouse_button = QPushButton("Mouse Hareket Ettir", self)
        self.move_mouse_button.setGeometry(100, 50, 100, 40)
        self.move_mouse_button.clicked.connect(self.start_mouse_movement)
        

        self.thread = None
        self.is_running = False

    def exit_application(self):
        QApplication.quit()

    def start_mouse_movement(self):
        self.move_mouse_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        self.thread = MouseMovementThread()
        self.thread.finished.connect(self.stop_mouse_movement)
        self.thread.start()

    def stop_mouse_movement(self):
        self.stop_button.setEnabled(False)
        self.move_mouse_button.setEnabled(True)
        if self.thread is not None:
            self.thread.stop()
            self.thread = None

class MouseMovementThread(QThread):
    def __init__(self):
        super().__init__()

    def run(self):
        pyautogui.FAILSAFE = False
        center_x, center_y = pyautogui.size()[0] // 2, pyautogui.size()[1] // 2
        radius = min(center_x, center_y) // 2
        while not self.isInterruptionRequested(): ##Donguyu for'dan while'a cektik
            angle = random.uniform(0, 2 * 3.14159)
            x = int(center_x + radius * math.cos(angle))
            y = int(center_y + radius * math.sin(angle))
            pyautogui.moveTo(x, y, duration=0.25)
            QThread.sleep(3) #time-sleep yeriine Qı 3 e cıkarıp hareketler arası bekleme suresını arttırdık

    def stop(self):
        self.requestInterruption()
        self.wait()

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())
