import json
import csv
import numpy as np
from sklearn.linear_model import LinearRegression
from datetime import datetime
from insumo import listar_insumos

def exibir_menu_relatorios(cursor):
    """
    Exibe o sub-menu para gerar relatórios.
    """
    while True:
        print("\n--- Relatórios ---")
        print("1. Gerar relatório de consumo")
        print("2. Gerar relatório de validade")
        print("3. Gerar relatório de movimentação por período")
        print("4. Prever estoque de insumo")
        print("0. Voltar ao menu principal")

        opcao = input("Escolha uma opção de relatório: ")

        if opcao == "1":
            gerar_relatorio_consumo_filtrado(cursor)  # Gera o relatório de consumo com filtros e CSV
        elif opcao == "2":
            gerar_relatorio_validade(cursor)  # Gera o relatório de validade
        elif opcao == "3":
            gerar_relatorio_movimentacao_periodo(cursor)  # Gera o relatório de movimentação por período
        elif opcao == "4":
            prever_estoque(cursor)  # Chama a previsão de estoque
        elif opcao == "0":
            break  # Volta ao menu principal
        else:
            print("Opção inválida! Tente novamente.")


def gerar_relatorio_consumo_filtrado(cursor):
    """
    Gera um relatório de consumo de insumos (somente saídas) com filtros opcionais de categoria e fornecedor.
    Exporta o resultado em formato JSON ou CSV, conforme escolha do usuário.
    """
    # Montar a query com base nos filtros fornecidos
    query = """
        SELECT i.nome, m.data, m.quantidade
        FROM insumos i
        JOIN movimentacoes m ON i.id = m.id_insumo
        WHERE m.tipo = 'saida'
    """

    # Executar a query final com os filtros aplicados (se houverem)
    cursor.execute(query)
    consumo = cursor.fetchall()

    # Solicitar ao usuário o formato de exportação desejado
    formato = input("Escolha o formato de saída (json/csv): ").strip().lower()

    # Gerar o relatório no formato JSON
    if formato == "json":
        if consumo:
            with open("relatorio_consumo.json", "w") as f:
                json.dump(
                    [{"insumo": row[0], "data": row[1].strftime("%Y-%m-%d"), "quantidade": row[2]} for row in consumo],
                    f, indent=4)
            print(f"Relatório de consumo gerado com sucesso no formato JSON! {len(consumo)} registros incluídos.")
        else:
            print("Nenhum dado encontrado com os filtros aplicados.")

    # Gerar o relatório no formato CSV
    elif formato == "csv":
        if consumo:
            with open("relatorio_consumo.csv", "w", newline='') as csvfile:
                fieldnames = ['Insumo', 'Data', 'Quantidade']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                writer.writeheader()
                for row in consumo:
                    writer.writerow({'Insumo': row[0], 'Data': row[1].strftime("%Y-%m-%d"), 'Quantidade': row[2]})

            print(f"Relatório de consumo gerado com sucesso no formato CSV! {len(consumo)} registros incluídos.")
        else:
            print("Nenhum dado encontrado com os filtros aplicados.")

    else:
        print("Formato inválido. Escolha 'json' ou 'csv'.")


def gerar_relatorio_validade(cursor):
    """
    Gera um relatório de insumos próximos à data de validade, exportado em formato JSON ou CSV.
    """
    cursor.execute("""
        SELECT nome, data_validade, estoque_atual
        FROM insumos
        WHERE data_validade IS NOT NULL AND data_validade <= SYSDATE + INTERVAL '30' DAY
        ORDER BY data_validade
    """)

    insumos = []
    for row in cursor:
        insumos.append({
            "Nome": row[0],
            "Validade": row[1].strftime("%Y-%m-%d"),
            "Estoque Atual": row[2]
        })

    while True:
        formato = input("Escolha o formato de saída (json/csv): ").strip().lower()
        if formato in ["json", "csv"]:
            break
        else:
            print("Formato inválido. Escolha 'json' ou 'csv'.")

    if formato == "json":
        with open("relatorio_validade.json", "w") as f:
            json.dump(insumos, f, indent=4)
        print(f"Relatório de validade gerado com sucesso no formato JSON! {len(insumos)} insumos incluídos.")
    elif formato == "csv":
        with open("relatorio_validade.csv", "w", newline='') as csvfile:
            fieldnames = ['Nome', 'Validade', 'Estoque Atual']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for insumo in insumos:
                writer.writerow(insumo)
        print(f"Relatório de validade gerado com sucesso no formato CSV! {len(insumos)} insumos incluídos.")

def gerar_relatorio_movimentacao_periodo(cursor):
    """
    Gera um relatório de movimentações de insumos (entrada e saída) dentro de um período específico de tempo.
    Exportado em formato JSON ou CSV.
    """
    data_inicio = input("Informe a data de início (YYYY-MM-DD): ").strip()
    data_fim = input("Informe a data de fim (YYYY-MM-DD): ").strip()

    # Validação de datas
    try:
        datetime.strptime(data_inicio, "%Y-%m-%d")
        datetime.strptime(data_fim, "%Y-%m-%d")
        if data_inicio > data_fim:
            print("Erro: A data de início não pode ser posterior à data de fim.")
            return
    except ValueError:
        print("Erro: Formato de data inválido. Use o formato YYYY-MM-DD.")
        return

    # Executar a query para buscar movimentações no período informado
    cursor.execute("""
        SELECT i.nome, m.data, m.tipo, m.quantidade
        FROM movimentacoes m
        JOIN insumos i ON m.id_insumo = i.id
        WHERE m.data BETWEEN TO_DATE(:data_inicio, 'YYYY-MM-DD') AND TO_DATE(:data_fim, 'YYYY-MM-DD')
        ORDER BY m.data
    """, {"data_inicio": data_inicio, "data_fim": data_fim})

    movimentacoes = []
    for row in cursor:
        movimentacoes.append({
            "Insumo": row[0],
            "Data": row[1].strftime("%Y-%m-%d"),
            "Tipo": row[2],
            "Quantidade": row[3]
        })

    # Solicitar ao usuário o formato de exportação desejado
    while True:
        formato = input("Escolha o formato de saída (json/csv): ").strip().lower()
        if formato in ["json", "csv"]:
            break
        else:
            print("Formato inválido. Escolha 'json' ou 'csv'.")

    # Gerar o relatório no formato JSON
    if formato == "json":
        with open("relatorio_movimentacao_periodo.json", "w") as f:
            json.dump(movimentacoes, f, indent=4)
        print(f"Relatório de movimentação gerado com sucesso no formato JSON! {len(movimentacoes)} registros incluídos.")

    # Gerar o relatório no formato CSV
    elif formato == "csv":
        with open("relatorio_movimentacao_periodo.csv", "w", newline='') as csvfile:
            fieldnames = ['Insumo', 'Data', 'Tipo', 'Quantidade']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for movimentacao in movimentacoes:
                writer.writerow(movimentacao)
        print(f"Relatório de movimentação gerado com sucesso no formato CSV! {len(movimentacoes)} registros incluídos.")


def prever_estoque(cursor):
    """
    Prevê quando o estoque de um insumo irá acabar, com base no histórico de movimentação (saída) e
    no consumo médio previsto usando regressão linear.
    """
    # Listar todos os insumos disponíveis para o usuário selecionar
    insumos = listar_insumos(cursor)
    if not insumos:
        print("Nenhum insumo cadastrado.")  # Se não houver insumos cadastrados, a função encerra aqui
        return

    # Solicitar ao usuário para escolher o ID do insumo para previsão
    while True:
        try:
            id_insumo = int(input("Escolha o ID do insumo (ou 0 para sair): "))
            if id_insumo == 0:
                print("Operação cancelada.")
                return

            # Verifica se o ID do insumo é válido e obtém o nome correspondente
            insumo_selecionado = next((insumo for insumo in insumos if insumo[0] == id_insumo), None)
            if insumo_selecionado:
                nome_insumo = insumo_selecionado[1]  # Obtém o nome do insumo
                break
            else:
                print("ID inválido. Tente novamente.")
        except ValueError:
            print("ID inválido. Tente novamente.")

    # Buscar movimentações de saída do insumo para previsão de consumo
    cursor.execute("""
        SELECT m.data, m.quantidade
        FROM movimentacoes m
        WHERE m.id_insumo = :id_insumo AND m.tipo = 'saida'
        ORDER BY m.data
    """, {"id_insumo": id_insumo})

    movimentacoes = cursor.fetchall()  # Lista de movimentações encontradas

    # Verifica se há movimentações suficientes para gerar a previsão
    if len(movimentacoes) < 2:
        print(f"Poucos dados para prever consumo do insumo '{nome_insumo}'.")  # Alerta de dados insuficientes
        return

    # Converter as datas para números inteiros (dias desde 01/01/1970) para serem usadas na regressão linear
    datas = np.array([(row[0] - datetime(1970, 1, 1)).days for row in movimentacoes]).reshape(-1, 1)
    quantidades = np.array([row[1] for row in movimentacoes])  # Quantidades retiradas nas movimentações

    # Criar o modelo de regressão linear e ajustar aos dados de consumo
    modelo = LinearRegression()
    modelo.fit(datas, quantidades)

    # Prever o consumo para a data atual
    data_atual = datetime.now()
    dias_atuais = (data_atual - datetime(1970, 1, 1)).days
    previsao_consumo = modelo.predict([[dias_atuais]])[0]  # Previsão de consumo futuro

    # Buscar o estoque atual do insumo para calcular em quantos dias ele vai acabar
    cursor.execute("SELECT estoque_atual FROM insumos WHERE id = :id_insumo", {"id_insumo": id_insumo})
    estoque_atual = cursor.fetchone()[0]  # Obter o estoque atual do insumo

    # Se a previsão de consumo for positiva, calcular os dias restantes para o fim do estoque
    if previsao_consumo > 0:
        dias_para_acabar = estoque_atual / previsao_consumo  # Calcula quantos dias faltam para acabar o estoque
        print(f"O insumo '{nome_insumo}' deve acabar em aproximadamente {int(dias_para_acabar)} dias.")
    else:
        print(f"O insumo '{nome_insumo}' está com previsão de consumo zero ou negativo.")  # Previsão inválida
