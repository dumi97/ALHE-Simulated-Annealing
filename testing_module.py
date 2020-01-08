import utils
from simulated_annealing_penalty import SimulatedAnnealingPenalty
from simulated_annealing_repair import SimulatedAnnealingRepair
from input import generate_accepted_input
from output import generate_accepted_output
import filozofia_input
import matematyka_input
import informatyka_techniczna_telekomunikacja_input


class TestingModule:
    def __init__(self, input_type="f", verbosity=0):
        # verbosity: 0 - no log file, 1 - log final result and basic info only, 2 - log whole result list, 3 - log everything
        self.verbosity = verbosity
        self.log_file = None
        self.used_field = None
        self.set_used_field(input_type)
        # temperature_results contain 2 tuples:
        #   1. lowest_iteration, lowest_iteration_score, lowest_iteration_temp
        #   2. lowest_best_score_iteration, best_score, best_score_lowest_iteration_temp
        self.temperature_results = []
        # penalty_results contain 2 tuples:
        #   1. lowest_iteration, lowest_iteration_score, lowest_iteration_auth_penalty, lowest_iteration_uni_penalty
        #   2. lowest_best_score_iteration, best_score, best_score_lowest_iteration_auth_penalty, best_score_lowest_iteration_uni_penalty
        self.penalty_results = []

    def log(self, min_verbosity, message):
        """
        Log a message to the log file if exists with specified minimum required verbosity.
        """
        if not self.log_file or self.verbosity < min_verbosity:
            return
        self.log_file.write(f"[{min_verbosity}] " + message + "\n")

    def set_used_field(self, input_type):
        if input_type == 'f':
            self.used_field = filozofia_input
        elif input_type == 'm':
            self.used_field = matematyka_input
        elif input_type == 'i':
            self.used_field = informatyka_techniczna_telekomunikacja_input
        else:
            self.used_field = filozofia_input

    def test_starting_temperature(self, number_of_iterations, min_temp, max_temp, temp_step, log_name="temperature_test_log.txt", log_type="w"):
        """
        Finds the temperature with the lowest number of iterations and the temperature with the best score and lowest
        number of iterations and puts them in temperature_results.
        """
        if max_temp < min_temp:
            print("Invalid temperature range")
            return

        if self.verbosity > 0:
            self.log_file = open(log_name, log_type)
            self.log(1, f"Testing temperature in range {min_temp}-{max_temp} with step {temp_step} for {number_of_iterations} iterations")

        lp_matrix, score_matrix, contribution_matrix, author_limits, n_rows, n_columns = generate_accepted_input(self.used_field)

        if temp_step < 1:
            temp_step = 1

        cur_temp = min_temp
        result_list = []
        while cur_temp <= max_temp:
            iteration_list = []
            sa = SimulatedAnnealingRepair(lp_matrix, score_matrix, contribution_matrix, author_limits, number_of_iterations, cur_temp, 0)

            for i in range(number_of_iterations):
                sa.simulated_annealing(1)
                iteration_list.append(sa.best_score)
                self.log(3, f"---cur_temp={cur_temp},\tannealing_iteration={len(iteration_list)},\tbest_score={sa.best_score}")

            iteration, best_score = self.find_last_iteration(iteration_list)
            result_list.append((cur_temp, iteration, best_score))

            self.log(2, f"cur_temp={cur_temp},\ttotal_iteration={iteration},\tbest_score={best_score}")

            cur_temp += temp_step

        self.get_temperature_results(result_list)
        self.log(1, f"Best iterations:\t\t\ttemp={self.temperature_results[0][2]}, iteration={self.temperature_results[0][0]}, score={self.temperature_results[0][1]}")
        self.log(1, f"Best iterations and score:\ttemp={self.temperature_results[1][2]}, iteration={self.temperature_results[1][0]}, score={self.temperature_results[1][1]}")
        if self.log_file:
            self.log_file.write("\n")
            self.log_file.close()
            self.log_file = None
        return

    def get_temperature_results(self, result_list):
        """
        Finds the temperature with lowest iterations and temperature with best score and lowest iterations in result_list.
        """
        lowest_iteration = -1
        lowest_iteration_score = 0
        lowest_iteration_temp = 0
        best_score = 0
        lowest_best_score_iteration = 0
        best_score_lowest_iteration_temp = 0
        for i in result_list:
            if lowest_iteration == -1 or i[1] < lowest_iteration:
                lowest_iteration_temp = i[0]
                lowest_iteration = i[1]
                lowest_iteration_score = i[2]

            if i[2] > best_score:
                best_score = i[2]
                lowest_best_score_iteration = i[1]
                best_score_lowest_iteration_temp = i[0]
            elif i[2] == best_score and i[1] < lowest_best_score_iteration:
                lowest_best_score_iteration = i[1]
                best_score_lowest_iteration_temp = i[0]

        self.temperature_results.append((lowest_iteration, lowest_iteration_score, lowest_iteration_temp))
        self.temperature_results.append((lowest_best_score_iteration, best_score, best_score_lowest_iteration_temp))

    def print_temperature_results(self):
        print("Last temperature test results:")
        print(f"Best iterations:\n\ttemp={self.temperature_results[0][2]}, iteration={self.temperature_results[0][0]}, score={self.temperature_results[0][1]}")
        print(f"Best iterations and score:\n\ttemp={self.temperature_results[1][2]}, iteration={self.temperature_results[1][0]}, score={self.temperature_results[1][1]}")

    def test_penalties(self, number_of_iterations, temperature, min_author, max_author, author_step, min_uni, max_uni, uni_step, log_name="penalty_test_log.txt", log_type="w"):
        """
        Finds penalties with the lowest number of iterations and penalties with the best score and lowest
        number of iterations and puts them in penalty_results.
        """
        if max_uni < min_uni or min_author < min_author:
            print("Invalid penalty range")
            return

        if self.verbosity > 0:
            self.log_file = open(log_name, log_type)
            self.log(1, f"Testing author penalty in range {min_author}-{max_author} with step {author_step} and "
                        f"university penalty in range {min_uni}-{max_uni} with step {uni_step} for {number_of_iterations} iterations with temperature {temperature}")

        lp_matrix, score_matrix, contribution_matrix, author_limits, n_rows, n_columns = generate_accepted_input(
            self.used_field)

        if author_step < 1:
            author_step = 1
        if uni_step < 1:
            uni_step = 1

        cur_author = min_author
        cur_uni = min_uni
        result_list = []
        while cur_uni < max_uni:
            while cur_author < max_author:
                iteration_list = []
                sa = SimulatedAnnealingPenalty(lp_matrix, score_matrix, contribution_matrix, author_limits,
                                               number_of_iterations, temperature, 0, cur_author, cur_uni)

                for i in range(number_of_iterations):
                    sa.simulated_annealing(1)
                    iteration_list.append(sa.best_score)
                    self.log(3, f"---cur_author={cur_author},\tcur_uni={cur_uni},\tannealing_iteration={len(iteration_list)},\tbest_score={sa.best_score}")

                iteration, best_score = self.find_last_iteration(iteration_list)
                result_list.append((cur_author, cur_uni, iteration, best_score))

                self.log(2, f"cur_author={cur_author},\tcur_uni={cur_uni},\ttotal_iteration={iteration},\tbest_score={best_score}")

                cur_author += author_step
            cur_uni += uni_step
            cur_author = min_author

        self.get_penalty_results(result_list)
        self.log(1, f"Best iterations:\t\t\tauthor={self.penalty_results[0][2]}, uni={self.penalty_results[0][3]}, iteration={self.penalty_results[0][0]}, score={self.penalty_results[0][1]}")
        self.log(1, f"Best iterations and score:\tauthor={self.penalty_results[1][2]}, uni={self.penalty_results[1][3]}, iteration={self.penalty_results[1][0]}, score={self.penalty_results[1][1]}")
        if self.log_file:
            self.log_file.write("\n")
            self.log_file.close()
            self.log_file = None
        return

    def get_penalty_results(self, result_list):
        """
        Finds the penalties with lowest iterations and penalties with best score and lowest iterations in result_list.
        """
        lowest_iteration = -1
        lowest_iteration_score = 0
        lowest_iteration_auth = 0
        lowest_iteration_uni = 0
        best_score = 0
        lowest_best_score_iteration = 0
        best_score_lowest_iteration_auth = 0
        best_score_lowest_iteration_uni = 0
        for i in result_list:
            if lowest_iteration == -1 or i[2] < lowest_iteration:
                lowest_iteration_auth = i[0]
                lowest_iteration_uni = i[1]
                lowest_iteration = i[2]
                lowest_iteration_score = i[3]

            if i[3] > best_score:
                best_score = i[3]
                lowest_best_score_iteration = i[2]
                best_score_lowest_iteration_uni = i[1]
                best_score_lowest_iteration_auth = i[0]
            elif i[3] == best_score and i[2] < lowest_best_score_iteration:
                lowest_best_score_iteration = i[2]
                best_score_lowest_iteration_uni = i[1]
                best_score_lowest_iteration_auth = i[0]

        self.penalty_results.append((lowest_iteration, lowest_iteration_score, lowest_iteration_auth, lowest_iteration_uni))
        self.penalty_results.append((lowest_best_score_iteration, best_score, best_score_lowest_iteration_auth, best_score_lowest_iteration_uni))

    def print_penalty_results(self):
        print("Last penalty test results:")
        print(f"Best iterations:\n\tauthor={self.penalty_results[0][2]}, uni={self.penalty_results[0][3]}, iteration={self.penalty_results[0][0]}, score={self.penalty_results[0][1]}")
        print(f"Best iterations and score:\n\tauthor={self.penalty_results[1][2]}, uni={self.penalty_results[1][3]}, iteration={self.penalty_results[1][0]}, score={self.penalty_results[1][1]}")

    @staticmethod
    def find_last_iteration(iteration_list):
        """
        Find when the last best value change occurred and what value it was.
        """
        last_score = iteration_list[len(iteration_list) - 1]
        for i in range(len(iteration_list) - 1, -1, -1):
            if last_score != iteration_list[i]:
                return i+2, last_score
        return 1, last_score


def test_temperature(iterations, mini, maxi, step, input_type="f", verbosity=0):
    module = TestingModule(input_type, verbosity)
    module.test_starting_temperature(iterations, mini, maxi, step)
    module.print_temperature_results()


def test_penalty(iterations, temperature, min_auth, max_auth, auth_step, min_uni, max_uni, uni_step, input_type="f", verbosity=0):
    module = TestingModule(input_type, verbosity)
    module.test_penalties(iterations, temperature, min_auth, max_auth, auth_step, min_uni, max_uni, uni_step)
    module.print_penalty_results()


# test_temperature(100, 10, 20, 1, verbosity=0)
test_penalty(100, 90, min_auth=10, max_auth=200, auth_step=10, min_uni=10, max_uni=100, uni_step=10, verbosity=0)
