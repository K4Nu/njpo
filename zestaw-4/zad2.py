def argument_limiter(a,b):
    def args_limiter(func):
        def wrapper(*args,**kwargs):
            nums=args
            limited_a = max(nums[0], a)
            limited_b = min(nums[1], b)
            return func(limited_a,limited_b)
        return wrapper
    return args_limiter

@argument_limiter(5,6)
def sum_range(a,b):
    count=0
    for i in range(a,b+1):
        count+=i
    return count
print(sum_range(1,10))