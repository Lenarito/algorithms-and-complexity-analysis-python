def rank_sort(arr, key=lambda x: x):
    n = len(arr)
    ranks = [0] * n
    for i in range(n):
        for j in range(n):
            if key(arr[j]) < key(arr[i]) or (key(arr[j]) == key(arr[i]) and j < i):
                ranks[i] += 1
    sorted_arr = [0] * n
    for i in range(n):
        sorted_arr[ranks[i]] = arr[i]
    for i in range(n):
        arr[i] = sorted_arr[i]
    return arr
