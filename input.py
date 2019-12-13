full_author_limit = 4.0

def generate_accepted_input(input_data):
    """
    Gets global matrixes and changes them to accepted form by simulated annealing algorithm.
    """

    return convert_input(input_data.w, input_data.u, input_data.pracownik, input_data.doktorant, input_data.udzial)

def convert_input(score_matrix, contribution_matrix, worker, doctoral, area_author_percentage_list):
    """
    Converts and calculates matrixes that are accepted by simulated annealing algorithm.
    Input matrixes contains authors that has zero contribution for specific articles - it is unnecessary data for simulated annealing algorithm.
    Unnecessary data is removed from matrixes.
    Author article limit has to be calculated based on area percentage and worker's university.
    It returns: matrix with orginal positions in matrix before removal (lp), dense score matrix, dense contribution matrix and calculated author_limit_list for specific domain.
    """

    author_limit_list = get_author_limit_list(worker, doctoral, area_author_percentage_list)
    return convert_matrixes_to_dense(score_matrix, contribution_matrix, author_limit_list)

def get_author_limit_list(worker, doctoral, area_author_percentage_list):
    """
    Calculates author articles contribution limit and checks if person is from university.
    Contribution limit is calculated by multiplying full author percentage limit and author's percentage in specific area.
    If author is not from university (is not worker and not doctoral of university), author limit percentage will be equal zero.
    """

    author_limit_list = []
    for i in range(len(area_author_percentage_list)):
        if worker[i] or doctoral[i]:
            author_limit_list.append(area_author_percentage_list[i] * full_author_limit)
        else:
            author_limit_list.append(0.0)

    return author_limit_list

def convert_matrixes_to_dense(score_matrix, contribution_matrix, author_limit_list):
    """
    Converts input matrixes to dense one.
    Input matrixes contains authors that has zero contribution for specific articles - it is unnecessary data for simulated annealing algorithm.
    Unnecessary data is removed from matrixes.
    It returns: matrix with orginal positions in matrix before removal (lp), dense score matrix, dense contribution matrix and calculated author_limit_list for specific domain.
    """

    lp_matrix = []
    dense_score_matrix = []
    dense_contribution_matrix = []
    dense_author_limit_list = []
    for i in range(len(contribution_matrix)):
        author_score = score_matrix[i]
        author_contribution = contribution_matrix[i]
        author_limit = author_limit_list[i]

        if author_limit != 0.0:
            dense_author_lp, dense_author_score, dense_author_contribution = convert_author_lists_to_dense(i, author_score, author_contribution)
            
            lp_matrix.append(dense_author_lp)
            dense_score_matrix.append(dense_author_score)
            dense_contribution_matrix.append(dense_author_contribution)
            dense_author_limit_list.append(author_limit)
        
    return lp_matrix, dense_score_matrix, dense_contribution_matrix, dense_author_limit_list

def convert_author_lists_to_dense(row, author_score, author_contribution):
    """
    Converts author's percentage contribution list to dense one.
    It removes articles that has no contribution by author (contribution is equal zero).
    Returns: coordinate matrix of position in original data, dense author score list and dense author contribution list.
    """

    dense_author_lp = []
    dense_author_score = []
    dense_author_contribution = []
    for j in range(len(author_contribution)):
        contribution = author_contribution[j]
        if contribution != 0:
            dense_author_lp.append((row, j))
            dense_author_score.append(author_score[j])
            dense_author_contribution.append(contribution)

    return dense_author_lp, dense_author_score, dense_author_contribution