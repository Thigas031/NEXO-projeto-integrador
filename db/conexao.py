import mysql.connector
from mysql.connector import Error

def criar_conexao():
    try:
        conexao = mysql.connector.connect(
            host="localhost",
            user="root",
            password="SUA_SENHA",
            database="meu_banco"
        )

        if conexao.is_connected():
            print("Conexão realizada com sucesso!")
            return conexao

    except Error as e:
        print(f"Erro ao conectar ao MySQL: {e}")
        return None