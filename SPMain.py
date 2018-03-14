from SumProductComputer import SumProductComputer

# Checks every pair of (not equal) numbers, who are greater than 1 (xy_min) and whose sum is smaller than 100 (sum_max).
# Checks those pairs for the truth of these four statements:
#  1: Someone who knows the product does not know what the numbers are.
#  2: Someone who knows statement #1 and knows the sum does not know what the numbers are.
#  3: Someone who knows statements #1-2 and knows the product DOES know what the numbers are.
#  4: Someone who knows statements #1-3 and knows the sum DOES know what the numbers are.
def main():
    print("######### Starting Sum Product problem ##############")

    xy_min = 2
    sum_max = 50

    sp_computer = SumProductComputer(xy_min, sum_max, 2)

    sp_computer.print_problem_description()
    sp_computer.print_parameters()

    answers = sp_computer.compute_possible_pairs()

    print_answers(answers)
    print("######### Finished Sum Product problem ##############")


def print_answers(answer_tuples):
    print('Answers:')
    for answer_tuple in answer_tuples:
        print('  {0}'.format(answer_tuple))


main()