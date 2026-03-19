/* ATIVIDADE AVALIATIVA 2
Suponha que a área comercial da empresa de Sucos de Frutas solicitou um relatório para acompanhar as vendas do ano de 2016 por sabores. 
Foi pedido que o relatório mostrasse uma coluna com os sabores, a quantidade (L) vendida no ano todo, 
ordenadas da maior para menor e a representação do percentual de venda de cada uma. 
Como desejamos os sabores, quantidade e ano, deveremos manipular três tabelas: 
itens_notas_fiscais, tabela_de_produtos e notas_fiscais. 
*/ 

SELECT SABOR AS SABORES FROM tabela_de_produtos TP
INNER JOIN itens_notas_fiscais INF 
ON TP.CODIGO_DO_PRODUTO = INF.CODIGO_DO_PRODUTO
INNER JOIN notas_fiscais NF 
ON NF.NUMERO = INF.NUMERO
WHERE YEAR(DATA_VENDA) = 2016;


FROM itens_notas_fiscais;
FROM notas_fiscais;
FROM tabela_de_produtos;

AS QUANTIDADE(L) ORDER BY DESC;
AS %_DE_VENDA;