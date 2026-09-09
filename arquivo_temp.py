varb = 1
varc = "abcd"
vard = 0.233
varf = True #False

print(type(varb))
print(type(varc))
print(type(vard))
print(type(varf))


## Operações numéricas

op1 = 1 + 3 #soma
op2 = 1 - 3 #subtração
op3 = 1 * 3 #multiplicação
op4 = 1 / 3 #divisão
op5 = 1 // 3 #divisão inteira
op6 = 2 ** 2 #potência
op7 = 3 % 5 #mod

calc = (3 + 5) / 7

## comparadores

print(3 == 3) #igualdade
print(3 != 2) #desigualdade
print(5 > 3) #maior
print(5 < 8) #menor
print(5 >= 3) #maior igual
print(5 <= 8) #menor igual

var1 = 3
var2 = 3

print(var1 is var2) #verifica idêntico
print(not var1 is var2) #verifica idêntico com negação

print(3 == 2 or 1 == 1) #operador ou
print(3 == 2 and 1 == 1) #operador e
print(2 == 2 or 3 == 2 and 1 == 1)

print(not 2 == 2 or 3 == 2 and 1 == 1) #operador e executa primeiro

# operações com strings

print("abcd" == "abcd") #compara valor
print("abcd" != "abcde") #compara valor
print("abcda" > "abcd") #compara tamanho
print("abc" < "abcd") #compara tamanho
print("abcd" >= "abcd") #compara tamanho
print("abcd" <= "abcd") #compara tamanho


# condicional if
if 3 < 2:
    print("condição")
elif 2 == 2:
    print("elif")
else:
    print("condição falsa")

varmatch = 6

#condicional match (switch case)
match varmatch:
    case 1:
        print("valor 1")
    case 2:
        print("valor 2")
    case 3:
        print("valor 3")
    case _:
        print("default!")
