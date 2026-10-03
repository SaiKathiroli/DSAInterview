"""
https://leetcode.com/problems/valid-palindrome/submissions/2160700112
"""

class Solution:
    def isPalindrome(self, s: str) -> bool:
        compare_s = ""
        for char in s:
            if char.isalnum():
                compare_s = compare_s + char.lower()

        compare_s = compare_s.strip()

        return compare_s == compare_s[::-1]


if __name__ == "__main__":
    solver = Solution()

    test_cases = [
        ("A man, a plan, a canal: Panama", True),
        ("race a car", False),
        (" ", True),
        ("0P", False),
        ("ab_a", True),
    ]

    for s, expected in test_cases:
        result = solver.isPalindrome(s)
        status = "PASS" if result == expected else "FAIL"
        print(f"[{status}] Input: {s!r:<35} | Got: {result:<5} | Expected: {expected}")
