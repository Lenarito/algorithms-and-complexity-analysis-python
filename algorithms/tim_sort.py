from .insertion_sort import insertion_sort

def merge(arr, start, mid, end, key=lambda x: x):
    if mid == end:
        return
    left = arr[start:mid+1]
    right = arr[mid+1:end+1]
    i = j = 0

    for k in range(start, end+1):
        if i < len(left) and (j >= len(right) or key(left[i]) <= key(right[j])):
            arr[k] = left[i]
            i += 1
        else:
            arr[k] = right[j]
            j += 1

def tim_sort(arr, key=lambda x: x):
    n = len(arr)
    RUN = 30

    for start in range(0, n, RUN):
        end = min(start + RUN, n)
        sorted_block = insertion_sort(arr[start:end], key=key)
        arr[start:end] = sorted_block

    size = RUN
    while size < n:
        for start in range(0, n, size * 2):
            mid = min(start + size - 1, n - 1)
            end = min(start + 2 * size - 1, n - 1)
            if mid < end:
                merge(arr, start, mid, end, key=key)
        size *= 2

    return arr
