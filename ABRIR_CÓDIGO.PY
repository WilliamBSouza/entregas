import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3

def exibir_dados():
    conexao = sqlite3.connect('entregas.db')
    cursor = conexao.cursor()

    # Execute a consulta para obter os dados da tabela "entregas_aberto"
    cursor.execute("""
    SELECT cod_entrega, cod_cliente, nome_cliente, bairro_cliente, observação
    FROM entregas_aberto 
    ORDER BY cod_entrega ASC;
    """,)
    dados_do_banco = cursor.fetchall()

    # Limpe a tabela antes de exibir os novos dados
    for row in tab_entregas_em_aberto.get_children():
        tab_entregas_em_aberto.delete(row)

    # Preencha a tabela com os novos dados
    for row in dados_do_banco:
        tab_entregas_em_aberto.insert("", tk.END, values=row)

    conexao.close()

def mover_para_rota():
    # Obtém as entregas selecionadas
    selecionados = tab_entregas_em_aberto.selection()

    if not selecionados:
        messagebox.showwarning("Aviso", "Nenhuma entrega selecionada.")
        return

    # Conecta-se ao banco de dados
    conexao = sqlite3.connect('entregas.db')
    cursor = conexao.cursor()

    # Move as entregas selecionadas para a tabela "entregas_rota"
    for item in selecionados:
        entrega_id = tab_entregas_em_aberto.item(item, "values")[0]
        cursor.execute("""
            INSERT INTO entregas_rota (cod_entrega, cod_cliente, nome_cliente, bairro_cliente, observacao)
            SELECT cod_entrega, cod_cliente, nome_cliente, bairro_cliente, observação
            FROM entregas_aberto
            WHERE cod_entrega = ?;
        """, (entrega_id,))
        cursor.execute("DELETE FROM entregas_aberto WHERE cod_entrega = ?", (entrega_id,))
        conexao.commit()

    conexao.close()

    # Atualiza a tabela após a transferência
    exibir_dados()

root = tk.Tk()
root.title("Tabela de Entregas em Aberto")
root.geometry("800x600")

tab_entregas_em_aberto = ttk.Treeview(root, height=10, columns=("col1", "col2", "col3", "col4", "col5"))
tab_entregas_em_aberto.heading("#0", text="")
tab_entregas_em_aberto.heading("#1", text="Cod. Entrega")
tab_entregas_em_aberto.heading("#2", text="Cod. Cliente")
tab_entregas_em_aberto.heading("#3", text="Cliente")
tab_entregas_em_aberto.heading("#4", text="Bairro")
tab_entregas_em_aberto.heading("#5", text="Observação")

tab_entregas_em_aberto.column("#0", width=1)
tab_entregas_em_aberto.column("#1", width=100)
tab_entregas_em_aberto.column("#2", width=100)
tab_entregas_em_aberto.column("#3", width=200)
tab_entregas_em_aberto.column("#4", width=150)
tab_entregas_em_aberto.column("#5", width=200)

tab_entregas_em_aberto.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.8)

btn_atualizar = tk.Button(root, text="Atualizar Dados", command=exibir_dados)
btn_atualizar.place(relx=0.2, rely=0.02)

btn_transferir = tk.Button(root, text="Transferir para Rota", command=mover_para_rota)
btn_transferir.place(relx=0.6, rely=0.02)

# Chame a função para exibir os dados inicialmente
exibir_dados()

root.mainloop()
