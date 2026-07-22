class Compra:
    def __init__(self, id_compra=None, data=None, valor_total=0.0, id_cliente=None, id_funcionario_caixa=None):
        self.id_compra = id_compra
        self.data = data
        self.valor_total = valor_total
        self.id_cliente = id_cliente
        self.id_funcionario_caixa = id_funcionario_caixa