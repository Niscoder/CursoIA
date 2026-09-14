#https://www.hackerrank.com/challenges/python-loops/problem?isFullScreen=true

n = int(input()) #input no prompt

arr = []
for i in range(n):
    arr.append(i)

for i in arr:
    print(i ** 2)
