import logging
from database import conectar_banco, criar_cursor, fechar_conexao, criar_tabelas
from insumo import cadastrar_insumo, registrar_movimentacao, consultar_estoque
from categoria import gerenciar_categorias
from unidade_medida import gerenciar_unidades_medida
from relatorio import exibir_menu_relatorios

# Configuração do logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def exibir_menu_principal():
    print("\n--- Sistema de Gestão de Estoque de Insumos ---")
    print("1. Cadastrar insumo")
    print("2. Registrar movimentação")
    print("3. Consultar estoque")
    print("4. Relatórios")  # Nova opção para relatórios
    print("5. Gerenciar categorias")
    print("6. Gerenciar unidades de medida")
    print("0. Sair")

def main():
    """
    Função principal do sistema.
    """
    connection = conectar_banco()
    if not connection:
        logging.error("Falha ao conectar ao banco de dados.")
        return

    cursor = criar_cursor(connection)
    if not cursor:
        logging.error("Falha ao criar cursor.")
        fechar_conexao(connection, None)
        return

    try:
        criar_tabelas(cursor)  # Chama a função para criar as tabelas
        connection.commit()  # Confirma as alterações no banco de dados

        while True:
            exibir_menu_principal()
            opcao = input("Escolha uma opção: ")

            if opcao == '1':
                cadastrar_insumo(cursor)
                connection.commit()
            elif opcao == '2':
                registrar_movimentacao(cursor)
                connection.commit()
            elif opcao == '3':
                consultar_estoque(cursor)
            elif opcao == '4':
                exibir_menu_relatorios(cursor)
            elif opcao == '5':
                gerenciar_categorias(cursor)
                connection.commit()
            elif opcao == '6':
                gerenciar_unidades_medida(cursor)
                connection.commit()
            elif opcao == '0':
                break
            else:
                print("Opção inválida!")
                logging.warning("Opção inválida selecionada.")

    except Exception as e:
        logging.error(f"Erro durante a execução do sistema: {e}")
    finally:
        fechar_conexao(connection, cursor)

if __name__ == "__main__":
    main()