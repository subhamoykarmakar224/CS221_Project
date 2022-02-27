# Positional Index
class Positions:
    def __init__(self):
        self.positions = dict()

    def add_position(self, doc_id, position):
        if doc_id not in self.positions:
            self.positions[doc_id] = set()
        self.positions.add(position)
