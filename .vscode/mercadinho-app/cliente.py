class Cliente:
    def __init__(self, id_cliente=None, nome=None, cpf=None, email=None, endereco_rua=None, endereco_num=None, endereco_bairro=None, endereco_cep=None, telefones=None):
        self.id_cliente = id_cliente
        self.nome = nome
        self.cpf = cpf
        self.email = email
        self.endereco_rua = endereco_rua
        self.endereco_num = endereco_num
        self.endereco_bairro = endereco_bairro
        self.endereco_cep = endereco_cep
        self.telefones = telefones if telefones is not None else []