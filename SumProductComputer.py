class SumProductComputer:

    @staticmethod
    def print_generic_problem_description():
        print('----- Description -----')
        print('Checks every pair of (not equal) numbers, who are at least than arg_min (default 2, first parameter) '
              'and whose sum is not greater than than sum_max (default 100, second parameter).')
        print('Checks those pairs for the truth of these four statements:')
        print(' 1: Someone who knows the product does not know what the numbers are.')
        print(' 2: Someone who knows statement #1 and knows the sum does not know what the numbers are.')
        print(' 3: Someone who knows statements #1-2 and knows the product DOES know what the numbers are.')
        print(' 4: Someone who knows statements #1-3 and knows the sum DOES know what the numbers are.')
        print('Visit https://en.wikipedia.org/wiki/Sum_and_Product_Puzzle for details')

    def __init__(self, arg_min=2, sum_max=100, verbosity=3):
        self.arg_min = arg_min
        self.sum_max = sum_max
        self.possible_pairs = []

        # verbosity uses integer levels.
        # 1 = don't print anything
        # 2 = print everything
        # 3 and up = print the first n-2 levels.
        self.verbosity = self.set_verbosity(verbosity)
        self.depth = 0

    def compute_possible_pairs(self):
        self.depth = 0
        self.print_if('----- Checking Possibilities -----')

        for x in range(self.arg_min, self.largest_x()):
            for y in range(x, self.sum_max):

                if self.satisfies_conditions(x, y):
                    self.print_if('{0} and {1} satisfy the conditions!'.format(x, y))
                    self.possible_pairs.append((x, y))

        self.print_if('----- Finished -----')
        self.print_if('')

        return self.possible_pairs

    def print_problem_description(self):
        print('----- Description -----')
        print('Checks every pair of (not equal) numbers, who are at least than arg_min ({0}) '
              'and whose sum is not greater than sum_max ({1}).'.format(str(self.arg_min), str(self.sum_max)))
        print('Checks those pairs for the truth of these four statements:')
        print(' 1: Someone who knows the product does not know what the numbers are.')
        print(' 2: Someone who knows statement #1 and knows the sum does not know what the numbers are.')
        print(' 3: Someone who knows statements #1-2 and knows the product DOES know what the numbers are.')
        print(' 4: Someone who knows statements #1-3 and knows the sum DOES know what the numbers are.')
        print('Visit https://en.wikipedia.org/wiki/Sum_and_Product_Puzzle for details')
        print('')

    def print_parameters(self):
        print('----- Parameters -----')
        print('Y > X >= ' + str(self.arg_min))
        print('X + Y <= ' + str(self.sum_max))
        print('')

    def satisfies_conditions(self, x, y):
        if not self.satisfies_basic_conditions(x, y):
            return False

        if not self.satisfies_statements(x, y):
            return False

        return True

    def satisfies_statements(self, x, y):
        self.depth += 1
        satisfies_first = self.satisfies_first_statement(x, y)
        self.depth -= 1
        if not satisfies_first:
            self.print_if('{0} and {1} doesn\'t work. Someone who knows the product will '
                          'know what they are.'.format(x, y))
            return False

        self.depth += 1
        satisfies_second = self.satisfies_second_statement(x, y)
        self.depth -= 1
        if not satisfies_second:
            self.print_if('{0} and {1} doesn\'t work. Someone who knows the sum and statement #1'
                          ' will know what they are.'.format(x, y))
            return False

        return True

    def satisfies_basic_conditions(self, x, y):
        if self.x_gte_y(x, y):
            self.print_if('{0} and {1} doesn\'t work. x ({0}) is greater than '
                          'or equal to y ({1}).'.format(x, y))
            return False

        if self.arg_too_small(x):
            self.print_if('{0} and {1} doesn\'t work. {0} is not greater than {2}.'.format(x, y, self.arg_min))
            return False

        if self.sum_too_large(x, y):
            self.print_if('{0} and {1} doesn\'t work. Sum is greater than {2}.'.format(x, y, self.sum_max))
            return False

        return True

    # 1. Someone who knows their product will know what they are.
    def satisfies_first_statement(self, x, y):
        product = x * y

        self.depth += 1
        pairs = self.get_satisfactory_pairs_with_product(product, 2)
        self.depth -= 1

        if len(pairs) < 2:
            self.print_if('{0} and {1} doesn\'t satisfy #1. There does not exist two pairs with'
                          ' their product ({2})'.format(x, y, product))
            return False
        self.print_if('{0} and {1} satisfy #1! Someone who knows their product will not know what they are,'
                      ' since ({2},{3}) and ({4},{5}) have the same '
                      'product.'.format(x, y, pairs[0][0], pairs[0][1], pairs[1][0], pairs[1][1]))
        return True

    def satisfies_second_statement(self, x, y):
        sum = x + y
        possible_pairs = []

        self.depth += 1
        pairs = self.get_satisfactory_pairs_with_sum(sum, 2)
        self.depth -= 1

        if len(pairs) < 2:
            self.print_if('{0} and {1} doesn\'t satisfy #2. There does not exist two pairs whose sum is'
                          ' {2} and whose product is not defined by the constraints'.format(x, y, sum))
            return False

        self.print_if('{0} and {1} satisfy #2! Someone who knows their sum and statement #1 will not know what'
                      ' they are, since ({2},{3}) and ({4},{5}) satisfy the same conditions.'
                      .format(x, y, pairs[0][0], pairs[0][1], pairs[1][0], pairs[1][1]))
        return True


    def x_gte_y(self, x, y):
        return x >= y

    def arg_too_small(self, x):
        return x < self.arg_min

    def sum_too_large(self, x, y):
        return x + y > self.sum_max

    def get_satisfactory_pairs_with_product(self, target_product, max_pairs_to_find):
        satisfactory_pairs = []
        for possible_x in range(self.arg_min, min(target_product, self.largest_x())):
            if target_product % possible_x != 0:
                self.print_if('{0} doesn\'t work. It cannot be part of a satisfactory pair with product {1}.'
                              ' It is not a factor of {1}.'.format(possible_x, target_product))
                continue

            possible_y = target_product / possible_x

            self.depth += 1
            satisfies_basic = self.satisfies_basic_conditions(possible_x, possible_y)
            self.depth -= 1
            if satisfies_basic:
                self.print_if('{0} and {1} work! They can be used to create product {2}'
                              .format(possible_x, possible_y, target_product))

                satisfactory_pairs.append((possible_x, possible_y))
                if len(satisfactory_pairs) >= max_pairs_to_find:
                    break

            else:
                self.print_if('{0} and {1} doesn\'t work. They cannot be used to create product {2}.'
                              ' They do not satisfy the basic conditions'
                              .format(possible_x, possible_y, target_product))

        return satisfactory_pairs

    def get_satisfactory_pairs_with_sum(self, target_sum, max_pairs_to_find):
        satisfactory_pairs = []

        for possible_x in range(self.arg_min, target_sum):
            possible_y = target_sum - possible_x

            self.depth += 1
            satisfies_basic_conditions = self.satisfies_basic_conditions(possible_x, possible_y)
            self.depth -= 1

            if satisfies_basic_conditions:
                self.depth += 1
                satisfies_first = self.satisfies_first_statement(possible_x, possible_y)
                self.depth -= 1

                if satisfies_first:
                    self.print_if('{0} and {1} works! They add up to {2} and their product ({3})'
                                  ' does not discern their identity.'
                                  .format(possible_x, possible_y, target_sum, possible_x*possible_y))
                    satisfactory_pairs.append((possible_x, possible_y))
                    if len(satisfactory_pairs) >= max_pairs_to_find:
                        break
                else:
                    self.print_if('{0} and {1} doesn\'t work. Their product ({2}) discerns their identity.'
                                  .format(possible_x, possible_y, possible_x*possible_y))

            else:
                self.print_if('{0} and {1} doesn\'t work. They cannot be used to create sum {2} since'
                              ' they do not satisfy the basic conditions.'.format(possible_x, possible_y, target_sum))

        return satisfactory_pairs

    def largest_x(self):
        if self.sum_max % 2 == 0:
            return (self.sum_max / 2) - 1

        return (self.sum_max - 1) / 2

    # level is the depth of this print. the printed string will be indented that many times
    # additionally, a level of 0 is considered "high-level" and is printed in verbosity=2 situations. Nothing else is.
    def print_if(self, text):
        indent = '   '

        if self.verbosity == 1:
            return
        if self.verbosity == 2:
            print('{0}{1}'.format(indent * self.depth, text))
            return
        if self.verbosity > 2:
            if self.depth < self.verbosity-2:
                print('{0}{1}'.format(indent * self.depth, text))
                return
            else:
                return

        raise Exception('invalid verbosity level {0}'.format(self.verbosity))

    @staticmethod
    def set_verbosity(verbosity):
        if verbosity < 0:
            raise Exception('Invalid verbosity {0}. Must be above 0. 0=default, 1=nothing, 2=everything,'
                            ' 3+ = n-1 levels of text'.format(verbosity))
        if verbosity == 0:
            return 3
        return verbosity
