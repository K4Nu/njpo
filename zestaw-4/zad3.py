from sympy import symbols, Eq, solve


def find_roots_in_range(a, b, equation):
    # Define a symbolic variable
    x = symbols('x')

    polynomial = eval(equation)

    roots = solve(Eq(polynomial, 0), x)

    for root in roots:
        root_value = root.evalf()
        if root.is_real and a <= root_value <= b:
            yield root_value


equation = "x**2 - 2"
root_generator = find_roots_in_range(-10, 10, equation)

for root in root_generator:
    print(root)
