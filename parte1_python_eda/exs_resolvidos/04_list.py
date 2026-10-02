#https://www.hackerrank.com/challenges/python-lists/problem?isFullScreen=true

N = int(input())

mylist = []

for _ in range(N):
    command = input()
    command_args = command.split()

    if command_args[0] == "insert":
        i = int(command_args[1])
        e = int(command_args[2])
        mylist.insert(i, e)
    elif command_args[0] == "print":
        print(mylist)
    elif command_args[0] == "remove":
        e = int(command_args[1])
        mylist.remove(e)
    elif command_args[0] == "append":
        e = int(command_args[1])
        mylist.append(e)
    elif command_args[0] == "sort":
        mylist.sort()
    elif command_args[0] == "pop":
        mylist.pop()
    elif command_args[0] == "reverse":
        mylist.reverse()
