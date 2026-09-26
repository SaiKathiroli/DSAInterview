from typing import List, Optional


# 1. Definition for a Node (as provided by LeetCode)
class Node:
    def __init__(self, val: Optional[int] = None, children: Optional[List['Node']] = None):
        self.val = val
        self.children = children if children is not None else []


# 2. Your workspace
class Solution:
    def preorder(self, root: 'Node') -> List[int]:
        # TODO: Implement your stack-based (or recursive) solution here
        output = []
        if root is None:
            return output
        stack = [root]

        while len(stack) > 1:
            node_under_consideration = stack.pop()
            output.append(node_under_consideration.val)
            stack.extend(node_under_consideration.children[::-1])

        return output


# ---------------------------------------------------------
# BOILERPLATE & TESTING CODE BELOW (You don't need to change this)
# ---------------------------------------------------------

def build_tree(values: List[Optional[int]]) -> Optional[Node]:
    """
    Helper function to build an N-ary tree from LeetCode's level-order array format.
    Example: [1, None, 3, 2, 4, None, 5, 6]
    """
    if not values:
        return None

    root = Node(values[0])
    queue = [root]
    i = 1

    while queue and i < len(values):
        # A None value in LeetCode's format separates groups of children
        if values[i] is None:
            i += 1

        parent = queue.pop(0)

        # Keep adding children to the current parent until we hit the next None or end of array
        while i < len(values) and values[i] is not None:
            child = Node(values[i])
            parent.children.append(child)
            queue.append(child)
            i += 1

    return root


def run_tests():
    sol = Solution()

    test_cases = [
        {
            "name": "Standard Tree",
            "input": [1, None, 3, 2, 4, None, 5, 6],
            "expected": [1, 3, 5, 6, 2, 4]
        },
        {
            "name": "Complex Tree",
            "input": [1, None, 2, 3, 4, 5, None, None, 6, 7, None, 8, None, 9, 10, None, None, 11, None, 12, None, 13,
                      None, None, 14],
            "expected": [1, 2, 3, 6, 7, 11, 14, 4, 8, 12, 5, 9, 13, 10]
        },
        {
            "name": "Empty Tree",
            "input": [],
            "expected": []
        }
    ]

    passed = 0
    for idx, tc in enumerate(test_cases, 1):
        root = build_tree(tc["input"])
        result = sol.preorder(root)

        if result == tc["expected"]:
            print(f"✅ Test {idx} ({tc['name']}) Passed!")
            passed += 1
        else:
            print(f"❌ Test {idx} ({tc['name']}) Failed!")
            print(f"   Expected: {tc['expected']}")
            print(f"   Got:      {result}")

    print(f"\nResult: {passed}/{len(test_cases)} tests passed.")


if __name__ == "__main__":
    run_tests()
