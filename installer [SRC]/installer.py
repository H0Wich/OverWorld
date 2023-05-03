#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import urllib.request
import zipfile
import winshell
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QProgressBar, QLabel
from win32com.client import Dispatch
from PyQt5.QtWidgets import QMessageBox

class Progress(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("OverWorld | By Howich")
        self.setFixedSize(300, 100)
        self.setStyleSheet("background-color: black;")

        layout = QVBoxLayout()

        label = QLabel(self)
        url = "https://raw.githubusercontent.com/H0Wich/overinstaller/main/image.png"
        data = urllib.request.urlopen(url).read()
        pixmap = QPixmap()
        pixmap.loadFromData(data)
        pixmap = pixmap.scaled(50, 50, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        label.setPixmap(pixmap)
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setStyleSheet(
            "QProgressBar {border: none; background-color: black; height: 20px;}"
            "QProgressBar::chunk {background-color: white;}"
        )
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setAlignment(Qt.AlignCenter)
        font = self.progress_bar.font()
        font.setPointSize(10)
        font.setFamily("Arial")
        self.progress_bar.setFont(font) 
        layout.addWidget(self.progress_bar)

        self.setLayout(layout)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_progress)
        self.timer.start(50)

        self.progress_bar.setValue(0)

    def update_progress(self):
        value = self.progress_bar.value()
        if value < 100:
            self.progress_bar.setValue(value + 1)
            if value == 50:
                url = "https://github.com/H0Wich/overinstaller/releases/download/overworld/game.zip"
                filename = "game.zip"
                urllib.request.urlretrieve(url, filename)
                install_dir = os.path.join("C:\\", "Program Files", "OverWorld")
                os.makedirs(install_dir, exist_ok=True)
                with zipfile.ZipFile(filename, "r") as zip_ref:
                    zip_ref.extractall(install_dir)
                os.remove(filename)
            elif value == 75:
                desktop = winshell.desktop()
                path = os.path.join(desktop, "OverWorld.lnk")
                target = r"C:\Program Files\OverWorld\OverWorld.exe"
                wDir = r"C:\Program Files\OverWorld"
                icon = r"C:\Program Files\OverWorld\OverWorld.exe"
                shell = Dispatch('WScript.Shell')
                shortcut = shell.CreateShortCut(path)
                shortcut.Targetpath = target
                shortcut.WorkingDirectory = wDir
                shortcut.IconLocation = icon
                shortcut.save()
            elif value == 99:
                 QMessageBox.about(self, "OverWorld", "The installation was successful, the game is already on the desktop!")
        else:
            self.timer.stop()
            exit()

if __name__ == "__main__":
    app = QApplication([])
    url = "https://raw.githubusercontent.com/H0Wich/overinstaller/main/icon.png"
    filename = "icon.png"
    urllib.request.urlretrieve(url, filename)
    app.setWindowIcon(QIcon(filename))
    window = Progress()
    window.show()
    app.exec_()
