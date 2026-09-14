#lista = ["olá", 130]

#lista_exemplo = ["oi", 3, True]
#lista_exemplo.append(0.356)
##lista_exemplo.append(lista)
#lista_exemplo.extend(lista)

#lista_exemplo = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

#slice1 = lista_exemplo[2:]
#slice2 = lista_exemplo[2:8]
#slice3 = lista_exemplo[1::4]

#slice4 = lista_exemplo[-1]
#slice5 = lista_exemplo[-3:-1]

##slice6 = lista_exemplo[::-1]
##slice7 = lista_exemplo[6:0:-1]

##print(slice1)
##print(slice2)
##print(slice3)
##print(slice4)
##print(slice5)   
##print(slice6) 
##print(slice7) 

##print(len(slice7))

#i = 0

#while i < 3:
#    print(lista_exemplo[i])
#    i +=1

for _ in range(int(input())):
    name = input()
    score = float(input())
    
array = [[name,score]]
array.sort()

print(array)