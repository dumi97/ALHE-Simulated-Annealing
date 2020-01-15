import utils
from simulated_annealing_penalty import SimulatedAnnealingPenalty
from simulated_annealing_repair import SimulatedAnnealingRepair
from input import generate_accepted_input
from output import generate_accepted_output
import filozofia_input
import matematyka_input
import informatyka_techniczna_telekomunikacja_input


def get_author_article_pairs_count(working_point):
    count = 0
    for row in working_point:
        count += len(row)

    return count


def print_best(iteration, simulated_annealing, n_rows, n_columns):
    if simulated_annealing.get_best_point() != -1:
        print(f"\n---{iteration} iteration best working_point:")
        utils.print_matrix(simulated_annealing.get_best_point())
        print(f"---{iteration} iteration best score: {simulated_annealing.get_best_score()}")
        print(f"--{iteration} iteration best iteration: {simulated_annealing.best_score_iteration}")
        print(f"\n---{iteration} iteration best working point in original form:")
        utils.print_matrix(generate_accepted_output(simulated_annealing.entry_matrix, simulated_annealing.get_best_point(), n_rows, n_columns))
    else:
        print("\n---No best working_point!!! No feasible solution found!!!")


def main(use_penalty, input_field, number_of_iterations=100000, starting_temperature=90, init_generation_mode=0):

    if input_field == 'f':
        used_input = filozofia_input
    elif input_field == 'm':
        used_input = matematyka_input
    elif input_field == 'i':
        used_input = informatyka_techniczna_telekomunikacja_input
    else:
        print("---Unknown input field")
        return

    lp_matrix, score_matrix, contribution_matrix, author_limits, n_rows, n_columns = generate_accepted_input(used_input)
    if use_penalty:
        simulated_annealing = SimulatedAnnealingPenalty(lp_matrix, score_matrix, contribution_matrix, author_limits, number_of_iterations, starting_temperature, init_generation_mode, 150, 200)
    else:
        simulated_annealing = SimulatedAnnealingRepair(lp_matrix, score_matrix, contribution_matrix, author_limits, number_of_iterations, starting_temperature, init_generation_mode)
    
    pair_count = get_author_article_pairs_count(simulated_annealing.working_point)
    print(f"---Pair author/article count: {pair_count}")

    if number_of_iterations < 1000*pair_count:
        print("Too small number of iterations")
        print(f"Should be greater or equal: {1000*pair_count}")
        return
    
    print("---Entry matrix (score, contribution, unit gain): ")
    utils.print_matrix(simulated_annealing.entry_matrix)
    print("---Init working point: ")
    utils.print_matrix(simulated_annealing.working_point)
    print("\n---Init working point in original form:")
    utils.print_matrix(generate_accepted_output(simulated_annealing.entry_matrix, simulated_annealing.working_point, n_rows, n_columns))

    stop_list = [1, 10*pair_count, 100*pair_count, 1000*pair_count]

    print("\n---Running Simulated Annealing...")
    prev_iteration = 0
    for stop in stop_list:
        iterations = stop - prev_iteration

        working_point, score = simulated_annealing.simulated_annealing(iterations)
        prev_iteration = stop

        print(f"---After {stop} iterations:")
        print(f"---{simulated_annealing.best_score_iteration} best iteration score: {simulated_annealing.get_best_score()}")

    print_best(prev_iteration, simulated_annealing, n_rows, n_columns)

    working_point, score = simulated_annealing.simulated_annealing()
    print_best(number_of_iterations, simulated_annealing, n_rows, n_columns)

if __name__ == '__main__':
    main(False, 'f', 100000)
