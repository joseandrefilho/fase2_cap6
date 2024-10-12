import re
from datetime import datetime
from categoria import obter_categorias, exibir_categorias
from unidade_medida import obter_unidades_medida, exibir_unidades_medida

def cadastrar_insumo(cursor):
    """
    Cadastra um novo insumo no banco de dados.
    """
    try:
        nome = obter_input("Nome do insumo: ")
        descricao = input("Descrição do insumo: ").strip()

        categorias = obter_categorias(cursor)
        exibir_categorias(categorias)
        id_categoria = obter_id_valido(categorias, "ID da categoria: ")

        unidades_medida = obter_unidades_medida(cursor)
        exibir_unidades_medida(unidades_medida)
        id_unidade_medida = obter_id_valido(unidades_medida, "ID da unidade de medida: ")

        fornecedor = input("Nome do fornecedor: ").strip()

        while True:
            data_validade = input("Data de validade (YYYY-MM-DD): ").strip()
            if validar_data(data_validade):
                break


        estoque_atual = obter_estoque("Estoque atual: ")
        estoque_minimo = obter_estoque("Estoque mínimo: ")

        cursor.execute(
            "INSERT INTO insumos (nome, descricao, id_categoria, id_unidade_medida, fornecedor, data_validade, estoque_atual, estoque_minimo) "
            "VALUES (:nome, :descricao, :id_categoria, :id_unidade_medida, :fornecedor, TO_DATE(:data_validade, 'YYYY-MM-DD'), :estoque_atual, :estoque_minimo)",
            {
                "nome": nome,
                "descricao": descricao,
                "id_categoria": id_categoria,
                "id_unidade_medida": id_unidade_medida,
                "fornecedor": fornecedor,
                "data_validade": data_validade,
                "estoque_atual": estoque_atual,
                "estoque_minimo": estoque_minimo
            }
        )
        print("Insumo cadastrado com sucesso!")
    except ValueError as ve:
        print(f"Erro de validação: {ve}")
    except Exception as error:
        print(f"Erro ao cadastrar insumo: {error}")


def consultar_estoque(cursor):
    """
    Consulta o estoque atual de um insumo e exibe o histórico de movimentações.
    """
    try:
        insumos = listar_insumos(cursor)
        id_insumo = obter_id_valido(insumos, "ID do insumo (ou 0 para sair): ", allow_zero=True)
        if id_insumo == 0:
            print("Operação cancelada.")
            return

        cursor.execute("SELECT estoque_atual FROM insumos WHERE id = :id", {"id": id_insumo})
        estoque_atual = cursor.fetchone()
        if estoque_atual:
            print(f"\nEstoque atual do insumo {id_insumo}: {estoque_atual[0]}")

            cursor.execute("""
                SELECT data, tipo, quantidade, observacao 
                FROM movimentacoes 
                WHERE id_insumo = :id_insumo 
                ORDER BY data DESC
            """, {"id_insumo": id_insumo})
            movimentacoes = cursor.fetchall()
            if movimentacoes:
                print("\nHistórico de movimentações:")
                for mov in movimentacoes:
                    print(f"  - Data: {mov[0].strftime('%Y-%m-%d')}, Tipo: {mov[1]}, Quantidade: {mov[2]}, Observação: {mov[3]}")
            else:
                print("\nNenhuma movimentação registrada para este insumo.")
        else:
            print("Insumo não encontrado.")
    except Exception as error:
        print(f"Erro ao consultar estoque: {error}")


def registrar_movimentacao(cursor, tipo, id_insumo, quantidade):
    """
    Registra uma movimentação de insumo, verificando se há estoque suficiente para saídas.

    Args:
    cursor: Conexão com o banco de dados.
    tipo: Tipo da movimentação ('entrada' ou 'saida').
    id_insumo: ID do insumo a ser movimentado.
    quantidade: Quantidade de insumo para a movimentação.
    """

    # Verifica o estoque atual do insumo antes de registrar a movimentação
    cursor.execute("SELECT estoque_atual FROM insumos WHERE id = :id_insumo", {"id_insumo": id_insumo})
    estoque_atual = cursor.fetchone()[0]

    if tipo == 'saida':
        # Verifica se há estoque suficiente para a movimentação
        if quantidade > estoque_atual:
            print(f"Erro: Quantidade insuficiente em estoque. Estoque atual: {estoque_atual}, quantidade solicitada: {quantidade}.")
            return  # Movimentação não permitida

    # Se for entrada ou saída com estoque suficiente, continua com a movimentação
    nova_quantidade = estoque_atual + quantidade if tipo == 'entrada' else estoque_atual - quantidade

    # Atualiza o estoque no banco de dados
    cursor.execute("""
        UPDATE insumos
        SET estoque_atual = :nova_quantidade
        WHERE id = :id_insumo
    """, {"nova_quantidade": nova_quantidade, "id_insumo": id_insumo})

    # Registrar a movimentação na tabela de movimentações
    cursor.execute("""
        INSERT INTO movimentacoes (id_insumo, tipo, quantidade, data)
        VALUES (:id_insumo, :tipo, :quantidade, :data)
    """, {
        "id_insumo": id_insumo,
        "tipo": tipo,
        "quantidade": quantidade,
        "data": datetime.now()
    })

    print(f"Movimentação de {tipo} de {quantidade} unidades registrada com sucesso!")


def obter_input(mensagem):
    """
    Obtém entrada do usuário com validação.
    """
    valor = input(mensagem).strip()
    if not valor:
        raise ValueError(f"{mensagem} não pode ser vazio.")
    return valor

def listar_insumos(cursor):
    """
    Lista todos os insumos disponíveis.
    """
    cursor.execute("SELECT id, nome FROM insumos")
    insumos = cursor.fetchall()
    print("Insumos disponíveis:")
    for insumo in insumos:
        print(f"   {insumo[0]} - {insumo[1]}")
    return insumos


def obter_id_valido(lista, mensagem, allow_zero=False):
    """
    Obtém e valida o ID de um item de uma lista.
    """
    while True:
        try:
            id_item = int(input(mensagem))
            if (allow_zero and id_item == 0) or id_item in [item[0] for item in lista]:
                return id_item
            else:
                print("ID inválido. Tente novamente.")
        except ValueError:
            print("Entrada inválida. Por favor, insira um número inteiro.")


def obter_data(mensagem):
    """
    Obtém e valida uma data no formato YYYY-MM-DD.
    """
    data = input(mensagem).strip()
    if not re.match(r"\d{4}-\d{2}-\d{2}", data):
        raise ValueError("Data deve estar no formato YYYY-MM-DD.")
    return data


def obter_quantidade(mensagem):
    """
    Obtém e valida uma quantidade.
    """
    while True:
        try:
            quantidade = int(input(mensagem))
            if quantidade < 0:
                print("O valor da Quantidade deve ser positivo. Tente novamente.")
            else:
                return quantidade
        except ValueError:
            print("Valor inválido. Por favor, insira um número.")


def obter_estoque(mensagem):
    """
    Obtém a quantidade de estoque e garante que seja um valor positivo.
    """
    while True:
        try:
            estoque = float(input(mensagem))
            if estoque < 0:
                print("O valor do estoque deve ser positivo. Tente novamente.")
            else:
                return estoque
        except ValueError:
            print("Valor inválido. Por favor, insira um número.")

def validar_data(data_input):
    """
    Valida a data no formato YYYY-MM-DD e verifica se não é uma data no passado.
    """
    try:
        data_valida = datetime.strptime(data_input, "%Y-%m-%d")
        if data_valida < datetime.now():
            print("A data de validade não pode ser no passado. Tente novamente.")
            return False
        return True
    except ValueError:
        print("Data inválida. Use o formato YYYY-MM-DD.")
        return False
