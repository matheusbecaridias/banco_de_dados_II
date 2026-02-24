/* 1. Selecione os campos nome, de_ferias e bairro a partir da tabela de
vendedores. Em seguida, selecione a vendedora com o nome de
‘Cláudia Morais’, cujo bairro é ‘Jardins’. Ela está de férias? */

SELECT nome, de_ferias, bairro FROM tabela_de_vendedores;
# Sim, 'Cláudia Morais', do bairro 'Jardins', está de férias;

/* 2. A partir da tabela de vendedores, selecione a pessoa que possui
comissão acima de 0.10 e que está de férias.*/

SELECT *  FROM tabela_de_vendedores where percentual_comissao > 0.10 and DE_FERIAS = '1';
#'00237', 'Roberta Martins', '0.11', '2017-03-18', '1', 'Copacabana'

/* 3. Realize uma consulta na tabela de notas fiscais, identificando o
número de matrícula 00237 ou a data de venda do dia 12-01-2015.
Por que o CPF desta tabela não é uma chave primária (PK)? */

SELECT * from notas_fiscais WHERE MATRICULA = '00237' OR DATA_VENDA = '2015-01-12';
# O CPF desta tabela não é uma chave primária porque ocorre mais de uma vez.

/* 4. Na tabela dos itens das notas fiscais, selecione o código do produto
e a quantidade vendida dos itens que possuam quantidade de venda
igual ou maior do que 99. Qual ou quais itens representam o maior
valor de venda? */

 SELECT CODIGO_DO_PRODUTO, QUANTIDADE FROM itens_notas_fiscais WHERE QUANTIDADE >= '99'; 
 
/* 5. Quem é o cliente que comprou 84 produtos com o número de código
igual a 1101035, cujo número da nota fiscal foi 102? Quem foi o
vendedor ou vendedora responsável e qual o nome do produto e seu
sabor? Gere o Diagrama de Entidade - Relacionamento para melhor
compreensão.*/
 
 SELECT NOME FROM tabela_de_clientes WHERE   
 