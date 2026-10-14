from typing import List


def merge(intervals: List[List[int]]) -> List[List[int]]:
    # TODO: Implement your solution here

    if len(intervals) <= 1:
        return intervals

    intervals.sort(key=lambda x: x[0])

    index = 0

    while index <= len(intervals) - 2:
        first = intervals[index][1]
        second = intervals[index + 1][0]
        value = first - second
        if value >= 0:
            right_1 = intervals[index][1]
            right_2 = intervals[index + 1][1]
            if right_2 >= right_1:
                correct_right = right_2
            else:
                correct_right = right_1
            new_child_list = [intervals[index][0], correct_right]
            intervals.pop(index + 1)
            intervals[index] = new_child_list
        else:
            index += 1

    return intervals


answer = merge([[1, 4], [1, 4], [1, 5], [1, 2]])
print(answer)