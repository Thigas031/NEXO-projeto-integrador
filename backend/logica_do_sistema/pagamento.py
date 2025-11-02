import database_config  # integração futura com o banco de dados
from datetime import datetime

class Pagamento:
    def __init__(self, id_pagamento, pedido, metodo):
        self.id_pagamento = id_pagamento
        self.pedido = pedido
        self.metodo = metodo
        self.valor = pedido.valor_total
        self.data = datetime.now()
        self.status = "Pendente"

    def processar_pagamento(self):
        if self.valor > 0:
            self.status = "Aprovado"
            self.pedido.finalizar_pedido()
        else:
            self.status = "Falhou"

    def __str__(self):
        return f"Pagamento {self.id_pagamento} - Pedido {self.pedido.id_pedido} - Status: {self.status}"