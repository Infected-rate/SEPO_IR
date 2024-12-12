import sys
from PyQt5.QtWidgets import QApplication
from image_app import ImageApp

# This is main function 

if __name__ == '__main__':
   # Create instance of QApplication (Handles the app's initialization and finalization)
   app = QApplication(sys.argv)
   
   # Create instance of our main window class (ImageApp)
   ex = ImageApp()
   
   # Start the application's event loop and exit with its return value
   # sys.exit ensures proper cleanup when the application terminates
   sys.exit(app.exec_())