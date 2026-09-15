# Faça um código em Python onde o usuário deve informar a quantidade de alunos que ele irá cadastrar,
# depois crie um loop para adicionar todos os alunos, devendo informar o nome e em seguida a nota do
# aluno. O sistema deve processar as informações e retornar uma lista de dicionários ou tuplas com todos
# os alunos. Depois retorne uma lista de dicionários ou tuplas contendo os alunos que foram aprovados
# (nota 60 ou maior), outra de alunos que ficaram de recuperação (nota entre 40 e baixo de 60),
# e a última de alunos que reprovaram. Todas as listas devem estar ordenadas em ordem de chamada e deve
# conter o número da chamada, nome e nota.

n = input()

array_alunos = []

for _ in range(int(n)):
    nome = input()
    nota = int(input())
    array_alunos.append([nome, nota])

array_alunos.sort()

array_dict_todos = []
array_dict_aprovados = []
array_dict_recuperacao = []
array_dict_reprovados = []

for idx, aluno in enumerate(array_alunos, 1):
    aluno_dict = {"chamanda": idx, "nome": aluno[0], "nota": aluno[1]}
    array_dict_todos.append(aluno_dict)
    if aluno_dict["nota"] >= 60:
        array_dict_aprovados.append(aluno_dict)

    elif aluno_dict["nota"] >= 40:
        array_dict_recuperacao.append(aluno_dict)

    else:
        array_dict_reprovados.append(aluno_dict)

print("Todos alunos:")
print(array_dict_todos)
print("Alunos aprovados:")
print(array_dict_aprovados)
print("Alunos recuperação:")
print(array_dict_recuperacao)
print("Alunos reprovados:")
print(array_dict_reprovados)
