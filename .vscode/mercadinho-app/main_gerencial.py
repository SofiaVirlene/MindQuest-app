import datetime
import sys
from conexao import Conexao
from cliente import Cliente
from cliente_dao import ClienteDAO
from funcionario import Funcionario
from funcionario_dao import FuncionarioDAO 
from fornecedor import Fornecedor
from fornecedor_dao import FornecedorDAO
from produto import Produto
from produto_dao import ProdutoDAO
from estoque_dao import EstoqueDAO
from compra_dao import CompraDAO

def verificar_autorizacao_gerente():
    """
    Função auxiliar para proteger opções restritas.
    Pede as credenciais do gerente e retorna o id_gerente se for válido.
    """
    print("\n" + "-" * 40)
    print("[🔒 ACESSO RESTRITO] Operação exclusiva para Gerentes.")
    print("-" * 40)
    
    login = input("Usuário/Login do Gerente: ").strip()
    senha = input("Senha do Gerente: ").strip()
    
    conexao = Conexao.obter_conexao()
    if conexao:
        nome_gerente = FuncionarioDAO.autenticar_gerente(conexao, login, senha)
        
        if nome_gerente:
            cursor = conexao.cursor()
            cursor.execute("SELECT id_funcionario FROM TFuncionario WHERE login = %s", (login,))
            id_gerente = cursor.fetchone()[0]
            cursor.close()
            conexao.close()
            
            print(f">> [Acesso Autorizado] Gerente: {nome_gerente}")
            print("-" * 40)
            return id_gerente
        else:
            conexao.close()
            print(">> [Erro] Login ou Senha incorretos ou usuário não possui cargo de Gerente!")
            print("-" * 40)
            return None
    else:
        print(">> [Erro] Não foi possível conectar ao banco de dados.")
        print("-" * 40)
        return None

def exibir_menu_gerencial():
    print("\n" + "="*40)
    print("      MERCADINHO - PAINEL ADMINISTRATIVO")
    print("="*40)
    print("1. Cadastrar Cliente (com Telefones)")
    print("2. Cadastrar Funcionário (Caixa / Gerente) 🔒")
    print("3. Cadastrar Fornecedor (com Telefones)")
    print("4. Cadastrar Produto (TProduto)")
    print("5. Vincular Produto ao Fornecedor (TFornecedor_produto)")
    print("6. Dar Entrada no Estoque (Apenas Gerente) 🔒")
    print("7. Relatório de Estoque Geral (JOIN / GROUP BY)")
    print("8. Painel Financeiro (Faturamento, Gastos e Lucro) 🔒")
    print("9. Central de Consultas (Contatos/Busca) 🔍")
    print("10. Central de Exclusões (Remover Dados) 🔒")
    print("0. Sair do Panel")
    print("="*40)

def submenu_consultas():
    while True:
        print("\n" + "-"*40)
        print("        🔍 CENTRAL DE CONSULTAS E CONTATOS")
        print("-"*40)
        print("1. Buscar Cliente (por CPF)")
        print("2. Buscar Funcionário (por CPF)")
        print("3. Buscar Fornecedor (por CNPJ)")
        print("0. Voltar ao Menu Principal")
        print("-"*40)
        
        escolha = input("Escolha uma opção de busca: ").strip()
        
        if escolha == "0":
            break
            
        if escolha not in ["1", "2", "3"]:
            print(">> Opção inválida! Tente novamente.")
            continue
            
        conexao = Conexao.obter_conexao()
        if not conexao:
            print(">> Erro ao conectar ao banco de dados.")
            continue

        try:
            if escolha == "1":
                cpf = input("\nDigite o CPF do Cliente: ").strip()
                res = ClienteDAO.buscar_por_cpf(conexao, cpf)
                if res:
                    print("\n" + "="*40)
                    print(f"ID Cliente: {res[0]}\nNome: {res[1]}\nEmail: {res[2]}\nContatos: {res[3]}")
                    print("="*40)
                else:
                    print(">> Cliente não encontrado.")
                    
            elif escolha == "2":
                cpf = input("\nDigite o CPF do Funcionário: ").strip()
                res = FuncionarioDAO.buscar_por_cpf(conexao, cpf)
                if res:
                    print("\n" + "="*40)
                    print(f"ID Funcionário: {res[0]}\nNome: {res[1]}\nCargo: {res[2]}\nContatos: {res[3]}")
                    print("="*40)
                else:
                    print(">> Funcionário não encontrado.")
                    
            elif escolha == "3":
                cnpj = input("\nDigite o CNPJ do Fornecedor: ").strip()
                res = FornecedorDAO.buscar_por_cnpj(conexao, cnpj)
                if res:
                    print("\n" + "="*40)
                    print(f"ID Fornecedor: {res[0]}\nNome: {res[1]}\nCNPJ: {res[2]}\nContatos: {res[3]}")
                    print("="*40)
                else:
                    print(">> Fornecedor não encontrado.")
        finally:
            conexao.close()

def submenu_exclusoes():
    while True:
        print("\n" + "-"*40)
        print("        ❌ CENTRAL DE EXCLUSÕES DE REGISTROS")
        print("-"*40)
        print("1. Excluir Cliente (por ID)")
        print("2. Excluir Funcionário (por ID)")
        print("3. Excluir Fornecedor (por ID)")
        print("0. Voltar ao Menu Principal")
        print("-"*40)
        
        escolha = input("Escolha o que deseja excluir: ").strip()
        
        if escolha == "0":
            break
            
        if escolha not in ["1", "2", "3"]:
            print(">> Opção inválida! Tente novamente.")
            continue
            
        if escolha == "1":
            id_c = int(input("\nDigite o ID do Cliente a ser removido: "))
            confirmar = input(f"Tem certeza que deseja apagar o Cliente ID {id_c}? (S/N): ").strip().upper()
            if confirmar == "S":
                if ClienteDAO.deletar(id_c):
                    print(">> [Sucesso] Cliente e contatos associados foram removidos!")
                else:
                    print(">> [Erro] Falha ao remover cliente.")
                    
        elif escolha == "2":
            id_f = int(input("\nDigite o ID do Funcionário a ser removido: "))
            cargo = input("Informe o Cargo exato (Caixa/Gerente): ").strip()
            confirmar = input(f"Tem certeza que deseja apagar o Funcionário ID {id_f}? (S/N): ").strip().upper()
            if confirmar == "S":
                if FuncionarioDAO.deletar(id_f, cargo):
                    print(f">> [Sucesso] {cargo} e dependências removidos com sucesso!")
                else:
                    print(">> [Erro] Falha ao remover funcionário. Verifique se digitou o cargo corretamente.")
                    
        elif escolha == "3":
            id_fo = int(input("\nDigite o ID do Fornecedor a ser removido: "))
            confirmar = input(f"Tem certeza que deseja apagar o Fornecedor ID {id_fo}? (S/N): ").strip().upper()
            if confirmar == "S":
                if FornecedorDAO.deletar(id_fo):
                    print(">> [Sucesso] Fornecedor e registros vinculados foram removidos!")
                else:
                    print(">> [Erro] Falha ao remover fornecedor.")

def main():
    while True:
        exibir_menu_gerencial()
        opcao = input("Escolha uma opção: ").strip()
        hoje = datetime.date.today().strftime('%Y-%m-%d')

        if opcao == "1":
            print("\n--- Novo Cliente ---")
            nome = input("Nome: ")
            cpf = input("CPF: ")
            email = input("Email: ")
            rua = input("Rua: ")
            num = int(input("Número: "))
            bairro = input("Bairro: ")
            cep = input("CEP: ")
            telefones = []
            while True:
                t = input("Telefone (ou Enter para finalizar): ")
                if not t: break
                telefones.append(t)
            c = Cliente(nome=nome, cpf=cpf, email=email, endereco_rua=rua, endereco_num=num, endereco_bairro=bairro, endereco_cep=cep, telefones=telefones)
            if ClienteDAO.inserir(c): print(">> Cliente gravado com sucesso!")

        elif opcao == "2":
            if verificar_autorizacao_gerente():
                print("\n--- Novo Funcionário Especializado ---")
                nome = input("Nome: ")
                cpf = input("CPF: ")
                salario = float(input("Salário: R$ "))
                data_adm = input("Data de Admissão (AAAA-MM-DD): ")
                print("Especialização:\n1 - Caixa\n2 - Gerente")
                sel = input("Opção: ")
                num_caixa, senha_master = None, None
                if sel == "1":
                    cargo = "Caixa"
                    num_caixa = int(input("Número do Terminal de Caixa: "))
                else:
                    cargo = "Gerente"
                    senha_master = input("Senha Master do Gerente: ")
                telefones = []
                while True:
                    t = input("Telefone (ou Enter para finalizar): ")
                    if not t: break
                    telefones.append(t)
                f = Funcionario(nome=nome, cpf=cpf, cargo=cargo, salario=salario, data_admissao=data_adm, telefones=telefones, num_caixa=num_caixa, senha_usuario=senha_master)
                if FuncionarioDAO.inserir(f): print(f">> {cargo} gravado com sucesso!")

        elif opcao == "3":
            print("\n--- Novo Fornecedor ---")
            nome_f = input("Nome do Fornecedor: ")
            cnpj = input("CNPJ: ")
            telefones = []
            while True:
                t = input("Telefone do Fornecedor (ou Enter para finalizar): ")
                if not t: break
                telefones.append(t)
            forn = Fornecedor(nome=nome_f, cnpj=cnpj, telefones=telefones)
            if FornecedorDAO.inserir(forn): print(">> Fornecedor gravado com sucesso!")

        elif opcao == "4":
            print("\n--- Novo Produto ---")
            nome = input("Nome do Produto: ")
            preco = float(input("Preço de Venda: R$ "))
            marca = input("Marca: ")
            p = Produto(nome=nome, preco=preco, marca=marca)
            if ProdutoDAO.inserir(p): print(">> Produto gravado com sucesso!")

        elif opcao == "5":
            print("\n--- Vincular Produto ao Fornecedor ---")
            id_f = int(input("ID do Fornecedor: "))
            id_p = int(input("ID do Produto: "))
            if FornecedorDAO.vincular_produto(id_f, id_p): print(">> Vínculo realizado com sucesso!")

        elif opcao == "6":
            id_gerente_validado = verificar_autorizacao_gerente()
            if id_gerente_validado:
                print("\n--- Entrada de Mercadoria (Estoque) ---")
                id_prod = int(input("ID do Produto: "))
                print(f"ID do Gerente Responsável (Autenticado): {id_gerente_validado}")
                qtd = int(input("Quantidade de entrada: "))
                if EstoqueDAO.dar_entrada(id_prod, id_gerente_validado, qtd, hoje): 
                    print(">> Estoque updated!")

        elif opcao == "7":
            print("\n--- Relatório Estatístico de Estoque ---")
            dados = EstoqueDAO.obter_relatorio_estoque()
            print("-" * 65)
            print(f"{'ID':<4} | {'Produto':<18} | {'Marca':<12} | {'Preço':<10} | {'Qtd Estoque'}")
            print("-" * 65)
            for d in dados: print(f"{d[0]:<4} | {d[1]:<18} | {d[2]:<12} | R$ {d[3]:<7.2f} | {d[4]}")
            print("-" * 65)

        elif opcao == "8":
            if verificar_autorizacao_gerente():
                print("\n" + "-"*40)
                print("      PAINEL FINANCEIRO GERENCIAL")
                print("-"*40)
                balanco = CompraDAO.obter_balanco_financeiro()
                if balanco:
                    print(f"Faturamento Total (Vendas): R$ {balanco['faturamento']:.2f}")
                    print(f"Gastos (Custo de Mercadoria): R$ {balanco['gastos']:.2f}")
                    print(f"Lucro Líquido Real:          R$ {balanco['lucro']:.2f}")
                    if balanco['faturamento'] > 0:
                        margem = (balanco['lucro'] / balanco['faturamento']) * 100
                        print(f"Margem de Lucro:               {margem:.1f}%")
                else:
                    print(">> Sem dados financeiros cadastrados.")
                print("-"*40)

        elif opcao == "9":
            submenu_consultas()
            
        elif opcao == "10":
            # Protege a área de exclusões pedindo autenticação do gerente primeiro
            if verificar_autorizacao_gerente():
                submenu_exclusoes()
            
        elif opcao == "0":
            print("Saindo do painel administrativo...")
            break
        else:
            print(">> Opção inválida!")

if __name__ == "__main__":
    main()