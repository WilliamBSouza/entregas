
import tkinter as tk
from tkinter import messagebox
import sqlite3

# Função para obter os dados do entregador a ser editado
def obter_dados_entregador():
    cod = entry_cod.get()

    if cod:
        conexao = sqlite3.connect('entregas.db')
        cursor = conexao.cursor()

        cursor.execute('SELECT nome, telefone FROM entregadores WHERE cod = ?', (cod,))
        cliente = cursor.fetchone()

        if cliente:
            entry_nome.delete(0, tk.END)
            entry_telefone.delete(0, tk.END)
            

            entry_nome.insert(0, cliente[0])
            entry_telefone.insert(0, cliente[1])
            
        else:
            messagebox.showwarning("Erro", "Entregador não encontrado.")

        cursor.close()
        conexao.close()
    else:
        messagebox.showwarning("Erro", "Por favor, insira o código do entregador.")

# Função para atualizar os dados do entregador no banco de dados
def atualizar_entregador():
    cod = entry_cod.get()
    nome = entry_nome.get()
    telefone = entry_telefone.get()
    

    if cod and nome and telefone:
        conexao = sqlite3.connect('entregas.db')
        cursor = conexao.cursor()

        cursor.execute('UPDATE entregadores SET nome = ?, telefone = ? WHERE cod = ?', (nome, telefone, cod))
        conexao.commit()

        cursor.close()
        conexao.close()

        messagebox.showinfo("Sucesso", "Entregador atualizado com sucesso!")

        # Limpar os campos de entrada após a atualização bem-sucedida
        entry_cod.delete(0, tk.END)
        entry_nome.delete(0, tk.END)
        entry_telefone.delete(0, tk.END)
        

    else:
        messagebox.showwarning("Erro", "Por favor, preencha todos os campos.")

def janela_editar_entregadores():
    root = tk.Tk()
    root.title("Editar Entregadores")
    root.geometry("350x200")
    
    label_cod = tk.Label(root, text="Código do Entregador:")
    label_cod.place(x=10, y=10)
    global entry_cod
    entry_cod = tk.Entry(root)
    entry_cod.place(x=140, y=10)

    btn_obter_dados = tk.Button(root, text="Obter Dados", command=obter_dados_entregador)
    btn_obter_dados.place(x=150, y=30)

    label_nome = tk.Label(root, text="Nome:")
    label_nome.place(x=10, y=70)
    global entry_nome
    entry_nome = tk.Entry(root)
    entry_nome.place(x=140, y=70)

    label_telefone = tk.Label(root, text="Telefone:")
    label_telefone.place(x=10, y=90)
    global entry_telefone
    entry_telefone = tk.Entry(root)
    entry_telefone.place(x=140, y=90)

    btn_atualizar = tk.Button(root, text="Atualizar", command=atualizar_entregador)
    btn_atualizar.place(x=160, y=120)

    root.mainloop()


janela_editar_entregadores()