-- 1. Tabela de Funcionários
CREATE TABLE TFuncionario (
    id_funcionario SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    cpf VARCHAR(14) UNIQUE NOT NULL,
    salario DECIMAL(10, 2) NOT NULL,
    email VARCHAR(100) NOT NULL,
    endereco_rua VARCHAR(100),
    endereco_num INT,
    endereco_bairro VARCHAR(100),
    endereco_cep VARCHAR(10)
);

-- 2. Atributo Multivalorado: Telefones do Funcionário[cite: 1]
CREATE TABLE TFuncionario_Telefone (
    id_funcionario INT NOT NULL,
    telefone VARCHAR(15) NOT NULL,
    PRIMARY KEY (id_funcionario, telefone),
    FOREIGN KEY (id_funcionario) REFERENCES TFuncionario(id_funcionario) ON DELETE CASCADE
);

-- 3. Especialização: Caixa[cite: 1]
CREATE TABLE TCaixa (
    id_funcionario INT PRIMARY KEY,
    num_caixa INT NOT NULL,
    FOREIGN KEY (id_funcionario) REFERENCES TFuncionario(id_funcionario) ON DELETE CASCADE
);

-- 4. Especialização: Gerente[cite: 1]
CREATE TABLE TGerente (
    id_funcionario INT PRIMARY KEY,
    senha_master VARCHAR(50) NOT NULL,
    FOREIGN KEY (id_funcionario) REFERENCES TFuncionario(id_funcionario) ON DELETE CASCADE
);

-- 5. Tabela de Clientes[cite: 1]
CREATE TABLE TCliente (
    id_cliente SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    cpf VARCHAR(14) UNIQUE,
    email VARCHAR(100),
    endereco_rua VARCHAR(100),
    endereco_num INT,
    endereco_bairro VARCHAR(100),
    endereco_cep VARCHAR(10)
);

-- 6. Atributo Multivalorado: Telefones do Cliente[cite: 1]
CREATE TABLE TCliente_Telefone (
    id_cliente INT NOT NULL,
    telefone VARCHAR(15) NOT NULL,
    PRIMARY KEY (id_cliente, telefone),
    FOREIGN KEY (id_cliente) REFERENCES TCliente(id_cliente) ON DELETE CASCADE
);

-- 7. Tabela de Fornecedores[cite: 1]
CREATE TABLE TFornecedor (
    id_fornecedor SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    cnpj VARCHAR(14) UNIQUE NOT NULL
);

-- 8. Atributo Multivalorado: Telefones do Fornecedor[cite: 1]
CREATE TABLE TFornecedor_Telefone (
    id_fornecedor INT NOT NULL,
    telefone VARCHAR(15) NOT NULL,
    PRIMARY KEY (id_fornecedor, telefone),
    FOREIGN KEY (id_fornecedor) REFERENCES TFornecedor(id_fornecedor) ON DELETE CASCADE
);

-- 9. Tabela de Produtos[cite: 1]
CREATE TABLE TProduto (
    id_produto SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    preco DECIMAL(10, 2) NOT NULL,
    marca VARCHAR(100)
);

-- 10. Tabela de Estoque[cite: 1]
CREATE TABLE TEstoque (
    id_estoque SERIAL PRIMARY KEY,
    quantidade INT NOT NULL,
    data_entrada DATE NOT NULL,
    data_atualizacao DATE NOT NULL,
    id_produto INT NOT NULL,
    id_funcionario_gerente INT NOT NULL,
    FOREIGN KEY (id_produto) REFERENCES TProduto(id_produto),
    FOREIGN KEY (id_funcionario_gerente) REFERENCES TGerente(id_funcionario)
);

-- 11. Tabela de Compras[cite: 1]
CREATE TABLE TCompra (
    id_compra SERIAL PRIMARY KEY,
    data DATE NOT NULL DEFAULT CURRENT_DATE,
    valor_total DECIMAL(10, 2) DEFAULT 0.00,
    id_cliente INT,
    id_funcionario_caixa INT NOT NULL,
    FOREIGN KEY (id_cliente) REFERENCES TCliente(id_cliente) ON DELETE SET NULL,
    FOREIGN KEY (id_funcionario_caixa) REFERENCES TCaixa(id_funcionario)
);

-- 12. Tabela Associativa: Itens da Compra[cite: 1]
CREATE TABLE TCompra_Produto (
    id_compra INT NOT NULL,
    id_produto INT NOT NULL,
    quantidade_vendida INT NOT NULL,
    preco_unitario DECIMAL(10, 2) NOT NULL,
    PRIMARY KEY (id_compra, id_produto),
    FOREIGN KEY (id_compra) REFERENCES TCompra(id_compra) ON DELETE CASCADE,
    FOREIGN KEY (id_produto) REFERENCES TProduto(id_produto)
);

-- 13. Tabela Associativa: Fornecedor e Produto[cite: 1]
CREATE TABLE TFornecedor_Produto (
    id_fornecedor INT NOT NULL,
    id_produto INT NOT NULL,
    PRIMARY KEY (id_fornecedor, id_produto),
    FOREIGN KEY (id_fornecedor) REFERENCES TFornecedor(id_fornecedor) ON DELETE CASCADE,
    FOREIGN KEY (id_produto) REFERENCES TProduto(id_produto) ON DELETE CASCADE
);