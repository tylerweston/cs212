# -----------------
# User Instructions
#
# Write a function, subway, that takes lines as input (read more about
# the **lines notation in the instructor comments box below) and returns
# a dictionary of the form {station:{neighbor:line, ...}, ... }
#
# For example, when calling subway(boston), one of the entries in the
# resulting dictionary should be 'foresthills': {'backbay': 'orange'}.
# This means that foresthills only has one neighbor ('backbay') and
# that neighbor is on the orange line. Other stations have more neighbors:
# 'state', for example, has 4 neighbors.
#
# Once you've defined your subway function, you can define a ride and
# longest_ride function. ride(here, there, system) takes as input
# a starting station (here), a destination station (there), and a subway
# system and returns the shortest path.
#
# longest_ride(system) returns the longest possible ride in a given
# subway system.

# -------------
# Grading Notes
#
# The subway() function will not be tested directly, only ride() and
# longest_ride() will be explicitly tested. If your code passes the
# assert statements in test_ride(), it should be marked correct.

def subway(**lines):
    """Define a subway map. Input is subway(linename='station1 station2...'...).
    Convert that and return a dict of the form: {station:{neighbor:line,...},...}"""
    stations = {}
    for line in lines:
        line_stations = lines[line].split()
        stations = update_station(stations,
                                  line_stations[0], {line_stations[1]:line})
        line_len = len(line_stations)
        for i in range(1, line_len - 1):
            previous = line_stations[i - 1]
            next_station = line_stations[i + 1]
            stations = update_station(stations,
                                      line_stations[i],
                                      {previous: line, next_station: line})
        stations = update_station(stations,
                                  line_stations[line_len - 1],
                                  {line_stations[line_len - 2]:line})
    return stations

def update_station(stations, current_station, neighbours):
    """ stations is the dictionary containing all stations. current_station
    is the station currently being processed. neighbours is a dictionary of
    neigbbours of the current station. """
    if current_station in stations:
        stations[current_station].update(neighbours)
    else:
        stations[current_station] = neighbours
    return stations

#small_city = subway(line_a='A B C D E', line_b='A F G C K E')

#print small_city

boston = subway(
    blue='bowdoin government state aquarium maverick airport suffolk revere wonderland',
    orange='oakgrove sullivan haymarket state downtown chinatown tufts backbay foresthills',
    green='lechmere science north haymarket government park copley kenmore newton riverside',
    red='alewife davis porter harvard central mit charles park downtown south umass mattapan')

#print boston

def at_destination(destination):
    """ Argument is the string that is the name of the destination"""
    def at_dest(curr_station):
        return curr_station == destination
    return at_dest

def station_successor(system):
    def s_successor(curr_station):
        if curr_station in system:
            return dict((station, line) # for this particular problem action is not necessary
                         for station, line in system[curr_station].iteritems())
        else:
            return {}
    return s_successor

# small_city = subway(line_a='A B C D E', line_b='A F G C K E')
# print station_successor(small_city)('A')
# print station_successor(boston)('state')

def ride(here, there, system=boston):
    "Return a path on the subway system from here to there."
    return shortest_path_search(here, station_successor(system), at_destination(there))

def longest_ride(system):
    """"Return the longest possible 'shortest path'
    ride between any two stops in the system."""
    all_rides = dict(((here, there), ride(here, there, system)) for here in system for there in system)
    max_len = -1
    longest_path = []
    for (here, there) in all_rides:
        this_ride = all_rides[(here, there)]
        if len(this_ride) > max_len:
                longest_path = this_ride
                max_len = len(this_ride)
    return longest_path

def shortest_path_search(start, successors, is_goal):
    """Find the shortest path from start state to a state
    such that is_goal(state) is true."""
    if is_goal(start):
        return [start]
    explored = set() # set of states we have visited
    frontier = [ [start] ] # ordered list of paths we have blazed
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
    return []

def path_states(path):
    "Return a list of states in this path."
    return path[0::2]

def path_actions(path):
    "Return a list of actions in this path."
    return path[1::2]

# small_city = subway(line_a='A B C D E', line_b='A F G C K E')
# print longest_ride(small_city)

#print ride('mit', 'government')

def test_ride():
    assert ride('mit', 'government') == [
        'mit', 'red', 'charles', 'red', 'park', 'green', 'government']
    assert ride('mattapan', 'foresthills') == [
        'mattapan', 'red', 'umass', 'red', 'south', 'red', 'downtown',
        'orange', 'chinatown', 'orange', 'tufts', 'orange', 'backbay', 'orange', 'foresthills']
    assert ride('newton', 'alewife') == [
        'newton', 'green', 'kenmore', 'green', 'copley', 'green', 'park', 'red', 'charles', 'red',
        'mit', 'red', 'central', 'red', 'harvard', 'red', 'porter', 'red', 'davis', 'red', 'alewife']
    assert (path_states(longest_ride(boston)) == [
        'wonderland', 'revere', 'suffolk', 'airport', 'maverick', 'aquarium', 'state', 'downtown', 'park',
        'charles', 'mit', 'central', 'harvard', 'porter', 'davis', 'alewife'] or
        path_states(longest_ride(boston)) == [
                'alewife', 'davis', 'porter', 'harvard', 'central', 'mit', 'charles',
                'park', 'downtown', 'state', 'aquarium', 'maverick', 'airport', 'suffolk', 'revere', 'wonderland'])
    assert len(path_states(longest_ride(boston))) == 16
    return 'test_ride passes'

print test_ride()
