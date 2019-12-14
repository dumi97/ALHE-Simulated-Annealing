class Entry:
    def __init__(self, lp, score, contribution):
        """
        lp - coordinates in orginal matrix as tuple (row, column) starting from zero index.
        score - article score for author.
        contribution - percentage author contribution to article.
        """
        
        self.lp = lp
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
