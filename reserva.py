from datetime import datetime
import sqlite3


class Reserva: 
    def __init__(self, user_id, automovel_id, data_inicio, data_final):
        self.user_id = user_id
        self.automovel_id = automovel_id

        self.data_inicio_db = self._formatar_data(data_inicio)
        self.data_final_db = self._formatar_data(data_final)


    @staticmethod
    def _formatar_data(data_br):
        data_formatada = datetime.strptime(data_br, "%d/%m/%Y").strftime("%Y-%m-%d")
        return data_formatada


    @classmethod
    def verificar_disp(cls, id_carro, data_inicial, data_final):
        data_inicial = cls._formatar_data(data_inicial)
        data_final = cls._formatar_data(data_final)
        conexao = sqlite3.connect('DataBase.db')
        cursor = conexao.cursor()
                
        try:
            cursor.execute("""SELECT * FROM reservas WHERE automovel_id = ? 
            AND data_inicio <= ? 
            AND data_final >= ?""", (id_carro, data_final, data_inicial)) 
            resultado = cursor.fetchone()
            if not resultado:
                return True
            else:
                return False

        
        finally:
            conexao.close()




    def salvar_datas(self):

        conexao = sqlite3.connect('DataBase.db')
        cursor = conexao.cursor()
                        
        try:
            cursor.execute("INSERT INTO reservas (automovel_id, user_id, data_inicio, data_final) VALUES (?, ?, ?, ?)", (self.automovel_id, self.user_id, self.data_inicio_db, self.data_final_db))
            conexao.commit()
            return True

        except Exception as e:
            print(f"Erro ao salvar: {e}")
            return False 

            
        finally:
            conexao.close()