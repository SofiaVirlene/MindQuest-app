class Estoque:
    def __init__(self, id_estoque=None, quantidade=None, data_entrada=None, data_atualizacao=None, id_produto=None, id_funcionario_gerente=None):
        self.id_estoque = id_estoque
        self.quantidade = quantidade
        self.data_entrada = data_entrada
        self.data_atualizacao = data_atualizacao
        self.id_produto = id_produto
        self.id_funcionario_gerente = id_funcionario_gerente