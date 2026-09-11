#https://www.hackerrank.com/challenges/list-comprehensions/problem?isFullScreen=true

x = int(input()) #input no prompt
y = int(input()) #input no prompt
z = int(input()) #input no prompt
n = int(input()) #input no prompt

arr = []

for i in range(x + 1):
    for j in range(y + 1):
        for k in range(z + 1):
            arr.append([i,j,k])

arr_result = []

for element in arr:
    soma = element[0] + element[1] + element[2]
    if soma != n:
        arr_result.append(element)

print(arr_result)
