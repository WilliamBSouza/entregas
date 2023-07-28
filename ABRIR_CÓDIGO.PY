from tkinter import *
from main import *
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import sqlite3
from tkcalendar import Calendar, DateEntry 


#criar a página da janela principal a partir deste código



def lista_selecao_entregador(event):
    
    if lista.curselection():  # Verifica se há alguma seleção
        index = lista.curselection()[0]
        item_selecionado = lista.get(index)
        return item_selecionado

    else:
        print("não tem nada selecionado")

def select_lista(tab_entregas_em_aberto, cursor, conexao,):
    tab_entregas_em_aberto.delete(*tab_entregas_em_aberto.get_children())

    
    entregador = lista.get(lista.curselection())  # Obtém o nome do entregador selecionado na lista

    # Utilizando parâmetros na consulta SQL
    cursor.execute("""
        SELECT cod_cliente, nome_cliente, bairro_cliente, data_entrega
        FROM entregas_aberto
                   
                   ;
    """, ( cod_cliente_entry))   #criar a entry para adicionar o cod do cliente ------------------------------------------------------------------------------------------------

#   -----------------linha 34 foi removido o código  WHERE cod_cliente = ?


    lista_entregas_aberto = cursor.fetchall()

    for row in lista_entregas_aberto:
        tab_entregas_em_aberto.insert("", tk.END, values=row) 

def janela_prncipal_parte_entregas_aberto():

    def on_pesquisar():  # adicionar a def para função adicionar entregas em aberto 
        # Chamar a função select_lista aqui para executar a pesquisa
        select_lista(tab_entregas_em_aberto, cursor, conexao, cod_cliente_entry)  #substituir o data entry poe cod_cliente_entry

    conexao = sqlite3.connect('entregas.db')
    cursor = conexao.cursor()
    cursor.execute('SELECT * FROM Entregadores')
    dados_do_banco = cursor.fetchall()
   
    root = tk.Tk()
    root.title("janela principal parte entregas em aberto")
    root.geometry("2000x1000")

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
    global cod_cliente_entry
    cod_cliente_entry = tk.Entry(root)
    cod_cliente_entry.place(x=150, y=1)

    btn_pesquisar = tk.Button(root, text="Pesquisar", command= on_pesquisar)
    btn_pesquisar.place(x=300, y=1 )  
    
    lista.bind('<<ListboxSelect>>', lista_selecao_entregador)

    tab_entregas_em_aberto = ttk.Treeview(root, height=3, columns=("col1", "col2", "col3", "col4", "col5", "col6", "col7","col8"))

    tab_entregas_em_aberto.heading("#0" , text="") #colocando os cabeçalhos das colunas
    tab_entregas_em_aberto.heading("#1" , text="Cod. Entrega") 
    tab_entregas_em_aberto.heading("#2" , text="Cod. cliente") 
    tab_entregas_em_aberto.heading("#3", text="Cliente")
    tab_entregas_em_aberto.heading("#4", text="Bairro")
    tab_entregas_em_aberto.heading("#5", text="Entregador")
    tab_entregas_em_aberto.heading("#6", text="Data Entrega")
    tab_entregas_em_aberto.heading("#7", text="Horário Saida")
    tab_entregas_em_aberto.heading("#8", text="Horário Chegada")

        #colocando o tamanho das colunas
    #o tamanho da coluna é dividida em 500 onde 50 seria 10% da tela
    tab_entregas_em_aberto.column("#0", width=0)
    tab_entregas_em_aberto.column("#1", width=80)
    tab_entregas_em_aberto.column("#2", width=30)
    tab_entregas_em_aberto.column("#3", width=150)
    tab_entregas_em_aberto.column("#4", width=90)
    tab_entregas_em_aberto.column("#5", width=90)
    tab_entregas_em_aberto.column("#6", width=50)
    tab_entregas_em_aberto.column("#7", width=50)
    tab_entregas_em_aberto.column("#8", width=50)
   
    tab_entregas_em_aberto.place(relx=0.11, rely=0.10 , relwidth=0.85, relheight=0.85)

    scrollista = Scrollbar(root, orient="vertical")
    tab_entregas_em_aberto.configure(yscroll=scrollista.set)
    scrollista.place(relx=0.96 , rely=0.1,relwidth=0.04, relheight=0.85)

    conexao = sqlite3.connect('entregas.db')
    cursor = conexao.cursor()

    #select_lista(tab_entregas_em_aberto, cursor, conexao,data_entry)  # Passa o tab_entregas, cursor e conexao como argumentos

   

    root.mainloop()
 


janela_prncipal_parte_entregas_aberto()


conexao.close()