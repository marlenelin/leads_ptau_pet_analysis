import numpy as np

def pooled_sd(x1, x2):
    x1 = np.array(x1)
    x2 = np.array(x2)

    n1 = len(x1)
    n2 = len(x2)

    s1 = x1.std(ddof=1)
    s2 = x2.std(ddof=1)

    return np.sqrt(((n1 - 1)*s1**2 + (n2 - 1)*s2**2) / (n1 + n2 - 2))