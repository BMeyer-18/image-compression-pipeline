from random import randrange

def quickselect(data, dim, left=0, right=-1, k=-1):
    """
    select point at sorted index
    """
    # set parameter defaults
    if right == -1:
        right = len(data)-1
    if k == -1:
        k = (right - left)//2

    # if there is only one element in the range, return it
    if left == right:
        return data[left][dim]

    # partition list
    idx = partition(data, dim, left=left, right=right)

    # if queried item is in position, return item
    if idx == k:
        return data[idx][dim]

    # recur through portion of partitioned list with queried index
    if k < idx:
        return quickselect(data, dim, left=left, right=idx-1, k=k)
    return quickselect(data, dim, left=idx+1, right=right, k=k)


def partition(data, dim, left=0, right=-1, pivot=-1):
    """
    partition list around item
    """
    # set parameter defaults
    if right == -1:
        right = len(data)-1
    if pivot == -1:
        pivot = randrange(right-left+1)+left

    # get value of original pivot
    pivotVal = data[pivot]

    # swap pivot with last element
    data[pivot] = data[right]
    data[right] = pivotVal

    # swap elements based on relation to pivot
    idx = left
    for i in range(left, right):
        if data[i][dim] <= pivotVal[dim]:
            # if element <= pivot, swap to the left
            temp = data[i]
            data[i] = data[idx]
            data[idx] = temp
            idx += 1

    # swap pivot into final position
    data[right] = data[idx]
    data[idx] = pivotVal

    return idx