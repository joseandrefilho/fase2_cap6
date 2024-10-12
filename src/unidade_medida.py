def gerenciar_unidades_medida(cursor):
    """
    Gerencia as operações de CRUD de unidades de medida.
    """
    while True:
        print("\n--- Gerenciar Unidades de Medida ---")
        print("1. Cadastrar unidade de medida")
        print("2. Listar unidades de medida")
        print("3. Atualizar unidade de medida")
        print("4. Excluir unidade de medida")
        print("0. Voltar")

        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            cadastrar_unidade_medida(cursor)
        elif opcao == '2':
            listar_unidades_medida(cursor)
        elif opcao == '3':
            atualizar_unidade_medida(cursor)
        elif opcao == '4':
            excluir_unidade_medida(cursor)
        elif opcao == '0':
            break
        else:
            print("Opção inválida!")


def cadastrar_unidade_medida(cursor):
    """
    Cadastra uma nova unidade de medida no banco de dados.
    """
    try:
        nome = obter_input("Nome da unidade de medida: ")
        sigla = obter_input("Sigla da unidade de medida: ")

        cursor.execute("INSERT INTO unidades_medida (nome, sigla) VALUES (:nome, :sigla)",
                       {"nome": nome, "sigla": sigla})
        print("Unidade de medida cadastrada com sucesso!")
    except ValueError as ve:
        print(f"Erro de validação: {ve}")
    except Exception as error:
        print(f"Erro ao cadastrar unidade de medida: {error}")


def listar_unidades_medida(cursor):
    """
    Lista todas as unidades de medida cadastradas.
    """
    try:
        unidades_medida = obter_unidades_medida(cursor)
        exibir_unidades_medida(unidades_medida)

    except Exception as error:
        print(f"Erro ao listar unidades de medida: {error}")



def atualizar_unidade_medida(cursor):
    """
    Atualiza os dados de uma unidade de medida existente.
    """
    try:
        unidades_medida = obter_unidades_medida(cursor)
        if not unidades_medida:
            print("Nenhuma unidade de medida disponível para atualização.")
            return

        exibir_unidades_medida(unidades_medida)
        id_unidade_medida = obter_id_unidade_medida(unidades_medida, "ID da unidade de medida a ser atualizada (ou 0 para sair): ")
        if id_unidade_medida == 0:
            print("Operação cancelada.")
            return

        nome = obter_input("Novo nome da unidade de medida: ")
        sigla = obter_input("Nova sigla da unidade de medida: ")

        cursor.execute("UPDATE unidades_medida SET nome = :nome, sigla = :sigla WHERE id = :id",
                       {"nome": nome, "sigla": sigla, "id": id_unidade_medida})
        print("Unidade de medida atualizada com sucesso!")
    except ValueError as ve:
        print(f"Erro de validação: {ve}")
    except Exception as error:
        print(f"Erro ao atualizar unidade de medida: {error}")


def excluir_unidade_medida(cursor):
    """
    Exclui uma unidade de medida do banco de dados.
    """
    try:
        unidades_medida = obter_unidades_medida(cursor)
        if not unidades_medida:
            print("Nenhuma unidade de medida disponível para exclusão.")
            return

        exibir_unidades_medida(unidades_medida)
        id_unidade_medida = obter_id_unidade_medida(unidades_medida, "ID da unidade de medida a ser excluída (ou 0 para sair): ")
        if id_unidade_medida == 0:
            print("Operação cancelada.")
            return

        cursor.execute("DELETE FROM unidades_medida WHERE id = :id", {"id": id_unidade_medida})
        print("Unidade de medida excluída com sucesso!")
    except ValueError as ve:
        print(f"Erro de validação: {ve}")
    except Exception as error:
        print(f"Erro ao excluir unidade de medida: {error}")


def obter_input(mensagem):
    """
    Obtém entrada do usuário com validação.
    """
    valor = input(mensagem)
    if not valor:
        raise ValueError(f"{mensagem} não pode ser vazio.")
    return valor


def obter_unidades_medida(cursor):
    """
    Obtém todas as unidades de medida do banco de dados.
    """
    cursor.execute("SELECT id, nome, sigla FROM unidades_medida")
    return cursor.fetchall()


def exibir_unidades_medida(unidades_medida):
    """
    Exibe as unidades de medida.
    """
    print("Unidades de medida disponíveis:")
    for unidade_medida in unidades_medida:
        print(f"   {unidade_medida[0]} - {unidade_medida[1]} - {unidade_medida[2]}")


def obter_id_unidade_medida(unidades_medida, mensagem):
    """
    Obtém e valida o ID da unidade de medida.
    """
    while True:
        try:
            id_unidade_medida = int(input(mensagem))
            if id_unidade_medida == 0 or id_unidade_medida in [unidade_medida[0] for unidade_medida in unidades_medida]:
                return id_unidade_medida
            else:
                print("ID da unidade de medida inválido. Tente novamente.")
        except ValueError:
            print("Entrada inválida. Por favor, insira um número inteiro.")