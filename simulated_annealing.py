import random
import math
import abc  # abc - Abstract Base Class
import copy
import random
from entry import Entry

university_full_limit = 3.0


class SimulatedAnnealing(abc.ABC):
    def __init__(self, lp_matrix, score_matrix, contribution_matrix, author_limit_list, iteration_count, start_temperature, init_generation_mode):
        self.entry_matrix = self.build_entry_matrix(lp_matrix, score_matrix, contribution_matrix)
        self.author_limit_list = author_limit_list
        self.university_limit = university_full_limit*len(author_limit_list)

        if init_generation_mode < 2:
            self.entry_matrix = self.sort_entry_matrix(self.entry_matrix)
            self.working_point = self.build_initial_working_point_matrix_fill(self.entry_matrix, init_generation_mode)
        elif init_generation_mode == 2:
            self.entry_matrix = self.sort_entry_matrix(self.entry_matrix)
            self.working_point = self.build_initial_working_point_matrix_heuristic(self.entry_matrix,  self.author_limit_list, self.university_limit)
        elif init_generation_mode == 3:
            self.entry_matrix = self.permutate_entry_matrix(self.entry_matrix)
            self.working_point = self.build_initial_working_point_matrix_heuristic(self.entry_matrix,  self.author_limit_list, self.university_limit)
            self.working_point = self.sort_working_point_matrix(self.entry_matrix, self.working_point)
            self.entry_matrix = self.sort_entry_matrix(self.entry_matrix)

        self.current_score = self.calculate_score()
        self.current_iteration = 0
        self.iteration_count = iteration_count
        self.start_temperature = start_temperature
        self.temperature = self.start_temperature
        self.best_point = copy.deepcopy(self.working_point)
        self.best_score = self.current_score

    @abc.abstractmethod
    def calculate_score(self):
        pass

    @abc.abstractmethod
    def calculate_neighbour_score(self, i, j):
        pass

    @abc.abstractmethod
    def modify_working_point(self, i, j):
        pass

    @staticmethod
    def build_entry_matrix(lp_matrix, score_matrix, contribution_matrix):
        """
        Build the matrix of entries containing score, contribution and profit gain of each article.
        Needs to be sorted after return.
        """

        entry_matrix = []
        for i in range(len(score_matrix)):
            lp_author = lp_matrix[i]
            score_author = score_matrix[i]
            contribution_author = contribution_matrix[i]

            entry_author = []
            for j in range(len(score_author)):
                entry_author.append(Entry(lp_author[j], score_author[j], contribution_author[j]))

            entry_matrix.append(entry_author)

        return entry_matrix

    @staticmethod
    def sort_entry_matrix(entry_matrix):
        """
        Sorts entry matrix.
        """

        for i in range(len(entry_matrix)):
            entry_matrix[i].sort()

        return entry_matrix

    @staticmethod
    def sort_working_point_matrix(entry_matrix, working_point):
        """
        Sorts working matrix according to entry matrix.
        Entry matrix must not be sorted.
        """

        entry_matrix = copy.deepcopy(entry_matrix)

        for i in range(len(entry_matrix)):
            author_entry_matrix = entry_matrix[i]
            for j in range(len(author_entry_matrix)):
                author_entry_matrix[j].lp = j

            author_entry_matrix.sort()

        sorted_working_point = []
        for i in range(len(entry_matrix)):
            author_entry_matrix = entry_matrix[i]
            author_working_point = working_point[i]

            length = len(author_entry_matrix)
            sorted_author_working_point = [False] * length
            for j in range(length):
                sorted_author_working_point[j] = author_working_point[author_entry_matrix[j].lp]

            sorted_working_point.append(sorted_author_working_point)

        return sorted_working_point

    @staticmethod
    def permutate_entry_matrix(entry_matrix):
        """
        Permutates entry matrix.
        Modifies entry matrix in argument.
        """

        for i in range(len(entry_matrix)):
            random.shuffle(entry_matrix[i])

        return entry_matrix

    @staticmethod
    def build_initial_working_point_matrix_fill(entry_matrix, fill):
        """
        Generates first working point matrix by filling structure with specified value.
        """

        working_point = []
        for entry_author in entry_matrix:
            working_point_author = [bool(fill)] * len(entry_author)
            working_point.append(working_point_author)

        return working_point

    @staticmethod
    def build_initial_working_point_matrix_heuristic(entry_matrix, author_limit_list, university_limit):
        """
        Generates first working point matrix by heuristic getting elements to contribution limits.
        """

        working_point = []
        university_contribution = 0
        for entry_author in entry_matrix:
            author_contribution = 0

            position = 0
            working_point_author = []
            for i in range(len(entry_author)):
                entry = entry_author[i]
                author_contribution += entry.contribution
                university_contribution += entry.contribution

                if author_contribution > author_limit_list[i] or university_contribution > university_limit:
                    author_contribution -= entry.contribution
                    university_contribution -= entry.contribution
                    break
                else:
                    position += 1

                working_point_author.append(True)

            for i in range(position, len(entry_author)):
                working_point_author.append(False)

            working_point.append(working_point_author)

        return working_point

    def save_best_point(self):
        self.best_point = copy.deepcopy(self.working_point)

    def get_best_point(self):
        return self.best_point

    def get_best_score(self):
        return self.best_score

    def simulated_annealing(self, iteration_count=0):
        """
        Makes iterations of simulated annealing algorithm.
        Returns working point and score of this point.
        While running specified iterations are made.
        """

        if iteration_count == 0:
            iteration_count = self.iteration_count
        else:
            iteration_count += self.current_iteration

            if iteration_count > self.iteration_count:
                iteration_count = self.iteration_count
        
        for i in range(self.current_iteration, iteration_count):
            self.current_iteration += 1
            self.update_temperature(i)
            self.iterate()

        return self.working_point, self.current_score

    def iterate(self):
        """
        One iteration of simulated annealing algorithm.
        Generates random neighbour point and makes decision about changing current working point with it.
        """

        i, j = self.generate_random_neighbour_change()
        neighbour_score = self.calculate_neighbour_score(i, j)

        if neighbour_score > self.current_score or random.random() <= self.calculate_acceptance_probability(neighbour_score):
            self.modify_working_point(i, j)
            self.current_score = neighbour_score
            if neighbour_score > self.best_score:
                self.best_score = neighbour_score
                self.save_best_point()

    def generate_random_neighbour_change(self):
        """
        Generates random coordinates for working point matrix.
        They can be used for random neighbour generation with change on one position in matrix.
        """

        i = random.randint(0, len(self.working_point)-1)
        j = random.randint(0, len(self.working_point[i])-1)

        return i, j

    def calculate_acceptance_probability(self, neighbour_score):
        """
        Calculates probability of accepting worse point than current working point.
        Checks if temperature is equal 0. In such situation it returns zero probability.
        """

        if self.temperature == 0:
            return 0
        else:
            return math.exp(-abs(self.current_score - neighbour_score) / self.temperature)

    def update_temperature(self, iteration):
        """
        Changes temperature depending on current iteration.
        new_temperature <- start_temperature * (iteration_count - iteration) / iteration_count
        """

        self.temperature = self.start_temperature * (self.iteration_count - iteration) / self.iteration_count
