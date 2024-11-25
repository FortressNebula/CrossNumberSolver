from functools import *
from math import *

log_file = open('log_copy2.txt', 'wt')

def get_digit(x, digit):
    return str(x)[digit]

def int_get_digit(x, digit):
    return int(get_digit(x, digit))

def check_clue_digits(value, value_digit, clue, clue_digit, olution_set):
    return not (clue in olution_set and get_digit(value, value_digit) != get_digit(olution_set[clue], clue_digit))

def digit_sum(n):
   r = 0
   while n:
       r, n = r + n % 10, n // 10
   return r

# clue checking
def check_1ac(value, solution_set):
    return check_clue_digits(value, 0, '1dn', 0, solution_set)
def check_1dn(value, solution_set):
    return check_clue_digits(value, 0, '1ac', 0, solution_set)
def check_2ac(value, solution_set):
    return check_clue_digits(value, 1, '3dn', 0, solution_set) and check_clue_digits(value, 0, '2dn', 0, solution_set)
def check_2dn(value, solution_set):
    return check_clue_digits(value, 2, '11ac', 0, solution_set) and check_clue_digits(value, 0, '2ac', 0, solution_set)

def check_3dn(value, solution_set):
    return check_clue_digits(value, 2, '11ac', 1, solution_set) and check_clue_digits(value, 0, '2ac', 1, solution_set)
def check_4ac(value, solution_set):
    return check_clue_digits(value, 1, '5dn', 0, solution_set)
def check_5dn(value, solution_set):
    return check_clue_digits(value, 0, '4ac', 1, solution_set)

def check_7dn(value, solution_set):
    return check_clue_digits(value, 2, '13ac', 1, solution_set)
def check_9dn(value, solution_set):
    return check_clue_digits(value, 2, '14ac', 1, solution_set)
def check_10dn(value, solution_set):
    return check_clue_digits(value, 1, '13ac', 0, solution_set)

def check_11ac(value, solution_set):
    return check_clue_digits(value, 0, '2dn', 2, solution_set) and check_clue_digits(value, 1, '3dn', 2, solution_set)
def check_12dn(value, solution_set):
    return check_clue_digits(value, 1, '14ac', 2, solution_set)
def check_13ac(value, solution_set):
    return check_clue_digits(value, 0, '10dn', 1, solution_set) and check_clue_digits(value, 1, '7dn', 2, solution_set)
def check_14ac(value, solution_set):
    return check_clue_digits(value, 2, '12dn', 1, solution_set) and check_clue_digits(value, 1, '9dn', 2, solution_set)

def check_clue(clue, value, solution_set):
    if clue == '1ac': return check_1ac(value, solution_set)
    if clue == '1dn': return check_1dn(value, solution_set)
    if clue == '2ac': return check_2ac(value, solution_set)
    if clue == '2dn': return check_2dn(value, solution_set)
    if clue == '3dn': return check_3dn(value, solution_set)
    if clue == '4ac': return check_4ac(value, solution_set)
    if clue == '5dn': return check_5dn(value, solution_set)
    if clue == '7dn': return check_7dn(value, solution_set)
    if clue == '9dn': return check_9dn(value, solution_set)
    if clue == '10dn': return check_10dn(value, solution_set)
    if clue == '11ac': return check_11ac(value, solution_set)
    if clue == '12dn': return check_12dn(value, solution_set)
    if clue == '13ac': return check_13ac(value, solution_set)
    if clue == '14ac': return check_14ac(value, solution_set)
    

class Clue:
    def __init__(self):
        self.solutions = []
    
    def get_solutions(self, solution_set):
        return self.solutions
    
class OpenClue(Clue):
    def __init__(self, length):
        self.solutions = [i for i in range(10**(length - 1), 10**length)]

class FixedClue(Clue):
    def __init__(self, solutions):
        self.solutions = solutions

class TransformativeClue(Clue):
    def __init__(self, transformation):
        self.transformation = transformation

    def get_solutions(self, solution_set):
        return self.transformation(solution_set)
    
# triplet syntactic sugar
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

class Puzzle:
    def __init__(self):
        # clues
        self.clues = {
            '1ac' : OpenClue(2),
            '1dn' : OpenClue(2),
            '2ac' : OpenClue(2),
            '2dn' : OpenClue(3),
            '3dn' : OpenClue(3),
            '4ac' : OpenClue(2),
            '5dn' : OpenClue(2),
            '7dn' : OpenClue(3),
            '9dn' : OpenClue(3),
            '10dn' : OpenClue(2),
            '11ac' : OpenClue(2),
            '12dn' : OpenClue(2),
            '13ac' : OpenClue(3),
            '14ac' : OpenClue(3),
        }

        self.solve_order = []
    
    def get_current_clue(self, solution_set: dict):
        for clue in self.solve_order:
            if clue not in solution_set:
                return clue
        return 'NONE'

    def final_constraints(self, solution_set):
        ac6 = int_get_digit(solution_set['1dn'], 1)*100 + int_get_digit(solution_set['7dn'], 0) * 10 + int_get_digit(solution_set['2dn'], 1)
        ac8 = int_get_digit(solution_set['5dn'], 1) + int_get_digit(solution_set['9dn'], 0) * 10 + int_get_digit(solution_set['3dn'], 1)*100
        
        if ac6 < 100 or ac8 < 100:
            return False
        
        solution_set['6ac'] = ac6
        solution_set['8ac'] = ac8
        answers = list(solution_set.values())
        
        # ensure there are no duplicate answers
        invalid = False
        for i, a in enumerate(answers):
            for j, b in enumerate(answers):
                if i != j and a == b:
                    return False

        perimeter = solution_set['1ac'] + solution_set['2ac'] + solution_set['4ac']

        # ensure some two answers differ by the perimeter
        #print(perimeter)
        #print(solution_set)
        for a in answers:
            for b in answers:
                #if abs(perimeter - abs(a-b)) < 10:
                #    print(perimeter-abs(a-b))
                if abs(a - b) == perimeter:
                    return True
        
        return False

    def solve(self):
        if len(self.solve_order) != len(self.clues.keys()):
            raise ValueError("Solving order must be assigned!")
        
        stack = [{}]

        # essentially doing a DFS in the possibity gfdd.
        # for each item in the stack, add all the branches of the possibility tree.

        while len(stack) > 0:
            solution_set = stack.pop()
            log_file.write(str(solution_set))
            current_clue = self.get_current_clue(solution_set)
            log_file.write(', solving for ' + current_clue)

            if current_clue == 'NONE':
                # we made it to the end of a tree branch without hitting a contradiction, we made it! 
                # sanitise
                if self.final_constraints(solution_set):
                    print(solution_set)
                    log_file.write(' VALID OMGGG')
                continue
            
            # using the clue, get a list of possible values for the clue.
            possible_values_for_clue = self.clues[current_clue].get_solutions(solution_set)
            possible_values_for_clue = list(dict.fromkeys(possible_values_for_clue))

            # cull possibilities
            og_length = len(possible_values_for_clue)
            possible_values_for_clue = list(filter(lambda x : check_clue(current_clue, x, solution_set), possible_values_for_clue))

            if possible_values_for_clue == []:
                log_file.write(' - STOPPED')
                if og_length != len(possible_values_for_clue):
                    log_file.write(' BECAUSE OF DIGITS')

            for value in possible_values_for_clue:
                # add the child node
                new_set = solution_set.copy()
                new_set[current_clue] = value
                stack.append(new_set)
            log_file.write('\n')

Q2 = Puzzle()
Q2.solve_order = ['1ac', '2ac', '4ac', '10dn', '12dn', '11ac', '5dn', '9dn', '14ac', '1dn', '7dn', '13ac', '2dn', '3dn']

#funky_triangle_triplets = [[21, 25, 45], [21, 65, 85], [25, 27, 39], [25, 33, 33], [25, 63, 65], [25, 65, 81], [25, 69, 77], [33, 55, 65], [35, 49, 69], [35, 51, 85], [35, 55, 63], [35, 55, 81], [39, 49, 65], [39, 55, 77], [45, 49, 77], [45, 91, 95], [49, 49, 55], [49, 57, 65], [49, 87, 95], [51, 55, 65], [51, 85, 95], [55, 81, 95], [55, 85, 91], [63, 91, 99], [63, 95, 95], [65, 75, 91], [65, 81, 85], [65, 93, 95], [69, 77, 85], [69, 85, 99], [69, 91, 93], [75, 85, 93], [75, 87, 91], [77, 81, 95], [77, 85, 91], [81, 81, 91], [81, 85, 87]]
funky_triangle_triplets = [[25, 69, 77], [49, 57, 65], [49, 87, 95], [69, 77, 85], [77, 81, 95]]
Q2.clues['1ac'] = TripletPrimaryClue(funky_triangle_triplets)
Q2.clues['2ac'] = TripletSecondaryClue(funky_triangle_triplets, '1ac')
Q2.clues['4ac'] = TripletTertiaryClue(funky_triangle_triplets, '1ac', '2ac')

primitive_2digit_triplets = [[20, 21, 29], [12, 35, 37], [28, 45, 53], [11, 60, 61], [33, 56, 65], [16, 63, 65], [48, 55, 73], [36, 77, 85], [13, 84, 85], [39, 80, 89], [65, 72, 97]]
Q2.clues['10dn'] = TripletPrimaryClue(primitive_2digit_triplets)
Q2.clues['12dn'] = TripletSecondaryClue(primitive_2digit_triplets, '10dn')
Q2.clues['11ac'] = TripletTertiaryClue(primitive_2digit_triplets, '10dn', '12dn')

primitive_beefy_triplets = [[15, 112, 113], [44, 117, 125], [88, 105, 137], [24, 143, 145], [17, 144, 145], [51, 140, 149], [85, 132, 157], [52, 165, 173], [19, 180, 181], [57, 176, 185], [95, 168, 193], [28, 195, 197], [84, 187, 205], [21, 220, 221], [60, 221, 229], [32, 255, 257], [96, 247, 265], [23, 264, 265], [69, 260, 269], [68, 285, 293], [25, 312, 313], [75, 308, 317], [36, 323, 325], [76, 357, 365], [27, 364, 365], [40, 399, 401], [29, 420, 421], [87, 416, 425], [84, 437, 445], [31, 480, 481], [93, 476, 485], [44, 483, 485], [92, 525, 533], [33, 544, 545], [48, 575, 577], [35, 612, 613], [52, 675, 677], [37, 684, 685], [39, 760, 761], [56, 783, 785], [41, 840, 841], [60, 899, 901], [43, 924, 925]]
Q2.clues['5dn'] = TripletPrimaryClue(primitive_beefy_triplets, 2)
Q2.clues['9dn'] = TripletSecondaryClue(primitive_beefy_triplets, '5dn', 3)
Q2.clues['14ac'] = TripletTertiaryClue(primitive_beefy_triplets, '5dn', '9dn', 3)

Q2.clues['1dn'] = TripletPrimaryClue(primitive_beefy_triplets, 2)
Q2.clues['7dn'] = TripletSecondaryClue(primitive_beefy_triplets, '1dn', 3)
Q2.clues['13ac'] = TripletTertiaryClue(primitive_beefy_triplets, '1dn', '7dn', 3)

def clue_3dn(solution_set):
    out = []
    for n in range(100, 1000):
        if sqrt(n + solution_set['2dn']) % 1 == 0:
            out.append(n)
    return out
Q2.clues['3dn'] = TransformativeClue(clue_3dn)

#print(len(primitive_beefy_triplets))
Q2.solve()

log_file.close()
# WE CANNOT FIND THE UNIQUE SOLUTION
# - solution checker is wrong?
#   - i dont think so lmfao
# - we are losing solutions during the DFS search
#   - clue digit checking?
#   - clue definitions and possibility accumulation?
#   - not enough hardcoded values??
#   - question is just wrong lmfao