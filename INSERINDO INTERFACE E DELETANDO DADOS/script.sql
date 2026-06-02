CREATE DATABASE IF NOT EXISTS sistema_clientes;
USE sistema_clientes;

CREATE TABLE IF NOT EXISTS clientes (
    cpf VARCHAR(11) PRIMARY KEY,
        nome VARCHAR(100) NOT NULL,
            email VARCHAR(100) NOT NULL,
                telefone VARCHAR(15)
                );
                