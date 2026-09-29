# Sistema de Gestão de Frota e Locação

> Sistema modular de gerenciamento de veículos, perfis de usuários e reservas de frota desenvolvido em Python puro, com persistência relacional em SQLite e interface de terminal (CLI).

---

## Visão Geral

O projeto foi arquitetado com base nas boas práticas de **Programação Orientada a Objetos (POO)** e separação de responsabilidades. O sistema conta com regras de negócio blindadas contra duplicidades e inconsistências, incluindo um **motor de reserva** que analisa e impede conflitos de datas no banco de dados.

---

## Tecnologias e Recursos Utilizados

- **Linguagem:** Python 3
- **Banco de Dados:** SQLite3
- **Expressões Regulares (`re`):** Validação e sanitização estrita de placas, CNHs e números de telefone
- **Manipulação Temporal (`datetime`):** Validação de calendário e conversão entre formato brasileiro (`DD/MM/AAAA`) e formato padrão ISO/banco (`AAAA-MM-DD`)
- **Versionamento:** Git e GitHub

---

## Destaques da Arquitetura e Segurança

- **Prevenção contra SQL Injection:** Todas as operações no banco utilizam queries parametrizadas (`?`) e blocos defensivos com `try/finally` para fechamento seguro de conexões.
- **Normalização e Sanitização de Dados:** 
  - Placas automotivas são padronizadas e salvas sem caracteres especiais em maiúsculas (`ABC1234`).
  - Documentos como CNH e telefone são sanitizados na entrada para remoção de pontuações indesejadas.
- **Camada de Apresentação Desacoplada:** A interface (`views.py`) utiliza fatiamento de strings (*slicing*) para exibir placas (`ABC-1234`) e dados de contato de forma legível sem poluir o banco de dados.
- **Algoritmo de Colisão de Reservas:** A classe `Reserva` executa consultas SQL comparando intervalos de datas (`data_inicio <= ? AND data_final >= ?`), impossibilitando a sobreposição de locações para o mesmo automóvel.
- **Modelagem com Classes Abstratas:** Uso de herança e polimorfismo via módulo `abc` para derivação de entidades especializadas (`Carro`, `Caminhao`, `Admin`, `UserRole`).

---

## Estrutura do Projeto

```text
├── automovel.py       # Classes de veículos (Automovel, Carro, Caminhao)
├── users.py           # Modelagem de usuários (User, Admin, UserRole)
├── reserva.py         # Motor de cálculo e persistência de reservas
├── views.py           # Camada de apresentação e interface CLI
├── errors.py          # Exceções personalizadas de negócio
├── __main__.py        # Script de inicialização das tabelas no banco
├── .gitignore         # Regras para exclusão de caches e bancos locais
└── README.md          # Documentação do projeto