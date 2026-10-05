# import top_classe
import numpy as np
from classes.top_classe import Turma, printar_info_turma

turma = Turma("A1", ["mat", "port", "prog"], ["André", "Maria", "Carlos"])
alunos = turma.alunos
notas = {"André": {"mat": 100, "port": 89, "prog": 75},
         "Maria": {"mat": 80, "port": 78, "prog": 96}}

turma.atribuir_notas(notas)
printar_info_turma(turma)


for aluno in turma.alunos:
    aluno.calcular_coeficiente()
    aluno.printar_aluno()

print(turma)

print(np.asarray([1,2,3]))
