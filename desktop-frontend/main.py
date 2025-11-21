import sys
from PyQt5.QtWidgets import QApplication
from views.main_window import MainWindow
from views.login_dialog import LoginDialog


def main():
    app = QApplication(sys.argv)
    
    login_dialog = LoginDialog()
    if login_dialog.exec_() == LoginDialog.Accepted:
        username, password = login_dialog.get_credentials()
        main_window = MainWindow(username, password)
        main_window.show()
        sys.exit(app.exec_())
    else:
        sys.exit(0)


if __name__ == '__main__':
    main()

