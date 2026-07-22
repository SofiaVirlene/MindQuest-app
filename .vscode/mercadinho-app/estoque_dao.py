from conexao import Conexao
from estoque import Estoque

class EstoqueDAO:
    @staticmethod
    def dar_entrada(id_produto, id_gerente, quantidade, data_entrada):
        conexao = Conexao.obter_conexao()
        if conexao is None: return False
        try:
            cursor = conexao.cursor()
            sql = """
                INSERT INTO TEstoque (quantidade, data_entrada, data_atualizacao, id_produto, id_funcionario_gerente)
                VALUES (%s, %s, %s, %s, %s);
            """
            cursor.execute(sql, (quantidade, data_entrada, data_entrada, id_produto, id_gerente))
            conexao.commit()
            cursor.close()
            return True
        except Exception as e:
            print(f"Erro ao dar entrada no estoque: {e}")
            return False
        finally:
            conexao.close()

    @staticmethod
    def obter_relatorio_estoque():
        conexao = Conexao.obter_conexao()
        if conexao is None: return []
        try:
            cursor = conexao.cursor()
            sql = """
                SELECT p.id_produto, p.nome, p.marca, p.preco, COALESCE(SUM(e.quantidade), 0)
                FROM TProduto p
                LEFT JOIN TEstoque e ON p.id_produto = e.id_produto
                GROUP BY p.id_produto, p.nome, p.marca, p.preco;
            """
            cursor.execute(sql)
            linhas = cursor.fetchall()
            cursor.close()
            return linhas
        except Exception as e:
            print(f"Erro ao gerar relatório de estoque: {e}")
            return []
        finally:
            conexao.close()