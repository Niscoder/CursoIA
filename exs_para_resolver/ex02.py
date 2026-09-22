def calculate(operation="soma", *args):
    
    operation = operation.strip().lower()

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
            return "Erro: Operação inválida."

op = input("Digite a operação desejada (soma, subtração, multiplicação, divisão): ")

entrada_numeros = input("Digite os números separados por espaço: ")
numeros = [float(x) for x in entrada_numeros.split()]

resultado = calculate(op, *numeros)
print(f"Resultado: {resultado}")  