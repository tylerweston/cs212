# -----------------
# User Instructions
#
# In this problem, you will solve the pouring problem for an arbitrary
# number of glasses. Write a function, more_pour_problem, that takes
# as input capacities, goal, and (optionally) start. This function should
# return a path of states and actions.
#
# Capacities is a tuple of numbers, where each number represents the
# volume of a glass.
#
# Goal is the desired volume and start is a tuple of the starting levels
# in each glass. Start defaults to None (all glasses empty).
#
# The returned path should look like [state, action, state, action, ... ]
# where state is a tuple of volumes and action is one of ('fill', i),
# ('empty', i), ('pour', i, j) where i and j are indices indicating the
# glass number.



def more_pour_problem(capacities, goal, start=None):
    """The first argument is a tuple of capacities (numbers) of glasses; the
    goal is a number which we must achieve in some glass.  start is a tuple
    of starting levels for each glass; if None, that means 0 for all.
    Start at start state and follow successors until we reach the goal.
    Keep track of frontier and previously explored; fail when no frontier.
    On success return a path: a [state, action, state2, ...] list, where an
    action is one of ('fill', i), ('empty', i), ('pour', i, j), where
    i and j are indices indicating the glass number."""
    water_levels = tuple()
    if start is None:
        water_levels = tuple(0 for _ in range(len(capacities)))
    else:
        water_levels = start
    return shortest_path_search(water_levels, psuccessors(capacities),
                                quantity_filled(goal))

def psuccessors(capacities):
    """This function takes a tuple containing the capacities as input and
    returns a function that computes the successors given the capacities"""
    def psuccessor_helper(state):
        water_levels = state
        successors = {}
        # Fill the cups, one a time
        for i in range(len(capacities)):
            new_levels = list(water_levels)
            new_levels[i] = capacities[i]
            successors[tuple(new_levels)] = ('fill', i)
        # Empty the cups, one a time
        for i in range(len(capacities)):
            new_levels = list(water_levels)
            new_levels[i] = 0
            successors[tuple(new_levels)] = ('empty', i)
        # pour between two cups, always from the ith to the jth.
        for i in range(len(capacities)):
            for j in range(len(capacities)):
                ith_level = water_levels[i]
                jth_level = water_levels[j]
                ith_cap = capacities[i]
                jth_cap = capacities[j]
                new_ith_level = new_jth_level = 0
                if ith_level + jth_level <= jth_cap:
                    new_ith_level = 0
                    new_jth_level = ith_level + jth_level
                else:
                    new_ith_level = ith_level - (jth_cap - jth_level)
                    new_jth_level = jth_cap # == jth_level + (jth_cap - jth_level)
                new_levels = list(water_levels)
                new_levels[i] = new_ith_level
                new_levels[j] = new_jth_level
                successors[tuple(new_levels)] = ('pour', i, j)
        return successors
    return psuccessor_helper

# state0 = (0, 0)
# print psuccessors((1, 2))(state0)
# state2 = ((1, 2, 5), (2, 3, 9))
# print psuccessors(state2)
# state3 = ((0, 2, 4), (2, 3, 9))
# print psuccessors(state3)


def quantity_filled(q):
    """This function takes a numerical value as an input and returns a function
    that tests if the quantity is filled for a state. """
    def q_filled(state):
        return q in state
    return q_filled

# state1 = ((1, 2, 5, 8), (2, 3, 6, 9))
# q1 = quantity_filled(1)
# print q1(state1)
# q2 = quantity_filled(3)
# print q2(state1)

def shortest_path_search(start, successors, is_goal):
    """Find the shortest path from start state to a state
    such that is_goal(state) is true."""
    if is_goal(start):
        return [start]
    explored = set()
    frontier = [ [start] ]
    while frontier:
        path = frontier.pop(0)
        s = path[-1]
        for (state, action) in successors(s).items():
            if state not in explored:
                explored.add(state)
                path2 = path + [action, state]
                if is_goal(state):
                    return path2
                else:
                    frontier.append(path2)
    return Fail

Fail = []

#print more_pour_problem((1, 2, 4, 8), 4)

def test_more_pour():
    assert more_pour_problem((1, 2, 4, 8), 4) == [
        (0, 0, 0, 0), ('fill', 2), (0, 0, 4, 0)]
    assert more_pour_problem((1, 2, 4), 3) == [
        (0, 0, 0), ('fill', 2), (0, 0, 4), ('pour', 2, 0), (1, 0, 3)]
    starbucks = (8, 12, 16, 20, 24)
    assert not any(more_pour_problem(starbucks, odd) for odd in (3, 5, 7, 9))
    assert all(more_pour_problem((1, 3, 9, 27), n) for n in range(28))
    assert more_pour_problem((1, 3, 9, 27), 28) == []
    return 'test_more_pour passes'

print test_more_pour()
