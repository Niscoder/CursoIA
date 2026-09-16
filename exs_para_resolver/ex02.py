# Crie um algoritmo em Python onde haverá uma função para realizar
# operações matemáticas. Essa função deve implementar soma, subtração,
# multiplicação e divisão. Como parâmetro, deve receber a informação de
# qual operação deverá ser executado, e a operação deverá ocorrer em todos
# os números recebidos por ela. Por exemplo, caso eu envie a informação de
# soma e os números 2, 5, 8 e 10, o resultado deve ser 2+5+8+10. Não há limites
# de números que devem ser passados como parâmetros, e se o tipo de operação não
# ser informado, deve-se utilizar como padrão a soma. (Verificações: retornar
# erro ao verificar que haverá divisão por 0)

operation = input("Digite a operação desejada (soma, subtração, multiplicação, divisão): ")

def calculate(operation="soma", *args):
    match operation:
        case "soma":
            return sum(args)

        case "subtração":
            if not args:
                return 0
            result = args[0]
            for num in args[1:]:
                result -= num
            return result

        case "multiplicação":
            if not args:
                return 0
            result = 1
            for num in args:
                result *= num
            return result

        case "divisão":
            if not args:
                return 0
            result = args[0]
            for num in args[1:]:
                if num == 0:
                    return "Erro: Divisão por zero não é permitida."
                result /= num
            return result

        case _:
            return sum(args)  # Padrão é soma