from main import main

def benchmark(use_penalty=False, input_field='f', number_of_iterations=100000, starting_temperature=9):
    print("\nInitial working point: full zero matrix")
    main(use_penalty, input_field, number_of_iterations, starting_temperature, init_generation_mode=0)

    print("\nInitial working point: full one matrix")
    main(use_penalty, input_field, number_of_iterations, starting_temperature, init_generation_mode=1)

    print("\nInitial working point: normal heuristic matrix")
    main(use_penalty, input_field, number_of_iterations, starting_temperature, init_generation_mode=2)

    for i in range(1, 26):
        print(f"\n{i}. Initial working point: permutate heuristic matrix")
        main(use_penalty, input_field, number_of_iterations, starting_temperature, init_generation_mode=3)

if __name__ == '__main__':
    benchmark(False, 'f', 100000, 9)
