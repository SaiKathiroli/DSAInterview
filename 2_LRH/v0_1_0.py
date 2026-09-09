"""
Given an array of bar heights in a histogram, find the area of the largest rectangle that can be formed.
Input:  heights = [2, 1, 5, 6, 2, 3]
Output: 10   → rectangle spanning bars 3 and 4 (height 5, width 2)
"""


def longest_rectangle_histogram(param: list[int]) -> int:

    if len(param) == 0:
        return 0

    area = max(param)

    for index, value in enumerate(param):
        scoped_bars = [value]
        temp_index = index
        while temp_index < len(param):
            rectangle_height = min(scoped_bars)
            rectangle_width = len(scoped_bars)
            area = max(area, rectangle_width * rectangle_height)
            if temp_index + 1 >= len(param):
                break
            scoped_bars.append(param[temp_index + 1])
            temp_index += 1

    return area


if __name__ == "__main__":
    max_area = longest_rectangle_histogram([2, 1, 5, 6, 2, 3])
    print(max_area)
