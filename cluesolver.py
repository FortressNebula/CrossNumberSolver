from functools import *
from math import *

# helper functions, probably dont touch these
# returns the nth digit of x as a string
def get_digit(x, n):
    return str(x)[n]

# returns the nth digit of x as an integer. if you need to get a specific digit, this is probably what you want.
def int_get_digit(x, n):
    return int(get_digit(x, n))

# reverses the digits of a number
def reverse(x):
    return int(str(x)[::-1])

def check_clue_digits(value, value_digit, clue, clue_digit, olution_set):
    return not (clue in olution_set and get_digit(value, value_digit) != get_digit(olution_set[clue], clue_digit))

def digit_sum(n):
   r = 0
   while n:
       r, n = r + n % 10, n // 10
   return r

def digit_product(n):
   r = 1
   while n:
       r, n = r * (n % 10), n // 10
   return r

# clue checking
# add functions to check the digits for each clue
# for example, if the second digit of 4ac was the same as the first digit of 5dn:
# (remember indexing starts at zero)
#
# def check_4ac(value, solution_set):
#     return check_clue_digits(value, 1, '5dn', 0, solution_set)
# def check_5dn(value, solution_set):
#     return check_clue_digits(value, 0, '4ac', 1, solution_set)

def check_clue(clue, value, solution_set):
    pass

    # connect the clue to the function here
    # e.g.
    # if clue == '1ac': return check_1ac(value, solution_set)
    

class Clue:
    # basic clue, if you need to create a special kind of clue then make a subclass of this
    def __init__(self):
        self.solutions = []
    
    # the point of a clue is to provide a list of possible solutions for it. for special clues, the subclass 
    # should override this and return some special list of possibilities.
    #
    # `solution_set` is a list of all the values for puzzles that have been calculated so far. if a clue
    # is dependent on another then you can reference it here.
    # e.g. if 1dn was the digit sum of 2dn:
    # return digit_sum(solution_set['2dn'])
    def get_solutions(self, solution_set):
        return self.solutions
    
class OpenClue(Clue):
    # an open clue. no constraints, so possible solutions are any number for the specified digit length.
    def __init__(self, length):
        self.solutions = [i for i in range(10**(length - 1), 10**length)]

class FixedClue(Clue):
    # a fixed clue. a specific set of numbers that this clue can hold
    def __init__(self, solutions):
        self.solutions = solutions

class TransformativeClue(Clue):
    # a general class for clues that transform others. e.g. digit sum of 2ac, digit product of 5dn, etc
    # for the `transformation` specify a function that takes in a solution set and returns a list of possible values
    # e.g.
    # def clue_3ac(solution_set):
    #   return [solution_set['1ac'] + digit_product(solution_set['1ac])] # yes even single values need to be in a list
    # three_across = TransformativeClue(clue_3ac)
    def __init__(self, transformation):
        self.transformation = transformation

    def get_solutions(self, solution_set):
        return self.transformation(solution_set)
    
# triplet classes are more complicated. the idea is its useful for clues where all three clues are part of some triplet
# e.g. a pythagorean triple.
# the primary secondary tertiary order is based on what order you put the clues in the solve_order list
# for more information on this, just ask me
class TripletPrimaryClue(Clue):
    def __init__(self, triplets, digits=0):
        self.solutions = []
        self.digits = digits
        for triplet in triplets:
            # pick any valid value
            for element in triplet:
                if len(str(element)) == self.digits or self.digits == 0:
                    self.solutions.append(element)

class TripletSecondaryClue(Clue):
    def __init__(self, triplets, primary, digits=0):
        self.primary = primary
        self.triplets = triplets
        self.digits = digits
    
    def get_solutions(self, solution_set):
        # find the solution that contains the value of the primary
        out = []
        for triplet in self.triplets:
            if solution_set[self.primary] in triplet:
                for element in triplet:
                    if element == solution_set[self.primary]:
                        continue
                    if len(str(element)) == self.digits or self.digits == 0:
                        out.append(element)
        return out

class TripletTertiaryClue(Clue):
    def __init__(self, triplets, primary, secondary, digits=0):
        self.primary = primary
        self.secondary = secondary
        self.triplets = triplets
        self.digits = digits
    
    def get_solutions(self, solution_set):
        # find the solution that contains the value of the primary
        for triplet in self.triplets:
            if solution_set[self.primary] in triplet and solution_set[self.secondary] in triplet:
                out = triplet.copy()
                out.remove(solution_set[self.primary])
                out.remove(solution_set[self.secondary])
                if len(str(out[0])) == self.digits or self.digits == 0:
                    return out
        return []

# the actual puzzle class. modify this 
class Puzzle:
    def __init__(self):
        # clues
        self.clues = {
            
        }
        # the order in which the DFS runs
        # this is important because if a clue is dependent on others (e.g. 5ac is equal to digit sum of 1dn) then it must be solved after
        # this must be specified manually 
        self.solve_order = []
    
    # use this to register new clues
    # dont change the function, simply call it
    def add_clue(self, name, length):
        self.clues[name] = OpenClue(length)
    
    # dont change this
    def get_current_clue(self, solution_set: dict):
        for clue in self.solve_order:
            if clue not in solution_set:
                return clue
        return 'NONE'
    
    # you can change this
    # once the program has found a possible set of values that work, you can perform any final checks here, like making sure all digits are used equally
    # return true if the solution is valid
    def final_constraints(solution_set):
        return True

    # dont change this
    def solve(self):
        if len(self.solve_order) != len(self.clues.keys()):
            raise ValueError("Solving order must be assigned!")
        
        stack = [{}]

        # essentially doing a DFS in the possibity tree.
        # for each item in the stack, add all the branches of the possibility tree.
        while len(stack) > 0:
            solution_set = stack.pop()
            current_clue = self.get_current_clue(solution_set)

            if current_clue == 'NONE':
                # we made it to the end of a tree branch without hitting a contradiction, we made it! 
                if self.final_constraints(solution_set):
                    print(solution_set)
                continue
            
            # using the clue, get a list of possible values for the clue.
            possible_values_for_clue = self.clues[current_clue].get_solutions(solution_set)
            # remove redundant possibilites
            possible_values_for_clue = list(dict.fromkeys(possible_values_for_clue))
            # cull possibilities
            possible_values_for_clue = list(filter(lambda x : check_clue(current_clue, x, solution_set), possible_values_for_clue))

            for value in possible_values_for_clue:
                # add the child node
                new_set = solution_set.copy()
                new_set[current_clue] = value
                stack.append(new_set)


