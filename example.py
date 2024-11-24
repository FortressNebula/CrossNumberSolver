from cluesolver import *

# for an example, this is puzzle S implemented 
# obviously in reality this wouldnt work since the possible clues havent been specified in the Puzzle class, you'd need to do this yourself for your clues

squares = [1, 4, 9, 16, 25, 36, 49, 64, 81, 100, 121, 144, 169, 196, 225, 256, 289, 324, 361, 400, 441, 484, 529, 576, 625, 676, 729, 784, 841, 900, 961]

S = Puzzle()
S.solve_order = ['4dn', '3ac', '2dn', '1ac', '1dn', '5ac']

S.clues['4dn'] = FixedClue([10, 15, 21, 28, 36, 45, 55, 66, 78, 91])

triangles = [21, 28, 36, 45, 55, 66, 78, 91, 105, 120,136, 153, 171, 190]
def clue_3ac(solution_set):
    out = []
    for triangle in triangles:
        number = triangle - solution_set['4dn']
        if number >= 10 and number < 100:
            out.append(number)
    return out
S.clues['3ac'] = TransformativeClue(clue_3ac)

def clue_2dn(solution_set):
    return [reverse(solution_set['3ac'])]
S.clues['2dn'] = TransformativeClue(clue_2dn)

def clue_1dn(solution_set):
    number = digit_sum(solution_set['1ac']) ** 2 + solution_set['3ac']
    if number >= 100 and number < 1000: # solutions can be length-checked easily like this
        return [number]
    else:
        return []
S.clues['1dn'] = TransformativeClue(clue_1dn)

S.solve()