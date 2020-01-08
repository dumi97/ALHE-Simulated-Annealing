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
        if max_temp < min_temp:
            print("Invalid temperature range")
            return

        if self.verbosity > 0:
            self.log_file = open(log_name, log_type)
            self.log(1, f"Testing temperature in range {min_temp}-{max_temp} with step {temp_step} for {number_of_iterations} iterations")

        lp_matrix, score_matrix, contribution_matrix, author_limits, n_rows, n_columns = generate_accepted_input(self.used_field)
        cur_temp = min_temp

        if temp_step < 1:
            temp_step = 1

        result_list = []
        while cur_temp <= max_temp:
            iteration_list = []
            sa = SimulatedAnnealingRepair(lp_matrix, score_matrix, contribution_matrix, author_limits,
                                           number_of_iterations, cur_temp, 0)

            for i in range(number_of_iterations):
                sa.simulated_annealing(1)
                iteration_list.append(sa.best_score)
                self.log(3, f"---cur_temp={cur_temp}, annealing_iteration={len(iteration_list)}, best_score={sa.best_score}")

            iteration, best_score = self.find_last_iteration(iteration_list)
            result_list.append((cur_temp, iteration, best_score))

            self.log(2, f"cur_temp={cur_temp}, total_iteration={iteration}, best_score={best_score}")

            cur_temp += temp_step

        self.get_temperature_results(result_list)
        self.log(1, f"Best iterations:\t\t\ttemp={self.temperature_results[0][2]}, iteration={self.temperature_results[0][0]}, score={self.temperature_results[0][1]}")
        self.log(1, f"Best iterations and score:\ttemp={self.temperature_results[1][2]}, iteration={self.temperature_results[1][0]}, score={self.temperature_results[1][1]}")
        if self.log_file:
            self.log_file.close()
            self.log_file = None
        return

    def get_temperature_results(self, result_list):
        """
        Finds the temperature with lowest iterations and temperature with best score and lowest iterations.
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
        print(f"Best iterations:\n\ttemp={self.temperature_results[0][2]}, iteration={self.temperature_results[0][0]}, score={self.temperature_results[0][1]}")
        print(f"Best iterations and score:\n\ttemp={self.temperature_results[1][2]}, iteration={self.temperature_results[1][0]}, score={self.temperature_results[1][1]}")



    @staticmethod
    def find_last_iteration(iteration_list):
        """
        Find when the last best value change occurred and what value it was.
        """
        last_score = iteration_list[len(iteration_list) - 1]
        for i in range(len(iteration_list) - 1, -1, -1):
            if last_score != iteration_list[i]:
                return i, last_score
        return 1, last_score


def test_temperature(iterations, mini, maxi, step, input_type="f", verbosity=0):
    module = TestingModule(input_type, verbosity)
    module.test_starting_temperature(iterations, mini, maxi, step)
    module.print_temperature_results()


test_temperature(100, 10, 20, 1, verbosity=0)
