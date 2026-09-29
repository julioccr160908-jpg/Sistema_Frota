import sqlite3
import os
import automovel
print(f"O script está rodando na pasta: {os.getcwd()}")

conexao = sqlite3.connect('DataBase.db')

cursor = conexao.cursor()

cursor.executescript("""CREATE TABLE automoveis (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tipo TEXT NOT NULL,
    placa TEXT UNIQUE NOT NULL,
    modelo TEXT NOT NULL,
    ano INTEGER NOT NULL,
    status TEXT DEFAULT 'Disponivel'
);

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    role TEXT NOT NULL,
    cnh TEXT UNIQUE NOT NULL,
    nome TEXT NOT NULL,
    telefone TEXT
);

CREATE TABLE reservas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    automovel_id INTEGER REFERENCES automoveis(id),
    user_id INTEGER REFERENCES users(id),
    data_inicio TEXT NOT NULL,
    data_final TEXT NOT NULL
);


""")



conexao.commit()

conexao.close()