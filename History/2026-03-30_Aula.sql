

#30/03/2026 - JSON Contains Path

CREATE TABLE X (Y JSON);

INSERT INTO X VALUES ('{"nome": "Roberto", "telefone": "1234-5678"}');
INSERT INTO X VALUES ('{"nome": "Maria"}');
INSERT INTO X VALUES ('{"nome":"Alberto", "endereco": "Rua x numero y"}');
INSERT INTO X VALUES ('{"nome":"Leticia", "endereco": "Rua x numero y", "telefone":"1234-5678"}');

SELECT Y FROM X;

select json_contains_path(Y, "ONE", '$.nome') FROM X;

SELECT Y FROM X;

#JSON_CONTAINS
/*Permite procurar o VALOR das propriedades/chaves
dentro do JSON*/

SELECT JSON_CONTAINS_PATH(Y, "ONE", '$.nome') FROM X;

SELECT JSON_CONTAINS_PATH (Y, "ALL", '$.nome', '$.endereco') FROM X;

SELECT JSON_CONTAINS(Y, '"1234-5678"', "$.telefone") FROM X;
SELECT * FROM X WHERE
JSON_CONTAINS(Y, '"1234-5678"', "$.telefone") = 1;

#JSON_SEARCH
/*Permite encontrar um VALOR em qualquer
proprieJSON_SEARCH()dade*/
SELECT JSON_SEARCH(Y, "ONE", "Maria") FROM X;

/*Exercício da aula 30.03.2026*/
SELECT * FROM countryinfo ORDER BY _id;

-- JSON_EXTRACT()
SELECT JSON_EXTRACT(Info, '$.populacao') AS populacao FROM countryinfo;

-- JSON_KEYS()
SELECT JSON_KEYS(json_doc[, path]);

-- JSON_SEARCH()
SELECT JSON_SEARCH(json_doc, one_or_all, search_str[, escape_char[, path] ...])

-- JSON_CONTAINS()
SELECT JSON_CONTAINS(target_json, candidate_json[, path]);

-- JSON_CONTAINS_PATH()
SELECT JSON_CONTAINS_PATH(json_doc, one_or_all, path[, path] ...);

