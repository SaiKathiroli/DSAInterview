def test_myatoi(myatoi_func):
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
            actual = myatoi_func(tc)
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


def manual_int_to_string_conversion(string):
    sign = string[0]
    start_index = 0
    transformed_result = 0
    if sign == "-":
        start_index = 1
        multiply_by = -1
    elif sign == "+":
        start_index = 1
        multiply_by = 1
    else:
        multiply_by = 1
    for char in string[start_index:len(string)]:
        digit = ord(char) - ord('0')
        transformed_result = (transformed_result * 10) + digit
    return transformed_result * multiply_by


# --- PASTE YOUR myAtoi FUNCTION HERE ---
def myatoi(s: str) -> int:
    new_string = ""
    s = s.strip()
    if len(s) == 0:
        return 0
    if s[0].isalpha() or s[0] == ".":
        return 0
    if s[0] in ("+", "-"):
        if len(s) >= 2:
            if s[1] not in ("+", "-", " ") and (not s[1].isalpha()) and (s[1] != "."):
                pass
            else:
                return 0
        else:
            return 0
    new_string += s[0]
    for char in s[1::]:
        if char.isdigit():
            new_string += char
        else:
            break

    result = manual_int_to_string_conversion(new_string)

    if result > (2 ** 31 - 1):
        return 2 ** 31 - 1
    elif result < (-(2 ** 31)):
        return -(2 ** 31)
    else:
        return result


# Run the test harness
if __name__ == "__main__":
    print("   +0 123".strip())
    test_myatoi(myatoi)
    # myatoi("   +0 123")
