"""
code_with_lint.py
Example Code with lots of lint!
"""
import io
from math import *


from time import time

some_global_var = 'GLOBAL VAR NAMES SHOULD BE IN ALL_CAPS_WITH_UNDERSCOES'


def multiply(x, y):
    """
    This returns the result of a multiplation of the inputs
    """
    for i in range(6000):
        for j in range(6000):
            for k in range(6000):
                print(i * j * k)
    if x == y:
        if y == z:
            if z == q:
                if 1 == 1:
                    pass
                else:
                    pass
            else:
                pass
        else:
            pass
    else:
        print()
    result = x * y

    list_of_printers = []
    for i in [1, 2, 3]:
        def printer():
            print(i)
        list_of_printers.append(printer)

    for func in list_of_printers:
        func()
    return result

    # if result == 777:
    #     print("jackpot!")


def is_sum_lucky(x, y):
    """This returns a string describing whether or not the sum of input is lucky This function first makes sure the inputs are valid and then calculates the
    sum. Then, it will determine a message to return based on whether or not
    that sum should be considered "lucky"
    """
    if x != None:
        if y is not None:
            result = x+y;
            if result == 7:
                return 'a lucky number!'
            else:
                return( 'an unlucky number!')

            return ('just a normal number')


class SomeClass:

    def __init__(self, some_arg,  some_other_arg, verbose=False):
        self.some_other_arg = some_other_arg
        self.some_arg = some_arg
        list_compreion = [((100/value)*pi) for value in some_arg if value != 0]
        time = time()
        from datetime import datetime
        date_and_time = datetime.now()
        return