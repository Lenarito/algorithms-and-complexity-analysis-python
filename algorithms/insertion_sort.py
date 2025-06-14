def insertion_sort(arr, key=lambda x: x):
    for i in range(1, len(arr)):
        current = arr[i]
        j = i - 1
        while j >= 0 and key(current) < key(arr[j]):
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = current
    return arr
