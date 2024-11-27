# player.py
class Player:
    def __init__(self, name):
        self.name = name
        self.points = 0
        self.completed_quests = []

    def add_points(self, points):
        self.points += points

    def complete_quest(self, quest_id):
        self.completed_quests.append(quest_id)
