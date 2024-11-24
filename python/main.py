import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import requests

# URL do servidor para requisições HTTP
SERVER_URL = "http://ip_do_servidor:5000"

# Função para exibir a tabela de movimentações
def exibir_tabela_via_http(sessao):
    try:
        response = requests.get(f"{SERVER_URL}/movimentacoes/{sessao}")
        response.raise_for_status()
        dados = response.json()

        nova_janela = tk.Toplevel()
        nova_janela.title(f"Tabela de Movimentação na sessão {sessao.capitalize()}")

        # Criar widget Treeview com colunas 'Movimentação', 'Data' e 'Hora'
        tree = ttk.Treeview(nova_janela, columns=('Movimentação', 'Data', 'Hora'), show='headings')
        tree.heading('Movimentação', text='Movimentação')
        tree.heading('Data', text='Data')
        tree.heading('Hora', text='Hora')
        tree.pack(fill=tk.BOTH, expand=True)

        for dado in dados:
            mov = dado.get('mov', 'N/A')  # Movimentação registrada
            if 'timestamp' in dado:
                try:
                    # Tentar interpretar o timestamp no formato ISO 8601
                    timestamp = datetime.fromisoformat(dado['timestamp'].replace("Z", "+00:00"))
                    data = timestamp.strftime('%d/%m/%Y')
                    hora = timestamp.strftime('%H:%M:%S')
                except ValueError:
                    data, hora = 'N/A', 'N/A'
            else:
                data, hora = 'N/A', 'N/A'
            tree.insert('', tk.END, values=(mov, data, hora))

    except requests.exceptions.RequestException as e:
        messagebox.showerror("Erro", f"Falha ao obter dados da sessão {sessao.capitalize()}. Detalhes: {e}")

# Função para gerar gráfico de pizza via HTTP
def gerar_grafico_pizza_http():
    sessoes = ['masculina', 'feminina', 'infantil', 'esportes']
    inicio_semana = datetime.now() - timedelta(days=7)
    visitas = {}

    try:
        for sessao in sessoes:
            response = requests.get(f"{SERVER_URL}/movimentacoes/{sessao}")
            response.raise_for_status()
            dados = response.json()

            # Filtrar movimentações da última semana
            visitas[sessao.capitalize()] = sum(
                1 for dado in dados if 'timestamp' in dado and
                datetime.fromisoformat(dado['timestamp'].replace("Z", "+00:00")) >= inicio_semana
            )

        # Gerar gráfico de pizza
        labels = [sessao for sessao, count in visitas.items() if count > 0]
        sizes = [count for count in visitas.values() if count > 0]

        if sizes:
            plt.figure(figsize=(8, 6))
            plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, colors=plt.cm.Paired.colors)
            plt.title("Porcentagem de Sessões Mais Visitadas (Últimos 7 dias)")
            plt.show()
        else:
            messagebox.showinfo("Sem Dados", "Não há movimentações registradas na última semana.")

    except requests.exceptions.RequestException as e:
        messagebox.showerror("Erro", f"Falha ao obter dados para o gráfico. Detalhes: {e}")
    except ValueError as e:
        messagebox.showerror("Erro", f"Falha ao processar datas. Detalhes: {e}")


# Função para criar a interface gráfica
def cria_tela():
    janela = tk.Tk()
    janela.title("Hub de Seleção de Sessões")
    janela.resizable(True, True)

    # Configuração de colunas para layout responsivo
    janela.columnconfigure(0, weight=1)
    janela.columnconfigure(1, weight=1)
    janela.rowconfigure(0, weight=1)
    janela.rowconfigure(1, weight=1)

    # Dicionário para facilitar a criação de botões para cada sessão
    sessoes = {
        "masculina": "Tabela Sessão Masculina",
        "feminina": "Tabela Sessão Feminina",
        "infantil": "Tabela Sessão Infantil",
        "esportes": "Tabela Sessão Esportes",
    }

    # Criar e posicionar botões dinamicamente
    for idx, (sessao, texto) in enumerate(sessoes.items()):
        botao = ttk.Button(janela, text=texto, command=lambda s=sessao: exibir_tabela_via_http(s))
        botao.grid(column=idx % 2, row=idx // 2, padx=10, pady=10)

    # Botão para gerar gráfico de pizza
    botaoGrafico = ttk.Button(janela, text="Exibir Gráfico de Sessões", command=gerar_grafico_pizza_http)
    botaoGrafico.grid(column=0, row=2, columnspan=2, padx=10, pady=10)

    janela.mainloop()

# Iniciar a interface gráfica
cria_tela()
