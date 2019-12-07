from simulated_annealing import SimulatedAnnealing
from utils import print_matrix


class SimulatedAnnealingRepair(SimulatedAnnealing):
    def __init__(self, score_matrix, contribution_matrix, author_limit_list, iteration_count, start_temperature):
        self.author_buffer = []
        self.university_buffer = 0
        super().__init__(score_matrix, contribution_matrix, author_limit_list, iteration_count, start_temperature)

    def calculate_score(self):
        """
        Calculates score for working point stored in object.
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

        # Debug prints
        #
        # print("[SimulatedAnnealingRepair Score] For working point: ")
        # print_matrix(self.working_point)
        # print(f"calculated score: {total_score}")
        # print(f"author_buffers: {self.author_buffer}")
        # print(f"university_buffer: {self.university_buffer}")

        return total_score

    def calculate_neighbour_score(self, i, j):
        """
        Calculates neighbour score with simulated repair without modifications.
        It does not change working point.
        """
        
        original_working_point = self.working_point

        # Debug prints
        #
        # print("[SimulatedAnnealingRepair Neighbour Score] For original point: ")
        # print_matrix(self.working_point)

        self.modify_working_point(i, j)
        neighbour_score = self.calculate_score()

        # Debug prints and asserts
        #
        # print(f"For fixed neighbour point ({i}, {j}): ")
        # print_matrix(self.working_point)
        # print(f"score: {neighbour_score}")
        # print(f"fixed author_buffers: {self.author_buffer}")
        # print(f"fixed university_buffer: {self.university_buffer}")
        # for i in range(len(self.author_limit_list)):
        #     assert self.author_buffer[i] <= self.author_limit_list[i],f"Repair author {i} limit check failed - is {self.author_buffer[i]}, limit {self.author_limit_list[i]}"
        # assert self.university_buffer <= self.university_limit,f"Repair university limit check failed - is {self.university_buffer}, limit {self.university_limit}"

        self.working_point = original_working_point
        return neighbour_score

    def modify_working_point(self, i, j):
        """
        Inverts bit (acceptance of article) of solution (working point) on specific coordinates.
        If solution is prohibited repairs it.
        """

        self.working_point[i][j] = not self.working_point[i][j]
        # calculate score to fill buffers
        self.calculate_score()

        # Debug prints
        #
        # print(f"author_buffers: {self.author_buffer}")
        # print(f"university_buffer: {self.university_buffer}")

        self.check_and_fix(i, j)

    def check_and_fix(self, changed_i, changed_j):
        """
        Repairs the current working point. This method does change the working point.
        It will AVOID fixing the neighbour's changed (i, j) point even if it has the lowest unit gain
        """

        # print("---------- Check-and-fix Starting\n---------- Fixing authors...")  # Debug

        # check and fix author limits
        for i in range(len(self.working_point)):
            if self.author_buffer[i] <= self.author_limit_list[i]:
                continue
            for j in range(len(self.working_point[i])):
                if self.working_point[i][j] and (i != changed_i or j != changed_j):

                    # print(f"---------- Fixing point ({i}, {j})")  # Debug

                    self.working_point[i][j] = False
                    self.author_buffer[i] -= self.entry_matrix[i][j].contribution
                    if self.author_buffer[i] <= self.author_limit_list[i]:
                        break

        # check and fix university limit
        if self.university_buffer <= self.university_limit:
            return

        # print("---------- Fixing university...")  # Debug

        current_lookups = [0] * len(self.working_point)
        while self.university_buffer > self.university_limit:
            lowest_gain = None
            index_to_remove = None

            # find current lowest unit gain to remove
            for i in range(len(current_lookups)):
                # search for the first True value until the end of list
                while not self.working_point[i][current_lookups[i]] or current_lookups[i] == -1:
                    self.increment_lookup_index(current_lookups, i)
                    # avoid fixing changed (i, j) point
                    if changed_i == i and changed_j == current_lookups[i]:
                        self.increment_lookup_index(current_lookups, i)

                # check if lookup index i reached end of list
                if current_lookups[i] == -1:
                    continue
                if lowest_gain is None or lowest_gain > self.entry_matrix[i][current_lookups[i]].unit_gain:
                    lowest_gain = self.entry_matrix[i][current_lookups[i]].unit_gain
                    index_to_remove = i

            # remove current lowest unit gain
            # print(f"---------- Fixing point ({index_to_remove}, {current_lookups[index_to_remove]})")  # Debug
            # assert self.working_point[index_to_remove][current_lookups[index_to_remove]] is True,f"Repair university fixing check failed - ({index_to_remove}, {current_lookups[index_to_remove]}) is already False"  # Debug
            self.working_point[index_to_remove][current_lookups[index_to_remove]] = False
            self.university_buffer -= self.entry_matrix[index_to_remove][current_lookups[index_to_remove]].contribution
            self.increment_lookup_index(current_lookups, index_to_remove)

    def increment_lookup_index(self, current_lookups, i):
        """
        Increments lookup index for university limit checking. If index reached end of list - set it to -1.
        """

        current_lookups[i] += 1
        if current_lookups[i] >= len(self.working_point[i]):
            current_lookups[i] = -1

