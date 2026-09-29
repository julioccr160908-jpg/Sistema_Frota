import errors
import re
from abc import ABC
import datetime
import sqlite3

class Automovel(ABC):

    status_auto = ["Disponivel","Manutencao", "ocupado"]

    @staticmethod
    def verificar_placa(placa: str):
        placa_limpa = placa.strip()
        
        padrao = r'^[A-Z]{3}-?[0-9][A-Z0-9][0-9]{2}$'
    
        if re.match(padrao, placa_limpa, re.IGNORECASE):
            return True
        return False


    def __init__(self,ano:int, modelo: str, placa: str, tipo:str, id:int=None, status:str= 'Disponivel'):
        self.id = id
        self.tipo = tipo
        self.placa = placa.replace('-', "").upper().strip()
        self.modelo = modelo
        self.ano = ano
        self.status = status

        if not self.verificar_placa(placa):
            raise errors.PlacaIncorretaErro(f"Placa {placa} é inválida")

        if tipo not in ['Carro', 'Caminhão']:
            raise errors.ModeloInvalido()
        

        self._placa = placa
        self.status = self.status_auto[0]


    def salvar(self):
        conexao = sqlite3.connect('DataBase.db')
        cursor = conexao.cursor()

        try:
            cursor.execute("""
                INSERT INTO automoveis (tipo, placa, modelo, ano, status) 
                VALUES (?, ?, ?, ?, ?)
            """, (self.tipo, self.placa, self.modelo, self.ano, self.status))

            conexao.commit()
            print(f"{self.tipo} {self.modelo} cadastrado com sucesso!")
            return True
        except sqlite3.IntegrityError:
            print("Erro: Esta placa já está cadastrada no sistema.")
            return False

        finally:
            conexao.close()

    @classmethod
    def listar_disponiveis(cls):
        conexao = sqlite3.connect('DataBase.db')
        cursor = conexao.cursor()
        
        try:
            cursor.execute("SELECT * FROM automoveis WHERE status = 'Disponivel'")
            carros_disponiveis = cursor.fetchall()
            return carros_disponiveis
        
        finally:
            conexao.close()

    @classmethod
    def buscar_por_placa(cls, placa:str):
        placa = placa.replace('-', "").upper()
        conexao = sqlite3.connect('DataBase.db')
        cursor = conexao.cursor()
        
        try:
            cursor.execute("""SELECT * FROM automoveis WHERE placa = ?
            """, (placa,))
            carro = cursor.fetchone()
            return carro

        
        except:
            print("Erro: Esta placa não foi encontrada no sistema.")
            return False
        
        finally:
            conexao.close()
        

    def atualizar_status(self, novo_status):
        conexao = sqlite3.connect('DataBase.db')
        cursor = conexao.cursor()
        
        try:
            cursor.execute("""UPDATE automoveis SET status = ? WHERE id = ?
            """, (novo_status, self.id))
            conexao.commit()
            return True

        finally:
            conexao.close()



class Carro(Automovel):

    def __init__(self, ano, modelo, placa):
        super().__init__(ano, modelo, placa, "Carro")



class Caminhao(Automovel):

    def __init__(self, ano, modelo, placa):
        super().__init__(ano, modelo, placa, "Caminhão")
        





