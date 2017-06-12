# --------------
# User Instructions
#
# Write a function, longest_subpalindrome_slice(text) that takes
# a string as input and returns the i and j indices that
# correspond to the beginning and end indices of the longest
# palindrome in the string.
#
# Grading Notes:
#
# You will only be marked correct if your function runs
# efficiently enough. We will be measuring efficency by counting
# the number of times you access each string. That count must be
# below a certain threshold to be marked correct.
#
# Please do not use regular expressions to solve this quiz!

def longest_subpalindrome_slice(text):
    "Return (i, j) such that text[i:j] is the longest palindrome in text."    
    l = len(text)
    if l == 0:
        return (0, 0)
    text = text.lower()
    flags = [[False for _ in range(l)] for _ in range(l)]
    #Base cases
    #all strings of length 1 are palindromes
    max_len = 1
    for i in range(l):
        flags[i][i] = True
    #check substrings of length 2
    start = 0
    for i in range(l - 1):
        if text[i] == text[i + 1]:
            flags[i][i+1] = True
            start = i
            max_len = 2
    #Induction: dynamic programming: check strings of length 3 to n
    for k in range(3, l + 1):
        for i in range(l - k + 1):
            j = i + k - 1
            if (flags[i+1][j-1] and text[i] == text[j]):
                flags[i][j] = True
                if (k > max_len):
                    start = i
                    max_len = k
    return (start, start + max_len)

def test():
    L = longest_subpalindrome_slice
    assert L('racecar') == (0, 7)
    assert L('Racecar') == (0, 7)
    assert L('RacecarX') == (0, 7)
    assert L('Race carr') == (7, 9)
    assert L('') == (0, 0)
    assert L('something rac e car going') == (8,21)
    assert L('xxxxx') == (0, 5)
    assert L('Mad am I ma dam.') == (0, 15)
    return 'tests pass'

print test()
