quantidade = int(input("Digite a quantidade de alunos a serem cadastrados: "))

Alunos = {}
AlunosAP = ()
AlunosREC = ()
AlunosREP = ()

for i in range(quantidade):
    nome = input("Nome do aluno: ")
    nota = float(input("Nota do aluno: "))
    Alunos[nome] = nota

alunos_ordenados = sorted(Alunos.items())

print(Alunos)


for indice, (nome, nota) in enumerate(alunos_ordenados, start = 1):

    aluno_info = (indice, nome, nota)

    if nota >= 60:
        AlunosAP += (aluno_info,)
    elif nota >= 40:
        AlunosREC += (aluno_info,)
    else:
        AlunosREP += (aluno_info,)

AlunosAP = sorted(AlunosAP)
AlunosREC = sorted(AlunosREC)
AlunosREP = sorted(AlunosREP)

print("Alunos aprovados:", AlunosAP)
print("Alunos em recuperação:", AlunosREC)
print("Alunos reprovados:", AlunosREP)