from tkinter import *
from funcoes import *
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import sqlite3
from tkcalendar import Calendar, DateEntry 

import tkinter as tk
from tkinter import ttk
import sqlite3

def Pesquisa_entregas_cliente():
    
    def selecionar_lista(tab_entregas, cursor, conexao, filtro_cliente):
        tab_entregas.delete(*tab_entregas.get_children())  # Limpa os dados existentes

        lista = cursor.execute("""
            SELECT cod_entrega, cod_cliente, nome_cliente, bairro, entregador, data_entrega, horário_saida, horário_chegada, observação
            FROM entregas_finalizadas
            WHERE cod_cliente LIKE ?
            ORDER BY data_entrega, horário_chegada ASC;
        """, ('%' + filtro_cliente + '%',)).fetchall()

        for row in lista:
            tab_entregas.insert("", tk.END, values=row)

    def selecionar_lista_filtro(tab_entregas, cursor, conexao, filtro_cliente):
        tab_entregas.delete(*tab_entregas.get_children())  # Limpa os dados existentes

        lista_filtro = cursor.execute("""
            SELECT cod_entrega, cod_cliente, nome_cliente, bairro, entregador, data_entrega, horário_saida, horário_chegada, observação
            FROM entregas_finalizadas
            WHERE nome_cliente LIKE ?
            ORDER BY data_entrega, horário_chegada ASC;
        """, ('%' + filtro_cliente + '%',)).fetchall()

        for row in lista_filtro:
            tab_entregas.insert("", tk.END, values=row)

    def filtrar_por_cliente():
        filtro_cliente = filtro_cliente_entry.get()
        selecionar_lista_filtro(tab_entregas, cursor, conexao, filtro_cliente)

    def limpar_filtro():
        filtro_cliente_entry.delete(0, tk.END)
        selecionar_lista(tab_entregas, cursor, conexao, "")

    root = tk.Tk()
    root.title("Pesquisa De Entregas Por Cliente E Todas Finalizadas")
    root.geometry("1200x500")

    conexao = sqlite3.connect('entregas.db')
    cursor = conexao.cursor()

    tab_entregas = ttk.Treeview(root, height=3, columns=("col1", "col2", "col3", "col4", "col5", "col6", "col7","col8","col9"))

    tab_entregas.heading("#0" , text="") #colocando os cabeçalhos das colunas
    tab_entregas.heading("#1" , text="Cod. Entrega") 
    tab_entregas.heading("#2" , text="Cod. cliente") 
    tab_entregas.heading("#3", text="Cliente")
    tab_entregas.heading("#4", text="Bairro")
    tab_entregas.heading("#5", text="Entregador")
    tab_entregas.heading("#6", text="Data Entrega")
    tab_entregas.heading("#7", text="Horário Saida")
    tab_entregas.heading("#8", text="Horário Chegada")
    tab_entregas.heading("#9", text="Observação")

    #colocando o tamanho das colunas
    tab_entregas.column("#0", width=0)
    tab_entregas.column("#1", width=100)
    tab_entregas.column("#2", width=50)
    tab_entregas.column("#3", width=200)
    tab_entregas.column("#4", width=125)
    tab_entregas.column("#5", width=100)
    tab_entregas.column("#6", width=50)
    tab_entregas.column("#7", width=50)
    tab_entregas.column("#8", width=50)
    tab_entregas.column("#9", width=100)
   
    tab_entregas.place(relx=0.01, rely=0.1 , relwidth=0.95, relheight=0.85)

    scrollista = tk.Scrollbar(root, orient="vertical")
    tab_entregas.configure(yscroll=scrollista.set)
    scrollista.place(relx=0.96 , rely=0.1, relwidth=0.04, relheight=0.85)

    filtro_cliente_label = tk.Label(root, text="Filtrar Nome do Cliente:")
    filtro_cliente_label.place(x=10, y=20) 

    filtro_cliente_entry = tk.Entry(root)
    filtro_cliente_entry.place(x=147, y=20)

    filtrar_btn = tk.Button(root, text="Filtrar", command=filtrar_por_cliente)
    filtrar_btn.place(x=280, y=15)

    limpar_filtro_btn = tk.Button(root, text="Limpar Filtro", command=limpar_filtro)
    limpar_filtro_btn.place(x=640, y=20)

    selecionar_lista(tab_entregas, cursor, conexao, " ")  # mostra todas as entregas finalizadas

    root.mainloop()

    conexao.close()



def lista_selecao_entregador(event):
    
    if lista.curselection():  # Verifica se há alguma seleção
        index = lista.curselection()[0]
        item_selecionado = lista.get(index)
        return item_selecionado

    else:
        print("não tem nada selecionado")

def select_lista(tab_pesquisa_data_entregador, cursor, conexao,data_entry):
    tab_pesquisa_data_entregador.delete(*tab_pesquisa_data_entregador.get_children())

    data = data_entry.get()  # Obtém a data digitada no Entry
    entregador = lista.get(lista.curselection())  # Obtém o nome do entregador selecionado na lista

    # Utilizando parâmetros na consulta SQL
    cursor.execute("""
        SELECT cod_entrega, cod_cliente, nome_cliente, bairro, entregador, data_entrega, horário_saida, horário_chegada, observação
        FROM entregas_finalizadas
        WHERE data_entrega = ? AND entregador = ?
        ORDER BY horário_chegada ASC;
    """, (data, entregador))

    lista_entregas = cursor.fetchall()

    for row in lista_entregas:
        tab_pesquisa_data_entregador.insert("", tk.END, values=row) 

def pesquisa_data_e_entregador_janela():

    def on_pesquisar():
        # Verifica se há alguma seleção na lista de entregadores
        if not lista.curselection():
            messagebox.showinfo("Aviso", "Selecione um entregador antes de pesquisar.")
            return

        # Chamar a função select_lista aqui para executar a pesquisa
        select_lista(tab_pesquisa_data_entregador, cursor, conexao, data_entry)

    conexao = sqlite3.connect('entregas.db')
    cursor = conexao.cursor()
    cursor.execute('SELECT * FROM Entregadores')
    dados_do_banco = cursor.fetchall()
    
    def run_interface_grafica_data_entregador():
        root = tk.Tk()
        root.title("Pesquisa Entregas Finalizadas Data E Entregador")
        root.geometry("1200x500")

        conexao = sqlite3.connect('entregas.db')
        cursor = conexao.cursor()

        # Criando uma lista com os nomes dos entregadores para exibir no Listbox
        cursor.execute('SELECT nome FROM Entregadores')
        dados_do_banco = cursor.fetchall()

        #adiciona lista selecionável
        global lista
        lista = tk.Listbox(root, selectmode=tk.SINGLE)
        lista.place(x=1, y= 1)

        for item in dados_do_banco:
            lista.insert(tk.END, item[0])
        
        # Adicionando um Entry para obter a data desejada
        global data_entry
        data_entry = DateEntry(root, date_pattern='yyyy-mm-dd')
        data_entry.place(x=150, y=1)

        btn_pesquisar = tk.Button(root, text="Pesquisar", command= on_pesquisar)
        btn_pesquisar.place(x=300, y=1 )  
        
        lista.bind('<<ListboxSelect>>', lista_selecao_entregador)
        global tab_pesquisa_data_entregador
        tab_pesquisa_data_entregador = ttk.Treeview(root, height=3, columns=("col1", "col2", "col3", "col4", "col5", "col6", "col7","col8","col9"))

        tab_pesquisa_data_entregador.heading("#0" , text="") #colocando os cabeçalhos das colunas
        tab_pesquisa_data_entregador.heading("#1" , text="Cod. Entrega") 
        tab_pesquisa_data_entregador.heading("#2" , text="Cod. cliente") 
        tab_pesquisa_data_entregador.heading("#3", text="Cliente")
        tab_pesquisa_data_entregador.heading("#4", text="Bairro")
        tab_pesquisa_data_entregador.heading("#5", text="Entregador")
        tab_pesquisa_data_entregador.heading("#6", text="Data Entrega")
        tab_pesquisa_data_entregador.heading("#7", text="Horário Saida")
        tab_pesquisa_data_entregador.heading("#8", text="Horário Chegada")
        tab_pesquisa_data_entregador.heading("#9", text="Observação")

            #colocando o tamanho das colunas
        #o tamanho da coluna é dividida em 500 onde 50 seria 10% da tela
        tab_pesquisa_data_entregador.column("#0", width=0)
        tab_pesquisa_data_entregador.column("#1", width=80)
        tab_pesquisa_data_entregador.column("#2", width=30)
        tab_pesquisa_data_entregador.column("#3", width=150)
        tab_pesquisa_data_entregador.column("#4", width=90)
        tab_pesquisa_data_entregador.column("#5", width=90)
        tab_pesquisa_data_entregador.column("#6", width=50)
        tab_pesquisa_data_entregador.column("#7", width=50)
        tab_pesquisa_data_entregador.column("#8", width=50)
        tab_pesquisa_data_entregador.column("#9", width=100)
    
        tab_pesquisa_data_entregador.place(relx=0.11, rely=0.10 , relwidth=0.85, relheight=0.85)

        scrollista = Scrollbar(root, orient="vertical")
        tab_pesquisa_data_entregador.configure(yscroll=scrollista.set)
        scrollista.place(relx=0.96 , rely=0.1,relwidth=0.04, relheight=0.85)

        conexao = sqlite3.connect('entregas.db')
        cursor = conexao.cursor()

        select_lista(tab_pesquisa_data_entregador, cursor, conexao,data_entry)  # Passa o tab_entregas, cursor e conexao como argumentos

        conexao.close()

        root.mainloop()
    if __name__ == "__main__":
        run_interface_grafica_data_entregador()

def selecct_lista_pesq_data(tab_pesquisa_data, cursor, conexao,data_entry):
    tab_pesquisa_data.delete(*tab_pesquisa_data.get_children())

    data = data_entry.get()  # Obtém a data digitada no Entry
   
    # Utilizando parâmetros na consulta SQL
    cursor.execute("""
    SELECT cod_entrega, cod_cliente, nome_cliente, bairro, entregador, data_entrega, horário_saida, horário_chegada,observação
    FROM entregas_finalizadas
    WHERE data_entrega = ? 
    ORDER BY horário_chegada ASC;
    """, (data,))

    lista_entregas = cursor.fetchall()

    for row in lista_entregas:
        tab_pesquisa_data.insert("", tk.END, values=row) 

def pesquisa_data_janela():

    def on_pesquisar():
        # Chamar a função selecct_lista_pesq_data aqui para executar a pesquisa
        selecct_lista_pesq_data(tab_pesquisa_data, cursor, conexao, data_entry)

    conexao = sqlite3.connect('entregas.db')
    cursor = conexao.cursor()
   
    root = tk.Tk()
    root.title("Pesquisa Entregas Finalizadas Por Data ")
    root.geometry("1200x500")

    conexao = sqlite3.connect('entregas.db')
    cursor = conexao.cursor()

    # Criando uma lista com os nomes dos entregadores para exibir no Listbox
    cursor.execute('SELECT nome FROM Entregadores')
    dados_do_banco = cursor.fetchall()
      
       # Adicionando um Entry para obter a data desejada
    global data_entry
    data_entry = DateEntry(root, date_pattern='yyyy-mm-dd')
    data_entry.place(x=400, y=5)

    btn_pesquisar = tk.Button(root, text="Pesquisar", command= on_pesquisar)
    btn_pesquisar.place(x=500, y=1 )  
    
    tab_pesquisa_data = ttk.Treeview(root, height=3, columns=("col1", "col2", "col3", "col4", "col5", "col6", "col7","col8","col9"))

    tab_pesquisa_data.heading("#0" , text="") #colocando os cabeçalhos das colunas
    tab_pesquisa_data.heading("#1" , text="Cod. Entrega") 
    tab_pesquisa_data.heading("#2" , text="Cod. cliente") 
    tab_pesquisa_data.heading("#3", text="Cliente")
    tab_pesquisa_data.heading("#4", text="Bairro")
    tab_pesquisa_data.heading("#5", text="Entregador")
    tab_pesquisa_data.heading("#6", text="Data Entrega")
    tab_pesquisa_data.heading("#7", text="Horário Saida")
    tab_pesquisa_data.heading("#8", text="Horário Chegada")
    tab_pesquisa_data.heading("#9", text="Observação")

        #colocando o tamanho das colunas
    #o tamanho da coluna é dividida em 500 onde 50 seria 10% da tela
    tab_pesquisa_data.column("#0", width=0)
    tab_pesquisa_data.column("#1", width=80)
    tab_pesquisa_data.column("#2", width=30)
    tab_pesquisa_data.column("#3", width=150)
    tab_pesquisa_data.column("#4", width=90)
    tab_pesquisa_data.column("#5", width=90)
    tab_pesquisa_data.column("#6", width=50)
    tab_pesquisa_data.column("#7", width=50)
    tab_pesquisa_data.column("#8", width=50)
    tab_pesquisa_data.column("#9", width=100)

    tab_pesquisa_data.place(relx=0.01, rely=0.10 , relwidth=0.95, relheight=0.85)

    scrollista = Scrollbar(root, orient="vertical")
    tab_pesquisa_data.configure(yscroll=scrollista.set)
    scrollista.place(relx=0.96 , rely=0.1,relwidth=0.04, relheight=0.85)

    selecct_lista_pesq_data(tab_pesquisa_data, cursor, conexao,data_entry)  # Passa o tab_entregas, cursor e conexao como argumentos

    root.mainloop()
    
    conexao.close()

def selecct_lista_pesq_hoje(tab_pesquisa_hoje, cursor, conexao,data_entry):
    tab_pesquisa_hoje.delete(*tab_pesquisa_hoje.get_children())

    data = data_entry.get()  # Obtém a data digitada no Entry
   
    # Utilizando parâmetros na consulta SQL
    cursor.execute("""
    SELECT cod_entrega, cod_cliente, nome_cliente, bairro, entregador, data_entrega, horário_saida, horário_chegada,observação
    FROM entregas_finalizadas
    WHERE data_entrega = ? 
    ORDER BY horário_chegada ASC;
    """, (data,))

    lista_entregas = cursor.fetchall()

    for row in lista_entregas:
        tab_pesquisa_hoje.insert("", tk.END, values=row) 

def pesquisa_hoje_janela():

    def on_pesquisar():
        # Chamar a função selecct_lista_pesq_hoje aqui para executar a pesquisa
        selecct_lista_pesq_hoje(tab_pesquisa_hoje, cursor, conexao, data_entry)

    conexao = sqlite3.connect('entregas.db')
    cursor = conexao.cursor()
   
    root = tk.Tk()
    root.title("Pesquisa Entregas Finalizadas De Hoje")
    root.geometry("1200x500")

    conexao = sqlite3.connect('entregas.db')
    cursor = conexao.cursor()

    # Criando uma lista com os nomes dos entregadores para exibir no Listbox
    cursor.execute('SELECT nome FROM Entregadores')
    dados_do_banco = cursor.fetchall()
      
       # Adicionando um Entry para obter a data desejada
    global data_entry
    data_entry = DateEntry(root, date_pattern='yyyy-mm-dd', date=datetime.date.today())
    data_entry.place(x=400, y=5)

    btn_pesquisar = tk.Button(root, text="Pesquisar", command= on_pesquisar)
    btn_pesquisar.place(x=500, y=1 )  
    
    tab_pesquisa_hoje = ttk.Treeview(root, height=3, columns=("col1", "col2", "col3", "col4", "col5", "col6", "col7","col8","col9"))

    tab_pesquisa_hoje.heading("#0" , text="") #colocando os cabeçalhos das colunas
    tab_pesquisa_hoje.heading("#1" , text="Cod. Entrega") 
    tab_pesquisa_hoje.heading("#2" , text="Cod. cliente") 
    tab_pesquisa_hoje.heading("#3", text="Cliente")
    tab_pesquisa_hoje.heading("#4", text="Bairro")
    tab_pesquisa_hoje.heading("#5", text="Entregador")
    tab_pesquisa_hoje.heading("#6", text="Data Entrega")
    tab_pesquisa_hoje.heading("#7", text="Horário Saida")
    tab_pesquisa_hoje.heading("#8", text="Horário Chegada")
    tab_pesquisa_hoje.heading("#9", text="Observação")

        #colocando o tamanho das colunas
    #o tamanho da coluna é dividida em 500 onde 50 seria 10% da tela
    tab_pesquisa_hoje.column("#0", width=0)
    tab_pesquisa_hoje.column("#1", width=80)
    tab_pesquisa_hoje.column("#2", width=30)
    tab_pesquisa_hoje.column("#3", width=150)
    tab_pesquisa_hoje.column("#4", width=90)
    tab_pesquisa_hoje.column("#5", width=90)
    tab_pesquisa_hoje.column("#6", width=50)
    tab_pesquisa_hoje.column("#7", width=50)
    tab_pesquisa_hoje.column("#8", width=50)
    tab_pesquisa_hoje.column("#9", width=100)

    tab_pesquisa_hoje.place(relx=0.01, rely=0.10 , relwidth=0.95, relheight=0.85)

    scrollista = Scrollbar(root, orient="vertical")
    tab_pesquisa_hoje.configure(yscroll=scrollista.set)
    scrollista.place(relx=0.96 , rely=0.1,relwidth=0.04, relheight=0.85)

    selecct_lista_pesq_hoje(tab_pesquisa_hoje, cursor, conexao,data_entry)  # Passa o tab_entregas, cursor e conexao como argumentos
    
    root.mainloop()
    conexao.close()

def select_Exibir_entregadores(tab_exibir_entregadores, cursor, conexao):
    tab_exibir_entregadores.delete(*tab_exibir_entregadores.get_children())
   
    # Utilizando parâmetros na consulta SQL
    cursor.execute("""
    SELECT cod, nome, telefone
    FROM entregadores 
    ORDER BY cod ASC;
    """,)

    lista_entregadores = cursor.fetchall()

    for row in lista_entregadores:
        tab_exibir_entregadores.insert("", tk.END, values=row)

def Exibir_entregadores_janela():

    root = tk.Tk()
    root.title("Exibir Entregadores")
    root.geometry("500x500")

    conexao = sqlite3.connect('entregas.db')
    cursor = conexao.cursor()

    tab_exibir_entregadores = ttk.Treeview(root, height=3, columns=("col1", "col2", "col3",))

    tab_exibir_entregadores.heading("#0" , text="") #colocando os cabeçalhos das colunas
    tab_exibir_entregadores.heading("#1" , text="Cod. Entregador") 
    tab_exibir_entregadores.heading("#2" , text="Nome") 
    tab_exibir_entregadores.heading("#3", text="Telefone")
    
        #colocando o tamanho das colunas
    #o tamanho da coluna é dividida em 500 onde 50 seria 10% da tela
    tab_exibir_entregadores.column("#0", width=0)
    tab_exibir_entregadores.column("#1", width=125)
    tab_exibir_entregadores.column("#2", width=150)
    tab_exibir_entregadores.column("#3", width=150)
    
    tab_exibir_entregadores.place(relx=0.01, rely=0.10 , relwidth=0.95, relheight=0.85)

    scrollista = Scrollbar(root, orient="vertical")
    tab_exibir_entregadores.configure(yscroll=scrollista.set)
    scrollista.place(relx=0.96 , rely=0.1,relwidth=0.04, relheight=0.85)

    select_Exibir_entregadores(tab_exibir_entregadores, cursor, conexao)

    root.mainloop()
    conexao.close()

def select_Exibir_clientes(tab_exibir_clientes, cursor, conexao):
    tab_exibir_clientes.delete(*tab_exibir_clientes.get_children())

    # Utilizando parâmetros na consulta SQL
    cursor.execute("""
    SELECT cod, nome, telefone, bairro
    FROM clientes 
    ORDER BY cod ASC;
    """,)

    lista_clientes = cursor.fetchall()

    for row in lista_clientes:
        tab_exibir_clientes.insert("", tk.END, values=row)

def exibir_clientes_janela():
    
    root = tk.Tk()
    root.title("Exibir Clientes")
    root.geometry("800x500")

    conexao = sqlite3.connect('entregas.db')
    cursor = conexao.cursor()

    tab_exibir_clientes = ttk.Treeview(root, height=3, columns=("col1", "col2", "col3","col4",))

    tab_exibir_clientes.heading("#0" , text="") #colocando os cabeçalhos das colunas
    tab_exibir_clientes.heading("#1" , text="Cod. Cliente") 
    tab_exibir_clientes.heading("#2" , text="Nome") 
    tab_exibir_clientes.heading("#3", text="Telefone")
    tab_exibir_clientes.heading("#4", text="Bairro")
    
        #colocando o tamanho das colunas
    #o tamanho da coluna é dividida em 500 onde 50 seria 10% da tela
    tab_exibir_clientes.column("#0", width=0)
    tab_exibir_clientes.column("#1", width=125)
    tab_exibir_clientes.column("#2", width=150)
    tab_exibir_clientes.column("#3", width=150)
    tab_exibir_clientes.column("#4", width=150)

    tab_exibir_clientes.place(relx=0.01, rely=0.10 , relwidth=0.95, relheight=0.85)

    scrollista = Scrollbar(root, orient="vertical")
    tab_exibir_clientes.configure(yscroll=scrollista.set)
    scrollista.place(relx=0.96 , rely=0.1,relwidth=0.04, relheight=0.85)

    select_Exibir_clientes(tab_exibir_clientes, cursor, conexao)

    root.mainloop()
    conexao.close()

# Função para adicionar um novo cliente ao banco de dados
def adicionar_cliente():
    cod = entry_cod.get()
    nome = entry_nome.get()
    telefone = entry_telefone.get()
    bairro = entry_bairro.get()

    if nome and telefone and bairro:
        conexao = sqlite3.connect('entregas.db')
        cursor = conexao.cursor()

        cursor.execute('INSERT INTO clientes (cod , nome, telefone, bairro) VALUES (?, ?, ?, ? ) ', ( cod, nome, telefone, bairro))
        conexao.commit()

        cursor.close()
        conexao.close()

        messagebox.showinfo("Sucesso", "Cliente adicionado com sucesso!")

        # Limpar os campos de entrada após a adição bem-sucedida
        entry_cod.delete(0, tk.END)
        entry_nome.delete(0, tk.END)
        entry_telefone.delete(0, tk.END)
        entry_bairro.delete(0, tk.END)

    else:
        messagebox.showwarning("Erro", "Por favor, preencha todos os campos.")

def janela_adicionar_cliente():
    root = tk.Tk()
    root.title("Adicionar Cliente")
    root.geometry("300x200")
    
    global entry_cod
    global entry_nome
    global entry_telefone
    global entry_bairro

    label_cod = tk.Label(root, text="Cod:")
    label_cod.place(x=10 , y= 10)
    entry_cod = tk.Entry(root)
    entry_cod.place(x=80 , y=10 )

    label_nome = tk.Label(root, text="Nome:")
    label_nome.place(x=10 ,y= 35)
    entry_nome = tk.Entry(root)
    entry_nome.place(x=80, y=35)

    label_telefone = tk.Label(root, text="Telefone:")
    label_telefone.place(x=10,y=60)
    entry_telefone = tk.Entry(root)
    entry_telefone.place(x=80,y=60)

    label_bairro = tk.Label(root, text="Bairro:")
    label_bairro.place(x=10,y=85)
    entry_bairro = tk.Entry(root)
    entry_bairro.place(x=80,y=85)

    btn_adicionar = tk.Button(root, text="Adicionar", command=adicionar_cliente)
    btn_adicionar.place(x= 100, y=120)

    root.mainloop()

def adicionar_entregador():
    cod = entry_cod.get()
    nome = entry_nome.get()
    telefone = entry_telefone.get()

    if nome and telefone and telefone:
        conexao = sqlite3.connect('entregas.db')
        cursor = conexao.cursor()

        cursor.execute('INSERT INTO entregadores (cod, nome, telefone) VALUES (?, ?, ?)', (cod, nome, telefone))
        conexao.commit()

        cursor.close()
        conexao.close()

        messagebox.showinfo("Sucesso", "Entregador adicionado com sucesso!")

        # Limpar os campos de entrada após a adição bem-sucedida
        entry_cod.delete(0, tk.END)
        entry_nome.delete(0, tk.END)
        entry_telefone.delete(0, tk.END)   

    else:
        messagebox.showwarning("Erro", "Por favor, preencha todos os campos.")

def janela_adicionar_entregador():
    root = tk.Tk()
    root.title("Adicionar Entregador")
    root.geometry("400x200")
    
    global entry_cod
    global entry_nome
    global entry_telefone

    label_cod = tk.Label(root, text="Cod:")
    label_cod.place(x=10 , y= 10)
    entry_cod = tk.Entry(root)
    entry_cod.place(x=80 , y=10 )

    label_nome = tk.Label(root, text="Nome:")
    label_nome.place(x=10 ,y= 35)
    entry_nome = tk.Entry(root)
    entry_nome.place(x=80, y=35)

    label_telefone = tk.Label(root, text="Telefone:")
    label_telefone.place(x=10,y=60)
    entry_telefone = tk.Entry(root)
    entry_telefone.place(x=80,y=60)

    btn_adicionar = tk.Button(root, text="Adicionar", command=adicionar_entregador)
    btn_adicionar.place(x= 100, y=120)

    root.mainloop()

def deletar_cliente():
    cod = entry_cod.get()

    if cod:
        resposta = messagebox.askquestion("Confirmação", "Tem certeza que deseja excluir o cliente? Esta ação não pode ser desfeita.")
        
        if resposta == 'yes':
            conexao = sqlite3.connect('entregas.db')
            cursor = conexao.cursor()

            cursor.execute('DELETE FROM clientes WHERE cod = ?', (cod,))
            conexao.commit()

            cursor.close()
            conexao.close()

            messagebox.showinfo("Sucesso", "Cliente excluído com sucesso!")

            # Limpar o campo de entrada após a exclusão bem-sucedida
            entry_cod.delete(0, tk.END)

    else:
        messagebox.showwarning("Erro", "Por favor, insira o código do cliente.")

def janela_deletar_cliente():
    root = tk.Tk()
    root.title("Deletar Cliente")
    root.geometry("300x100")
    
    label_cod = tk.Label(root, text="Código do Cliente:")
    label_cod.place(x=10, y=20)
    global entry_cod
    entry_cod = tk.Entry(root)
    entry_cod.place(x=120, y=20)

    btn_deletar = tk.Button(root, text="Deletar", command=deletar_cliente)
    btn_deletar.place(x=150, y=60)

    root.mainloop()

# Função para excluir um entregador do banco de dados
def deletar_entregador():
    cod = entry_cod.get()

    if cod:
        resposta = messagebox.askquestion("Confirmação", "Tem certeza que deseja excluir o entregador? Esta ação não pode ser desfeita.")
        
        if resposta == 'yes':
            conexao = sqlite3.connect('entregas.db')
            cursor = conexao.cursor()

            cursor.execute('DELETE FROM entregadores WHERE cod = ?', (cod,))
            conexao.commit()

            cursor.close()
            conexao.close()

            messagebox.showinfo("Sucesso", "Entregador excluído com sucesso!")

            # Limpar o campo de entrada após a exclusão bem-sucedida
            entry_cod.delete(0, tk.END)

    else:
        messagebox.showwarning("Erro", "Por favor, insira o código do entregador.")

def janela_deletar_entregador():
    root = tk.Tk()
    root.title("Deletar Entregador")
    root.geometry("300x100")
    
    label_cod = tk.Label(root, text="Código do Entregador:")
    label_cod.place(x=10, y=20)
    global entry_cod
    entry_cod = tk.Entry(root)
    entry_cod.place(x=135, y=20)

    btn_deletar = tk.Button(root, text="Deletar", command=deletar_entregador)
    btn_deletar.place(x=150, y=60)

    root.mainloop()

# Função para excluir uma entregas em aberto do banco de dados
def deletar_entrega_aberto():
    cod = entry_cod.get()

    if cod:
        resposta = messagebox.askquestion("Confirmação", "Tem certeza que deseja excluir a entrega em aberto? Esta ação não pode ser desfeita.")
        
        if resposta == 'yes':
            conexao = sqlite3.connect('entregas.db')
            cursor = conexao.cursor()

            cursor.execute('DELETE FROM entregas_aberto WHERE cod_entrega = ?', (cod,))
            conexao.commit()

            cursor.close()
            conexao.close()

            messagebox.showinfo("Sucesso", "Entrega em aberto excluída com sucesso!")

            # Limpar o campo de entrada após a exclusão bem-sucedida
            entry_cod.delete(0, tk.END)

    else:
        messagebox.showwarning("Erro", "Por favor, insira o código da entrega.")

def janela_deletar_entrega_em_aberto():
    root = tk.Tk()
    root.title("Deletar Entrega Em Aberto")
    root.geometry("300x100")
    
    label_cod = tk.Label(root, text="Código da entrega:")
    label_cod.place(x=10, y=20)
    global entry_cod
    entry_cod = tk.Entry(root)
    entry_cod.place(x=135, y=20)

    btn_deletar = tk.Button(root, text="Deletar", command=deletar_entrega_aberto)
    btn_deletar.place(x=150, y=60)

    root.mainloop()

# Função para excluir uma entregas em rota do banco de dados
def deletar_entrega_rota():
    cod = entry_cod.get()

    if cod:
        resposta = messagebox.askquestion("Confirmação", "Tem certeza que deseja excluir a entrega em rota? Esta ação não pode ser desfeita.")
        
        if resposta == 'yes':
            conexao = sqlite3.connect('entregas.db')
            cursor = conexao.cursor()

            cursor.execute('DELETE FROM entregas_rota WHERE cod_entrega = ?', (cod,))
            conexao.commit()

            cursor.close()
            conexao.close()

            messagebox.showinfo("Sucesso", "Entrega em rota excluída com sucesso!")

            # Limpar o campo de entrada após a exclusão bem-sucedida
            entry_cod.delete(0, tk.END)

    else:
        messagebox.showwarning("Erro", "Por favor, insira o código da entrega.")

def janela_deletar_entrega_em_rota():
    root = tk.Tk()
    root.title("Deletar Entrega Em Rota")
    root.geometry("300x100")
    
    label_cod = tk.Label(root, text="Código da entrega:")
    label_cod.place(x=10, y=20)
    global entry_cod
    entry_cod = tk.Entry(root)
    entry_cod.place(x=135, y=20)

    btn_deletar = tk.Button(root, text="Deletar", command=deletar_entrega_rota)
    btn_deletar.place(x=150, y=60)

    root.mainloop()

# Função para excluir uma entregas finalizadas do banco de dados
def deletar_entrega_finalizada():
    cod = entry_cod.get()

    if cod:
        resposta = messagebox.askquestion("Confirmação", "Tem certeza que deseja excluir a entrega finalizada? Esta ação não pode ser desfeita.")
        
        if resposta == 'yes':
            conexao = sqlite3.connect('entregas.db')
            cursor = conexao.cursor()

            cursor.execute('DELETE FROM entregas_finalizadas WHERE cod_entrega = ?', (cod,))
            conexao.commit()

            cursor.close()
            conexao.close()

            messagebox.showinfo("Sucesso", "Entrega finalizada excluída com sucesso!")

            # Limpar o campo de entrada após a exclusão bem-sucedida
            entry_cod.delete(0, tk.END)

    else:
        messagebox.showwarning("Erro", "Por favor, insira o código da entrega.")

def janela_deletar_entrega_finalizada():
    root = tk.Tk()
    root.title("Deletar Entrega Finalizada")
    root.geometry("300x100")
    
    label_cod = tk.Label(root, text="Código da entrega:")
    label_cod.place(x=10, y=20)
    global entry_cod
    entry_cod = tk.Entry(root)
    entry_cod.place(x=135, y=20)

    btn_deletar = tk.Button(root, text="Deletar", command=deletar_entrega_finalizada)
    btn_deletar.place(x=150, y=60)

    root.mainloop()

# Função para obter os dados do cliente a ser editado
def obter_dados_cliente():
    cod = entry_cod.get()

    if cod:
        conexao = sqlite3.connect('entregas.db')
        cursor = conexao.cursor()

        cursor.execute('SELECT nome, telefone, bairro FROM clientes WHERE cod = ?', (cod,))
        cliente = cursor.fetchone()

        if cliente:
            entry_nome.delete(0, tk.END)
            entry_telefone.delete(0, tk.END)
            entry_bairro.delete(0, tk.END)

            entry_nome.insert(0, cliente[0])
            entry_telefone.insert(0, cliente[1])
            entry_bairro.insert(0, cliente[2])
        else:
            messagebox.showwarning("Erro", "Cliente não encontrado.")

        cursor.close()
        conexao.close()
    else:
        messagebox.showwarning("Erro", "Por favor, insira o código do cliente.")

# Função para atualizar os dados do cliente no banco de dados
def atualizar_cliente():
    cod = entry_cod.get()
    nome = entry_nome.get()
    telefone = entry_telefone.get()
    bairro = entry_bairro.get()

    if cod and nome and telefone and bairro:
        conexao = sqlite3.connect('entregas.db')
        cursor = conexao.cursor()

        cursor.execute('UPDATE clientes SET nome = ?, telefone = ?, bairro = ? WHERE cod = ?', (nome, telefone, bairro, cod))
        conexao.commit()

        cursor.close()
        conexao.close()

        messagebox.showinfo("Sucesso", "Cliente atualizado com sucesso!")

        # Limpar os campos de entrada após a atualização bem-sucedida
        entry_cod.delete(0, tk.END)
        entry_nome.delete(0, tk.END)
        entry_telefone.delete(0, tk.END)
        entry_bairro.delete(0, tk.END)

    else:
        messagebox.showwarning("Erro", "Por favor, preencha todos os campos.")

def janela_editar_cliente():
    root = tk.Tk()
    root.title("Editar Cliente")
    root.geometry("350x200")
    
    label_cod = tk.Label(root, text="Código do Cliente:")
    label_cod.place(x=10, y=10)
    global entry_cod
    entry_cod = tk.Entry(root)
    entry_cod.place(x=120, y=10)

    btn_obter_dados = tk.Button(root, text="Obter Dados", command=obter_dados_cliente)
    btn_obter_dados.place(x=150, y=30)

    label_nome = tk.Label(root, text="Nome:")
    label_nome.place(x=10, y=70)
    global entry_nome
    entry_nome = tk.Entry(root)
    entry_nome.place(x=120, y=70)

    label_telefone = tk.Label(root, text="Telefone:")
    label_telefone.place(x=10, y=90)
    global entry_telefone
    entry_telefone = tk.Entry(root)
    entry_telefone.place(x=120, y=90)

    label_bairro = tk.Label(root, text="Bairro:")
    label_bairro.place(x=10, y=110)
    global entry_bairro
    entry_bairro = tk.Entry(root)
    entry_bairro.place(x=120, y=110)

    btn_atualizar = tk.Button(root, text="Atualizar", command=atualizar_cliente)
    btn_atualizar.place(x=160, y=130)

    root.mainloop()

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

def janela_principal():
    
    def sair():
        if messagebox.askokcancel("Sair", "Deseja realmente sair?"):
            root.quit()
    

    ############### INICIO JANELA PRINCIPAL    #############

    root = tk.Tk()
    root.title("Gerenciador De Entregas")
    root.geometry("1250x700")

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
        "Adicionar Cliente": janela_adicionar_cliente,
        "Adicionar Entregador": janela_adicionar_entregador,
        "-": None,  # Linha separadora
        "Sair": sair
    })

    menu_Deletar = criar_submenu(barra_menu, {
        "Deletar Cliente": janela_deletar_cliente,
        "Deletar Entregador": janela_deletar_entregador,
        "Deletar Entrega Em Aberto": janela_deletar_entrega_em_aberto,
        "Deletar Entrega Em Rota": janela_deletar_entrega_em_rota,
        "Deletar Entrega Finalizada": janela_deletar_entrega_finalizada
    })

    menu_exibir = criar_submenu(barra_menu, {
        "Exibir Clientes": exibir_clientes_janela,
        "Exibir Entregadores": Exibir_entregadores_janela
    })

    menu_editar = criar_submenu(barra_menu, {
        "Editar Clientes": janela_editar_cliente,
        "Editar Entregadores": janela_editar_entregadores
    })

    menu_pesquisa = criar_submenu(barra_menu, {
        "Pesquisa Entregas De Hoje": pesquisa_hoje_janela,
        "Pesquisa Entregas Por Data": pesquisa_data_janela,
        "Pesquisa Entregas Data E Entregador": pesquisa_data_e_entregador_janela,
        "Pesquisa Entregas Por Cliente E Todas Finalizadas": Pesquisa_entregas_cliente
    })

    # Adiciona os menus principais à barra de menu
    barra_menu.add_cascade(label="Adicionar", menu=menu_adicionar)
    barra_menu.add_cascade(label="Deletar", menu=menu_Deletar)
    barra_menu.add_cascade(label="Exibir", menu=menu_exibir)
    barra_menu.add_cascade(label="Editar", menu=menu_editar)
    barra_menu.add_cascade(label="Pesquisa", menu=menu_pesquisa)

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

        exibir_entregas_rota()
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
            #messagebox.showinfo("Sucesso", "Entrega adicionada com sucesso!")
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

    def alterar_observacao():
        selecionados = tab_entregas_em_aberto.selection()

        if not selecionados:
            messagebox.showwarning("Aviso", "Nenhuma entrega selecionada para alterar a observação.")
            return

        if len(selecionados) > 1:
            messagebox.showwarning("Aviso", "Selecione apenas uma entrega para alterar a observação.")
            return

        entrega_id = tab_entregas_em_aberto.item(selecionados[0], "values")[0]

        # Criar a nova janela (toplevel)
        global janela_alterar_observacao
        janela_alterar_observacao = tk.Toplevel(root)
        janela_alterar_observacao.title("Alterar observação")
        janela_alterar_observacao.geometry("400x150")

        # Widgets da nova janela
        label_nova_observacao = tk.Label(janela_alterar_observacao, text="Nova observação:")
        label_nova_observacao.pack()

        nova_observacao_entry = tk.Entry(janela_alterar_observacao, width=50)
        nova_observacao_entry.pack()

        btn_confirmar_alteracao = tk.Button(janela_alterar_observacao, text="Confirmar Alteração",
                                            command=lambda: confirmar_alteracao(entrega_id, nova_observacao_entry.get()))
        btn_confirmar_alteracao.pack()

    def confirmar_alteracao(entrega_id, nova_observacao):
        conexao = sqlite3.connect('entregas.db')
        cursor = conexao.cursor()

        try:
            cursor.execute("UPDATE entregas_aberto SET observação = ? WHERE cod_entrega = ?", (nova_observacao, entrega_id))
            conexao.commit()
            messagebox.showinfo("Sucesso", "observação alterada com sucesso!")
            exibir_dados()
        except sqlite3.Error as e:
            messagebox.showerror("Erro", "Ocorreu um erro ao alterar a observação:\n" + str(e))
        finally:
            conexao.close()

        # Fechar a janela de alteração
        janela_alterar_observacao.destroy()


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

    tab_entregas_em_aberto.place(relx=0.1, rely=0.15, relwidth=0.8, relheight=0.35)

    entregadores_combobox = ttk.Combobox(root, values=[])
    entregadores_combobox.place(relx=0.60, rely=0.01, relwidth=0.09, relheight= 0.035)
    exibir_entregadores()

    label_entregas_aberto = tk.Label(root, text="ENTREGAS EM ABERTO", fg="blue", font=("Arial", 16, "bold"))
    label_entregas_aberto.place(relx=0.37, rely=0.097, relwidth=0.20, relheight= 0.035)

    btn_atualizar = tk.Button(root, text="Atualizar Dados", command=exibir_dados)
    btn_atualizar.place(relx=0.40, rely=0.01, relwidth=0.09, relheight= 0.035)

    btn_transferir = tk.Button(root, text="Transferir para Rota", command=mover_para_rota)
    btn_transferir.place(relx=0.60, rely=0.05, relwidth=0.09, relheight= 0.035)

    # Adicionando widgets para adicionar entregas em aberto
    label_cod_cliente = tk.Label(root, text="Código do Cliente:")
    label_cod_cliente.place(relx=0.001, rely=0.01, relwidth=0.15, relheight= 0.035)

    cod_cliente_entry = tk.Entry(root)
    cod_cliente_entry.place(relx=0.12, rely=0.01, relwidth=0.08, relheight= 0.035)

    label_observacao = tk.Label(root, text="Observação:")
    label_observacao.place(relx=0.022, rely=0.05, relwidth=0.09, relheight= 0.035)

    observacao_entry = tk.Entry(root,width=50)
    observacao_entry.place(relx=0.12, rely=0.05, relwidth=0.20, relheight= 0.035)

    btn_adicionar_entrega = tk.Button(root, text="Adicionar Entrega em Aberto", command=adicionar_entrega_aberto)
    btn_adicionar_entrega.place(relx=0.12, rely=0.093, relwidth=0.14, relheight= 0.035)

    btn_deletar_entrega = tk.Button(root, text="Deletar Entrega", command=deletar_entrega_aberto,bg="red", fg="black")
    btn_deletar_entrega.place(relx=0.80, rely=0.05, relwidth=0.09, relheight= 0.035)

    btn_alterar_observacao = tk.Button(root, text="Alterar observação", command=alterar_observacao)
    btn_alterar_observacao.place(relx=0.4, rely=0.05,relwidth=0.09, relheight= 0.035)



    ######################## entregas em rota ###############################

    def exibir_dados_rota():
        conexao = sqlite3.connect('entregas.db')
        cursor = conexao.cursor()

        cursor.execute("""
        SELECT cod_entrega, cod_cliente, nome_cliente, bairro, observação, entregador, horário_saida
        FROM entregas_rota 
        ORDER BY cod_entrega ASC;
        """)
        dados_do_banco = cursor.fetchall()

        for row in tab_entregas_em_rota.get_children():
            tab_entregas_em_rota.delete(row)

        for row in dados_do_banco:
            tab_entregas_em_rota.insert("", tk.END, values=row)

        conexao.close()

    def alterar_observacao_rota():
        selecionados = tab_entregas_em_rota.selection()

        if not selecionados:
            messagebox.showwarning("Aviso", "Nenhuma entrega selecionada para alterar a observação.")
            return

        if len(selecionados) > 1:
            messagebox.showwarning("Aviso", "Selecione apenas uma entrega para alterar a observação.")
            return

        entrega_id = tab_entregas_em_rota.item(selecionados[0], "values")[0]

        # Criar a nova janela (toplevel)
        global janela_alterar_observacao
        janela_alterar_observacao = tk.Toplevel(root)
        janela_alterar_observacao.title("Alterar observação")
        janela_alterar_observacao.geometry("400x150")

        # Widgets da nova janela
        label_nova_observacao_rota = tk.Label(janela_alterar_observacao, text="Nova observação Em Rota:")
        label_nova_observacao_rota.pack()

        nova_observacao_entry = tk.Entry(janela_alterar_observacao, width=50)
        nova_observacao_entry.pack()

        btn_confirmar_alteracao_rota = tk.Button(janela_alterar_observacao, text="Confirmar Alteração",
                                            command=lambda: confirmar_alteracao_rota(entrega_id, nova_observacao_entry.get()))
        btn_confirmar_alteracao_rota.pack()

    def confirmar_alteracao_rota(entrega_id, nova_observacao):
        conexao = sqlite3.connect('entregas.db')
        cursor = conexao.cursor()

        try:
            cursor.execute("UPDATE entregas_rota SET observação = ? WHERE cod_entrega = ?", (nova_observacao, entrega_id))
            conexao.commit()
            messagebox.showinfo("Sucesso", "observação alterada com sucesso!")
            exibir_dados_rota()
        except sqlite3.Error as e:
            messagebox.showerror("Erro", "Ocorreu um erro ao alterar a observação:\n" + str(e))
        finally:
            conexao.close()

        # Fechar a janela de alteração
        janela_alterar_observacao.destroy()

    def exibir_entregadores_rota():
        conexao = sqlite3.connect('entregas.db')
        cursor = conexao.cursor()

        cursor.execute("""
        SELECT cod, telefone, nome
        FROM entregadores 
        ORDER BY cod ASC;
        """)
        dados_entregadores = cursor.fetchall()

        entregadores_rota_combobox['values'] = [nome for _, _, nome in dados_entregadores]

        conexao.close()

    def filtrar_entregas_rota():
        entregador_selecionado = entregadores_rota_combobox.get()

        if not entregador_selecionado:
            messagebox.showwarning("Aviso", "Selecione um entregador para filtrar as entregas.")
            return

        conexao = sqlite3.connect('entregas.db')
        cursor = conexao.cursor()

        cursor.execute("""
        SELECT cod_entrega, cod_cliente, nome_cliente, bairro, observação, entregador,horário_saida
        FROM entregas_rota
        WHERE entregador = ?;
        """, (entregador_selecionado,))

        dados_do_banco = cursor.fetchall()

        for row in tab_entregas_em_rota.get_children():
            tab_entregas_em_rota.delete(row)

        for row in dados_do_banco:
            tab_entregas_em_rota.insert("", tk.END, values=row)

        conexao.close()

    def exibir_entregas_rota():
        conexao = sqlite3.connect('entregas.db')
        cursor = conexao.cursor()

        cursor.execute("""
        SELECT cod_entrega, cod_cliente, nome_cliente, bairro, observação, entregador,horário_saida
        FROM entregas_rota
        ORDER BY horário_saida ASC;
        """)
        dados_do_banco = cursor.fetchall()

        for row in tab_entregas_em_rota.get_children():
            tab_entregas_em_rota.delete(row)

        for row in dados_do_banco:
            tab_entregas_em_rota.insert("", tk.END, values=row)

        conexao.close()

    def mover_para_finalizadas():
        selecionados = tab_entregas_em_rota.selection()

        if not selecionados:
            messagebox.showwarning("Aviso", "Nenhuma entrega selecionada.")
            return

        horario_chegada = datetime.datetime.now().strftime("%H:%M:%S")

        conexao = sqlite3.connect('entregas.db')
        cursor = conexao.cursor()

        for item in selecionados:
            entrega_id = tab_entregas_em_rota.item(item, "values")[0]
            #cursor.execute("UPDATE entregas_rota SET horário_chegada = ? WHERE cod_entrega = ?", (horario_chegada, entrega_id))
            cursor.execute("""INSERT INTO entregas_finalizadas( cod_entrega, cod_entregador , nome_cliente , bairro , telefone_entregador , entregador , data_entrega , horário_saida , horário_chegada , cod_cliente , observação )
                    SELECT cod_entrega, cod_entregador,nome_cliente,bairro, telefone_entregador, entregador,data_entrega, horário_saida, ? ,cod_cliente, observação
                    FROM entregas_rota WHERE cod_entrega = ?""", (horario_chegada, entrega_id))

            cursor.execute("DELETE FROM entregas_rota WHERE cod_entrega = ?", (entrega_id,))
            conexao.commit()

        conexao.close()

        exibir_entregas_rota()
        

    def deletar_entrega_rota():
        selecionados = tab_entregas_em_rota.selection()

        if not selecionados:
            messagebox.showwarning("Aviso", "Nenhuma entrega selecionada para deletar.")
            return

        resposta = messagebox.askyesno("Confirmação", "Tem certeza que deseja deletar a(s) entrega(s) selecionada(s)?")

        if resposta:
            conexao = sqlite3.connect('entregas.db')
            cursor = conexao.cursor()

            for item in selecionados:
                entrega_id = tab_entregas_em_rota.item(item, "values")[0]
                cursor.execute("DELETE FROM entregas_rota WHERE cod_entrega = ?", (entrega_id,))
                conexao.commit()

            conexao.close()

            exibir_entregas_rota()

    def limpar_filtro_entregas_rota():
        # Chamada para exibir todas as entregas em rota novamente
        exibir_entregas_rota()

    def alterar_entregador_rota():
        selecionados = tab_entregas_em_rota.selection()

        if not selecionados:
            messagebox.showwarning("Aviso", "Nenhuma entrega selecionada para alterar o entregador.")
            return

        if len(selecionados) > 1:
            messagebox.showwarning("Aviso", "Selecione apenas uma entrega para alterar o entregador.")
            return

        entrega_id = tab_entregas_em_rota.item(selecionados[0], "values")[0]

        # Criar a nova janela (toplevel)
        global janela_alterar_entregador
        janela_alterar_entregador = tk.Toplevel(root)
        janela_alterar_entregador.title("Alterar Entregador em Rota")
        janela_alterar_entregador.geometry("400x150")

        # Widgets da nova janela
        label_novo_entregador = tk.Label(janela_alterar_entregador, text="Novo Entregador:")
        label_novo_entregador.pack()

        novo_entregador_combobox = ttk.Combobox(janela_alterar_entregador, values=entregadores_rota_combobox['values'])
        novo_entregador_combobox.pack()

        btn_confirmar_alteracao_entregador = tk.Button(janela_alterar_entregador, text="Confirmar Alteração",
                                            command=lambda: confirmar_alteracao_entregador(entrega_id, novo_entregador_combobox.get()))
        btn_confirmar_alteracao_entregador.pack()

    def confirmar_alteracao_entregador(entrega_id, novo_entregador):
        conexao = sqlite3.connect('entregas.db')
        cursor = conexao.cursor()

        try:
            cursor.execute("UPDATE entregas_rota SET entregador = ? WHERE cod_entrega = ?", (novo_entregador, entrega_id))
            conexao.commit()
            messagebox.showinfo("Sucesso", "Entregador alterado com sucesso!")
            exibir_dados_rota()
        except sqlite3.Error as e:
            messagebox.showerror("Erro", "Ocorreu um erro ao alterar o entregador:\n" + str(e))
        finally:
            conexao.close()

        # Fechar a janela de alteração
        janela_alterar_entregador.destroy()

    tab_entregas_em_rota = ttk.Treeview(root, height=10, columns=("col1", "col2", "col3", "col4", "col5", "col6","col7"), selectmode="extended")
    tab_entregas_em_rota.heading("#0", text="")
    tab_entregas_em_rota.heading("#1", text="Cod. Entrega")
    tab_entregas_em_rota.heading("#2", text="Cod. Cliente")
    tab_entregas_em_rota.heading("#3", text="Cliente")
    tab_entregas_em_rota.heading("#4", text="Bairro")
    tab_entregas_em_rota.heading("#5", text="Observação")
    tab_entregas_em_rota.heading("#6", text="Entregador")
    tab_entregas_em_rota.heading("#7", text="Horário Saída")

    tab_entregas_em_rota.column("#0", width=0)
    tab_entregas_em_rota.column("#1", width=100)
    tab_entregas_em_rota.column("#2", width=100)
    tab_entregas_em_rota.column("#3", width=200)
    tab_entregas_em_rota.column("#4", width=150)
    tab_entregas_em_rota.column("#5", width=200)
    tab_entregas_em_rota.column("#6", width=100)
    tab_entregas_em_rota.column("#7", width=100)

    tab_entregas_em_rota.place(relx=0.1, rely=0.59, relwidth=0.8, relheight=0.35)

    btn_transferir_finalizadas = tk.Button(root, text="Transferir para Finalizadas", command=mover_para_finalizadas,bg="green",fg="white")
    btn_transferir_finalizadas.place(relx=0.60, rely=0.54, relwidth=0.12, relheight= 0.035)

    btn_deletar_rota = tk.Button(root, text="Deletar Entrega em Rota", command=deletar_entrega_rota, bg="red", fg="black")
    btn_deletar_rota.place(relx=0.80, rely=0.52, relwidth=0.12, relheight= 0.035)

    entregadores_rota_combobox = ttk.Combobox(root, values=[])
    entregadores_rota_combobox.place(relx=0.105, rely=0.505, relwidth=0.09, relheight= 0.03)
    exibir_entregadores_rota()

    btn_alterar_observacao_rota = tk.Button(root, text="Alterar observação Em Rota", command=alterar_observacao_rota)
    btn_alterar_observacao_rota.place(relx=0.26, rely=0.545, relwidth=0.12, relheight= 0.035)

    btn_filtrar_rota = tk.Button(root, text="Filtrar por Entregador", command=filtrar_entregas_rota)
    btn_filtrar_rota.place(relx=0.20, rely=0.505, relwidth=0.10, relheight= 0.035)

    # Botão para limpar o filtro
    btn_limpar_filtro = tk.Button(root, text="Limpar Filtro", command=limpar_filtro_entregas_rota)
    btn_limpar_filtro.place(relx=0.31, rely=0.505, relwidth=0.07, relheight= 0.035)

    label_entregas_aberto = tk.Label(root, text="ENTREGAS EM ROTA", fg="blue", font=("Arial", 16, "bold"))
    label_entregas_aberto.place(relx=0.38, rely=0.54, relwidth=0.20, relheight= 0.035)

    # Botão para alterar entregador em rota
    btn_alterar_entregador_rota = tk.Button(root, text="Alterar Entregador Em Rota", command=alterar_entregador_rota)
    btn_alterar_entregador_rota.place(relx=0.105, rely=0.545, relwidth=0.15, relheight= 0.035)



    exibir_entregas_rota()
    exibir_dados()

    conexao.close()

    root.mainloop()

janela_principal()