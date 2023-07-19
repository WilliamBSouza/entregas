from tkinter import *
from tkinter import Tk
from main import *
#cores

cor0 = "#f0f3f5"  # Preta / black
cor1 = "#feffff"  # branca / white
cor2 = "#3fb5a3"  # verde / green
cor3 = "#38576b"  # valor / value
cor4 = "#403d3d"   # letra / letters


def adicionar_cliente():
    janela = Tk()
    janela.title("Adicionar Cliente")
    janela.geometry ("300x350")
    
    janela.mainloop()

def menu_adicionar():
    janela = Tk()
    janela.title("Menu Adicionar")
    janela.geometry ("300x350")

    botão_Adicionar_cliente = Button(janela,text= "Adicionar Cliente",command=adicionar_cliente,width= 39, height=2,font=("Arial 8 bold"),bg=cor2, fg=cor1,relief=RAISED, overrelief=RIDGE)
    botão_Adicionar_cliente.place(x=5, y=10) 

    janela.mainloop()

def menu_deletar():
    janela = Tk()
    janela.title("Menu Deletar")
    janela.geometry ("300x350")
 

    janela.mainloop()

def menu_exibir():
    janela = Tk()
    janela.title("Menu Exibir")
    janela.geometry ("300x350")
 
    janela.mainloop()

def menu_pesquisar():
    janela = Tk()
    janela.title("Menu Pesquisar")
    janela.geometry ("300x350")
 

    janela.mainloop()

def menu():
    
    janela = Tk()
    janela.title("Menu")
    janela.geometry("310x200")
    janela.configure(background=cor1)

    botão_Adicionar = Button(janela,text= "Menu Adicionar",command=menu_adicionar,width= 39, height=2,font=("Arial 8 bold"),bg=cor2, fg=cor1,relief=RAISED, overrelief=RIDGE)
    botão_Adicionar.place(x=5, y=10) 
    botão_Deletar = Button(janela,text= "Menu Deletar",command=menu_deletar,width= 39, height=2,font=("Arial 8 bold"),bg=cor2, fg=cor1,relief=RAISED, overrelief=RIDGE)
    botão_Deletar.place(x=5, y=60) 
    botão_Exibir = Button(janela,text= "Menu Exibir",command=menu_exibir,width= 39, height=2,font=("Arial 8 bold"),bg=cor2, fg=cor1,relief=RAISED, overrelief=RIDGE)
    botão_Exibir.place(x=5, y=110) 
    botão_Pesquisar = Button(janela,text= "Menu Pesquisar",command=menu_pesquisar,width= 39, height=2,font=("Arial 8 bold"),bg=cor2, fg=cor1,relief=RAISED, overrelief=RIDGE)
    botão_Pesquisar.place(x=5, y=160)

    janela.mainloop()


menu()