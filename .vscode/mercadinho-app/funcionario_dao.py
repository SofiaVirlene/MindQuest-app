from conexao import Conexao
from funcionario import Funcionario

class FuncionarioDAO:
    @staticmethod
    def inserir(func):
        conexao = Conexao.obter_conexao()
        if conexao is None: 
            return False
        try:
            cursor = conexao.cursor()
            
            # 1. Insere na tabela mãe (TFuncionario) e recupera o ID
            sql_mae = """
                INSERT INTO TFuncionario (nome, cpf, salario, data_admissao, login, senha, cargo)
                VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id_funcionario;
            """
            cursor.execute(sql_mae, (func.nome, func.cpf, func.salario, func.data_admissao, func.login, func.senha, func.cargo))
            id_func_gerado = cursor.fetchone()[0]
            
            # 2. Insere os telefones na tabela associativa
            sql_tel = "INSERT INTO TFuncionario_Telefone (id_funcionario, telefone) VALUES (%s, %s);"
            for tel in func.telefones:
                cursor.execute(sql_tel, (id_func_gerado, tel))

            # 3. Insere na tabela filha específica dependendo da especialização (cargo)
            if func.cargo.lower() == "caixa":
                sql_filha = "INSERT INTO TCaixa (id_funcionario, num_caixa) VALUES (%s, %s);"
                cursor.execute(sql_filha, (id_func_gerado, func.num_caixa))
                
            elif func.cargo.lower() == "gerente":
                sql_filha = "INSERT INTO TGerente (id_funcionario, senha_usuario) VALUES (%s, %s);"
                cursor.execute(sql_filha, (id_func_gerado, func.senha_usuario))
                
            conexao.commit()
            cursor.close()
            return True
        except Exception as e:
            print(f"Erro ao inserir funcionário especializado: {e}")
            return False
        finally:
            conexao.close()

    @staticmethod
    def listar_todos():
        conexao = Conexao.obter_conexao()
        if conexao is None: return []
        try:
            cursor = conexao.cursor()
            sql = """
                SELECT f.id_funcionario, f.nome, f.cpf, f.salario, f.data_admissao, t.telefone
                FROM TFuncionario f
                LEFT JOIN TFuncionario_Telefone t ON f.id_funcionario = t.id_funcionario;
            """
            cursor.execute(sql)
            linhas = cursor.fetchall()
            cursor.close()
            
            funcionarios_dict = {}
            for l in linhas:
                id_f, nome, cpf, salario, data, tel = l
                if id_f not in funcionarios_dict:
                    funcionarios_dict[id_f] = Funcionario(id_f, nome, cpf, "Funcionário", salario, str(data))
                if tel:
                    funcionarios_dict[id_f].telefones.append(tel)
                    
            return list(funcionarios_dict.values())
        except Exception as e:
            print(f"Erro ao listar funcionários: {e}")
            return []
        finally:
            conexao.close()

    @staticmethod
    def autenticar_gerente(conexao, login, senha):
        """
        Busca no banco se existe um funcionário com o login, senha e cargo de Gerente.
        Retorna o nome do gerente se encontrar, ou None se os dados estiverem errados.
        """
        cursor = conexao.cursor()
        sql = """
            SELECT nome FROM TFuncionario 
            WHERE login = %s AND senha = %s AND cargo = 'Gerente';
        """
        try:
            cursor.execute(sql, (login, senha))
            resultado = cursor.fetchone()
            if resultado:
                return resultado[0]  # Retorna o nome do gerente encontrado
            return None
        except Exception as e:
            print(f"Erro ao consultar autenticação: {e}")
            return None
        finally:
            cursor.close()
            
    @staticmethod
    def buscar_por_cpf(conexao, cpf):
        cursor = conexao.cursor()
        query = """
            SELECT f.id_funcionario, f.nome, f.cargo, 
                   COALESCE(string_agg(t.telefone, ', '), 'Sem telefone') as telefones
            FROM TFuncionario f
            LEFT JOIN TFuncionario_Telefone t ON f.id_funcionario = t.id_funcionario
            WHERE f.cpf = %s
            GROUP BY f.id_funcionario, f.nome, f.cargo;
        """
        cursor.execute(query, (cpf,))
        return cursor.fetchone()
    
    @staticmethod
    def deletar(id_funcionario, cargo):
        conexao = Conexao.obter_conexao()
        if conexao is None:
            return False
        try:
            cursor = conexao.cursor()
            
            # 1. Remove os telefones vinculados
            sql_tel = "DELETE FROM TFuncionario_Telefone WHERE id_funcionario = %s;"
            cursor.execute(sql_tel, (id_funcionario,))
            
            # 2. Remove da tabela filha específica baseada no cargo
            if cargo.lower() == "caixa":
                sql_filha = "DELETE FROM TCaixa WHERE id_funcionario = %s;"
                cursor.execute(sql_filha, (id_funcionario,))
            elif cargo.lower() == "gerente":
                sql_filha = "DELETE FROM TGerente WHERE id_funcionario = %s;"
                cursor.execute(sql_filha, (id_funcionario,))
            
            # 3. Agora sim, remove da tabela mãe
            sql_func = "DELETE FROM TFuncionario WHERE id_funcionario = %s;"
            cursor.execute(sql_func, (id_funcionario,))
            
            conexao.commit()
            cursor.close()
            return True
        except Exception as e:
            print(f"Erro ao deletar funcionário: {e}")
            return False
        finally:
            conexao.close()
    
    @staticmethod
    def autenticar_caixa(conexao, id_funcionario, num_caixa):
        """
        Verifica se o funcionário existe, se ele é um Caixa e se está alocado
        no número de terminal correto. Retorna o nome do operador.
        """
        cursor = conexao.cursor()
        sql = """
            SELECT f.nome 
            FROM TFuncionario f
            JOIN TCaixa c ON f.id_funcionario = c.id_funcionario
            WHERE f.id_funcionario = %s AND c.num_caixa = %s AND f.cargo = 'Caixa';
        """
        try:
            cursor.execute(sql, (id_funcionario, num_caixa))
            resultado = cursor.fetchone()
            if resultado:
                return resultado[0]  # Retorna o nome do(a) operador(a)
            return None
        except Exception as e:
            print(f"Erro ao autenticar operador de caixa: {e}")
            return None
        finally:
            cursor.close()