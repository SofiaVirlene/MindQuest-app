class Funcionario:
    def __init__(self, id_funcionario=None, nome=None, cpf=None, cargo=None, salario=None, data_admissao=None, telefones=None, num_caixa=None, senha_usuario=None):
        self.id_funcionario = id_funcionario
        self.nome = nome
        self.cpf = cpf
        self.cargo = cargo # 'Caixa' ou 'Gerente'
        self.salario = salario
        self.data_admissao = data_admissao
        self.telefones = telefones if telefones is not None else []
        
        # Atributos específicos das tabelas filhas
        self.num_caixa = num_caixa
        self.senha_usuario = senha_usuario