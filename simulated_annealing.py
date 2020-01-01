import random
import math
import abc  # abc - Abstract Base Class
import copy
from entry import Entry

university_full_limit = 3.0


class SimulatedAnnealing(abc.ABC):
    def __init__(self, lp_matrix, score_matrix, contribution_matrix, author_limit_list, iteration_count, start_temperature):
        self.entry_matrix, self.working_point = self.build_initial_matrices(lp_matrix, score_matrix, contribution_matrix)
        self.author_limit_list = author_limit_list
        self.university_limit = university_full_limit*len(author_limit_list)
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
    def build_initial_matrices(lp_matrix, score_matrix, contribution_matrix):
        """
        Build the matrix of entries containing score, contribution and profit gain of each article, then sort it.
        Also generates first random working point matrix. Returns both generated matrices.
        """

        entry_matrix = []
        working_point = []
        for i in range(len(score_matrix)):
            lp_author = lp_matrix[i]
            score_author = score_matrix[i]
            contribution_author = contribution_matrix[i]

            entry_author = []
            working_point_author = []
            for j in range(len(score_author)):
                entry_author.append(Entry(lp_author[j], score_author[j], contribution_author[j]))
                working_point_author.append(bool(random.getrandbits(1)))

            entry_author.sort()
            entry_matrix.append(entry_author)
            working_point.append(working_point_author)

        return entry_matrix, working_point

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
        
        for i in range(self.current_iteration, iteration_count):
            self.current_iteration = i
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
