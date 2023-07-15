import sqlite3
import os
from datetime import date
from datetime import datetime

def obter_horario_atual():
    horario_atual = datetime.now().strftime("%H:%M:%S")
    return horario_atual

def obter_data_atual():
    data_atual = date.today()
    return data_atual

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
#cursor.execute('CREATE TABLE entregas_aberto (cod_cliente INT, nome_cliente VARCHAR(45), bairro_cliente VARCHAR(40))')
#cursor.execute('CREATE TABLE entregas_rota (cod_entrega INT PRIMARY KEY, cod_entregador INT, nome_cliente , bairro , telefone_entregador)')
#cursor.execute('ALTER TABLE entregas_rota ADD COLUMN Entregador VARCHAR(45)')
#cursor.execute('ALTER TABLE entregas_rota ADD COLUMN data_entrega DATE')
#cursor.execute('ALTER TABLE entregas_rota ADD COLUMN horário_saida VARCHAR(10) ')
#cursor.execute('CREATE TABLE entregas_finalizadas (cod_entrega INT PRIMARY KEY, cod_entregador INT, nome_cliente , bairro , telefone_entregador, Entregador, data_entrega, horário_saida, horário_chegada)')


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

def add_entregas_aberto():
    limpa_terminal()
    print("-" * 50)
    codigo_cliente = input("Digite o código do cliente: ")

    # Verifica se o cliente existe na tabela clientes
    cursor.execute('SELECT cod FROM clientes WHERE cod = ?', (codigo_cliente,))
    result = cursor.fetchone()

    if result is None:
        # Cliente não encontrado
        print("O cliente com o código fornecido não existe.")
    else:
        # Recupera as informações do cliente
        cursor.execute('SELECT nome, bairro FROM clientes WHERE cod = ?', (codigo_cliente,))
        cliente_info = cursor.fetchone()

        # Insere a entrega em aberto com as informações do cliente
        cursor.execute('INSERT INTO entregas_aberto VALUES(?,?,?)', (codigo_cliente, cliente_info[0], cliente_info[1]))

        # Confirma as alterações
        conexao.commit()

        print("Entrega em aberto adicionada com sucesso!")
    
    print("-" * 50)


def exibir_entregas_aberto():
    limpa_terminal()
    print("Entregas em Aberto:")
    print("*" * 50)
    cursor.execute('SELECT * FROM entregas_aberto ORDER BY cod_cliente ASC')
    registros = cursor.fetchall()
    for registro in registros:
        print(registro)
    print("*" * 50)

def exibir_entregas_rota():
    limpa_terminal()
    print("Entregas em rota:")
    print("*" * 50)
    cursor.execute('SELECT * FROM entregas_rota ORDER BY cod_entrega ASC')
    registros = cursor.fetchall()

    for registro in registros:
        print(registro)
    print("*" * 50)
    
def adicionar_entregador_rota(cod_cliente, cod_entregador):
    # Verifica se o cliente em entregas_aberto existe
    cursor.execute('SELECT cod_cliente FROM entregas_aberto WHERE cod_cliente = ?', (cod_cliente,))
    result_cliente = cursor.fetchone()

    # Verifica se o entregador existe
    cursor.execute('SELECT cod FROM entregadores WHERE cod = ?', (cod_entregador,))
    result_entregador = cursor.fetchone()

    if result_cliente is None:
        # Cliente em entregas_aberto não encontrado
        print("O cliente não está em entregas em aberto.")
    elif result_entregador is None:
        # Entregador não encontrado
        print("O entregador com o código fornecido não existe.")
    else:
        # Recupera as informações do cliente em entregas_aberto
        cursor.execute('SELECT nome_cliente, bairro_cliente FROM entregas_aberto WHERE cod_cliente = ?', (cod_cliente,))
        entrega_info = cursor.fetchone()

        # Recupera as informações do entregador em entregadores
        cursor.execute('SELECT nome, telefone FROM entregadores WHERE cod = ?', (cod_entregador,))
        entregador_info = cursor.fetchone()

        # Gera um novo código de entrega único
        cursor.execute('SELECT MAX(cod_entrega) FROM entregas_rota')
        max_cod_entrega = cursor.fetchone()[0]
        novo_cod_entrega = 1 if max_cod_entrega is None else max_cod_entrega + 1

        # Obtém a data atual
        data_entrega = obter_data_atual()

        # Obtém o horário atual
        horario_saida = obter_horario_atual()
        
         # Insere a entrega em rota com o entregador e o horário de saída
        cursor.execute('INSERT INTO entregas_rota (cod_entrega, cod_entregador, nome_cliente, bairro,telefone_entregador, entregador, data_entrega, horário_saida) VALUES (?,?,?,?,?,?,?,?)', (novo_cod_entrega, cod_entregador, entrega_info[0], entrega_info[1],entregador_info[1], entregador_info[0],data_entrega, horario_saida))

        
        # Confirma as alterações
        conexao.commit()

        print("Entrega adicionada à rota com sucesso.")

def delete_entregas_aberto(cod_cliente):
    # Limpa o terminal
    limpa_terminal()

    print("-" * 50)

    conexao = sqlite3.connect('entregas.db')
    cursor = conexao.cursor()

    # Verifica se o ID existe na tabela
    cursor.execute('SELECT cod_cliente FROM entregas_aberto WHERE cod_cliente = ?', (cod_cliente,))
    result = cursor.fetchone()

    if result is None:
        # ID não encontrado
        print("O cliente com o código fornecido não tem entregas em aberto.")
    else:
        # Executa a instrução DELETE
        cursor.execute('DELETE FROM entregas_aberto WHERE cod_cliente = ?', (cod_cliente,))

        # Confirma as alterações
        conexao.commit()

        print("entrega deletada com sucesso.")

def delete_entregas_rota(cod_entrega):
    # Limpa o terminal
    limpa_terminal()

    print("-" * 50)

    conexao = sqlite3.connect('entregas.db')
    cursor = conexao.cursor()

    # Verifica se o ID existe na tabela
    cursor.execute('SELECT cod_entrega FROM entregas_rota WHERE cod_entrega = ?', (cod_entrega,))
    result = cursor.fetchone()

    if result is None:
        # ID não encontrado
        print("O código de entrega fornecido não existe em entregas em rota.")
    else:
        # Executa a instrução DELETE
        cursor.execute('DELETE FROM entregas_rota WHERE cod_entrega = ?', (cod_entrega,))

        # Confirma as alterações
        conexao.commit()

        print("entrega deletada com sucesso.")

    # Fecha a conexão
    conexao.close()

def entregas_finalizadas():
    # Limpa o terminal
    limpa_terminal()

    print("-" * 50)

    conexao = sqlite3.connect('entregas.db')
    cursor = conexao.cursor()

    #criar def para pegar informaçoes de entregas em rota e adicionar horário chegada e retirar de entregas em rota
    


while True:
    selecao = input(""" Opções:
                    [1] Adicionar Cliente
                    [2] Adicionar Entregador
                    [3] Exibir Clientes
                    [4] Exibir Entregadores
                    [5] Deletar Cliente
                    [6] Deletar Entregador
                    [7] Adicionar Entregas em Aberto 
                    [8] Adicionar Entregas em Rota 
                    [9] Adicionar Entregas finalizadas  x 
                    [10] Entregas finalizadas por dia x
                    [11] Exibir Entregas Em Aberto
                    [12] Deletar Entrega Em Aberto
                    [13] Deletar Entregas Em Rota
                    [14] Exibir Entregas Em Rota
                    [15] 
                    [16] Sair
                    digite a opção: """)
    
    if selecao == "1": # adiciona clientes
        add_clientes()

    if selecao =="2": # adiciona entregadores
        add_entregadores()
    
    if selecao == "3": # exibe clientes
        exibir_clientes()
    
    if selecao == "4": # exibe entregadores
        exibir_entregadores()
    
    if selecao == "5": # deleta cliente
        id_cliente_a_deletar = input("Digite o código do cliente a ser deletado: ")
        delete_cliente(id_cliente_a_deletar)

    if selecao == "6": # deleta entregador
        id_entregador_a_deletar = input("Digite o código do entregador a ser deletado: ")
        delete_entregador(id_entregador_a_deletar)
    
    if selecao == "7": # entregas em aberto
        add_entregas_aberto ()


    if selecao == "8": # entregas em rota
        exibir_entregas_aberto()
        codigo_cliente = input("Digite o código do cliente da entrega selecionada: ")
        codigo_entregador = input("Digite o código do entregador: ")
        adicionar_entregador_rota(int(codigo_cliente), int(codigo_entregador))

    if selecao == "9": # adicionar entregas
        pass

    if selecao == "10": #entregas finalizadas por dia
        pass

    if selecao == "11": #exibir entregas em aberto
        exibir_entregas_aberto()

    if selecao == "12": #deletar entregas em aberto
        cod_entrega_aberto = input("Digite o código do cliente que deseja deletar a entrega em aberto: ")
        delete_entregas_aberto(cod_entrega_aberto)  

    if selecao == "13": #deletar entregas em rota
        cod_entrega_rota = input("Digite o código da entrega que deseja deletar de entregas em rota: ")
        delete_entregas_rota(cod_entrega_rota)  
    
    if selecao == "14": # exibe entregas em rota 
        exibir_entregas_rota()

    elif selecao == "16":  # sair 
        break

# Fecha a conexão
conexao.close()