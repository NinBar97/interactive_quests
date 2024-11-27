# quests/quest.py
class Quest:
    def __init__(self, quest_id, description, difficulty):
        self.quest_id = quest_id
        self.description = description
        self.difficulty = difficulty

    def start(self):
        raise NotImplementedError("Each quest must implement the start method.")

    def interact(self):
        """Method for interactive elements, can be overridden."""
        pass
