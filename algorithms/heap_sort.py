def heapify(arr, n, i, key):
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2

    if left < n and key(arr[left]) > key(arr[largest]):
        largest = left
    if right < n and key(arr[right]) > key(arr[largest]):
        largest = right
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify(arr, n, largest, key)

def heap_sort(arr, key=lambda x: x):
    n = len(arr)
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i, key)
    for i in range(n - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        heapify(arr, i, 0, key)
    return arr
