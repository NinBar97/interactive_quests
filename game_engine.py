# game_engine.py

from player import Player
from user_interface import UserInterface
from quests.quest1 import Quest1
from quests.quest2 import Quest2
from tkinter import messagebox
from ui_utils import setup_styles


class GameEngine:
    def __init__(self):
        self.ui = UserInterface()
        self.ui.game_engine = self  # Set reference to GameEngine in UI
        self.player = None
        self.current_quest_index = 0

        # Initialize quests
        self.quests = [Quest1(self.ui), Quest2(self.ui)]
        for quest in self.quests:
            quest.completion_callback = self.quest_completed

        # Set UI callback
        self.ui.start_quest_journey_callback = self.start_quest_journey

    def start_game(self):
        """
        Launches the game by starting the user interface loop.
        """
        self.ui.run()

    def start_quest_journey(self):
        """
        Initializes the player's profile and starts the first or next quest.
        """
        if not self.player:
            self.player = Player(self.ui.player_name.get())
            self.ui.player_points.set(self.player.points)
        self.start_next_quest()

    def start_next_quest(self):
        """
        Starts the next quest if available; otherwise, displays completion message.
        """
        # Destroy any existing widgets in content_frame
        #for widget in self.ui.content_frame.winfo_children():
        #    widget.destroy()

        if self.current_quest_index < len(self.quests):
            next_quest = self.quests[self.current_quest_index]
            next_quest.start()
        else:
            self.ui.show_completion_message()

    def quest_completed(self, quest_id, difficulty):
        """
        Marks a quest as completed, updates player stats, and progresses to the next quest.
        """
        self.player.complete_quest(quest_id)
        points_earned = difficulty * 10
        self.player.add_points(points_earned)
        self.ui.player_points.set(self.player.points)
        self.current_quest_index += 1

        # Proceed to the next quest
        self.start_next_quest()


if __name__ == "__main__":
    game = GameEngine()
    game.start_game()
