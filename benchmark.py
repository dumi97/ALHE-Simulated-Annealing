import sys
import os

from main import main


class PrintWriter:
    def __init__(self, filename, stdout):
        self.file = open(filename, "w+")
        self.stdout = stdout

    def write(self, obj):
        self.file.write(obj)
        self.stdout.write(obj)

    def flush(self):
        self.file.flush()
        self.stdout.flush()


def benchmark(dir, use_penalty=False, input_field='f', number_of_iterations=100000, starting_temperature=9, author_penalty=150, university_penalty=200):
    os.mkdir(dir)
    stdout = sys.stdout
    sys.stdout = PrintWriter(dir + '/i1_log.txt', stdout)
    print("\nInitial working point: full zero matrix")
    main(use_penalty, input_field, number_of_iterations, starting_temperature, init_generation_mode=0, author_penalty=author_penalty, university_penalty=university_penalty)

    sys.stdout = PrintWriter(dir + '/i2_log.txt', stdout)
    print("\nInitial working point: full one matrix")
    main(use_penalty, input_field, number_of_iterations, starting_temperature, init_generation_mode=1, author_penalty=author_penalty, university_penalty=university_penalty)

    sys.stdout = PrintWriter(dir + '/i3_log.txt', stdout)
    print("\nInitial working point: normal heuristic matrix")
    main(use_penalty, input_field, number_of_iterations, starting_temperature, init_generation_mode=2, author_penalty=author_penalty, university_penalty=university_penalty)

    for i in range(1, 26):
        sys.stdout = PrintWriter(dir + f'/i{i+3}_log.txt', stdout)
        print(f"\n{i}. Initial working point: permutate heuristic matrix")
        main(use_penalty, input_field, number_of_iterations, starting_temperature, init_generation_mode=3, author_penalty=author_penalty, university_penalty=university_penalty)

if __name__ == '__main__':
    benchmark('./test', True, 'm', 300000, 17, 50, 30)
