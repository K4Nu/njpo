from time import perf_counter
import time
from functools import wraps
def timer_decor(func):
    def wrapper(*args, **kwargs):
        start = perf_counter()  # Start the timer
        result = func(*args, **kwargs)  # Execute the function
        stop = perf_counter()  # Stop the timer
        print(f'Time of {func.__name__} is {stop - start} seconds')
        return result  # Return the result of the function
    return wrapper


def time_evaluation_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not hasattr(wrapper, "depth"):
            wrapper.depth = 0
            wrapper.start_time = time.time()

        wrapper.depth += 1

        result = func(*args, **kwargs)

        wrapper.depth -= 1

        if wrapper.depth == 0:
            end_time = time.time()
            print(f"Total time taken for the recursion: {end_time - wrapper.start_time} seconds")
            del wrapper.start_time  # Reset for the next call
            del wrapper.depth  # Clean up the depth attribute

        return result

    return wrapper
