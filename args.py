# *args all positional arguments in a tuple

def add_numbers(*args):
    print(sum(args))


add_numbers(1, 4, 6, 7)


# **kwargs

def print_info(**kwargs):
    print(kwargs)


print_info(name="John", age="30")
