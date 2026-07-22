from conexao import Conexao
from cliente import Cliente

class ClienteDAO:
    @staticmethod
    def inserir(cliente):
        conexao = Conexao.obter_conexao()
        if conexao is None:
            return False
        try:
            cursor = conexao.cursor()
            # 1. Insere os dados principais e pega o ID gerado
            sql = """
                INSERT INTO TCliente (nome, cpf, email, endereco_rua, endereco_num, endereco_bairro, endereco_cep)
                VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id_cliente;
            """
            cursor.execute(sql, (cliente.nome, cliente.cpf, cliente.email, 
                                 cliente.endereco_rua, cliente.endereco_num, 
                                 cliente.endereco_bairro, cliente.endereco_cep))
            id_cliente_gerado = cursor.fetchone()[0]
            
            # 2. Salva cada telefone na tabela associativa
            sql_tel = "INSERT INTO TCliente_Telefone (id_cliente, telefone) VALUES (%s, %s);"
            for tel in cliente.telefones:
                cursor.execute(sql_tel, (id_cliente_gerado, tel))
                
            conexao.commit()
            cursor.close()
            return True
        except Exception as e:
            print(f"Erro ao inserir cliente e telefones: {e}")
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
            # Usa LEFT JOIN para buscar os telefones associados
            sql = """
                SELECT c.id_cliente, c.nome, c.cpf, c.email, c.endereco_rua, c.endereco_num, c.endereco_bairro, c.endereco_cep, t.telefone
                FROM TCliente c
                LEFT JOIN TCliente_Telefone t ON c.id_cliente = t.id_cliente;
            """
            cursor.execute(sql)
            linhas = cursor.fetchall()
            cursor.close()
            
            clientes_dict = {}
            for l in linhas:
                id_c, nome, cpf, email, rua, num, bairro, cep, tel = l
                if id_c not in clientes_dict:
                    clientes_dict[id_c] = Cliente(id_c, nome, cpf, email, rua, num, bairro, cep)
                if tel:
                    clientes_dict[id_c].telefones.append(tel)
                    
            return list(clientes_dict.values())
        except Exception as e:
            print(f"Erro ao listar clientes: {e}")
            return []
        finally:
            conexao.close()

    @staticmethod
    def buscar_por_cpf(conexao, cpf):
        cursor = conexao.cursor()
        query = """
            SELECT c.id_cliente, c.nome, c.email, 
                   COALESCE(string_agg(t.telefone, ', '), 'Sem telefone') as telefones
            FROM TCliente c
            LEFT JOIN TCliente_Telefone t ON c.id_cliente = t.id_cliente
            WHERE c.cpf = %s
            GROUP BY c.id_cliente, c.nome, c.email;
        """
        cursor.execute(query, (cpf,))
        return cursor.fetchone()
        
    @staticmethod
    def deletar(id_cliente):
        conexao = Conexao.obter_conexao()
        if conexao is None:
            return False
        try:
            cursor = conexao.cursor()
            
            # 1. Remove primeiro os telefones vinculados ao cliente
            sql_tel = "DELETE FROM TCliente_Telefone WHERE id_cliente = %s;"
            cursor.execute(sql_tel, (id_cliente,))
            
            # 2. Agora remove o cliente da tabela principal
            sql_cliente = "DELETE FROM TCliente WHERE id_cliente = %s;"
            cursor.execute(sql_cliente, (id_cliente,))
            
            conexao.commit()
            cursor.close()
            return True
        except Exception as e:
            print(f"Erro ao deletar cliente: {e}")
            return False
        finally:
            conexao.close()