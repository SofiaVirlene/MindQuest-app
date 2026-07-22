from conexao import Conexao
from fornecedor import Fornecedor

class FornecedorDAO:
    @staticmethod
    def inserir(fornecedor):
        conexao = Conexao.obter_conexao()
        if conexao is None:
            return False
        try:
            cursor = conexao.cursor()
            
            # 1. Inserir o Fornecedor com o campo 'nome' exato do diagrama
            sql_fornecedor = """
                INSERT INTO TFornecedor (nome, cnpj)
                VALUES (%s, %s) RETURNING id_fornecedor;
            """
            cursor.execute(sql_fornecedor, (fornecedor.nome, fornecedor.cnpj))
            id_fornecedor_gerado = cursor.fetchone()[0]
            
            # 2. Inserir todos os telefones em TFornecedor_telefone
            sql_telefone = """
                INSERT INTO TFornecedor_telefone (id_fornecedor, telefone)
                VALUES (%s, %s);
            """
            for tel in fornecedor.telefones:
                cursor.execute(sql_telefone, (id_fornecedor_gerado, tel))
                
            conexao.commit()
            cursor.close()
            return True
        except Exception as e:
            print(f"Erro ao inserir fornecedor e telefones: {e}")
            return False
        finally:
            conexao.close()

    @staticmethod
    def vincular_produto(id_fornecedor, id_produto):
        """Preenche a tabela associativa TFornecedor_produto do diagrama"""
        conexao = Conexao.obter_conexao()
        if conexao is None:
            return False
        try:
            cursor = conexao.cursor()
            sql = """
                INSERT INTO TFornecedor_produto (id_fornecedor, id_produto)
                VALUES (%s, %s);
            """
            cursor.execute(sql, (id_fornecedor, id_produto))
            conexao.commit()
            cursor.close()
            return True
        except Exception as e:
            print(f"Erro ao vincular produto ao fornecedor: {e}")
            return False
        finally:
            conexao.close()

    @staticmethod
    def listar_todos():
        conexao = Conexao.obter_conexao()
        if conexao is None:
            return []
        try:
            cursor = conexao.cursor()
            
            sql = """
                SELECT f.id_fornecedor, f.nome, f.cnpj, t.telefone
                FROM TFornecedor f
                LEFT JOIN TFornecedor_telefone t ON f.id_fornecedor = t.id_fornecedor;
            """
            cursor.execute(sql)
            linhas = cursor.fetchall()
            cursor.close()
            
            fornecedores_dict = {}
            for l in linhas:
                id_f, nome, cnpj, tel = l
                if id_f not in fornecedores_dict:
                    fornecedores_dict[id_f] = Fornecedor(id_f, nome, cnpj)
                if tel:
                    fornecedores_dict[id_f].telefones.append(tel)
                    
            return list(fornecedores_dict.values())
        except Exception as e:
            print(f"Erro ao listar fornecedores: {e}")
            return []
        finally:
            conexao.close()
        
    @staticmethod
    def buscar_por_cnpj(conexao, cnpj):
        cursor = conexao.cursor()
        query = """
            SELECT f.id_fornecedor, f.nome, f.cnpj, 
                   COALESCE(string_agg(t.telefone, ', '), 'Sem telefone') as telefones
            FROM TFornecedor f
            LEFT JOIN TFornecedor_telefone t ON f.id_fornecedor = t.id_fornecedor
            WHERE f.cnpj = %s
            GROUP BY f.id_fornecedor, f.nome, f.cnpj;
        """
        cursor.execute(query, (cnpj,))
        return cursor.fetchone()

    @staticmethod
    def deletar(id_fornecedor):
        conexao = Conexao.obter_conexao()
        if conexao is None:
            return False
        try:
            cursor = conexao.cursor()
            
            # 1. Remove os telefones vinculados
            sql_tel = "DELETE FROM TFornecedor_telefone WHERE id_fornecedor = %s;"
            cursor.execute(sql_tel, (id_fornecedor,))
            
            # 2. Se houver produtos vinculados na tabela associativa, remove também
            sql_prod = "DELETE FROM TFornecedor_produto WHERE id_fornecedor = %s;"
            cursor.execute(sql_prod, (id_fornecedor,))
            
            # 3. Por fim, remove o fornecedor
            sql_forn = "DELETE FROM TFornecedor WHERE id_fornecedor = %s;"
            cursor.execute(sql_forn, (id_fornecedor,))
            
            conexao.commit()
            cursor.close()
            return True
        except Exception as e:
            print(f"Erro ao deletar fornecedor: {e}")
            return False
        finally:
            conexao.close()