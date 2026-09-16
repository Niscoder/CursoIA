# Crie um sistema para cadastrar alunos de uma turma, deve conter nas informação
# dos alunos o nome e as notas de cada disciplina. Aluno deve ser uma classe para
# salvar as informações, e deverá ter um método para calcular o coeficiente do aluno,
# e outro para printar as informações do aluno com o nome, o nome de cada
# disciplina com a nota do aluno, e o coeficiente.

class Turma:
    def __init__(self, nome, disciplinas, alunos) -> None:
        self.nome = nome
        self.disciplinas = disciplinas
        self.alunos = []
        self.inserir_alunos(alunos)

    def inserir_alunos(self, alunos):
        for aluno in alunos:
            self.alunos.append(Aluno(aluno, self.disciplinas))

    def atribuir_notas(self, notas):
        for aluno in alunos:
            if aluno.nome in notas:
                for disc, nota in notas[aluno.nome].items():
                    aluno.atribuir_nota(disc, nota)

class Aluno:
    def __init__(self, nome, disciplinas) -> None:
        self.nome = nome
        self.disciplinas = {}
        self.coeficiente = 0
        for disc in disciplinas:
            self.disciplinas[disc] = None

    def atribuir_nota(self, disc, nota):
        if disc in self.disciplinas.keys():
            self.disciplinas[disc] = nota

    def calcular_coeficiente(self):
        soma_notas = 0
        for nota in self.disciplinas.values():
            if not nota is None:
                soma_notas = soma_notas + nota

        self.coeficiente = soma_notas / len(self.disciplinas)

    def printar_aluno(self):
        print(f"Aluno: {self.nome}, Notas: {self.disciplinas}, Coeficiente: {self.coeficiente}")



turma = Turma("A1", ["mat", "port", "prog"], ["André", "Maria", "Carlos"])
alunos = turma.alunos
notas = {"André": {"mat": 100, "port": 89, "prog": 75},
         "Maria": {"mat": 80, "port": 78, "prog": 96}}

turma.atribuir_notas(notas)

for aluno in turma.alunos:
    aluno.calcular_coeficiente()
    aluno.printar_aluno()

