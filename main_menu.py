import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, 
    QSplitter, QTextEdit, QPushButton, QStackedWidget
    )
from PyQt5.QtCore import Qt

class MainMenuPage(QWidget):
    def __init__(self):
        super().__init__()

        # Create a vertical layout
        main_layout = QVBoxLayout()

        # Create a splitter to divide the screen
        splitter = QSplitter(Qt.Horizontal)

        # Create the left section (25% of the screen)
        left_section = QWidget()
        left_layout = QVBoxLayout()

        # Create a button list to add to the layout
        btn_dict = {
            "Financial Records": "Financial Records", 
            "Inventory Records": "Inventory Records", 
            "Staff Records": "Staff Records", 
            "Parents Records": "Parents Records"
            }

        #Create some buttons
        for b_name, tag in btn_dict.items():
            button = QPushButton(b_name, left_section)
            button.clicked.connect(lambda _, c=tag: self.display_content(c))
            left_layout.addWidget(button)

        left_section.setLayout(left_layout)
        
        # Create the right section (75% of the screen)
        right_section = QWidget()
        right_layout = QVBoxLayout()

        # Add a stacked widget to the right section to display content
        self.content_display = QStackedWidget(right_section)

        default_content = QLabel('Select a button to display content', right_section)
        right_layout.addWidget(default_content)
        right_layout.addWidget(self.content_display)
        right_section.setLayout(right_layout)
        
        # Add sections to the splitter
        splitter.addWidget(left_section)
        splitter.addWidget(right_section)

        # Set the initial sizes of the sections
        splitter.setSizes([1, 3])

        # Add the splitter to the main layout
        main_layout.addWidget(splitter)

        # Set the layout to the window
        self.setLayout(main_layout)

        # Set window properties
        self.setWindowTitle('Main Menu Page')
        self.setGeometry(400, 100, 1200, 900)
    
    def display_content(self, button_tag):
        # Insert the new data into the split screen
        while self.content_display.count() > 0:
            widget = self.content_display.widget(0)
            self.content_display.removeWidget(widget)
            widget.deleteLater()
        
        # Add new content
        content_label = QLabel(button_tag)
        self.content_display.addWidget(content_label)
        self.content_display.setCurrentWidget(content_label)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Create and show the main menu page
    main_menu_page = MainMenuPage()
    main_menu_page.show()

    sys.exit(app.exec_())