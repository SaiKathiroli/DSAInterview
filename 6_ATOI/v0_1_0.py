"""
def myAtoi(s: str) -> int:
    new_string = ""
    sign_count = 0
    for ch in s:
        if ch == " " and len(new_string) < 1:
            continue
        if ch == " " and len(new_string) >= 1:
            break
        if (ch == "+" or ch == "-") and (sign_count == 0) and len(new_string) < 1:
            new_string += ch
            sign_count += 1
            continue
        if (ch == "+" or ch == "-") and len(new_string) >= 1:
            break
        if ch.isalpha():
            break
        if ch == ".":
            break
        if ch.isdigit():
            new_string += ch
            continue

    if len(new_string) >= 1:
        result = int(new_string)
    else:
        result = 0

    if result > (2 ** 31 - 1):
        return 2 ** 31 - 1
    elif result < (-(2 ** 31)):
        return -(2 ** 31)
    else:
        return result
"""

"""
print(myAtoi("42"))
print(myAtoi("-042"))
print(myAtoi("1337c0d3"))
print(myAtoi("0-1"))
print(myAtoi("words and 987"))
"""


def test_myAtoi(myAtoi_func):
    test_cases = [
        # Original tests
        "42", "-042", "1337c0d3", "0-1", "words and 987",

        # Whitespaces and Signs
        "   -42", "   +0 123", "+-12", "-+12", " - 42", "+",

        # Boundary / Overflow Clamping
        "2147483647", "-2147483648", "2147483648", "-2147483649",
        "99999999999999999", "-99999999999999999",

        # Leading Zeros and Length Tricks
        "0000000000012345678", "000000000002147483648", "-000000000000001",

        # Interrupted and Empty Strings
        "3.14159", "", "   "
    ]

    expected_results = [
        42, -42, 1337, 0, 0,
        -42, 0, 0, 0, 0, 0,
        2147483647, -2147483648, 2147483647, -2147483648,
        2147483647, -2147483648,
        12345678, 2147483647, -1,
        3, 0, 0
    ]

    passed = 0
    failed = 0
    failed_details = []

    print(f"{'STATUS':<8} | {'INPUT':<25} | {'EXPECTED':<12} | {'ACTUAL'}")
    print("-" * 70)

    for i, tc in enumerate(test_cases):
        expected = expected_results[i]

        try:
            actual = myAtoi_func(tc)
            if actual == expected:
                status = "✅ PASS"
                passed += 1
            else:
                status = "❌ FAIL"
                failed += 1
                failed_details.append(f"Input: '{tc}' | Expected: {expected} | Actual: {actual}")

        except Exception as e:
            # Catches out-of-bounds, type errors, or any other crash in your code
            status = "💥 CRASH"
            actual = f"Error: {type(e).__name__} ({str(e)})"
            failed += 1
            failed_details.append(f"Input: '{tc}' | Expected: {expected} | Actual: CRASHED - {actual}")

        print(f"{status:<8} | \"{tc}\"{' ' * (23 - len(tc))} | {expected:<12} | {actual}")

    # Print Final Summary
    print("\n" + "=" * 50)
    print("📝 TEST SUMMARY")
    print("=" * 50)
    print(f"Total Tests : {len(test_cases)}")
    print(f"Passed      : {passed} ✅")
    print(f"Failed      : {failed} ❌")

    if failed > 0:
        print("\n🔍 FAILED TEST DETAILS:")
        for detail in failed_details:
            print(f"  - {detail}")
    else:
        print("\n🏆 PERFECT SCORE! All edge cases handled.")


# --- PASTE YOUR myAtoi FUNCTION HERE ---
def myAtoi(s: str) -> int:
    new_string = ""
    sign_count = 0
    for ch in s:
        if ch == " " and len(new_string) < 1:
            continue
        if ch == " " and len(new_string) >= 1:
            break
        if (ch == "+" or ch == "-") and (sign_count == 0) and len(new_string) < 1:
            new_string += ch
            sign_count += 1
            continue
        if (ch == "+" or ch == "-") and len(new_string) >= 1:
            break
        if ch.isalpha():
            break
        if ch == ".":
            break
        if ch.isdigit():
            new_string += ch
            continue

    if len(new_string) >= 1 and new_string.strip("+").isdigit():
        result = int(new_string)
    elif len(new_string) >= 1 and new_string.strip("-").isdigit():
        result = int(new_string)
    else:
        result = 0

    if result > (2 ** 31 - 1):
        return 2 ** 31 - 1
    elif result < (-(2 ** 31)):
        return -(2 ** 31)
    else:
        return result


# Run the test harness
if __name__ == "__main__":
    test_myAtoi(myAtoi)