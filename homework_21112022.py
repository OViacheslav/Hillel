import random


def retry(attempts=5, desired_value=None):
    def wrapper(func):
        def inner(*args, **kwargs):
            for counter in range(attempts):
                test_result = func(*args, **kwargs)
                if test_result == desired_value:
                    success = f'Success! After {counter} attempts. Desired value: {desired_value}.'
                    return success

            return 'The desired value could not be reached'

        return inner

    return wrapper


@retry(attempts=30, desired_value=2)
def get_random_value():
    return random.choice((1, 2, 3, 4, 5))


@retry(attempts=2, desired_value=[1, 2, 3])
def get_random_values(choices, size=2):
    return random.choices(choices, k=size)


def print_square(n):
    c = n - 2  # Amount of needed strings between upper and lower strings
    print(n * '* ')

    def inner_sides():
        nonlocal c
        if c == 0:
            return

        result = '*' + ((n - 2) * '  ') + ' *'
        print(result)
        c -= 1
        inner_sides()

    if n > 1:
        inner_sides()
        print(n * '* ')
