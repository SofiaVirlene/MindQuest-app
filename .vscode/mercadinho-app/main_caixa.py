import datetime
import sys
from conexao import Conexao
from funcionario_dao import FuncionarioDAO
from compra_dao import CompraDAO
from cliente_dao import ClienteDAO  # Importado para permitir a busca por CPF

def realizar_login_caixa():
    print("\n" + "=" * 40)
    print("       SISTEMA MERCADINHO - TELA DE CAIXA       ")
    print("=" * 40)
    
    tentativas = 3
    while tentativas > 0:
        try:
            id_func = int(input("Digite seu ID de Funcionário: ").strip())
            num_caixa = int(input("Digite o Número do Terminal/Caixa: ").strip())
        except ValueError:
            print("\n[Erro] Por favor, insira apenas números válidos!")
            tentativas -= 1
            continue
        
        conexao = Conexao.obter_conexao()
        if conexao:
            nome_caixa = FuncionarioDAO.autenticar_caixa(conexao, id_func, num_caixa)
            conexao.close()
            
            if nome_caixa:
                print(f"\n[Caixa Liberado] Operador(a): {nome_caixa}")
                print("=" * 40 + "\n")
                return id_func  # Retorna o ID autenticado para usar nas vendas
            else:
                tentativas -= 1
                print(f"\n[Erro] Identificação incorreta ou funcionário não alocado neste caixa.")
                if tentativas > 0:
                    print(f"Você tem mais {tentativas} tentativa(s).\n")
        else:
            print("[Erro] Não foi possível conectar ao banco de dados.")
            return None
            
    print("\n[Acesso Bloqueado] Número de tentativas esgotadas.")
    print("=" * 40)
    return None

def exibir_menu_caixa():
    print("\n" + "="*40)
    print("      MERCADINHO - FRENTE DE CAIXA")
    print("="*40)
    print("1. Registrar Nova Venda (Cupom Fiscal)")
    print("0. Fechar Caixa")
    print("="*40)

def main(id_caixa_autenticado):
    while True:
        exibir_menu_caixa()
        opcao = input("Escolha uma opção: ").strip()
        hoje = datetime.date.today().strftime('%Y-%m-%d')

        if opcao == "1":
            print("\n--- Nova Venda (TCompra) ---")
            
            conexao = Conexao.obter_conexao()
            if not conexao:
                print(">> Erro ao conectar ao banco de dados para iniciar a venda.")
                continue

            try:
                id_cli = 1  # Padrão: Consumidor Geral
                cpf_input = input("CPF do Cliente (ou Enter para Consumidor Geral): ").strip()
                
                if cpf_input:
                    # Faz a busca utilizando o método que você já possui
                    dados_cliente = ClienteDAO.buscar_por_cpf(conexao, cpf_input)
                    if dados_cliente:
                        id_cli = dados_cliente[0]
                        nome_cli = dados_cliente[1]
                        print(f">> Cliente Identificado: {nome_cli}")
                    else:
                        print(">> [Aviso] CPF não cadastrado! A venda será registrada como Consumidor Geral.")
                else:
                    print(">> Identificado como: Consumidor Geral")

                # Utiliza automaticamente o ID capturado na tela de login
                id_caixa = id_caixa_autenticado
                print(f"Funcionário Operador do Caixa: {id_caixa}")
                
                itens = []
                while True:
                    id_p = input("ID do Produto (ou Enter para fechar carrinho): ").strip()
                    if not id_p: 
                        break
                    qtd = int(input("Quantidade: "))
                    prec = float(input("Preço Unitário: R$ "))
                    itens.append({'id_produto': int(id_p), 'quantidade': qtd, 'preco_unitario': prec})
                
                if itens:
                    CompraDAO.registrar_venda(id_cli, id_caixa, hoje, itens)
                else:
                    print(">> Carrinho vazio. Venda cancelada.")
                    
            except ValueError:
                print(">> Erro: Insira dados válidos.")
            finally:
                conexao.close()  # Garante o fechamento da conexão após finalizar ou cancelar a venda

        elif opcao == "0":
            print("Encerrando o terminal de vendas... Até logo!")
            break

if __name__ == "__main__":
    id_operador = realizar_login_caixa()
    
    if id_operador is not None:
        main(id_operador)
    else:
        print("Finalizando o terminal...")
        sys.exit()