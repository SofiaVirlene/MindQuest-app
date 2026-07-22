-- Tabela de Diretores
CREATE TABLE diretores (
    id_diretor SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    nacionalidade VARCHAR(50),
    data_nascimento DATE
);

-- Tabela de Filmes
CREATE TABLE filmes (
    id_filme SERIAL PRIMARY KEY,
    titulo VARCHAR(150) NOT NULL,
    genero VARCHAR(50),
    duracao_minutos INT,
    id_diretor INT REFERENCES diretores(id_diretor)
);

-- Tabela de Sessões (Exibições)
CREATE TABLE sessoes (
    id_sessao SERIAL PRIMARY KEY,
    id_filme INT REFERENCES filmes(id_filme),
    sala INT,
    horario TIME,
    ingressos_vendidos INT,
    valor_ingresso DECIMAL(10, 2)
);

-- Inserção de Dados
INSERT INTO diretores (nome, nacionalidade, data_nascimento) VALUES 
('Christopher Nolan', 'Britânico', '1970-07-30'),
('Greta Gerwig', 'Americana', '1983-08-04'),
('Martin Scorsese', 'Americano', '1942-11-17'),
('Bong Joon-ho', 'Coreano', '1969-09-14');

INSERT INTO filmes (titulo, genero, duracao_minutos, id_diretor) VALUES 
('Oppenheimer', 'Drama', 180, 1),
('Inception', 'Ficção Científica', 148, 1),
('Barbie', 'Comédia', 114, 2),
('Lady Bird', 'Drama', 94, 2),
('Killers of the Flower Moon', 'Crime', 206, 3),
('Taxi Driver', 'Drama', 114, 3),
('Parasite', 'Suspense', 132, 4),
('Snowpiercer', 'Ação', 126, 4);

INSERT INTO sessoes (id_filme, sala, horario, ingressos_vendidos, valor_ingresso) VALUES 
(1, 1, '14:00', 120, 45.00), (1, 1, '19:00', 150, 50.00),
(3, 2, '13:30', 200, 35.00), (3, 2, '16:00', 180, 35.00),
(7, 3, '21:00', 95, 40.00), (5, 4, '15:00', 60, 40.00),
(2, 5, '22:30', 45, 30.00), (8, 3, '18:00', 70, 30.00);