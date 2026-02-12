CREATE SCHEMA IF NOT EXISTS Escola;
USE Escola;
CREATE table if not exists Alunos (
Id INT(10) Primary key auto_increment NOT NULL,   
Data_de_nascimento Date,
Zona_urbana VARCHAR (100),
Veiculo_proprio BIT,
Ocupacao VARCHAR (100)
);

insert into Alunos (Data_de_nascimento, Zona_urbana, Veiculo_proprio, Ocupacao) 
VALUES ('2006-10-10', 'Leste', 0, 'analista de suporte'),
('2026-09-06', 'Sul',   1, 'Produção'),
('1993-05-01', 'Oeste', 0, 'Estoquista'),
('1998-01-30', 'Oeste', 1, 'Estudante'),
('2003-12-13', 'Oeste', 0, 'Auxiliar Financeiro'),
('2000-05-19', 'Oeste', 0, 'Assistente de TI'),
('1976-05-03', 'Oeste', 0, 'Estudante'),
('1977-05-16', 'Norte', 0, 'Organização'),
('2002-08-30', 'Cambé', 0, 'Estudante')
;  

select * from Alunos;

#1. Menores de 18 anos
SELECT * From Alunos WHERE Data_de_nascimento > DATE_SUB(CURRENT_DATE(), INTERVAL 18 YEAR);
#2. Maiores de 18 anos
SELECT * From Alunos WHERE Data_de_nascimento <= DATE_SUB(CURRENT_DATE(),INTERVAL 18 YEAR);
#3. Veiculo proprio
SELECT * From Alunos WHERE Veiculo_proprio = 1;
#4.Apenas região
SELECT * From Alunos WHERE Veiculo_proprio;
#5.Trabalham com TI
SELECT * FROM Alunos WHERE Ocupacao LIKE '%TI';
#6.Estuda e tem carro proprio
SELECT * From Alunos WHERE Veiculo_proprio = 1 and Ocupacao = 'Estudante'

#7. A partir da analise dos dados consultados na tabela alunos, é possível notar que: 
  1. Embora a maioria dos alunos seja maior de idade, apenas dois possuem veículo próprio. Esse dado sugere um recorte social de vulnerabilidade ou desigualdade financeira entre o grupo;
  2. Contudo, a maioria reside em regiões próximas ao colégio, o que pode indicar que a distância e a dificuldade de locomoção são barreiras para estudantes de zonas mais remotas;
  3. A baixa atuação atual na área de TI sinaliza uma tendência de transição de carreira ou de busca pelo primeiro ingresso qualificado no mercado através da profissionalização;
  4. Portanto, o perfil socioeconômico predominante é de adultos que buscam ascensão econômica por meio da inserção no setor tecnológico.
