#https://www.hackerrank.com/challenges/list-comprehensions/problem?isFullScreen=true

x = int(input()) #input no prompt
y = int(input()) #input no prompt
z = int(input()) #input no prompt
n = int(input()) #input no prompt

arr = []

for i in range(x + 1):
    for j in range(y + 1):
        for k in range(z + 1):
            if n != (i + j + k):
                arr.append([i,j,k])

print(arr)
