# player.py

from typing import List


class Player:
    def __init__(self, name: str):
        """
        Initializes a new player with a name, starting points, and an empty quest history.
        """
        self.name: str = name
        self.points: int = 0
        self.completed_quests: List[int] = []

    def add_points(self, points: int) -> None:
        """
        Adds points to the player's score.
        """
        self.points += points

    def complete_quest(self, quest_id: int) -> None:
        """
        Records a quest as completed by its ID.
        """
        self.completed_quests.append(quest_id)

    def has_completed_quest(self, quest_id: int) -> bool:
        """
        Checks if a quest has already been completed.
        """
        return quest_id in self.completed_quests

    def reset(self) -> None:
        """
        Resets the player's score and completed quests (useful for restarting the game).
        """
        self.points = 0
        self.completed_quests = []
