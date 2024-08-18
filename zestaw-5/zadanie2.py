from functools import lru_cache, cached_property, cache
from decorator import timer_decor,time_evaluation_decorator

@time_evaluation_decorator
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

@time_evaluation_decorator
@cache
def fibonacci_2(n):
    if n <= 1:
        return n
    return fibonacci_2(n - 1) + fibonacci_2(n - 2)

@time_evaluation_decorator
@lru_cache(maxsize=5)
def fibonacci_3(n):
    if n <= 1:
        return n
    return fibonacci_3(n - 1) + fibonacci_3(n - 2)
print("fibonacci without cache")
fibonacci(35)
print("fibonacci with cache")
fibonacci_2(35)
print("fibonacci with lru_cache=5")
fibonacci_3(35)