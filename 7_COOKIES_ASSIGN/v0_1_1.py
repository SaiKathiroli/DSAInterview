from typing import List


def findContentChildren(g: List[int], s: List[int]) -> int:
    """
    g: greed factor of each child
    s: size of each cookie
    Returns: maximum number of content children
    """
    # TODO: Implement your solution here
    count = 0
    for indexs, values in enumerate(s):
        target_index = len(g)
        target_value = 2 ** 31
        for indexg, valueg in enumerate(g):
            # values >= valueg
            if values >= valueg:
                if valueg <= target_value:
                    target_value = valueg
                    target_index = min(target_index, indexg)

        if target_index != len(g):
            g.pop(target_index)
            count += 1

    return count


print(findContentChildren([1, 2, 3], [1, 1]))
