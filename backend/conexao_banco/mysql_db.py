import database_config  # integração futura com o banco de dados
import mysql.connector

class BancoDeDados:
    # Classe responsável pela conexão e execução de comandos no MySQL.
    # Use-a para criar tabelas e realizar operações CRUD.

    def __init__(self, host, user, password, database):
        self.conexao = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.cursor = self.conexao.cursor()

    def executar(self, comando, valores=None):
        self.cursor.execute(comando, valores or ())
        self.conexao.commit()

    def consultar(self, comando, valores=None):
        self.cursor.execute(comando, valores or ())
        return self.cursor.fetchall()

    def fechar(self):
        self.cursor.close()
        self.conexao.close()