INSERINDO INTERFACE E DELETANDO DADOS

Após finalizar a integração entre a página web, o servidor
Flask e o Banco de Dados, vamos incrementar a aplicação, ou
seja, adicionar outras funcionalidades.
1ª Funcionalidade: Tente criar uma tabela que exiba os clientes
após realização do cadastro. Para exibir os dados o Python deve
buscá-los no MySQL, então o Flask envia os dados para o HTML
e o Jinja2 (mecanismo de template da web para Python,
pesquisem mais sobre) exibe a tabela.
2ª Funcionalidade: Adicione um botão em cada cliente que
possibilite a sua exclusão. Para evitar erros, como excluir todos
os dados da tabela, vocês podem utilizar o CPF, que é uma
chave primária, como forma de realizar a exclusão com maior
segurança. Pode-se realizar o import da função redirect e
url_for, do Flask, para que a página atualize as informações na
tela.

CRIANDO NOVA TABELA
A página web que está sendo desenvolvida terá uma nova
tabela, a de produtos. Inicialmente vocês deverão criar uma nova
pasta para esta tabela e nela adicionar as pastas templates,
static e os arquivos necessários (futuramente iremos alterar os
locais dos arquivos).
Crie uma tabela no MySQL, selecionando o mesmo banco
de dados da tabela cliente. Esta tabela será relacionada ao
cadastro dos produtos e deve conter no mínimo quatro
campos. Lembrem-se de definir os tipos de dados, chave
primária e garantir que os campos não aceitem valores nulos.
Vocês têm liberdade para escolherem o tipo de produto.
Desenvolvam um arquivo HTML contendo o <form></form>
responsável por captar os dados e <table></table> para exibir os
produtos após o cadastro, além de um arquivo CSS para
estilização.
Seria possível adicionar diversos produtos (ou clientes)
simultaneamente antes de submeter o formulário? (ainda não
precisam aplicar a resposta, apenas pesquisar sobre)

Por fim, desenvolvam os algoritmos, em Python,
necessários para:
● Adicionar os produtos no banco de dados;
● Visualizar os produtos adicionados em uma tabela;
● Excluir os produtos do banco de dados.
