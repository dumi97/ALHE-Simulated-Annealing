import random


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


temperature = 90


def print_matrix(matrix):
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            print(f"{matrix[i][j]} ", end="", flush=True)
        print("")


def build_initial_matrices(score_matrix, contribution_matrix):
    """
    Build the matrix of entries containing score, contribution and profit gain of each article, then sort it.
    Also generates first random working point matrix. Returns both generated matrices.
    """
    entry_matrix = [[] for i in range(len(score_matrix))]
    working_point = [[] for i in range(len(entry_matrix))]
    for i in range(len(score_matrix)):
        for j in range(len(score_matrix[i])):
            entry_matrix[i].append(Entry(score_matrix[i][j], contribution_matrix[i][j]))
            working_point[i].append(random.randint(0, 1))
        entry_matrix[i].sort()
    return entry_matrix, working_point


def iterate(entry_matrix, working_point):
    print("Running an iteration by doing complicated stuff")
