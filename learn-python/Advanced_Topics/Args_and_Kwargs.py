# *args and **kwargs

def example_function(*args, **kwargs):
    print("Args:", args)
    print("Kwargs:", kwargs)

example_function(1, 2, 3, a=4, b=5)
