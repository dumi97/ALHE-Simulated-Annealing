from simulated_annealing import SimulatedAnnealing


class SimulatedAnnealingPenalty(SimulatedAnnealing):
    def __init__(self, lp_matrix, score_matrix, contribution_matrix, author_limit_list, iteration_count,
                 start_temperature, init_generation_mode, author_penalty, university_penalty):
        self.author_penalty = author_penalty
        self.university_penalty = university_penalty
        super().__init__(lp_matrix, score_matrix, contribution_matrix, author_limit_list, iteration_count, start_temperature, init_generation_mode)

    def calculate_score(self):
        """
        Calculates score for working point stored in object.
        """
        author_buffer = []
        university_buffer = 0
        total_score = 0
        total_author_penalty = 0
        total_university_penalty = 0
        for i in range(len(self.working_point)):
            author_buffer.append(0)
            for j in range(len(self.working_point[i])):
                if self.working_point[i][j]:
                    total_score += self.entry_matrix[i][j].score
                    author_buffer[i] += self.entry_matrix[i][j].contribution
                    university_buffer += self.entry_matrix[i][j].contribution

                    if author_buffer[i] > self.author_limit_list[i]:
                        total_author_penalty += self.author_penalty
                    if university_buffer > self.university_limit:
                        total_university_penalty += self.university_penalty

        total_score = total_score - total_author_penalty - total_university_penalty
        return total_score

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
        Inverts bit (acceptance of article) of solution (working point) on specific coordinates.
        """

        self.working_point[i][j] = not self.working_point[i][j]
