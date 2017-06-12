# -----------------
# User Instructions
#
# Write a function, csuccessors, that takes a state (as defined below)
# as input and returns a dictionary of {state:action} pairs.
#
# A state is a tuple with six entries: (M1, C1, B1, M2, C2, B2), where
# M1 means 'number of missionaries on the left side.'
#
# An action is one of the following ten strings:
#
# 'MM->', 'MC->', 'CC->', 'M->', 'C->', '<-MM', '<-MC', '<-M', '<-C', '<-CC'
# where 'MM->' means two missionaries travel to the right side.
#
# We should generate successor states that include more cannibals than
# missionaries, but such a state should generate no successors.

def csuccessors(state):
    """Find successors (including those that result in dining) to this
    state. But a state where the cannibals can dine has no successors."""
    M1, C1, B1, M2, C2, B2 = state
    successors = {}
    action = ''
    if C1 > M1 or C2 > M2:
        return successors
    source = destination = ()
    for i in range(3):
        for j in range(3 - i):
            if i == j == 0:
                continue
            if B1 == 1:
                source = (M1, C1)
                destination = (M2, C2)
            else:
                source = (M2, C2)
                destination = (M1, C1)
            source = (source[0]-i, source[1]-j)
            destination = (destination[0]+i, destination[1]+j)
            M1_ = C1_ = B1_ = M2_ = C2_ = B2_ = 0
            if B1 == 1:
                B2_ = 1
                B1_ = 0
                action = i * 'M' + j * 'C' + '->'
                M1_ = source[0]
                C1_ = source[1]
                M2_ = destination[0]
                C2_ = destination[1]
            else:
                B1_ = 1
                B2_ = 0
                action = '<-' + i * 'M' + j * 'C'
                M1_ = destination[0]
                C1_ = destination[1]
                M2_ = source[0]
                C2_ = source[1]
            key = (M1_, C1_, B1_, M2_, C2_, B2_)
            if key not in successors:
                successors[key] = action
    return successors


def test():
    assert csuccessors((2, 2, 1, 0, 0, 0)) == {(2, 1, 0, 0, 1, 1): 'C->',
                                               (1, 2, 0, 1, 0, 1): 'M->',
                                               (0, 2, 0, 2, 0, 1): 'MM->',
                                               (1, 1, 0, 1, 1, 1): 'MC->',
                                               (2, 0, 0, 0, 2, 1): 'CC->'}
    assert csuccessors((1, 1, 0, 4, 3, 1)) == {(1, 2, 1, 4, 2, 0): '<-C',
                                               (2, 1, 1, 3, 3, 0): '<-M',
                                               (3, 1, 1, 2, 3, 0): '<-MM',
                                               (1, 3, 1, 4, 1, 0): '<-CC',
                                               (2, 2, 1, 3, 2, 0): '<-MC'}
    assert csuccessors((1, 4, 1, 2, 2, 0)) == {}
    return 'tests pass'

print test()
