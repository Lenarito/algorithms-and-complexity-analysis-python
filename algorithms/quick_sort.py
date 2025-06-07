import random
import sys

sys.setrecursionlimit(2000)

def partition(arr, low, high, key):
    pivot_index = random.randint(low, high)
    arr[high], arr[pivot_index] = arr[pivot_index], arr[high]
    pivot = key(arr[high])
    i = low - 1
    for j in range(low, high):
        if key(arr[j]) <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1

def quick_sort(arr, low=0, high=None, key=lambda x: x):
    if high is None:
        high = len(arr) - 1

    while low < high:
        pi = partition(arr, low, high, key)

        if pi - low < high - pi:
            quick_sort(arr, low, pi - 1, key=key)
            low = pi + 1
        else:
            quick_sort(arr, pi + 1, high, key=key)
            high = pi - 1

    return arr
