import threading
from flask import Flask, request, jsonify
from pymongo import MongoClient
import tkinter as tk
from tkinter import ttk

# Configuração do Flask
app = Flask(__name__)

# Configuração do MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['arduino']  # Nome do banco de dados


# Função para buscar dados e exibi-los em uma tabela em uma nova janela
def exibir_tabela_masculina():
    collection = db['masculina']
    
    nova_janela = tk.Toplevel()
    nova_janela.title("Tabela de Movimentação na sessão masculina")
    
    # Criar um widget Treeview com colunas 'Data' e 'Hora'
    tree = ttk.Treeview(nova_janela, columns=('Data', 'Hora'), show='headings')
    tree.heading('Data', text='Data')
    tree.heading('Hora', text='Hora')
    tree.pack(fill=tk.BOTH, expand=True)

    # Buscar dados do MongoDB ordenados por timestamp (do mais recente para o mais antigo)
    sala = list(collection.find({}, {'_id': 0, 'mov': 1, 'timestamp': 1}).sort('timestamp', -1))
    for dado in sala:
        # Converter o timestamp para uma string legível, se existir
        data = dado['timestamp'].strftime('%d/%m/%Y') if 'timestamp' in dado else 'N/A'
        hora = dado['timestamp'].strftime('%H:%M:%S') if 'timestamp' in dado else 'N/A'
        tree.insert('', tk.END, values=(data, hora))


def exibir_grafico():
    collection = db['sala']

    

# Função para criar a interface gráfica
def cria_tela():
    janela = tk.Tk()
    janela.title("Hub de seleção")
    janela.resizable(True, True)

    # Configuração de colunas para expansão
    janela.columnconfigure(0, weight=1)
    janela.columnconfigure(1, weight=1)
    janela.rowconfigure(0, weight=1)

    # Criar e posicionar os botões
    botaoTabela = ttk.Button(janela, text="Exibir Tabela Sala", command=exibir_tabela_sala)
    botaoTabela.grid(column=0, row=0, padx=10, pady=10)

    botaoGrafico = ttk.Button(janela, text="Exibir Gráfico Sala", command=exibir_grafico_sala)
    botaoGrafico.grid(column=1, row=0, padx=10, pady=10)

    janela.mainloop()

# Iniciar a interface gráfica
cria_tela()
