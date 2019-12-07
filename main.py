from test_data import score_matrix, contribution_matrix, author_limits
import utils
from simulated_annealing_penalty import SimulatedAnnealingPenalty
from simulated_annealing_repair import SimulatedAnnealingRepair


def main():
    print("Hello World!")
    # simulated_annealing = SimulatedAnnealingPenalty(score_matrix, contribution_matrix, author_limits, 100, 90, 150, 200)
    simulated_annealing = SimulatedAnnealingRepair(score_matrix, contribution_matrix, author_limits, 100, 90)
    print("Entry matrix (score, contribution, unit gain): ")
    utils.print_matrix(simulated_annealing.entry_matrix)
    print("Random working point: ")
    utils.print_matrix(simulated_annealing.working_point)
    working_point, score = simulated_annealing.simulated_annealing()
    print("Working_point:")
    utils.print_matrix(working_point)
    print(f"Score: {score}")


main()
