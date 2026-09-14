"""


things to do:

for each value in a list
find the left index , right index
calculate the width, you have the height is value
calculate area
store in area = max (area, current_area)

1. create an empty stack
2. initialize a max_area
3. loop enters
-> pick the element - find the left and right index for that element
left_index = the index where the value is less than current value
right_index = same

just put the left_index alone in monotonic stack - to avoid recalculation



"""


def longest_rectangle_in_histogram(arr: list) -> int:

    if len(arr) == 0:
        return 0

    max_area = 0

    for index, value in enumerate(arr):
        left_index = index-1
        right_index = index+1
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

if __name__ == "__main__":
    arr_pass = [2,1,5,6,2,3]
    area_returned = longest_rectangle_in_histogram(arr_pass)
    print(area_returned)