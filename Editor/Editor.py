from PySide.QtGui import QApplication

import sys
import EditorMainWindow


class Editor():
    def __init__(self):
        self.__app = QApplication(sys.argv)
        self.__mainWindow = EditorMainWindow.EditorMainWindow()

    def start(self):
        return self.__app.exec_()


def check_python_version():
    if sys.version_info < (3,0,0):
        sys.stderr.write("You need python3 at least, but python %s.%s.%s used !\n" % sys.version_info[:3])
        exit(1)

check_python_version()
editor = Editor()
sys.exit(editor.start())
