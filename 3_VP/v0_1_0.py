def test():
    string = "A man, a plan, a canal: Panama"
    usable = "".join([ch for ch in string if ch.isalnum()]).lower()
    print(usable)
    reversed_usable = usable[::-1].lower()
    print(reversed_usable)
    print(reversed_usable == usable)


test()
