from test_data import score_matrix, contribution_matrix, author_limits
import utils
from simulated_annealing_penalty import SimulatedAnnealingPenalty
from simulated_annealing_repair import SimulatedAnnealingRepair
from input import generate_accepted_input
from output import generate_accepted_output
import filozofia_input
import informatyka_techniczna_telekomunikacja_input

def main():
    print("Hello World!")
    lp_matrix, score_matrix, contribution_matrix, author_limits, n_rows, n_columns = generate_accepted_input(filozofia_input)
    # simulated_annealing = SimulatedAnnealingPenalty(score_matrix, contribution_matrix, author_limits, 100, 90, 150, 200)
    simulated_annealing = SimulatedAnnealingRepair(lp_matrix, score_matrix, contribution_matrix, author_limits, 100, 90)
    print("Entry matrix (score, contribution, unit gain): ")
    utils.print_matrix(simulated_annealing.entry_matrix)
    print("Random working point: ")
    utils.print_matrix(simulated_annealing.working_point)
    working_point, score = simulated_annealing.simulated_annealing()
    print("Last working_point:")
    utils.print_matrix(working_point)
    print(f"Last Score: {score}")
    print("Best working_point:")
    utils.print_matrix(simulated_annealing.get_best_point())
    print(f"Best score: {simulated_annealing.get_best_score()}")
    print("Best working_point in orginal form:")
    utils.print_matrix(generate_accepted_output(simulated_annealing.entry_matrix, simulated_annealing.get_best_point(), n_rows, n_columns))

main()
