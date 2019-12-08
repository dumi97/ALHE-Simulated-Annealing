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

        # Debug prints and variables
        #
        # old_value = self.working_point[i][j]
        # print("[SimulatedAnnealingRepair Neighbour Score] For original point: ")
        # print_matrix(self.working_point)

        self.working_point[i][j] = not self.working_point[i][j]
        neighbour_score = self.calculate_score()

        # Debug prints
        #
        # print(f"unfixed score: {neighbour_score}")
        # print(f"unfixed author_buffers: {self.author_buffer}")
        # print(f"unfixed university_buffer: {self.university_buffer}")

        neighbour_score = self.check_and_fix(i, j, False, neighbour_score)

        # Debug prints and asserts
        #
        # print(f"For fixed neighbour point ({i}, {j}): ")
        # print_matrix(self.working_point)
        # print(f"score: {neighbour_score}")
        # print(f"fixed author_buffers: {self.author_buffer}")
        # print(f"fixed university_buffer: {self.university_buffer}")
        # for k in range(len(self.author_limit_list)):
        #     assert self.author_buffer[k] <= self.author_limit_list[i], f"Repair author {k} limit check failed - is {self.author_buffer[k]}, limit {self.author_limit_list[k]}"
        # assert self.university_buffer <= self.university_limit, f"Repair university limit check failed - is {self.university_buffer}, limit {self.university_limit}"

        self.working_point[i][j] = not self.working_point[i][j]

        # Debug prints
        #
        # print("Restored working point: ")
        # print_matrix(self.working_point)
        # assert self.working_point[i][j] == old_value, f"Matrix check failed - working point not restored (was {old_value}, is {self.working_point[i][j]})"

        return neighbour_score

    def modify_working_point(self, i, j):
        """
        Inverts bit (acceptance of article) of solution (working point) on specific coordinates.
        If solution is prohibited repairs it.
        """

        self.working_point[i][j] = not self.working_point[i][j]
        # calculate score to fill buffers
        self.calculate_score()
        self.check_and_fix(i, j, True, 0)

        # Debug prints
        #
        # for k in range(len(self.author_limit_list)):
        #     assert self.author_buffer[k] <= self.author_limit_list[i],f"Repair author {k} limit check failed - is {self.author_buffer[k]}, limit {self.author_limit_list[k]}"
        # assert self.university_buffer <= self.university_limit,f"Repair university limit check failed - is {self.university_buffer}, limit {self.university_limit}"
        # print(f"Point modified at ({i}, {j}) and returned as: ")
        # print_matrix(self.working_point)
        # print(f"modified author_buffers: {self.author_buffer}")
        # print(f"modified university_buffer: {self.university_buffer}")

    def check_and_fix(self, changed_i, changed_j, modify_list, current_score):
        """
        Repairs the current working point. It can also simulate repair and calculate score without changing the point.
        It will AVOID fixing the neighbour's changed (i, j) point even if it has the lowest unit gain
        """

        # Debug prints
        #
        # print("---------- Check-and-fix Starting") if modify_list else print("---------- Check-and-fix Simulation Starting")
        # print("---------- Fixing authors...")

        # check and fix author limits
        changed_positions = set()
        for i in range(len(self.working_point)):
            if self.author_buffer[i] <= self.author_limit_list[i]:
                continue
            for j in range(len(self.working_point[i])):
                if self.working_point[i][j] and (i != changed_i or j != changed_j):

                    print(f"---------- Fixing point ({i}, {j})")  # Debug

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

        # print("---------- Fixing university...")  # Debug

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
                        # print(f"---------- Point ({i}, {current_lookups[i]}) marked as changed in current simulation")  # Debug
                        valid = False
                        self.increment_lookup_index(current_lookups, i)


                # check if lookup index i reached end of list
                if current_lookups[i] == -1:
                    continue
                if lowest_gain is None or lowest_gain > self.entry_matrix[i][current_lookups[i]].unit_gain:
                    lowest_gain = self.entry_matrix[i][current_lookups[i]].unit_gain
                    index_to_remove = i

            # remove current lowest unit gain
            # print(f"---------- Fixing point ({index_to_remove}, {current_lookups[index_to_remove]})")  # Debug
            # assert self.working_point[index_to_remove][current_lookups[index_to_remove]] is True, f"Repair university fixing check failed - ({index_to_remove}, {current_lookups[index_to_remove]}) is already False"  # Debug
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

