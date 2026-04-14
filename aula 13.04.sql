SELECT * FROM tb_object_funcionario;

SELECT JSON_EXTRACT(JSON, "$.Primeiro_Nome", "$.Data_Nascimento", "$.Numero_Departamento") 
FROM tb_object_funcionario;

SELECT JSON_EXTRACT(JSON, "$.Primeiro_Nome"), 
JSON_EXTRACT(JSON, "$.Data_Nascimento"), 
JSON_EXTRACT(JSON, "$.Salario") 
FROM tb_object_funcionario;

SELECT T1.PARENTESCO, T1.SEXO FROM tb_object_funcionario
CROSS JOIN
JSON_TABLE(
JSON_EXTRACT(JSON, "$.Dependentes"), "$[*]"
COLUMNS(PARENTESCO VARCHAR(20) PATH "$.Parentesco",
SEXO VARCHAR(2) PATH "$.Sexo")
) AS T1;

/* Crie uma tabela baseada no campo dependentes com uma
coluna para Sexo, Parentesco, Data de Nascimento e Nome
-do dependente (tb_object_funcionario). Além disso, utilize 
o INNER JOIN para adicionar 
o nome do deparatamento (tb_departamento). */


