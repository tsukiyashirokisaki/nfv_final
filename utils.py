def hash2code(s):
    h = 0
    for c in s:
        h = (31 * h + ord(c)) & 0xFFFFFFFF
    return ((h + 0x80000000) & 0xFFFFFFFF) - 0x80000000
# http://hk.noobyard.com/article/p-kkdkmrff-ch.html
