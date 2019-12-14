def generate_accepted_output(lp_matrix, working_point, n_rows, n_columns):
    lp_row = 0
    output = []
    for i in range(n_rows):
        output_author = [0] * n_columns

        lp_author = lp_matrix[lp_row]

        lp_real_row = -1
        if lp_author != []:
            lp_real_row, _ = lp_author[0]

        if lp_real_row == i:
            working_point_row = working_point[lp_row]
            for j in range(len(lp_author)):
                _, column = lp_author[j]
                output_author[column] = int(working_point_row[j])

            lp_row += 1

        output.append(output_author)

    return output