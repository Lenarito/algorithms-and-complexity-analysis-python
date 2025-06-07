def shell_sort(arr, key=lambda x: x, gaps=None):
    n = len(arr)
    if gaps is None:
        gaps = []
        gap = n // 2
        while gap > 0:
            gaps.append(gap)
            gap //= 2
    for gap in gaps:
        for i in range(gap, n):
            temp = arr[i]
            j = i
            while j >= gap and key(arr[j - gap]) > key(temp):
                arr[j] = arr[j - gap]
                j -= gap
            arr[j] = temp
    return arr
