# game_engine.py

from player import Player
from user_interface import UserInterface
from quests.quest1 import Quest1
from quests.quest2 import Quest2
from tkinter import messagebox


class GameEngine:
    def __init__(self):
        self.ui = UserInterface()
        self.player = None
        self.current_quest_index = 0

        # Initialize quests and set completion callbacks
        self.quests = [Quest1(self.ui), Quest2(self.ui)]
        for quest in self.quests:
            quest.completion_callback = self.quest_completed

        # Set the callback for starting the quest journey
        self.ui.start_quest_journey_callback = self.start_quest_journey

    def start_game(self):
        self.ui.run()

    def start_quest_journey(self):
        try:
            if not self.player:
                self.player = Player(self.ui.player_name.get())
                self.ui.player_points.set(self.player.points)
            self.start_next_quest()
        except Exception as e:
            print(f"Exception in start_quest_journey: {e}")

    def start_next_quest(self):
        print("GameEngine.start_next_quest called")  # Debugging statement
        if self.current_quest_index < len(self.quests):
            quest = self.quests[self.current_quest_index]
            print(f"Starting Quest {quest.quest_id}")  # Debugging statement
            quest.start()
        else:
            messagebox.showinfo("Info", "No more quests available.")

    def quest_completed(self, quest_id, difficulty):
        print(f"Quest {quest_id} completed")  # Debugging statement
        self.player.complete_quest(quest_id)
        self.player.add_points(difficulty * 10)
        self.ui.player_points.set(self.player.points)
        self.current_quest_index += 1

    def view_status(self):
        self.ui.view_status()


if __name__ == "__main__":
    game = GameEngine()
    game.start_game()
