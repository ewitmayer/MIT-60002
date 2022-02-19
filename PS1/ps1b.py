###########################
# 6.0002 Problem Set 1b: Space Change
# Name:
# Collaborators:
# Time:
# Author:

# ================================
# Part B: Golden Eggs
# ================================

# Problem 1
def dp_make_weight(egg_weights, target_weight, memo={}):
    """
    Find number of eggs to bring back, using the smallest number of eggs. Assumes there is
    an infinite supply of eggs of each weight, and there is always a egg of value 1.
    
    Parameters:
    egg_weights - tuple of integers, available egg weights sorted from smallest to largest value
    (1 = d1 < d2 < ... < dk)
    target_weight - int, amount of weight we want to find eggs to fit
    memo - dictionary, OPTIONAL parameter for memoization (you may not need to use this parameter
    depending on your implementation)
    
    Returns: int, smallest number of eggs needed to make target weight
    """
    sorted_eggs = sorted(egg_weights, reverse=True)     # sort eggs by weight (descending order)
    number_of_eggs = 0                                  # number of eggs to handle
    remaining_weight = target_weight                    # available weight, decreased when eggs are transported.
    for index in range(len(sorted_eggs)):
        eggs_to_take = remaining_weight // sorted_eggs[index]
        number_of_eggs += eggs_to_take
        remaining_weight -= eggs_to_take * sorted_eggs[index]
        if remaining_weight == 0:                       # end loop if remaining weight is exhausted
            break
    return number_of_eggs


if __name__ == '__main__':
    weights = (1, 5, 10, 25)
    n = 99
    print("Egg weights = (1, 5, 10, 25)")
    print("n = 99")
    print("Expected output: 9 (3 * 25 + 2 * 10 + 4 * 1 = 99)")
    print("Actual output:", dp_make_weight(weights, n))
    print()

    weights = (1, 2, 3, 5, 10, 50)
    n = 998
    print("Egg weights = (1, 2, 3, 5, 50)")
    print("n = 998")
    print("Expected ouput: 25 (19 * 50 + 4 * 10 + 1 * 5 + 1 * 3 = 998)")
    print("Actual output:", dp_make_weight(weights, n))
    print()

    weights = (3, 5, 10, 20)
    n = 598
    print("Egg weights = (3, 5, 10, 20)")
    print("n = 598")
    print("Expected output: 28 (29 * 20 + 1 * 10 + 1 * 5 + 1 * 3 = 32)")
    print("Actual output:", dp_make_weight(weights, n))
    print()
