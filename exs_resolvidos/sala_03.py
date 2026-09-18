# Crie um sistema para cadastrar alunos de uma turma, deve conter nas informação
# dos alunos o nome e as notas de cada disciplina. Aluno deve ser uma classe para
# salvar as informações, e deverá ter um método para calcular o coeficiente do aluno,
# e outro para printar as informações do aluno com o nome, o nome de cada
# disciplina com a nota do aluno, e o coeficiente.

class Aluno:
    def __init__(self, nome, disciplinas):
        self.nome = nome
        self.disciplinas = disciplinas

    def calcular_coeficiente(self):

        if not self.disciplinas:
            return 0.0

        soma_notas = sum(self.disciplinas.values())
        coeficiente = soma_notas / len(self.disciplinas)
        return coeficiente

    def imprimir_info(self):
        print(f"Nome: {self.nome}")
        print("Disciplinas")

        for disciplina, nota in self.disciplinas.items():
            print(f"  {disciplina}: {nota}")

        coeficiente = self.calcular_coeficiente()
        print(f"Coeficiente: {coeficiente:.2f}")

aluno1 = Aluno("João", {"Matemática": 8.5, "Português": 7.0, "História": 9.0})
aluno2 = Aluno("Maria", {"Matemática": 9.5, "Português": 8.0, "História": 7.5})

aluno1.imprimir_info()
aluno2.imprimir_info()