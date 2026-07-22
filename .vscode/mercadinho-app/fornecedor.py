class Fornecedor:
    def __init__(self, id_fornecedor=None, nome_fantasia=None, cnpj=None, email=None, telefones=None):
        self.id_fornecedor = id_fornecedor
        self.nome_fantasia = nome_fantasia
        self.cnpj = cnpj
        self.email = email
        self.telefones = telefones if telefones is not None else []