# Crie um algoritmo em Python onde haverá uma função para realizar
# operações matemáticas. Essa função deve implementar soma, subtração,
# multiplicação e divisão. Como parâmetro, deve receber a informação de
# qual operação deverá ser executado, e a operação deverá ocorrer em todos
# os números recebidos por ela. Por exemplo, caso eu envie a informação de
# soma e os números 2, 5, 8 e 10, o resultado deve ser 2+5+8+10. Não há limites
# de números que devem ser passados como parâmetros, e se o tipo de operação não
# ser informado, deve-se utilizar como padrão a soma. (Verificações: retornar
# erro ao verificar que haverá divisão por 0)


def operacao(*valores, op="soma"):
    resultado = (valores[0])
    
    if op not in ["soma", "sub", "mult", "div"]:
        op = "soma"

    if op == "soma":
        for n in valores[1:]:
            resultado = resultado + n

    elif op == "sub":
        for n in valores[1:]:
            resultado = resultado - n

    elif op == "mult":
        for n in valores[1:]:
            resultado = resultado * n

    elif op == "div":
        for n in valores[1:]:
            if n == 0:
                return "Erro, divisão por zero!"
            
            resultado = resultado / n

    return resultado


print(operacao(2, 5, 1))
print(operacao(2, 5, 1, op="sub"))
print(operacao(2, 5, 1, op="mult"))
print(operacao(10, 5, 2, op="div"))
print(operacao(0, 5, 2, op="div"))
print(operacao(10, 0, 2, op="div"))