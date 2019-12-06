from simulated_annealing import SimulatedAnnealing

class SimulatedAnnealingRepair(SimulatedAnnealing):
    def __init__(self, score_matrix, contribution_matrix, author_limit_list, iteration_count, start_temperature):
        super().__init__(score_matrix, contribution_matrix, author_limit_list, iteration_count, start_temperature)

    def calculate_score(self):
        """
        Calculates score for working point stored in object.
        """

        return 0

    def calculate_neighbour_score(self, i, j):
        """
        Calculates neighbour score with simulated repair without modifications.
        It does not change working point.
        """

        return 0

    def modify_working_point(self, i, j):
        """
        Inverts bit (acceptance of article) of solution (working point) on specific coodinates.
        If solution is prohibited repairs it.
        """

        self.working_point[i][j] = not self.working_point[i][j]