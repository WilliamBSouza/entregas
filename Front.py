from tkinter import *
from main import *
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import sqlite3
#cores

cor0 = "#f0f3f5"  # Preta / black
cor1 = "#feffff"  # branca / white
cor2 = "#3fb5a3"  # verde / green
cor3 = "#38576b"  # valor / value
cor4 = "#403d3d"   # letra / letters



def todas_entregas_finalizadas():
    
 #   def ondoubleclick( event):      mexer mais a frente com este código 
 #       tab_entregas.selection()
        
    def selecionar_lista(tab_entregas, cursor, conexao):  
        for item in tab_entregas.get_children()[1:]:
            tab_entregas.delete(item)

        lista = cursor.execute("""SELECT cod_entrega, cod_cliente, nome_cliente, bairro, entregador, data_entrega, horário_saida, horário_chegada 
                               FROM entregas_finalizadas 
                               ORDER BY data_entrega ASC; """)

        for row in lista:
            tab_entregas.insert("", tk.END, values=(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]))

           
    
    root = tk.Tk()
    root.title("Todas Entregas Finalizadas")
    root.geometry("1000x500")


    tab_entregas = ttk.Treeview(root, height=3, columns=("col1", "col2", "col3", "col4", "col5", "col6", "col7","col8"))

    tab_entregas.heading("#0" , text="") #colocando os cabeçalhos das colunas
    tab_entregas.heading("#1" , text="Cod. Entrega") 
    tab_entregas.heading("#2" , text="Cod. cliente") 
    tab_entregas.heading("#3", text="Cliente")
    tab_entregas.heading("#4", text="Bairro")
    tab_entregas.heading("#5", text="Entregador")
    tab_entregas.heading("#6", text="Data Entrega")
    tab_entregas.heading("#7", text="Horário Saida")
    tab_entregas.heading("#8", text="Horário Chegada")

        #colocando o tamanho das colunas
    #o tamanho da coluna é dividida em 500 onde 50 seria 10% da tela
    tab_entregas.column("#0", width=0)
    tab_entregas.column("#1", width=100)
    tab_entregas.column("#2", width=50)
    tab_entregas.column("#3", width=200)
    tab_entregas.column("#4", width=125)
    tab_entregas.column("#5", width=100)
    tab_entregas.column("#6", width=50)
    tab_entregas.column("#7", width=50)
    tab_entregas.column("#8", width=50)
   

    tab_entregas.place(relx=0.01, rely=0.1 , relwidth=0.95, relheight=0.85)

    scrollista = Scrollbar(root, orient="vertical")
    tab_entregas.configure(yscroll=scrollista.set)
    scrollista.place(relx=0.96 , rely=0.1,relwidth=0.04, relheight=0.85)

    conexao = sqlite3.connect('entregas.db')
    cursor = conexao.cursor()

    selecionar_lista(tab_entregas, cursor, conexao)  # Passa o tab_entregas, cursor e conexao como argumentos

    conexao.close()

    root.mainloop()

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
        SELECT cod_entrega, cod_cliente, nome_cliente, bairro, entregador, data_entrega, horário_saida, horário_chegada
        FROM entregas_finalizadas
        WHERE data_entrega = ? AND entregador = ?
        ORDER BY horário_chegada ASC;
    """, (data, entregador))

    lista_entregas = cursor.fetchall()

    for row in lista_entregas:
        tab_pesquisa_data_entregador.insert("", tk.END, values=row) 

def pesquisa_data_e_entregador_janela():

    #CRIANDO A LISTA PARA SELECIONAR ENTREGADORES 

    conexao = sqlite3.connect('entregas.db')
    cursor = conexao.cursor()
    cursor.execute('SELECT * FROM Entregadores')
    dados_do_banco = cursor.fetchall()
   
    root = tk.Tk()
    root.title("Pesquisa Entregas Finalizadas Data Entregador")
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
    data_entry = tk.Entry(root)
    data_entry.place(x=150, y=1)

    btn_pesquisar = tk.Button(root, text="Pesquisar", command=lambda: select_lista(tab_pesquisa_data_entregador, cursor, conexao,data_entry))
    btn_pesquisar.place(x=300, y=1 )  
    
    lista.bind('<<ListboxSelect>>', lista_selecao_entregador)

    tab_pesquisa_data_entregador = ttk.Treeview(root, height=3, columns=("col1", "col2", "col3", "col4", "col5", "col6", "col7","col8"))

    tab_pesquisa_data_entregador.heading("#0" , text="") #colocando os cabeçalhos das colunas
    tab_pesquisa_data_entregador.heading("#1" , text="Cod. Entrega") 
    tab_pesquisa_data_entregador.heading("#2" , text="Cod. cliente") 
    tab_pesquisa_data_entregador.heading("#3", text="Cliente")
    tab_pesquisa_data_entregador.heading("#4", text="Bairro")
    tab_pesquisa_data_entregador.heading("#5", text="Entregador")
    tab_pesquisa_data_entregador.heading("#6", text="Data Entrega")
    tab_pesquisa_data_entregador.heading("#7", text="Horário Saida")
    tab_pesquisa_data_entregador.heading("#8", text="Horário Chegada")

        #colocando o tamanho das colunas
    #o tamanho da coluna é dividida em 500 onde 50 seria 10% da tela
    tab_pesquisa_data_entregador.column("#0", width=0)
    tab_pesquisa_data_entregador.column("#1", width=100)
    tab_pesquisa_data_entregador.column("#2", width=50)
    tab_pesquisa_data_entregador.column("#3", width=200)
    tab_pesquisa_data_entregador.column("#4", width=125)
    tab_pesquisa_data_entregador.column("#5", width=100)
    tab_pesquisa_data_entregador.column("#6", width=50)
    tab_pesquisa_data_entregador.column("#7", width=50)
    tab_pesquisa_data_entregador.column("#8", width=50)
   

    tab_pesquisa_data_entregador.place(relx=0.01, rely=0.1 , relwidth=0.95, relheight=0.85)

    scrollista = Scrollbar(root, orient="vertical")
    tab_pesquisa_data_entregador.configure(yscroll=scrollista.set)
    scrollista.place(relx=0.96 , rely=0.1,relwidth=0.04, relheight=0.85)

    conexao = sqlite3.connect('entregas.db')
    cursor = conexao.cursor()

    select_lista(tab_pesquisa_data_entregador, cursor, conexao,data_entry)  # Passa o tab_entregas, cursor e conexao como argumentos

    conexao.close()

    root.mainloop()

def pesquisa_data_e_entregador():
    entregador_pesquisa = input("digite o código do entregador que deseja pesquisar: ")
    data_pesquisa1 = input("Digite a data que deseja pesquisar (AAAA-MM-DD): ")
            
    try:
        pesquisa_data_entregador(entregador_pesquisa, data_pesquisa1)
       
    except Exception as e:
        print(f"Ocorreu um erro na pesquisa: {e}")

def pesquisa_Finalizadas_data ():
    data_pesquisa = input("Digite a data que deseja pesquisar (AAAA-MM-DD): ")
    pesquisa_por_data(data_pesquisa)

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
    "Pesquisa Entregas Por Data": pesquisa_Finalizadas_data,
    "Pesquisa Entregas Data E Entregador": pesquisa_data_e_entregador_janela,
    "Todas Entregas Finalizadas": todas_entregas_finalizadas

})


# Adiciona os menus principais à barra de menu
barra_menu.add_cascade(label="Adicionar", menu=menu_adicionar)
barra_menu.add_cascade(label="Deletar", menu=menu_Deletar)
barra_menu.add_cascade(label="Exibir", menu=menu_exibir)
barra_menu.add_cascade(label="Editar", menu=menu_editar)
barra_menu.add_cascade(label="Pesquisa", menu=menu_pesquisa)

conexao.close()

root.mainloop()

