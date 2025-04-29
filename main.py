import sys
from PyQt6.QtWidgets import QApplication
from database_module import Database
from graphics_module import Graphics
from ui_module import MyWindow
from PyQt6.QtWebEngineWidgets import QWebEngineView

if __name__ == "__main__":
    app = QApplication(sys.argv)

    db = Database()
    browser = QWebEngineView()
    graphics = Graphics(db.cursor, browser)
    window = MyWindow(db, graphics)
    window.show()

    sys.exit(app.exec())

    