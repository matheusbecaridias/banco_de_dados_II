/* ATIVIDADE AVALIATIVA 2
Suponha que a área comercial da empresa de Sucos de Frutas solicitou um relatório para acompanhar as vendas do ano de 2016 por sabores. 
Foi pedido que o relatório mostrasse uma coluna com os sabores, a quantidade (L) vendida no ano todo, 
ordenadas da maior para menor e a representação do percentual de venda de cada uma. 
Como desejamos os sabores, quantidade e ano, deveremos manipular três tabelas: 
itens_notas_fiscais, tabela_de_produtos e notas_fiscais. 
*/ 

SELECT 
    SABORES,
    QUANTIDADE_ITEM,
    ANO,
    QUANTIDADE_TOTAL,
    (QUANTIDADE_ITEM / QUANTIDADE_TOTAL * 100) AS PERCENTUAL
FROM (
    SELECT 
        TP.SABOR AS SABORES, 
        SUM(INF.QUANTIDADE) AS QUANTIDADE_ITEM,
        YEAR(NF.DATA_VENDA) AS ANO,
        (SELECT SUM(INF.QUANTIDADE) 
            FROM itens_notas_fiscais INF
            INNER JOIN notas_fiscais NF
                ON NF.NUMERO = INF.NUMERO
            WHERE YEAR(NF.DATA_VENDA) = 2016
        ) AS QUANTIDADE_TOTAL
    FROM tabela_de_produtos TP
    INNER JOIN itens_notas_fiscais INF 
        ON TP.CODIGO_DO_PRODUTO = INF.CODIGO_DO_PRODUTO
    INNER JOIN notas_fiscais NF 
        ON NF.NUMERO = INF.NUMERO
    WHERE YEAR(NF.DATA_VENDA) = 2016
    GROUP BY TP.SABOR, YEAR(NF.DATA_VENDA)
) AS VENDAS_2016
ORDER BY QUANTIDADE_ITEM DESC;
