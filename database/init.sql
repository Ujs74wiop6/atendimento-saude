-- Tabela "1" 
CREATE TABLE paciente (
    id SERIAL PRIMARY KEY,              
    nome VARCHAR(100) NOT NULL,
    cpf VARCHAR(14)  NOT NULL UNIQUE,     
    data_nascimento DATE NOT NULL,
    telefone VARCHAR(20),                     
    removido BOOLEAN NOT NULL DEFAULT false 
);

-- Tabela "N"
CREATE TABLE consulta (
    id SERIAL PRIMARY KEY,
    paciente_id INTEGER NOT NULL REFERENCES paciente(id),  
    data_consulta DATE NOT NULL,
    descricao VARCHAR(255)  NOT NULL,
    valor NUMERIC(10,2) NOT NULL CHECK (valor >= 0),     
    removido BOOLEAN NOT NULL DEFAULT false
);

-- Tabela sem relação
CREATE TABLE usuario (
    id SERIAL PRIMARY KEY,
    login VARCHAR(50) NOT NULL UNIQUE,
    senha VARCHAR(100) NOT NULL,  
    removido BOOLEAN NOT NULL DEFAULT false
);

-- Usuário inicial
INSERT INTO usuario (login, senha) VALUES ('dw3', 'dw3');
