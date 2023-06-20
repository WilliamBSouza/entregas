from tkinter import *
import sqlite3

lime = "#00FF00"
alice_blue = "#F0F8FF"
MediumSpringGreen = "#00FA9A"
Branco = '#FFFFFF'
preto = '#000000'
azul_fundo = "#1e3743"
corborda = "#759fe6"
corfundoframe = "#dfe3ee"
corbotão = "#187db2"

janela = Tk()
janela.geometry("1200x900")
janela.title('Pedidos')


def conecta_bd_clientes():
    conn = sqlite3.connect("clientes.bd")
    cursor = conn.cursor()
    return conn, cursor


def conecta_bd_entregadores():
    conn = sqlite3.connect("entregadores.bd")
    cursor = conn.cursor()
    return conn, cursor


def desconectar_bd(conn):
    conn.close()
    print("Desconectando banco de dados")


def monta_tabelas():
    conn_clientes, cursor_clientes = conecta_bd_clientes()
    conn_entregadores, cursor_entregadores = conecta_bd_entregadores()

    # Criar tabela clientes
    cursor_clientes.execute("""
    CREATE TABLE IF NOT EXISTS clientes(
        cod INTEGER PRIMARY KEY,
        nome_cliente CHAR(40) NOT NULL,
        telefone INTEGER(20),
        cidade CHAR(40)
    );""")
    conn_clientes.commit()
    print("BANCO DE DADOS CLIENTES CRIADO")

    # Criar tabela entregadores
    cursor_entregadores.execute("""
    CREATE TABLE IF NOT EXISTS entregadores(
        cod INTEGER PRIMARY KEY,
        nome_entregador CHAR(40) NOT NULL
    );""")
    conn_entregadores.commit()
    print("BANCO DE DADOS ENTREGADORES CRIADO")

    desconectar_bd(conn_clientes)
    desconectar_bd(conn_entregadores)

def adicionar_cliente(nome, telefone, cidade):
    conn, cursor = conecta_bd_clientes()

    try:
        # Executar a inserção dos dados do cliente
        cursor.execute("INSERT INTO clientes (nome_cliente, telefone, cidade) VALUES (?, ?, ?)",
                       (nome, telefone, cidade))
        conn.commit()
        print("Cliente adicionado ao banco de dados com sucesso!")
        return True
    except Exception as e:
        print("Erro ao adicionar cliente:", e)
        return False
    finally:
        desconectar_bd(conn)


#resultado = adicionar_cliente("William ", "11931075977", "São Paulo")
#if resultado:
    print("Cliente adicionado com sucesso!")
#else:
    print("Falha ao adicionar cliente.")


def exibir_clientes():
    conn, cursor = conecta_bd_clientes()

    # Executar a consulta para obter os clientes cadastrados
    cursor.execute("SELECT * FROM clientes")
    clientes = cursor.fetchall()

    # Exibir os clientes
    if clientes:
        for cliente in clientes:
            print("Código:", cliente[0])
            print("Nome:", cliente[1])
            print("Telefone:", cliente[2])
            print("Cidade:", cliente[3])
            print("--------------------")
    else:
        print("Não há clientes cadastrados.")

    desconectar_bd(conn)

def excluir_cliente(codigo):
    conn, cursor = conecta_bd_clientes()

    # Executar a exclusão do cliente com o código especificado
    cursor.execute("DELETE FROM clientes WHERE cod = ?", (codigo,))
    conn.commit()

    if cursor.rowcount > 0:
        print("Cliente excluído com sucesso!")
    else:
        print("Cliente não encontrado.")

    desconectar_bd(conn)


excluir_cliente()#colocar nos parenteses o codigo que seseja excluir 

exibir_clientes()
monta_tabelas()
janela.mainloop()
