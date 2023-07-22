from tkinter import *
from main import *
import tkinter as tk
from tkinter import messagebox
import sqlite3
#cores

cor0 = "#f0f3f5"  # Preta / black
cor1 = "#feffff"  # branca / white
cor2 = "#3fb5a3"  # verde / green
cor3 = "#38576b"  # valor / value
cor4 = "#403d3d"   # letra / letters

def pesquisa_por_data_hoje():
        data_hoje = datetime.date.today().isoformat()
        pesquisa_por_data(data_hoje)


def sair():
    if messagebox.askokcancel("Sair", "Deseja realmente sair?"):
        root.quit()

root = tk.Tk()
root.title("Gerenciador De Entregas")
root.geometry("500x250")

conexao = sqlite3.connect('entregas.db')
cursor = conexao.cursor()

# Função para criar um submenu em cascata
def criar_submenu(parent, options):
    submenu = tk.Menu(parent, tearoff=0)
    for label, command in options.items():
        if label == "-":  # Adiciona uma linha separadora
            submenu.add_separator()
        else:
            submenu.add_command(label=label, command=command)
    return submenu

# Cria a barra de menu principal
barra_menu = tk.Menu(root)
root.config(menu=barra_menu)

# Cria os menus principais
menu_adicionar = criar_submenu(barra_menu, {
    "Adicionar Cliente": lambda: print("cliente"),
    "Adicionar Entregador": lambda: print("entregador"),
    "-": None,  # Linha separadora
    "Sair": sair
})

menu_Deletar = criar_submenu(barra_menu, {
    "Deletar Cliente": lambda: print("Deletar Cliente"),
    "Deletar Entregador": lambda: print("Deletar Entregador"),
    "Deletar Entrega Em Aberto": lambda: print("Deletar Entrega Em aberto"),
    "Deletar Entrega Em Rota": lambda: print("Deletar Entrega Em Rota")
})

menu_exibir = criar_submenu(barra_menu, {
    "Exibir Clientes": lambda : print("Exibir Clientes"),
    "Exibir Entregadores": lambda : print("Exibir Enregadores")
})

menu_editar = criar_submenu(barra_menu, {
    "Editar Clientes": lambda : print("Editar Clientes"), #criar as funções no backend
    "Editar Entregadores": lambda : print("Editar Enregadores") #criar as funções no backend
})

menu_pesquisa = criar_submenu(barra_menu, {
    "Pesquisa Entregas De Hoje": pesquisa_por_data_hoje,
   
})


# Adiciona os menus principais à barra de menu
barra_menu.add_cascade(label="Adicionar", menu=menu_adicionar)
barra_menu.add_cascade(label="Deletar", menu=menu_Deletar)
barra_menu.add_cascade(label="Exibir", menu=menu_exibir)
barra_menu.add_cascade(label="Editar", menu=menu_editar)
barra_menu.add_cascade(label="Pesquisa", menu=menu_pesquisa)

conexao.close()

root.mainloop()

