###########################
# 6.0002 Problem Set 1a: Space Cows 
# Name:
# Collaborators:
# Time:

from ps1_partition import get_partitions

# ================================
# Part A: Transporting Space Cows
# ================================

# Problem 1


def load_cows(filename):
    """
    Read the contents of the given file.  Assumes the file contents contain
    data in the form of comma-separated cow name, weight pairs, and return a
    dictionary containing cow names as keys and corresponding weights as values.

    Parameters:
    filename - the name of the data file as a string

    Returns:
    a dictionary of cow name (string), weight (int) pairs
    """
    cow_dict = {}
    file = open(filename, 'r')
    for line in file:
        name, weight = line.split(',')
        cow_dict[name] = int(weight)

    file.close()
    print(cow_dict)
    return cow_dict


# Problem 2


def greedy_cow_transport(cows, limit=10):
    """
    Uses a greedy heuristic to determine an allocation of cows that attempts to
    minimize the number of spaceship trips needed to transport all the cows. The
    returned allocation of cows may or may not be optimal.
    The greedy heuristic should follow the following method:

    1. As long as the current trip can fit another cow, add the largest cow that will fit
        to the trip
    2. Once the trip is full, begin a new trip to transport the remaining cows

    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    sorted_cows = sorted(cows.items(), key=lambda x: x[1], reverse=True)  # sort list in ascending order
    result = []  # the main list
    trip = 0
    while len(sorted_cows) > 0:  # continue until all cows are gone
        trip_limit = limit  # initial limit
        result.append([])  # initiating inner list.
        removed_cows = []  # list of cows already used
        for cow in sorted_cows:
            if cow[1] <= trip_limit:  # checking weight against limit
                result[trip].append(cow[0])
                removed_cows.append(sorted_cows.index(cow))
                trip_limit -= cow[1]  # remove weight of cow from available limit
        trip += 1
        for cow_index in sorted(removed_cows, reverse=True):
            sorted_cows.pop(cow_index)
    return result

# Problem 3


def brute_force_cow_transport(cows,limit=10):
    """
    Finds the allocation of cows that minimizes the number of spaceship trips
    via brute force.  The brute force algorithm should follow the following method:

    1. Enumerate all possible ways that the cows can be divided into separate trips 
        Use the given get_partitions function in ps1_partition.py to help you!
    2. Select the allocation that minimizes the number of trips without making any trip
        that does not obey the weight limitation
            
    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    # TODO: Your code here
    pass
        
# Problem 4


def compare_cow_transport_algorithms():
    """
    Using the data from ps1_cow_data.txt and the specified weight limit, run your
    greedy_cow_transport and brute_force_cow_transport functions here. Use the
    default weight limits of 10 for both greedy_cow_transport and
    brute_force_cow_transport.
    
    Print out the number of trips returned by each method, and how long each
    method takes to run in seconds.

    Returns:
    Does not return anything.
    """
    # TODO: Your code here
    pass


if __name__ == '__main__':
    cows = load_cows('ps1_cow_data.txt')
    result = greedy_cow_transport(cows)
    print("greedy cow transport result: \n", result,"\n-----------")