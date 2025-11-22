import sys
from PyQt5.QtWidgets import QApplication
from views.main_window import MainWindow
from views.auth_dialog import AuthDialog


def main():
    app = QApplication(sys.argv)
    
    auth_dialog = AuthDialog()
    if auth_dialog.exec_() == AuthDialog.Accepted:
        username, password = auth_dialog.get_credentials()
        main_window = MainWindow(username, password)
        main_window.showMaximized()
        sys.exit(app.exec_())
    else:
        sys.exit(0)


if __name__ == '__main__':
    main()

