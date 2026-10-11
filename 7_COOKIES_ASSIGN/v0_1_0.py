from typing import List


class Solution:
    def findContentChildren(self, g: List[int], s: List[int]) -> int:
        """
        g: greed factor of each child
        s: size of each cookie
        Returns: maximum number of content children
        """
        # TODO: Implement your solution here
        count = 0
        for indexs, values in enumerate(s):
            target_index = len(g)
            for indexg, valueg in enumerate(g):
                # values >= valueg
                if values >= valueg:
                    target_index = min(target_index, indexg)

            if target_index != len(g):
                g.pop(target_index)
                count += 1

        return count


# =====================================================================
# Test Suite & Harness
# =====================================================================

TEST_CASES = [
    {
        "name": "LeetCode Example 1 (Fewer cookies than children)",
        "g": [1, 2, 3],
        "s": [1, 1],
        "expected": 1,
    },
    {
        "name": "LeetCode Example 2 (Surplus of large cookies)",
        "g": [1, 2],
        "s": [1, 2, 3],
        "expected": 2,
    },
    {
        "name": "Empty cookies list (s is empty)",
        "g": [1, 2, 3],
        "s": [],
        "expected": 0,
    },
    {
        "name": "All cookies too small",
        "g": [5, 6, 7],
        "s": [1, 2, 3, 4],
        "expected": 0,
    },
    {
        "name": "Single child, matching cookie",
        "g": [3],
        "s": [3],
        "expected": 1,
    },
    {
        "name": "Single child, insufficient cookie",
        "g": [4],
        "s": [3],
        "expected": 0,
    },
    {
        "name": "Exact 1-to-1 match",
        "g": [1, 2, 3, 4],
        "s": [1, 2, 3, 4],
        "expected": 4,
    },
    {
        "name": "Unsorted inputs requiring ordering",
        "g": [10, 9, 8, 7],
        "s": [5, 6, 7, 8],
        "expected": 2,
    },
    {
        "name": "Duplicate greed factors and duplicate cookie sizes",
        "g": [2, 2, 2],
        "s": [1, 2, 2],
        "expected": 2,
    },
    {
        "name": "Greedy trap (prevent wasting large cookies on small greed)",
        "g": [1, 2, 3],
        "s": [3],
        "expected": 1,
    },
    {
        "name": "Partial overlap requiring optimal pairing",
        "g": [2, 3, 4],
        "s": [1, 2, 3],
        "expected": 2,
    },
    {
        "name": "Constraint boundary values (up to 2^31 - 1)",
        "g": [2147483647, 1],
        "s": [1, 2147483647],
        "expected": 2,
    },
    {
        "name": "Large surplus of small cookies that cannot satisfy high greed",
        "g": [100],
        "s": [1] * 50,
        "expected": 0,
    },
]


def run_tests():
    solver = Solution()
    passed = 0
    total = len(TEST_CASES)

    print(f"Running {total} test cases for '455. Assign Cookies'...\n" + "-" * 60)

    for idx, tc in enumerate(TEST_CASES, start=1):
        g_input = tc["g"].copy()
        s_input = tc["s"].copy()
        expected = tc["expected"]
        name = tc["name"]

        try:
            actual = solver.findContentChildren(g_input, s_input)
            if actual == expected:
                print(f"[PASS] Case {idx:02d}: {name}")
                passed += 1
            else:
                print(f"[FAIL] Case {idx:02d}: {name}")
                print(f"       Input:    g={tc['g']}, s={tc['s']}")
                print(f"       Expected: {expected}")
                print(f"       Actual:   {actual}\n")
        except NotImplementedError:
            print("Error: Solution is not yet implemented.")
            return
        except Exception as e:
            print(f"[ERROR] Case {idx:02d}: {name} raised {type(e).__name__}: {e}")

    print("-" * 60)
    print(f"Summary: {passed}/{total} tests passed.")


if __name__ == "__main__":
    run_tests()
