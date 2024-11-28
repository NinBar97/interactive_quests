# quests/quest.py
import tkinter as tk
from tkinter import ttk

class Quest:
    def __init__(self, quest_id, description, difficulty, ui):
        """
        Base class for a quest.
        """
        self.quest_id = quest_id
        self.description = description
        self.difficulty = difficulty
        self.ui = ui
        self.completion_callback = None  # Will be set by GameEngine

    def start(self):
        """
        Starts the quest. Should be overridden by derived classes.
        """
        raise NotImplementedError("Each quest must implement the 'start' method.")

    def end_quest(self):
        """
        Ends the quest and triggers the completion callback.
        """
        if self.completion_callback:
            self.completion_callback(self.quest_id, self.difficulty)

    def display_message(self, frame, message, error=False, success=False):
        """
        Displays a feedback message to the player.
        """
        if self.message_label:
            self.message_label.destroy()
        color = 'red' if error else 'green' if success else 'black'
        self.message_label = ttk.Label(self.control_frame, text=message, style='Quest.TLabel')
        self.message_label.configure(foreground=color)
        self.message_label.pack(pady=5)
