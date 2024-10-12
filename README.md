
# FIAP - Faculdade de Informática e Administração Paulista

<p align="center">
<a href= "https://www.fiap.com.br/"><img src="assets/logo-fiap.png" alt="FIAP - Faculdade de Informática e Administração Paulista" border="0" width=40% height=40%></a>
</p>

<br>

# Gestão de Estoque de Insumos

## Grupo 73

## 👨‍🎓 Integrantes: 
- <a href="https://www.linkedin.com/in/joseandrefilho">Jose Andre Filho</a>

## 👩‍🏫 Professores:
### Tutor(a) 
- <a href="https://www.linkedin.com/in/lucas-gomes-moreira-15a8452a/">Lucas Gomes Moreira</a>
### Coordenador(a)
- <a href="https://www.linkedin.com/in/profandregodoi/">André Godoi Chiovato</a>

## 📜 Descrição

O projeto de Gestão de Estoque de Insumos foi desenvolvido para solucionar um problema comum no agronegócio: o controle eficiente de insumos essenciais, como fertilizantes, sementes e defensivos agrícolas. A proposta do sistema é garantir que as necessidades de reposição de insumos sejam previstas com precisão, evitando desperdícios e a falta de produtos críticos para o funcionamento da operação agrícola.

Desenvolvido com base nos conteúdos abordados nos capítulos 3 a 6 do curso, o projeto utiliza **Python** para implementar as funcionalidades e está integrado a um banco de dados **Oracle** para gerenciar os insumos e movimentações. O sistema também oferece flexibilidade na geração de relatórios, permitindo exportação em formatos **JSON** e **CSV**, o que facilita o uso dos dados em outras ferramentas ou análises.

O sistema oferece as seguintes funcionalidades principais:
- **Cadastro de insumos**: Os usuários podem cadastrar insumos com informações completas, como categoria, unidade de medida, fornecedor, data de validade, estoque mínimo e estoque atual. Isso assegura que todos os dados críticos dos insumos estejam centralizados e acessíveis.
- **Registro de movimentações**: O sistema permite registrar movimentações de entrada e saída de insumos, atualizando automaticamente o estoque. As movimentações são essenciais para o monitoramento do fluxo de insumos e para o controle das quantidades disponíveis.
- **Consulta de estoque**: Através do sistema, os usuários podem consultar o estoque atual de qualquer insumo e visualizar dados importantes, como a validade dos produtos e a quantidade mínima de estoque. Isso ajuda na tomada de decisões sobre novas compras ou a utilização de insumos que estão próximos do vencimento.
- **Previsão de estoque**: Utilizando a técnica de **regressão linear**, o sistema é capaz de prever quando o estoque de um insumo específico irá se esgotar. Essa previsão é feita com base no consumo histórico do insumo, proporcionando aos gestores informações valiosas para planejar reabastecimentos e evitar a falta de materiais.
- **Geração de relatórios**: O sistema permite gerar relatórios detalhados sobre o consumo e a movimentação de insumos. Esses relatórios podem ser filtrados por categoria ou fornecedor, oferecendo uma visão personalizada dos dados. Os relatórios podem ser exportados tanto em **JSON** quanto em **CSV**, o que facilita a integração com outras ferramentas de análise ou apresentação.

Com essas funcionalidades, o sistema de Gestão de Estoque de Insumos se destaca por sua capacidade de fornecer controle total sobre o fluxo de insumos em uma operação agrícola, oferecendo previsões baseadas em dados e ferramentas analíticas que ajudam na tomada de decisão.


## 📁 Estrutura de pastas

Dentre os arquivos e pastas presentes na raiz do projeto, definem-se:

- <b>assets</b>: aqui estão os arquivos relacionados a elementos não-estruturados deste repositório, como imagens.
- <b>src</b>: Todo o código fonte criado para o desenvolvimento do projeto.
- <b>README.md</b>: arquivo que serve como guia e explicação geral sobre o projeto (o mesmo que você está lendo agora).

## 🔧 Como executar o código

### Configurações necessárias:

1. **Banco de dados**:

   O sistema cria automaticamente as tabelas necessárias no banco de dados Oracle ao ser executado pela primeira vez. Não é necessário criar as tabelas manualmente. Certifique-se de que as informações de conexão com o banco de dados estão corretas no arquivo `.env`.

2. **Configurar variáveis de ambiente**:

   Crie um arquivo `.env` na raiz do projeto com as informações de acesso ao banco de dados:

   ```bash
   DB_USER=seu_usuario
   DB_PASSWORD=sua_senha
   DB_DSN=seu_dsn

3. **Instale as dependências**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Execute o projeto**:
   ```bash
   python src/main.py
   ```

### Executando o código:
- **Cadastro de insumos**: Acesse a opção 1 no menu principal para cadastrar insumos.
- **Registrar movimentação**: Use a opção 2 para registrar entradas ou saídas de insumos.
- **Consultar estoque**: Utilize a opção 3 para consultar o estoque atual.
- **Gerar relatórios**: A opção 4 permite gerar relatórios de consumo, validade ou movimentação, e exportar em **JSON** ou **CSV**. Você também pode aplicar filtros como categoria e fornecedor.

## 🗃 Histórico de lançamentos

* 1.0.0 - 12/10/2024
    * Primeira versão funcional do sistema de gestão de estoque de insumos com suporte para JSON e CSV
    * Adição da funcionalidade de previsão de estoque usando regressão linear
    * Adição da funcionalidade de geração de relatórios com filtros dinâmicos
    * Integração com o banco de dados Oracle
    * Criação do módulo de movimentação de insumos

## 📋 Licença

<img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/cc.svg?ref=chooser-v1"><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/by.svg?ref=chooser-v1"><p xmlns:cc="http://creativecommons.org/ns#" xmlns:dct="http://purl.org/dc/terms/"><a property="dct:title" rel="cc:attributionURL" href="https://github.com/agodoi/template">MODELO GIT FIAP</a> por <a rel="cc:attributionURL dct:creator" property="cc:attributionName" href="https://fiap.com.br">Fiap</a> está licenciado sobre <a href="http://creativecommons.org/licenses/by/4.0/?ref=chooser-v1" target="_blank" rel="license noopener noreferrer" style="display:inline-block;">Attribution 4.0 International</a>.</p>