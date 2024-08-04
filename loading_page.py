import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt, QTimer

# Internal module inport
from main_menu import MainMenuPage

class LoadingPage(QWidget):
    def __init__(self) -> None:
        super().__init__()

        # Set up the layout
        layout = QVBoxLayout()

        # Add the logo
        self.logo = QLabel(self)
        # Add the logo in the resource directory
        pixmap = QPixmap('resources/logo.png')
        self.logo.setPixmap(pixmap)
        self.logo.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.logo)

        # Add the title
        self.title = QLabel('Refiners Schools Administrative App', self)
        self.title.setFont(QFont('Arial', 20, QFont.Bold))
        self.title.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.title)

        # Set the layout to the window
        self.setLayout(layout)

        # Set window properties
        self.setWindowTitle('Loading Page')
        self.setGeometry(600, 200, 800, 700)

        # Add timer setup to ensure the switch to the main page
        self.timer = QTimer(self)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.main_menu)
        self.timer.start(5000)
    
    def main_menu(self) -> None:
        self.main_menu_app = MainMenuPage()
        self.main_menu_app.show()
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Create and show the loading page
    loading_page = LoadingPage()
    loading_page.show()

    sys.exit(app.exec_())
