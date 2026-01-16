import os
from pathlib import Path
from typing import Tuple

from PyQt5.QtCore import pyqtSlot, QThread, QObject, pyqtSignal
from PyQt5.QtWidgets import QWidget, QMessageBox, QApplication, QVBoxLayout, \
    QHBoxLayout, QLayout, QListWidgetItem

from compounds.Footer import Footer
from compounds.GameView import GameView
from compounds.Header import Header
from helper.MutableString import MutableString
from helper.SharedState import SharedState
from other.GroupList import GroupList


class Worker(QObject):
    """
    Worker to simulate games in parallel
    """

    # Signal to show worker is finished
    finished: pyqtSignal = pyqtSignal()

    def __init__(self, xx: str, yy: str, ref_to_game: 'TournamentGUI'):
        """
        Constructor to create the worker

        :param xx: Player A
        :param yy: Player B
        :param ref_to_game: Reference to original game
        """
        super().__init__()
        self.xx = xx
        self.yy = yy
        self.ref = ref_to_game

    @staticmethod
    def get_results() -> Tuple[str, str]:
        """
        Function to retrieve data from files

        :return: List of winner and number of moves
        """
        with open('Win.txt', 'r') as win_file:
            winner = win_file.readline().replace('\n', '')
        with open('5GewinntState.txt', 'r') as state_file:
            moves = state_file.readline().split()[1].replace('\n', '')
        return winner, moves

    def run(self):
        """
        Worker method which simulates the games
        """
        # Run A vs B
        self.ref.game_1.game.watch(f"./5GewinntState_{self.xx}_{self.yy}.png")
        os.system(
            f'python ./5Gewinnt.py '
            f'"{SharedState.groups[self.xx]}" '
            f'"{SharedState.groups[self.yy]}" '
            f'"{self.xx}" "{self.yy}"'
        )
        # Update results
        winner, moves = Worker.get_results()
        self.ref.winner_1.update_text(winner)
        self.ref.num_moves_1.update_text(moves)
        self.ref.game_1.game.save_to_gif()
        self.ref.game_1.game.stop_watch(f"./5GewinntState_{self.xx}_{self.yy}.png")
        # Run B vs A
        self.ref.game_2.game.watch(f"./5GewinntState_{self.yy}_{self.xx}.png")
        os.system(
            f'python ./5Gewinnt.py '
            f'"{SharedState.groups[self.yy]}" '
            f'"{SharedState.groups[self.xx]}" '
            f'"{self.yy}" "{self.xx}"')
        # Update results
        winner, moves = Worker.get_results()
        self.ref.winner_2.update_text(winner)
        self.ref.num_moves_2.update_text(moves)
        self.ref.game_2.game.save_to_gif()
        self.ref.game_2.game.stop_watch(f"./5GewinntState_{self.yy}_{self.xx}.png")
        self.finished.emit()


def set_enable_layout(layout: QLayout, state: bool):
    """
    Function to iteratively enable/disable widgets

    :param layout: Layout to iterate
    :param state: State to set
    """
    for i in range(layout.count()):
        item = layout.itemAt(i)
        # Change depending on widget or layout
        as_widget = item.widget()
        if as_widget is not None:
            as_widget.setEnabled(state)
        as_layout = item.layout()
        if as_layout is not None:
            set_enable_layout(as_layout, state)


class TournamentGUI(QWidget):

    def __init__(self):
        super().__init__()
        left_layout = QVBoxLayout()
        # Overall view
        header = Header()
        self.game_1 = GameView()
        self.game_2 = GameView()
        self.footer = Footer()
        # String which can change
        self.team_xx = MutableString()
        self.team_yy = MutableString()
        self.winner_1 = MutableString()
        self.num_moves_1 = MutableString()
        self.winner_2 = MutableString()
        self.num_moves_2 = MutableString()
        # Connect string to widgets
        for label in [header.team_xx, self.game_1.player_A, self.game_2.player_B]:
            self.team_xx.register_label(label)
        for label in [header.team_yy, self.game_1.player_B, self.game_2.player_A]:
            self.team_yy.register_label(label)
        self.winner_1.register_label(self.game_1.winner)
        self.num_moves_1.register_label(self.game_1.moves)
        self.winner_2.register_label(self.game_2.winner)
        self.num_moves_2.register_label(self.game_2.moves)
        # Propagate drag and drop
        header.team_xx.dropped.connect(self.team_xx.update_text)
        header.team_yy.dropped.connect(self.team_yy.update_text)
        header.team_xx.dragged.connect(self.team_xx.update_text)
        header.team_yy.dragged.connect(self.team_yy.update_text)
        # Build left side
        left_layout.addWidget(header)
        left_layout.addWidget(self.game_1)
        left_layout.addWidget(self.game_2)
        left_layout.addWidget(self.footer)
        # Teams
        layout = QHBoxLayout()
        layout.addLayout(left_layout)
        group_list = GroupList()
        layout.addWidget(group_list)
        self.setLayout(layout)
        # Setup threading
        self.game_thread: QThread = QThread(self)
        self.worker: Worker = Worker("", "", self)
        # Connect with button
        self.footer.start_game.connect(self.start_game)
        self.footer.reset_game.connect(self.reset)
        # Connect clicks
        group_list.group_list_widget.itemDoubleClicked.connect(self.double_clicked)
        # Set base width and height
        screen = QApplication.desktop().screenGeometry()
        self.resize(screen.width() * 0.5, screen.height())
        self.setWindowTitle("5 Wins tournament")
        self.updateGeometry()
        self.reset()
        gif = Path(f"./GIF")
        gif.mkdir(parents=True, exist_ok=True)

    def reset(self):
        """
        Method to reset labels and game view
        """
        for mutable_string in [self.team_xx, self.team_yy,
                               self.winner_1, self.winner_2,
                               self.num_moves_1, self.num_moves_2]:
            mutable_string.update_text("")
        self.game_1.game.clear()
        self.game_2.game.clear()
        set_enable_layout(self.layout(), True)

    # Slot to set label by using double click
    @pyqtSlot(QListWidgetItem)
    def double_clicked(self, item: QListWidgetItem):
        if self.team_xx.text == "":
            self.team_xx.update_text(item.text())
        elif self.team_yy.text == "":
            self.team_yy.update_text(item.text())

    # Slot to start game thread
    @pyqtSlot()
    def start_game(self):
        if self.team_xx.text == "" or self.team_yy == "":
            QMessageBox.warning(self, "Missing team", "Please provide two teams to battle")
            return
        # Start main script
        xx = self.team_xx.text
        yy = self.team_yy.text
        # Setup and run worker
        self.game_thread = QThread()
        self.worker = Worker(xx, yy, self)
        self.worker.moveToThread(self.game_thread)
        self.game_thread.started.connect(lambda: set_enable_layout(self.layout(), False))
        self.game_thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.game_thread.quit)
        self.worker.finished.connect(lambda: self.footer.reset_button.setEnabled(True))
        self.worker.finished.connect(self.worker.deleteLater)
        self.game_thread.finished.connect(self.game_thread.deleteLater)
        self.game_thread.start()

    def maximumHeight(self) -> int:
        # Hint for max height
        return QApplication.desktop().screenGeometry().height()
