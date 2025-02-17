from __future__ import annotations

from PySide6.QtWidgets import QApplication

import sys

class Application(QApplication):
    def __init__(self):
        super().__init__()

        from App.ServiceProvider import ServiceProvider
        self.__serviceProvider:ServiceProvider = ServiceProvider()

    @staticmethod
    def instance() -> Application:
        from PySide6.QtCore import QCoreApplication
        return QCoreApplication.instance()

    def service(self):
        return self.__serviceProvider

    def run(self):
        mainWindow = self.__serviceProvider.MainWindowView()
        mainWindow.show()
        sys.exit(self.exec())
