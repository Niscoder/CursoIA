#https://www.hackerrank.com/challenges/collections-counter/problem?isFullScreen=true

from collections import Counter

x = int(input())
shoes_array = input().split()
shoes_count = Counter(shoes_array)
n = int(input())

payment = 0

for i in range(n):
    shoes_value = input().split()
    shoes = shoes_value[0]
    value = int(shoes_value[1])
    if shoes_count[shoes] > 0:
        shoes_count[shoes] = shoes_count[shoes] - 1
        payment = payment + value

print(payment)
