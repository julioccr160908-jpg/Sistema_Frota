from abc import ABC
import re
import sqlite3

class User(ABC):

    @staticmethod
    def validar_cnh(cnh: str) -> bool:
        cnh_numeros = re.sub(r'\D', '', cnh)
        return len(cnh_numeros) == 11

    @staticmethod
    def validar_telefone(telefone: str) -> bool:
        tel_numeros = re.sub(r'\D', '', telefone)
        return len(tel_numeros) in [10, 11]


    def __init__(self, cnh, nome:str, telefone:str, role, id=None):
        if not self.validar_cnh(cnh):
            raise ValueError(f"A CNH '{cnh}' é inválida. Deve conter 11 dígitos.")
            
        if not self.validar_telefone(telefone):
            raise ValueError(f"O telefone '{telefone}' é inválido. Padrão esperado: (DD) XXXXX-XXXX.")
        self.id = id
        self.role = role
        self.telefone = re.sub(r'\D', '', telefone)
        self.nome = nome
        self.cnh = re.sub(r'\D', '', cnh)




    def salvar(self):
        conexao = sqlite3.connect('DataBase.db')
        cursor = conexao.cursor()

        try:
            cursor.execute("""
                INSERT INTO users (role, cnh, nome, telefone) 
                VALUES (?, ?, ?, ?)
            """, (self.role, self.cnh, self.nome, self.telefone))

            conexao.commit()
            print(f"{self.role} {self.nome} cadastrado com sucesso!")
            return True
        except sqlite3.IntegrityError:
            print("Erro: Esta CNH já está cadastrada no sistema.")
            return False

        finally:
            conexao.close()


    @classmethod
    def buscar_por_cnh(cls, cnh):
        cnh_limpa = re.sub(r'\D', '', cnh)
        conexao = sqlite3.connect('DataBase.db')
        cursor = conexao.cursor()
        
        try:
            cursor.execute("""SELECT * FROM users WHERE cnh = ?
            """, (cnh_limpa,))
            pessoa = cursor.fetchone()
            return pessoa

        
        except:
            print("Erro: Esta CNH não foi encontrada no sistema.")
            return None
        
        finally:
            conexao.close()




class UserRole(User):
    def __init__(self, cnh, nome, telefone, id=None):
        super().__init__(cnh, nome, telefone, "User", id)


class Admin(User):
    def __init__(self, cnh, nome, telefone, id=None):
        super().__init__(cnh, nome, telefone, "Admin", id)
        
