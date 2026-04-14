/* 
Matheus Becari(DS)

Pesquise sobre as funções abaixo e execute-as no MySQL. 
Ao fim, demonstrem para mim o que fizeram. */

-- FUNÇÕES:
-- JSON_MERGE_PATCH;
SELECT 
    CPF,
    JSON_MERGE_PATCH(
        JSON_OBJECT('Primeiro_Nome', 'João', 'Salario', 30000),
        JSON_OBJECT('Salario', 35000, 'NovoCampo', 'Teste')
    ) AS merge_patch
FROM tb_object_funcionario
WHERE CPF = '12345678966';

-- JSON_MERGE_PRESERVE;
SELECT 
    CPF,
    JSON_MERGE_PRESERVE(
        JSON_OBJECT('Primeiro_Nome', 'João', 'Salario', 30000),
        JSON_OBJECT('Salario', 35000, 'NovoCampo', 'Teste')
    ) AS merge_preserve
FROM tb_object_funcionario
WHERE CPF = '12345678966';

-- JSON_DEPTH;
SELECT 
    CPF,
    JSON_DEPTH(JSON) AS depth
FROM tb_object_funcionario
WHERE CPF = '12345678966';

-- JSON_LENGTH;
SELECT 
    CPF,
    JSON_LENGTH(JSON) AS quantidade_chaves_primeiro_nivel,
    JSON_LENGTH(JSON, '$.Dependentes') AS length
FROM tb_object_funcionario
WHERE CPF = '12345678966';

-- JSON_TYPE;
SELECT 
    CPF,
    JSON_TYPE(JSON) AS tipo_principal,
    JSON_TYPE(JSON_EXTRACT(JSON, '$.Primeiro_Nome')) AS tipo_primeiro_nome,
    JSON_TYPE(JSON_EXTRACT(JSON, '$.Dependentes')) AS type
FROM tb_object_funcionario
WHERE CPF = '12345678966';

-- JSON_VALID;
SELECT 
    CPF,
    JSON_VALID(JSON) AS json_eh_valido,
    JSON_VALID('{"nome": "teste"}') AS exemplo_valido,
    JSON_VALID('nome: teste') AS exemplo_invalido
FROM tb_object_funcionario
WHERE CPF = '12345678966';
