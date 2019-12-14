import utils
from simulated_annealing_penalty import SimulatedAnnealingPenalty
from simulated_annealing_repair import SimulatedAnnealingRepair
from input import generate_accepted_input
from output import generate_accepted_output
import filozofia_input
import matematyka_input
import informatyka_techniczna_telekomunikacja_input


def main(use_penalty, input_field, number_of_iterations=100, starting_temperature=90):

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
        simulated_annealing = SimulatedAnnealingPenalty(lp_matrix, score_matrix, contribution_matrix, author_limits, number_of_iterations, starting_temperature, 150, 200)
    else:
        simulated_annealing = SimulatedAnnealingRepair(lp_matrix, score_matrix, contribution_matrix, author_limits, number_of_iterations, starting_temperature)
    print("---Entry matrix (score, contribution, unit gain): ")
    utils.print_matrix(simulated_annealing.entry_matrix)
    print("---Random working point: ")
    utils.print_matrix(simulated_annealing.working_point)
    print("\n---Running Simulated Annealing...")
    working_point, score = simulated_annealing.simulated_annealing()
    print("\n---Last working_point:")
    utils.print_matrix(working_point)
    print(f"Last Score: {score}")
    print("\n---Best working_point:")
    utils.print_matrix(simulated_annealing.get_best_point())
    print(f"---Best score: {simulated_annealing.get_best_score()}")
    print("\n---Best working_point in original form:")
    utils.print_matrix(generate_accepted_output(simulated_annealing.entry_matrix, simulated_annealing.get_best_point(), n_rows, n_columns))


main(True, 'f', 10000)
