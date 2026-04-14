/* Exibam uma tabela com a população total e a média da expectativa de vida 
de cada continente para os países que são monarquias. Agrupe e ordene os dados exibidos.
*/

SELECT JSON_PRETTY(doc) FROM countryinfo;

SELECT 
JSON_EXTRACT(doc, '$.Name') AS pais,
FORMAT(SUM(JSON_EXTRACT (doc, '$.demographics.Population')), 2) AS populacaototal,
CONCAT(ROUND(AVG(JSON_EXTRACT (doc, '$.demographics.LifeExpectancy'))),' anos') AS mediaExpectativaVida,
JSON_EXTRACT(doc, '$.geography.Continent') AS continente,
JSON_EXTRACT(doc, '$.government.GovernmentForm') AS Governo
FROM countryinfo 
WHERE JSON_EXTRACT(doc, '$.government.GovernmentForm') LIKE '%Monarchy%'
group by continente, governo, pais
ORDER BY continente
;

/*
Questão 2
Utilize 3 usos da função JSON utilizando diferentes chaves e valores
*/

select
	json_extract(doc, '$.Name') as nome,
	json_unquote(json_extract(doc, '$.geography.Continent')) as continente,
    json_pretty(doc) as jon_formatado
from countryinfo;
    