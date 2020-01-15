from main import main

def benchmark(use_penalty=False, input_field='f', number_of_iterations=100000, starting_temperature=9):
    print("Initial working point: full zero matrix")
    main(use_penalty, input_field, number_of_iterations, starting_temperature, init_generation_mode=0)

    print("Initial working point: full one matrix")
    main(use_penalty, input_field, number_of_iterations, starting_temperature, init_generation_mode=1)

    print("Initial working point: normal heuristic matrix")
    main(use_penalty, input_field, number_of_iterations, starting_temperature, init_generation_mode=2)

    for i in range(25):
        print("1. Initial working point: permutate heuristic matrix")
        main(use_penalty, input_field, number_of_iterations, starting_temperature, init_generation_mode=3)

benchmark(False, 'f', 100000, 9)
