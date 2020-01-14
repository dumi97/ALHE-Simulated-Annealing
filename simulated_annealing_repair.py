from simulated_annealing import SimulatedAnnealing


class SimulatedAnnealingRepair(SimulatedAnnealing):
    def __init__(self, lp_matrix, score_matrix, contribution_matrix, author_limit_list, iteration_count, start_temperature, init_generation_mode):
        self.author_buffer = []
        self.university_buffer = 0
        super().__init__(lp_matrix, score_matrix, contribution_matrix, author_limit_list, iteration_count, start_temperature, init_generation_mode)

    def calculate_score(self):
        """
        Calculates score for working point stored in object.
        Returns score and True (point is always feasible).
        Does point repairing (fixing).
        """
        total_score = self.calculate_score_without_repairing()
        total_score = self.check_and_fix(0, 0, True, total_score)

        return total_score, True
    
    def calculate_score_without_repairing(self):
        """
        Calculates score for working point stored in object.
        Returns score and True (point is always feasible).
        """
        self.author_buffer = []
        self.university_buffer = 0
        total_score = 0
        for i in range(len(self.working_point)):
            self.author_buffer.append(0)
            for j in range(len(self.working_point[i])):
                if self.working_point[i][j]:
                    total_score += self.entry_matrix[i][j].score
                    self.author_buffer[i] += self.entry_matrix[i][j].contribution
                    self.university_buffer += self.entry_matrix[i][j].contribution

        return total_score

    def calculate_neighbour_score(self, i, j):
        """
        Calculates neighbour score with simulated repair without modifications.
        It does not change working point.
        Returns score and True (point is always feasible).
        """

        self.working_point[i][j] = not self.working_point[i][j]

        neighbour_score = self.calculate_score_without_repairing()
        neighbour_score = self.check_and_fix(i, j, False, neighbour_score)

        self.working_point[i][j] = not self.working_point[i][j]

        return neighbour_score, True

    def modify_working_point(self, i, j):
        """
        Inverts bit (acceptance of article) of solution (working point) on specific coordinates.
        If solution is prohibited repairs it.
        """

        self.working_point[i][j] = not self.working_point[i][j]
        # calculate score to fill buffers
        self.calculate_score()

    def check_and_fix(self, changed_i, changed_j, modify_list, current_score):
        """
        Repairs the current working point. It can also simulate repair and calculate score without changing the point.
        It will AVOID fixing the neighbour's changed (i, j) point even if it has the lowest unit gain
        """

        # check and fix author limits
        changed_positions = set()
        for i in range(len(self.working_point)):
            if self.author_buffer[i] <= self.author_limit_list[i]:
                continue
            for j in range(len(self.working_point[i])):
                if self.working_point[i][j] and (i != changed_i or j != changed_j):

                    # print(f"---------- Fixing point ({i}, {j})")  # Debug

                    if modify_list:
                        self.working_point[i][j] = False
                    else:
                        changed_positions.add((i, j))
                    current_score -= self.entry_matrix[i][j].score
                    self.author_buffer[i] -= self.entry_matrix[i][j].contribution
                    self.university_buffer -= self.entry_matrix[i][j].contribution
                    if self.author_buffer[i] <= self.author_limit_list[i]:
                        break

        # check and fix university limit
        if self.university_buffer <= self.university_limit:
            return current_score

        current_lookups = [0] * len(self.working_point)
        while self.university_buffer > self.university_limit:
            lowest_gain = None
            index_to_remove = None

            # find current lowest unit gain to remove
            for i in range(len(current_lookups)):
                # search for the first valid True value until the end of list
                valid = False
                while not valid:
                    valid = True
                    # reached end of list
                    if current_lookups[i] == -1:
                        break
                    # entry is false
                    if not self.working_point[i][current_lookups[i]]:
                        valid = False
                        self.increment_lookup_index(current_lookups, i)
                    # avoid fixing changed (i, j) point
                    elif changed_i == i and changed_j == current_lookups[i]:
                        valid = False
                        self.increment_lookup_index(current_lookups, i)
                    # if this is a simulation check if entry has already been changed, if so - skip it
                    elif not modify_list and (i, current_lookups[i]) in changed_positions:
                        valid = False
                        self.increment_lookup_index(current_lookups, i)

                # check if lookup index i reached end of list
                if current_lookups[i] == -1:
                    continue
                if lowest_gain is None or lowest_gain > self.entry_matrix[i][current_lookups[i]].unit_gain:
                    lowest_gain = self.entry_matrix[i][current_lookups[i]].unit_gain
                    index_to_remove = i

            # remove current lowest unit gain
            if modify_list:
                self.working_point[index_to_remove][current_lookups[index_to_remove]] = False
            current_score -= self.entry_matrix[index_to_remove][current_lookups[index_to_remove]].score
            self.author_buffer[index_to_remove] -= self.entry_matrix[index_to_remove][current_lookups[index_to_remove]].contribution
            self.university_buffer -= self.entry_matrix[index_to_remove][current_lookups[index_to_remove]].contribution
            self.increment_lookup_index(current_lookups, index_to_remove)

        return current_score

    def increment_lookup_index(self, current_lookups, i):
        """
        Increments lookup index for university limit checking. If index reached end of list - set it to -1.
        """

        current_lookups[i] += 1
        if current_lookups[i] >= len(self.working_point[i]):
            current_lookups[i] = -1
