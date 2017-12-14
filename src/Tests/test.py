import numpy as np
import math
import scipy.integrate as integrate
import scipy.optimize as optimize


# 3500
def f1(x, t):
    return 70 if x < t < x + 50 else 0


# 600
def f2(x, t):
    return 30 if x < t < x + 20 else 0


# 600
def f3(x, t):
    return 20 if x < t < x + 30 else 0


# 1875
def f4(x, t):
    return 125 if x < t < x + 15 else 0


# 231250.0
def f(x):
    return math.fsum(
        map(
            lambda t: 10*f1(x[0], t) + 10*f2(x[1], t) + 10*f3(x[2], t) + 10*f4(x[3], t) - pow(t-25, 2),
            range(100)
        )
    )


def p(t):
    return pow(t-25, 2)


minimum_x1 = 0.0
minimum_y1 = math.inf
for i in range(100):
    val = math.fsum(
        map(
            lambda t: f1(i, t) - p(t),
            range(100)
        )
    )
    if val < minimum_y1:
        minimum_y1 = val
        minimum_x1 = i

minimum_x2 = 0.0
minimum_y2 = math.inf
for i in range(100):
    val = math.fsum(
        map(
            lambda t: f1(minimum_x1, t) + f4(i, t) - p(t),
            range(100)
        )
    )
    if val < minimum_y2:
        minimum_y2 = val
        minimum_x2 = i

minimum_x3 = 0.0
minimum_y3 = math.inf
for i in range(100):
    val = math.fsum(
        map(
            lambda t: f1(minimum_x1, t) + f4(minimum_x2, t) + f2(i, t) - p(t),
            range(100)
        )
    )
    if val < minimum_y1:
        minimum_y3 = val
        minimum_x3 = i

print(math.fsum(
        map(
            lambda t: f1(np.random.randint(0, 100), t) + f4(np.random.randint(0, 100), t)
                      + f2(np.random.randint(0, 100), t) - p(t),
            range(100)
        )
    )
)
print(math.fsum(
        map(
            lambda t: f1(minimum_x1, t) + f4(minimum_x2, t) + f2(minimum_x3, t) - p(t),
            range(100)
        )
    )
)
