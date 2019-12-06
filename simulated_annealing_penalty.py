from simulated_annealing import SimulatedAnnealing

class SimulatedAnnealingPenalty(SimulatedAnnealing):
    def __init__(self, score_matrix, contribution_matrix, author_limit_list, iteration_count, start_temperature, author_penalty, university_penalty):
        super().__init__(score_matrix, contribution_matrix, author_limit_list, iteration_count, start_temperature)
        self.author_penalty = author_penalty
        self.university_penalty = university_penalty

    def calculate_score(self):
        """
        Calculates score for working point stored in object.
        """

        return 0

    def calculate_neighbour_score(self, i, j):
        """
        Calculates neighbour score.
        It does not change working point.
        """

        self.modify_working_point(i, j)
        score = self.calculate_score()
        self.modify_working_point(i, j)

        return score

    def modify_working_point(self, i, j):
        """
        Inverts bit (acceptance of article) of solution (working point) on specific coodinates.
        """

        self.working_point[i][j] = not self.working_point[i][j]