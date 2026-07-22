from conexao import Conexao
from compra import Compra

class CompraDAO:
    @staticmethod
    def registrar_venda(id_cliente, id_caixa, data_venda, lista_itens):
        conexao = Conexao.obter_conexao()
        if conexao is None: return False
        try:
            cursor = conexao.cursor()
            valor_total = sum(item['quantidade'] * item['preco_unitario'] for item in lista_itens)
            
            sql_compra = """
                INSERT INTO TCompra (data, valor_total, id_cliente, id_funcionario_caixa)
                VALUES (%s, %s, %s, %s) RETURNING id_compra;
            """
            cursor.execute(sql_compra, (data_venda, valor_total, id_cliente, id_caixa))
            id_compra_gerado = cursor.fetchone()[0]
            
            sql_item = """
                INSERT INTO TCompra_produto (id_produto, id_compra, quantidade_vendida, preco_unitario)
                VALUES (%s, %s, %s, %s);
            """
            for item in lista_itens:
                cursor.execute(sql_item, (item['id_produto'], id_compra_gerado, item['quantidade'], item['preco_unitario']))
                
                # Baixa automática no estoque mantendo fidelidade ao diagrama original
                sql_baixa = """
                    INSERT INTO TEstoque (quantidade, data_entrada, data_atualizacao, id_produto, id_funcionario_gerente)
                    VALUES (%s, %s, %s, %s, NULL);
                """
                cursor.execute(sql_baixa, (-item['quantidade'], data_venda, data_venda, item['id_produto']))

            conexao.commit()
            cursor.close()
            print(f">> Venda finalizada com sucesso! Total: R$ {valor_total:.2f}")
            return True
        except Exception as e:
            print(f"Erro ao registrar a venda: {e}")
            return False
        finally:
            conexao.close()

    @staticmethod
    def obter_balanco_financeiro():
        conexao = Conexao.obter_conexao()
        if conexao is None: return None
        try:
            cursor = conexao.cursor()
            # Regra de negócio: Custo é estimado em 60% do valor de venda praticado
            sql = """
                SELECT 
                    COALESCE(SUM(quantidade_vendida * preco_unitario), 0) as faturamento_total,
                    COALESCE(SUM(quantidade_vendida * preco_unitario * 0.60), 0) as custo_total
                FROM TCompra_produto;
            """
            cursor.execute(sql)
            resultado = cursor.fetchone()
            cursor.close()
            
            faturamento = float(resultado[0])
            gastos = float(resultado[1])
            lucro = faturamento - gastos
            
            return {"faturamento": faturamento, "gastos": gastos, "lucro": lucro}
        except Exception as e:
            print(f"Erro ao gerar balanço financeiro: {e}")
            return None
        finally:
            conexao.close()