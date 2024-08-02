import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt

class LoadingPage(QWidget):
    def __init__(self):
        super().__init__()

        # Set up the layout
        layout = QVBoxLayout()

        # Add the logo
        self.logo = QLabel(self)
        pixmap = QPixmap('resources/logo.png')  # Ensure the logo.png file is in the same directory or provide the correct path
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
        self.setGeometry(100, 100, 400, 300)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Create and show the loading page
    loading_page = LoadingPage()
    loading_page.show()

    sys.exit(app.exec_())
