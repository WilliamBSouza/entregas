import sqlite3
import os

def limpa_terminal():
    if os.name == 'nt':
        os.system('cls')

    else:
        os.system('clear')

conexao = sqlite3.connect('entregas.db')
cursor = conexao.cursor()

# Cria a tabela
#cursor.execute('CREATE TABLE clientes (cod INT PEIMARY KEY, nome VARCHAR(45), telefone VARCHAR(20), bairro VARCHAR(40))')
#cursor.execute('CREATE TABLE entregadores (cod INT PEIMARY KEY, nome VARCHAR(45), telefone VARCHAR(20))')

def add_clientes():

    #limpa o terminal
    limpa_terminal()
    print("-" * 50)
    codigo_cliente = input("Digite o código do cliente: ")
    nome = input("Digite o nome do cliente: ")
    telefone = input("Digite o telefone do cliente: ")
    bairro = (input("Digite o bairro do cliente: "))
   

    cursor.execute('INSERT INTO clientes VALUES(?,?,?,?)', (codigo_cliente, nome, telefone, bairro))

    # Confirma as alterações
    conexao.commit()

    print("Cliente adicionado com sucesso!")
    print("-" * 50)

def add_entregadores():

    #limpa o terminal
    limpa_terminal()
    print("-" * 50)
    codigo_entregador = input("Digite o código do entregador: ")
    nome = input("Digite a nome do entregador: ")
    telefone = input("Digite o telefone do entregador: ")
    

    cursor.execute('INSERT INTO entregadores VALUES(?,?,?)', (codigo_entregador, nome, telefone))

    # Confirma as alterações
    conexao.commit()

    print("Entregador adicionado com sucesso!")
    print("-" * 50)

def exibir_clientes():
    
    #limpa o terminal
    limpa_terminal()
    print("ID,Nome,telefone,bairro")
    print("*" * 50)
    # Executa a consulta SELECT em ordem crescente por id ORDER BY
    cursor.execute('SELECT * FROM clientes ORDER BY cod ASC')

    # Recupera todos os registros
    registros = cursor.fetchall()

    # Exibe os registros
    for registro in registros:
        print(registro)
    
    print("*" * 50)

def exibir_entregadores():
    
    #limpa o terminal
    limpa_terminal()
    print("ID,Nome,telefone")
    print("*" * 50)
    # Executa a consulta SELECT em ordem crescente por id ORDER BY
    cursor.execute('SELECT * FROM entregadores ORDER BY cod ASC')

    # Recupera todos os registros
    registros = cursor.fetchall()

    # Exibe os registros
    for registro in registros:
        print(registro)
    
    print("*" * 50)

def delete_entregador(cod):
    # Limpa o terminal
    limpa_terminal()

    print("-" * 50)

    conexao = sqlite3.connect('entregas.db')
    cursor = conexao.cursor()

    # Verifica se o ID existe na tabela
    cursor.execute('SELECT cod FROM entregadores WHERE cod = ?', (cod,))
    result = cursor.fetchone()

    if result is None:
        # ID não encontrado
        print("O entregador com o código fornecido não existe.")
    else:
        # Executa a instrução DELETE
        cursor.execute('DELETE FROM entregadores WHERE cod = ?', (cod,))

        # Confirma as alterações
        conexao.commit()

        print("entregador deletado com sucesso.")

    # Fecha a conexão
    conexao.close()

def delete_cliente(cod):
    # Limpa o terminal
    limpa_terminal()

    print("-" * 50)

    conexao = sqlite3.connect('entregas.db')
    cursor = conexao.cursor()

    # Verifica se o ID existe na tabela
    cursor.execute('SELECT cod FROM clientes WHERE cod = ?', (cod,))
    result = cursor.fetchone()

    if result is None:
        # ID não encontrado
        print("O cliente com o código fornecido não existe.")
    else:
        # Executa a instrução DELETE
        cursor.execute('DELETE FROM clientes WHERE cod = ?', (cod,))

        # Confirma as alterações
        conexao.commit()

        print("cliente deletado com sucesso.")

    # Fecha a conexão
    conexao.close()


while True:
    selecao = input(""" Opções:
                    [1] Adicionar Cliente
                    [2] Adicionar Entregador
                    [3] Exibir Clientes
                    [4] Exibir Entregadores
                    [5] Deletar Cliente
                    [6] Deletar Entregador
                    [7] Sair
                    digite a opção: """)
    if selecao == "1":
        add_clientes()

    if selecao =="2":
        add_entregadores()
    
    if selecao == "3":
        exibir_clientes()
    
    if selecao == "4":
        exibir_entregadores()
    
    if selecao == "5":
        id_cliente_a_deletar = input("Digite o código do cliente a ser deletado: ")
        delete_cliente(id_cliente_a_deletar)

    if selecao == "6":
        id_entregador_a_deletar = input("Digite o código do entregador a ser deletado: ")
        delete_entregador(id_entregador_a_deletar)
    
    elif selecao == "7":
        break


# Fecha a conexão
conexao.close()