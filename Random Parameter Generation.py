import random
import numpy as np

def ddd(low, high, size):
    return [random.randint(low, high) for _ in range(size)]

a = 1

#generate demand value
ranges = [(a*250, a*300), (a*300, a*350), (a*350, a*400), (a*400, a*450)]

#generate supply value

# ranges = [(a*90,a*140),(a*80,a*130),(a*70,a*120),(a*60,a*110)]

result = [
    [
        ddd(int(low), int(high), 100)  # number of samples
        for _ in range(12)  # number of sites
    ]
    for (low, high) in ranges
]

print(result)