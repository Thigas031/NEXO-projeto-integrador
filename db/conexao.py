import mysql.connector
from mysql.connector import Error

class ConexaoMySQL:
    def __init__(self, host="localhost", usuario="root", senha="root", banco="Nexo"):
        self.host = host
        self.usuario = usuario
        self.senha = senha
        self.banco = banco
        self.conexao = None

    def conectar(self):
        try:
            self.conexao = mysql.connector.connect(
                host=self.host,
                user=self.usuario,
                password=self.senha,
                database=self.banco
            )
            return self.conexao
        except Error as e:
            print(f"Erro ao conectar ao MySQL: {e}")
            return None

    def fechar(self):
        if self.conexao:
            self.conexao.close()

    def executar(self, query, valores=None, fetch=False):
        if not self.conexao:
            self.conectar()

        cursor = self.conexao.cursor(dictionary=True)
        try:
            cursor.execute(query, valores)
            if fetch:
                return cursor.fetchall()
            self.conexao.commit()
        except Error as e:
            print(f"Erro ao executar comando SQL: {e}")
            self.conexao.rollback()
        finally:
            cursor.close()

# Exemplo de uso
if __name__ == "__main__":
    db = ConexaoMySQL()
    db.conectar()

    # Criar tabela de clientes
    db.executar(
        """
        CREATE TABLE IF NOT EXISTS clientes (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nome VARCHAR(100) NOT NULL,
            contato VARCHAR(200)
        ) ENGINE=InnoDB;
        """
    )

    # Cadastrar um cliente
    db.executar(
        "INSERT INTO clientes (nome, contato) VALUES (%s, %s)",
        ("Thiago", "9999-9999")
    )

    # Buscar clientes
    clientes = db.executar("SELECT * FROM clientes", fetch=True)
    print(clientes)

    db.fechar()