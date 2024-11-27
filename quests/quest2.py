# quests/quest2.py
from quests.quest import Quest


class Quest2(Quest):
    def __init__(self, ui):
        super().__init__(
            quest_id=2,
            description="Placeholder...",
            difficulty=2,
        )
        self.ui = ui

    def start(self):
        print(self.description)
        # Implement ODE problem here
        self.interact()

    def interact(self):
        # Visualization or interactive solution
        pass  # Placeholder
