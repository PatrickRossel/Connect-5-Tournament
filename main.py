"""This script runs the GUI

You may change anything you want. If you have any questions: yfrank@students.uni-mainz.de
(18.09.22)

(Would be nice to decouple the main window and the execution of the matches)
"""
import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QStyleFactory

from TournamentGUI import TournamentGUI
from helper.SharedState import SharedState


def main():
    # Create and init game. Then run
    app = QApplication(sys.argv)
    # Set style of application
    app.setStyle(QStyleFactory.create("Fusion"))
    QApplication.setWindowIcon(QIcon("images/JGU.png"))
    # Start and show GUI
    SharedState.init()
    gui = TournamentGUI()
    gui.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
