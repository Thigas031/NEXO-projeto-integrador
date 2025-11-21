class Cliente:
    def __init__(self, id, nome, contato=""):
        self.id = id
        self.nome = nome
        self.contato = contato

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "contato": self.contato
        }