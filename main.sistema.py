# ============================
# ARQUIVO: main_sistema.py
# ============================

import tkinter as tk
from tkinter import ttk, messagebox
from partes_do_sistema.cliente import Cliente
from partes_do_sistema.vendedor import Vendedor
from partes_do_sistema.produto import Produto
from logica_do_sistema.estoque import Estoque
from conexao_banco.mysql_db import BancoDeDados


# ============================
# CONFIGURAÇÃO DO BANCO
# ============================

# ============================
# INTERFACE TKINTER
# ============================
