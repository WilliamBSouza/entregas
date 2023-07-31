import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3
from datetime import date
import datetime


def exibir_dados():
    conexao = sqlite3.connect('entregas.db')
    cursor = conexao.cursor()

    cursor.execute("""
    SELECT cod_entrega, cod_cliente, nome_cliente, bairro_cliente, observação
    FROM entregas_aberto 
    ORDER BY cod_entrega ASC;
    """)
    dados_do_banco = cursor.fetchall()

    for row in tab_entregas_em_aberto.get_children():
        tab_entregas_em_aberto.delete(row)

    for row in dados_do_banco:
        tab_entregas_em_aberto.insert("", tk.END, values=row)

    conexao.close()

def exibir_entregadores():
    conexao = sqlite3.connect('entregas.db')
    cursor = conexao.cursor()

    cursor.execute("""
    SELECT cod, telefone, nome
    FROM entregadores 
    ORDER BY cod ASC;
    """)
    dados_entregadores = cursor.fetchall()

    entregadores_combobox['values'] = [nome for _, _, nome in dados_entregadores]

    conexao.close()

def mover_para_rota():
    
    selecionados = tab_entregas_em_aberto.selection()

    if not selecionados:
        messagebox.showwarning("Aviso", "Nenhuma entrega selecionada.")
        return

    entregador_selecionado = entregadores_combobox.get()
    if not entregador_selecionado:
        messagebox.showwarning("Aviso", "Selecione um entregador antes de transferir as entregas.")
        return

    data_entrega = date.today().strftime("%Y-%m-%d")  # Obtém a data atual no formato "YYYY-MM-DD"
    horario_saida = datetime.datetime.now().strftime("%H:%M:%S")

    conexao = sqlite3.connect('entregas.db')
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT cod, telefone, nome
        FROM entregadores
        WHERE nome = ?;
    """, (entregador_selecionado,))

    entregador_dados = cursor.fetchone()

    for item in selecionados:
        entrega_id = tab_entregas_em_aberto.item(item, "values")[0]
        cursor.execute("""
            INSERT INTO entregas_rota (cod_entrega, cod_cliente, nome_cliente, bairro, observação, cod_entregador, telefone_entregador, entregador, data_entrega, horário_saida)
            SELECT cod_entrega, cod_cliente, nome_cliente, bairro_cliente, observação, ?, ?, ?, ?, ? FROM entregas_aberto
            WHERE cod_entrega = ?;
        """, (entregador_dados[0], entregador_dados[1], entregador_dados[2], data_entrega, horario_saida, entrega_id))
        cursor.execute("DELETE FROM entregas_aberto WHERE cod_entrega = ?", (entrega_id,))
        conexao.commit()

    conexao.close()

    exibir_dados()


def adicionar_entrega_aberto():
    cod_cliente = cod_cliente_entry.get()
    observacao = observacao_entry.get()

    if not cod_cliente :
        messagebox.showwarning("Aviso", "Por favor, insira o código do cliente.")
        return

    cod_entrega = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") #o código da entrega é a data e hora exata 
    conexao = sqlite3.connect('entregas.db')
    cursor = conexao.cursor()

    try:
        cursor.execute("""
            INSERT INTO entregas_aberto (cod_cliente, nome_cliente, bairro_cliente, observação, cod_entrega)
            SELECT cod, nome, bairro, ?, ? FROM clientes
            WHERE cod = ?;
        """, (observacao, cod_entrega, cod_cliente))
        conexao.commit()
        messagebox.showinfo("Sucesso", "Entrega adicionada com sucesso!")
        exibir_dados()
    except sqlite3.Error as e:
        messagebox.showerror("Erro", "Ocorreu um erro ao adicionar a entrega:\n" + str(e))
    finally:
        conexao.close()

    cod_cliente_entry.delete(0, tk.END)
    observacao_entry.delete(0, tk.END)

def deletar_entrega_aberto():
    selecionados = tab_entregas_em_aberto.selection()

    if not selecionados:
        messagebox.showwarning("Aviso", "Nenhuma entrega selecionada para deletar.")
        return

    resposta = messagebox.askyesno("Confirmação", "Tem certeza que deseja deletar a(s) entrega(s) selecionada(s)?")

    if resposta:
        conexao = sqlite3.connect('entregas.db')
        cursor = conexao.cursor()

        for item in selecionados:
            entrega_id = tab_entregas_em_aberto.item(item, "values")[0]
            cursor.execute("DELETE FROM entregas_aberto WHERE cod_entrega = ?", (entrega_id,))
            conexao.commit()

        conexao.close()

        exibir_dados()

def alterar_anotacao():
    selecionados = tab_entregas_em_aberto.selection()

    if not selecionados:
        messagebox.showwarning("Aviso", "Nenhuma entrega selecionada para alterar a anotação.")
        return

    if len(selecionados) > 1:
        messagebox.showwarning("Aviso", "Selecione apenas uma entrega para alterar a anotação.")
        return

    entrega_id = tab_entregas_em_aberto.item(selecionados[0], "values")[0]

    # Criar a nova janela (toplevel)
    global janela_alterar_anotacao
    janela_alterar_anotacao = tk.Toplevel(root)
    janela_alterar_anotacao.title("Alterar Anotação")
    janela_alterar_anotacao.geometry("400x150")

    # Widgets da nova janela
    label_nova_anotacao = tk.Label(janela_alterar_anotacao, text="Nova Anotação:")
    label_nova_anotacao.pack()

    nova_anotacao_entry = tk.Entry(janela_alterar_anotacao, width=50)
    nova_anotacao_entry.pack()

    btn_confirmar_alteracao = tk.Button(janela_alterar_anotacao, text="Confirmar Alteração",
                                        command=lambda: confirmar_alteracao(entrega_id, nova_anotacao_entry.get()))
    btn_confirmar_alteracao.pack()

def confirmar_alteracao(entrega_id, nova_anotacao):
    conexao = sqlite3.connect('entregas.db')
    cursor = conexao.cursor()

    try:
        cursor.execute("UPDATE entregas_aberto SET observação = ? WHERE cod_entrega = ?", (nova_anotacao, entrega_id))
        conexao.commit()
        messagebox.showinfo("Sucesso", "Anotação alterada com sucesso!")
        exibir_dados()
    except sqlite3.Error as e:
        messagebox.showerror("Erro", "Ocorreu um erro ao alterar a anotação:\n" + str(e))
    finally:
        conexao.close()

    # Fechar a janela de alteração
    janela_alterar_anotacao.destroy()

root = tk.Tk()
root.title("Tabela de Entregas em Aberto")
root.geometry("2000x1000")

tab_entregas_em_aberto = ttk.Treeview(root, height=10, columns=("col1", "col2", "col3", "col4", "col5"), selectmode="extended")
tab_entregas_em_aberto.heading("#0", text="")
tab_entregas_em_aberto.heading("#1", text="Cod. Entrega")
tab_entregas_em_aberto.heading("#2", text="Cod. Cliente")
tab_entregas_em_aberto.heading("#3", text="Cliente")
tab_entregas_em_aberto.heading("#4", text="Bairro")
tab_entregas_em_aberto.heading("#5", text="Observação")

tab_entregas_em_aberto.column("#0", width=0)
tab_entregas_em_aberto.column("#1", width=100)
tab_entregas_em_aberto.column("#2", width=100)
tab_entregas_em_aberto.column("#3", width=200)
tab_entregas_em_aberto.column("#4", width=150)
tab_entregas_em_aberto.column("#5", width=200)

tab_entregas_em_aberto.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.4)

entregadores_combobox = ttk.Combobox(root, values=[])
entregadores_combobox.place(x=750,y=25)
exibir_entregadores()

btn_atualizar = tk.Button(root, text="Atualizar Dados", command=exibir_dados)
btn_atualizar.place(x=500,y=25)

btn_transferir = tk.Button(root, text="Transferir para Rota", command=mover_para_rota)
btn_transferir.place(x=755,y=55)

# Adicionando widgets para adicionar entregas em aberto
label_cod_cliente = tk.Label(root, text="Código do Cliente:")
label_cod_cliente.place(x=20,y=20)

cod_cliente_entry = tk.Entry(root)
cod_cliente_entry.place(x=125,y=20)

label_observacao = tk.Label(root, text="Observação:")
label_observacao.place(x=20,y=45)

observacao_entry = tk.Entry(root,width=50)
observacao_entry.place(x=125,y=45)

btn_adicionar_entrega = tk.Button(root, text="Adicionar Entrega em Aberto", command=adicionar_entrega_aberto)
btn_adicionar_entrega.place(x=40, y= 70)

btn_deletar_entrega = tk.Button(root, text="Deletar Entrega", command=deletar_entrega_aberto,bg="red", fg="black")
btn_deletar_entrega.place(x=1200, y=25)

btn_alterar_anotacao = tk.Button(root, text="Alterar Anotação", command=alterar_anotacao)
btn_alterar_anotacao.place(x=40, y=110)

exibir_dados()

root.mainloop()
