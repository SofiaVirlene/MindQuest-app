from conexao import Conexao
from produto import Produto

class ProdutoDAO:
    @staticmethod
    def inserir(produto):
        conexao = Conexao.obter_conexao()
        if conexao is None: return False
        try:
            cursor = conexao.cursor()
            sql = "INSERT INTO TProduto (nome, preco, marca) VALUES (%s, %s, %s);"
            cursor.execute(sql, (produto.nome, produto.preco, produto.marca))
            conexao.commit()
            cursor.close()
            return True
        except Exception as e:
            print(f"Erro ao inserir produto: {e}")
            return False
        finally:
            conexao.close()

    @staticmethod
    def listar_todos():
        conexao = Conexao.obter_conexao()
        if conexao is None: return []
        try:
            cursor = conexao.cursor()
            sql = "SELECT id_produto, nome, preco, marca FROM TProduto;"
            cursor.execute(sql)
            linhas = cursor.fetchall()
            cursor.close()
            return [Produto(l[0], l[1], l[2], l[3]) for l in linhas]
        except Exception as e:
            print(f"Erro ao listar produtos: {e}")
            return []
        finally:
            conexao.close()