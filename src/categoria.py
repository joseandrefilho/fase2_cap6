def gerenciar_categorias(cursor):
    """
    Gerencia as operações de CRUD de categorias.
    """
    while True:
        print("\n--- Gerenciar Categorias ---")
        print("1. Cadastrar categoria")
        print("2. Listar categorias")
        print("3. Atualizar categoria")
        print("4. Excluir categoria")
        print("0. Voltar")

        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            cadastrar_categoria(cursor)
        elif opcao == '2':
            listar_categorias(cursor)
        elif opcao == '3':
            atualizar_categoria(cursor)
        elif opcao == '4':
            excluir_categoria(cursor)
        elif opcao == '0':
            break
        else:
            print("Opção inválida!")


def cadastrar_categoria(cursor):
    """
    Cadastra uma nova categoria no banco de dados.
    """
    try:
        nome = obter_input("Nome da categoria: ")

        cursor.execute("INSERT INTO categorias (nome) VALUES (:nome)", {"nome": nome})
        print("Categoria cadastrada com sucesso!")
    except ValueError as ve:
        print(f"Erro de validação: {ve}")
    except Exception as error:
        print(f"Erro ao cadastrar categoria: {error}")


def listar_categorias(cursor):
    """
    Lista todas as categorias cadastradas.
    """
    try:
        categorias = obter_categorias(cursor)
        exibir_categorias(categorias)

    except Exception as error:
        print(f"Erro ao listar categorias: {error}")




def atualizar_categoria(cursor):
    """
    Atualiza os dados de uma categoria existente.
    """
    try:
        categorias = obter_categorias(cursor)
        if not categorias:
            print("Nenhuma categoria disponível para atualização.")
            return

        exibir_categorias(categorias)
        id_categoria = obter_id_categoria(categorias, "ID da categoria a ser atualizada (ou 0 para sair): ")
        if id_categoria == 0:
            print("Operação cancelada.")
            return

        nome = obter_input("Novo nome da categoria: ")

        cursor.execute("UPDATE categorias SET nome = :nome WHERE id = :id", {"nome": nome, "id": id_categoria})
        print("Categoria atualizada com sucesso!")
    except ValueError as ve:
        print(f"Erro de validação: {ve}")
    except Exception as error:
        print(f"Erro ao atualizar categoria: {error}")


def excluir_categoria(cursor):
    """
    Exclui uma categoria do banco de dados.
    """
    try:
        categorias = obter_categorias(cursor)
        if not categorias:
            print("Nenhuma categoria disponível para exclusão.")
            return

        exibir_categorias(categorias)
        id_categoria = obter_id_categoria(categorias, "ID da categoria a ser excluída (ou 0 para sair): ")
        if id_categoria == 0:
            print("Operação cancelada.")
            return

        cursor.execute("DELETE FROM categorias WHERE id = :id", {"id": id_categoria})
        print("Categoria excluída com sucesso!")
    except Exception as error:
        print(f"Erro ao excluir categoria: {error}")


def obter_input(mensagem):
    """
    Obtém entrada do usuário com validação.
    """
    valor = input(mensagem).strip()
    if not valor:
        raise ValueError(f"{mensagem} não pode ser vazio.")
    return valor


def obter_categorias(cursor):
    """
    Obtém todas as categorias do banco de dados.
    """
    cursor.execute("SELECT id, nome FROM categorias")
    return cursor.fetchall()


def exibir_categorias(categorias):
    """
    Exibe as categorias.
    """
    print("Categorias disponíveis:")
    for categoria in categorias:
        print(f"   {categoria[0]} - {categoria[1]}")


def obter_id_categoria(categorias, mensagem):
    """
    Obtém e valida o ID da categoria.
    """
    while True:
        try:
            id_categoria = int(input(mensagem))
            if id_categoria == 0 or id_categoria in [categoria[0] for categoria in categorias]:
                return id_categoria
            else:
                print("ID da categoria inválido. Tente novamente.")
        except ValueError:
            print("Entrada inválida. Por favor, insira um número inteiro.")