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
