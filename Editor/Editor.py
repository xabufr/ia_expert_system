from PySide.QtGui import QApplication

import sys
import EditorMainWindow


class Editor():
    def __init__(self):
        self.__app = QApplication(sys.argv)
        self.__mainWindow = EditorMainWindow.EditorMainWindow()

    def start(self):
        return self.__app.exec_()


editor = Editor()
sys.exit(editor.start())
