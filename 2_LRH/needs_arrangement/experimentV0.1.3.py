
def longest_rectangle_in_histogram(arr: list) -> int:

    if len(arr) == 0:
        return 0

    max_area = 0

    for index, value in enumerate(arr):
        left_index = index-1
        right_index = index+1
        monotonic_stack = []
        while not (left_index < 0):
            left_value = arr[left_index]
            if left_value < value:
                break
            left_index = left_index - 1
        while not (right_index > len(arr)-1):
            right_value =arr[right_index]
            if right_value < value:
                break
            right_index = right_index + 1

        width = right_index - left_index - 1
        height = value
        area = width * height
        max_area = max(area, max_area)
    return max_area

