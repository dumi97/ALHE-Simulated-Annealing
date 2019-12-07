class Entry:
    def __init__(self, score, contribution):
        self.score = score
        self.contribution = contribution
        self.unit_gain = score / contribution

    # string representation
    def __str__(self):
        return f"({self.score}, {self.contribution}, {self.unit_gain})"

    # comparing Entries for sorting
    def __eq__(self, other):
        return self.unit_gain == other.unit_gain

    def __gt__(self, other):
        return self.unit_gain > other.unit_gain
