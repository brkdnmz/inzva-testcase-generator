# Always good to prepare solutions with various languages (namely C++ & Python)!
# Helps adjusting constraints properly. For instance, if they are too large for Python, lower them.

n = int(input())
a = list(map(int, input().split()))
distincts = set()
for x in a:
    distincts.add(x)
    print(len(distincts), end=" ")
