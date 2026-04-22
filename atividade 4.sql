/*CENTRO EST EDU PROF P MARIA R CASTALDI
Curso Técnico em Análise e Desenvolvimento de Sistemas
Banco de Dados II

ATIVIDADE 3 - CONSULTAS MYSQL COM JSON 

Baseando-se no banco de dados world_x, realize as seguintes consultas:

/*Consulta 1: Escreva uma consulta que retorne o nome do país e 
a expectativa de vida de todos os países que pertencem à América do Sul.*/


SELECT 
    JSON_UNQUOTE(JSON_EXTRACT(doc, '$.Name')) AS Nome_Pais,
    JSON_EXTRACT(doc, '$.demographics.LifeExpectancy') AS Expectativa_Vida
FROM countryinfo
WHERE JSON_UNQUOTE(JSON_EXTRACT(doc, '$.geography.Continent')) = 'South America';


/*Consulta 2: Escreva uma consulta que liste todos os países onde o Produto Nacional Bruto (GNP) é maior que 500.000 e 
que possuam o idioma Inglês como um de seus idiomas oficiais.*/

SELECT JSON_UNQUOTE(JSON_EXTRACT(c.data, '$.Name')) AS Nome_Pais
FROM paises c
JOIN countrylanguage cl ON JSON_UNQUOTE(JSON_EXTRACT(c.data, '$.Code')) = cl.CountryCode
WHERE CAST(JSON_UNQUOTE(JSON_EXTRACT(c.data, '$.GNP')) AS DECIMAL(10,2)) > 500000
  AND cl.Language = 'English'
  AND cl.IsOfficial = 'T';

/* Agora, a partir do banco de dados empresa, realize as seguintes consultas:

/*Consulta 3: Desenvolva uma consulta que retorne o nome do funcionário e 
o conteúdo do campo JSON apenas para os funcionários com pelo menos um dependente do sexo Feminino. */


SELECT 
    CONCAT(f.PRIMEIRO_NOME, ' ', f.NOME_MEIO, ' ', f.ULTIMO_NOME) AS NOME_FUNCIONARIO,
    obj.JSON
FROM tb_funcionario f
INNER JOIN tb_object_funcionario obj 
    ON f.CPF = obj.CPF
WHERE f.CPF IN (
    SELECT DISTINCT CPF_FUNCIONARIO
    FROM tb_dependente
    WHERE SEXO = 'F'
);

/*Consulta 4: Utilizando a função JSON_TABLE, retorne todos os dependentes cadastrados no banco de dados. 
A consulta deve retornar: o nome, parentesco e data de nascimento do dependente e o nome do funcionário. */

SELECT 
    CONCAT(f.PRIMEIRO_NOME, ' ', f.NOME_MEIO, ' ', f.ULTIMO_NOME) AS NOME_FUNCIONARIO,
    jt.NOME_DEPENDENTE,
    jt.PARENTESCO,
    jt.DATA_NASCIMENTO
FROM tb_object_funcionario obj
INNER JOIN tb_funcionario f 
    ON obj.CPF = f.CPF
CROSS JOIN JSON_TABLE(
    obj.JSON,
    '$.dependentes[*]'
    COLUMNS (
        NOME_DEPENDENTE  VARCHAR(100) PATH '$.nome',
        PARENTESCO       VARCHAR(50)  PATH '$.parentesco',
        DATA_NASCIMENTO  DATE         PATH '$.data_nascimento'
    )
) AS jt;
