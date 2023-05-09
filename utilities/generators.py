import random


def id_generator(length=10) -> int:

    """ ID Generator for bank account number """

    # generate a random number with length
    return random.randint(10**(length-1), (10**length)-1)
