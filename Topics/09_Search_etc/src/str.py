def test_str():
    #can concatenate strings
    str1 = "Hello" + " world"

    #can slice strings
    str2 = str1[1:4]
    print("str1:", str1)  # prints "Hello world!!!"
    print("str2:", str2)  # prints "ell"

    # assign str3 as another name for the contents of str1
    str3 = str1
    print("str3:", str3)    # prints "Hello world"

    # can reassign, but it's still immutable
    str1 = str1 + "!!!"
    # the original string is unmodified.  We created a new string and
    # called it str1, replacing the old meaning of the name str1
    print("str1:", str1)  # prints "Hello world!!!"
    print("str3:", str3)  # prints "Hello world"

test_str()
