def intro_sort(arr, key=lambda x: x):
    max_depth = 2 * (len(arr).bit_length())
    _intro_sort(arr, 0, len(arr) - 1, max_depth, key)

def _intro_sort(arr, start, end, max_depth, key):
    if end - start < 16:
        _insertion_sort(arr, start, end, key)
    elif max_depth == 0:
        _heap_sort(arr, start, end, key)
    else:
        pivot = partition(arr, start, end, key)
        _intro_sort(arr, start, pivot - 1, max_depth - 1, key)
        _intro_sort(arr, pivot + 1, end, max_depth - 1, key)

def _insertion_sort(arr, start, end, key):
    for i in range(start + 1, end + 1):
        current = arr[i]
        j = i - 1
        while j >= start and key(arr[j]) > key(current):
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = current

def _heap_sort(arr, start, end, key):
    def heapify(n, i):
        largest = i
        left = 2 * i + 1
        right = 2 * i + 2
        if left < n and key(heap[left]) > key(heap[largest]):
            largest = left
        if right < n and key(heap[right]) > key(heap[largest]):
            largest = right
        if largest != i:
            heap[i], heap[largest] = heap[largest], heap[i]
            heapify(n, largest)

    heap = arr[start:end + 1]
    n = len(heap)
    for i in range(n // 2 - 1, -1, -1):
        heapify(n, i)
    for i in range(n - 1, 0, -1):
        heap[0], heap[i] = heap[i], heap[0]
        heapify(i, 0)

    arr[start:end + 1] = heap

def partition(arr, low, high, key):
    pivot = arr[high]
    i = low
    for j in range(low, high):
        if key(arr[j]) < key(pivot):
            arr[i], arr[j] = arr[j], arr[i]
            i += 1
    arr[i], arr[high] = arr[high], arr[i]
    return i
