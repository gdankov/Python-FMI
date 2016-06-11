from itertools import permutations


def solvable_tiles(size=3):
    perms = permutations(range(size ** 2))
    for perm in perms:
        if is_solvable(perm, size):
            yield to_tile(perm, size)


def is_solvable(x, size):
    even_inversions = count_inversions(x) % 2 == 0

    if(size % 2 != 0 and even_inversions or
       size % 2 == 0 and blank_on_even_row(x, size) is not even_inversions):
        return True
    else:
        return False


def blank_on_even_row(permutation, size):
    row_counter = 1
    for i in range(len(permutation) - size, -1, -size):
        if(0 in permutation[i:i+size]):
            return row_counter % 2 == 0
        else:
            row_counter += 1


def to_tile(permutation, size):
    result = tuple(tuple(permutation[i:i+size])
                   for i in range(0, len(permutation), size))
    return result


def count_inversions(array):
    return merge(array)[1]


def merge(array):
    if (len(array) < 2):
        return array, 0

    middle_index = int(len(array) / 2)

    left = merge(array[:middle_index])
    right = merge(array[middle_index:])
    count = left[1] + right[1]

    return merge_helper(left[0], right[0], count)


def merge_helper(left, right, count):
    left_length = len(left)
    right_length = len(right)

    sorted_array = []
    i, j = 0, 0

    while i < left_length and j < right_length:
        if left[i] == 0:
            i += 1
        elif right[j] == 0:
            j += 1
        elif left[i] <= right[j]:
            sorted_array.append(left[i])
            i += 1
        elif left[i] > right[j]:
            sorted_array.append(right[j])
            count += left_length - i
            j += 1

    sorted_array += left[i:]
    sorted_array += right[j:]

    return sorted_array, count
