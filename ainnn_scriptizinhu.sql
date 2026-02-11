CREATE SCHEMA Escola;
CREATE table Alunos (
Id INT(10) Primary key auto_increment NOT NULL,   
Data_de_nascimento Date,
Zona_urbana VARCHAR (100),
Veiculo_proprio BIT,
Ocupacao VARCHAR (100)
);

insert into Alunos (Data_de_nascimento, Zona_urbana, Veiculo_proprio, Ocupacao) 
VALUES (('2006-10-10', 'Leste', '0', 'analista de suporte'),
('2026-09-06', 'Sul',   '1', 'Produção'),
('1993-05-01', 'Oeste', '0', 'Estoquista'),
('1998-01-30', 'Oeste', '1', 'Estudante'),
('2003-12-13', 'Oeste', '0', 'Auxiliar Financeiro'),
('2000-05-19', 'Oeste', '0', 'Assistente de TI'),
('1976-05-03', 'Oeste', '0', 'Estudante'),
('1977-05-16', 'Norte', '0', 'Organização'),
('2002-08-30', 'Cambé', '0', 'Estudante');  
--1.
SELECT * From Alunos WHERE Data_de_nascimento > DATE_SUB (CURRENT_DATE,INTERVAL 18 YEARS)
--2.
SELECT * From Alunos WHERE Data_de_nascimento <= DATE_SUB (CURRENT_DATE,INTERVAL 18 YEARS)
--3.
SELECT * From Alunos WHERE
--4.
SELECT * From Alunos WHERE
--5.
SELECT * From Alunos WHERE
--6.
SELECT * From Alunos WHERE
--7.
SELECT * From Alunos WHERE
