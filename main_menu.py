import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QSplitter, QTextEdit
from PyQt5.QtCore import Qt

class MainMenuPage(QWidget):
    def __init__(self):
        super().__init__()

        # Create a vertical layout
        layout = QVBoxLayout()

        # Create a splitter to divide the screen
        splitter = QSplitter(Qt.Horizontal)

        # Create the left section (25% of the screen)
        left_section = QWidget()
        left_layout = QVBoxLayout()
        left_label = QLabel('Left Section - 25%', left_section)
        left_layout.addWidget(left_label)
        left_section.setLayout(left_layout)
        
        # Create the right section (75% of the screen)
        right_section = QWidget()
        right_layout = QVBoxLayout()
        right_label = QLabel('Right Section - 75%', right_section)
        right_layout.addWidget(right_label)
        right_section.setLayout(right_layout)
        
        # Add sections to the splitter
        splitter.addWidget(left_section)
        splitter.addWidget(right_section)

        # Set the initial sizes of the sections
        splitter.setSizes([1, 3])

        # Add the splitter to the main layout
        layout.addWidget(splitter)

        # Set the layout to the window
        self.setLayout(layout)

        # Set window properties
        self.setWindowTitle('Main Menu Page')
        self.setGeometry(100, 100, 800, 600)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Create and show the main menu page
    main_menu_page = MainMenuPage()
    main_menu_page.show()

    sys.exit(app.exec_())