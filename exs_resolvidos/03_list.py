#https://www.hackerrank.com/challenges/nested-list/problem?isFullScreen=true


alunos_notas = []
notas = []

for _ in range(int(input())):
    name = input()
    score = float(input())
    alunos_notas.append([name, score])
    if notas.count(score) == 0:
        notas.append(score) 

alunos_notas.sort()
notas.sort()
segunda_menor_nota = notas[1]

for aluno in alunos_notas:
    if segunda_menor_nota == aluno[1]:
        print(aluno[0])
