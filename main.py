from test_data import score_matrix, contribution_matrix, author_limits
import utils


def main():
    print("Hello World!")
    (entry_matrix, working_point) = utils.build_initial_matrices(score_matrix, contribution_matrix)
    print("Entry matrix (score, contribution, unit gain): ")
    utils.print_matrix(entry_matrix)
    print("Random working point: ")
    utils.print_matrix(working_point)
    for i in range(3):
        utils.iterate(entry_matrix, working_point)


main()
