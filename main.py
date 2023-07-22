import sqlite3
import os
from datetime import date
from datetime import datetime
import datetime
import time

def obter_horario_atual():
    horario_atual = datetime.datetime.now()
    horario_formatado = horario_atual.strftime("%H:%M:%S")

    return horario_formatado

# Função para obter a data atual para cod unico
def data_cod_unico():
    return datetime.now().strftime('%Y-%m-%d')

# Função para obter o horário atual para cod unico
def horario_cod_unico():
    return datetime.now().strftime('%H:%M:%S')

def obter_data_atual():
    data_atual = date.today()
    return data_atual

def obter_data_atual_teste():
    data_atual = str(date.today())
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
#cursor.execute('ALTER TABLE entregas_aberto ADD COLUMN cod_entrega VARCHAR(25)')
#cursor.execute('ALTER TABLE entregas_rota ADD COLUMN data_entrega DATE')
#cursor.execute('ALTER TABLE entregas_rota ADD COLUMN horário_saida VARCHAR(10) ')
#cursor.execute('CREATE TABLE entregas_finalizadas (cod_entrega INT PRIMARY KEY, cod_entregador INT, nome_cliente , bairro , telefone_entregador, Entregador, data_entrega, horário_saida, horário_chegada)')
#cursor.execute('ALTER TABLE entregas_rota ADD COLUMN cod_cliente INT')
#cursor.execute('ALTER TABLE entregas_finalizadas ADD COLUMN cod_cliente INT')

################################################################################################################################################
                           #TESTE       TESTE                    TESTE


def pesquisa_por_data_hoje():
        data_hoje = datetime.date.today().isoformat()
        pesquisa_por_data(data_hoje)


################################################################################################################################################





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

def excluir_entrega_aberto_rota(cod_entrega):
    # Verifica se a entrega em entregas_aberto existe
    cursor.execute('SELECT cod_entrega FROM entregas_aberto WHERE cod_entrega = ?', (cod_entrega,))
    result_entrega = cursor.fetchone()

    if result_entrega is None:
        # Entrega em entregas_aberto não encontrada
        print("A entrega não está em entregas em aberto.")
    else:
        # Executa a instrução DELETE
        cursor.execute('DELETE FROM entregas_aberto WHERE cod_entrega = ?', (cod_entrega,))

        # Confirma as alterações
        conexao.commit()

        print("Entrega em aberto excluída com sucesso.")

def excluir_entrega_rota_finalizadas(cod_entrega):
    # Verifica se a entrega em entregas_aberto existe
    cursor.execute('SELECT cod_entrega FROM entregas_rota WHERE cod_entrega = ?', (cod_entrega,))
    result_entrega_rota = cursor.fetchone()

    if result_entrega_rota is None:
        # Entrega em entregas_rota não encontrada
        print("A entrega não está em entregas em rota.")
    else:
        # Executa a instrução DELETE
        cursor.execute('DELETE FROM entregas_rota WHERE cod_entrega = ?', (cod_entrega,))

        # Confirma as alterações
        conexao.commit()

        print("Entrega em rota excluída com sucesso.")

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

        # Criar o valor único para a coluna cod_entrega
        cod_entrega_unico = f"{obter_data_atual()} {obter_horario_atual()}"

        # Insere a entrega em aberto com as informações do cliente
        cursor.execute('INSERT INTO entregas_aberto VALUES(?,?,?,?)', (codigo_cliente, cliente_info[0], cliente_info[1],cod_entrega_unico))

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

def exibir_entregas_finalizadas():
    limpa_terminal()
    print("Entregas finalizadas:")
    print("*" * 50)
    cursor.execute('SELECT * FROM entregas_finalizadas ORDER BY cod_entrega ASC')
    registros = cursor.fetchall()

    for registro in registros:
        print(registro)
    print("*" * 50)
    
def adicionar_entregador_rota(cod_cliente, cod_entregador): # adiciona entregas em rota
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
        cursor.execute('SELECT nome_cliente, bairro_cliente , cod_entrega, cod_cliente FROM entregas_aberto WHERE cod_cliente = ?', (cod_cliente,))
        entrega_info = cursor.fetchone()

        # Recupera as informações do entregador em entregadores
        cursor.execute('SELECT nome, telefone FROM entregadores WHERE cod = ?', (cod_entregador,))
        entregador_info = cursor.fetchone()

        # Obtém a data atual
        data_entrega = obter_data_atual()

        # Obtém o horário atual
        horario_saida = obter_horario_atual()
        
         # Insere a entrega em rota com o entregador e o horário de saída
        cursor.execute('INSERT INTO entregas_rota (cod_entrega, cod_entregador, nome_cliente, bairro,telefone_entregador, entregador, data_entrega, horário_saida,cod_cliente) VALUES (?,?,?,?,?,?,?,?,?)', (entrega_info[2], cod_entregador, entrega_info[0], entrega_info[1],entregador_info[1], entregador_info[0],data_entrega, horario_saida,entrega_info[3]))

        #exclui entrega em aberto quando vai para entregas em rota
        excluir_entrega_aberto_rota(entrega_info[2])

   
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

    #criar def para pegar informaçoes de entregas em rota e adicionar horário chegada e retirar de entregas em rota
def adicionar_entregas_finalizadas(cod_entrega):
    # Verifica se a entrega em entregas_rota existe
    cursor.execute('SELECT cod_entrega FROM entregas_rota WHERE cod_entrega = ?', (cod_entrega,))
    result_entrega = cursor.fetchone()

    if result_entrega is None:
        # Entrega em entregas_aberto não encontrado
        print("A entrega não está em entregas em aberto.")
    
    else:
        # Recupera as informações da entrega em entregas_rota
        cursor.execute('SELECT cod_entrega,cod_entregador, nome_cliente, bairro,telefone_entregador, Entregador, data_entrega, horário_saida, cod_cliente FROM entregas_rota WHERE cod_entrega = ?', (cod_entrega,))
        entrega_rota_info = cursor.fetchone()

        # Obtém o horário atual
        horario_chegada = obter_horario_atual()
        
        # Insere a entrega em rota com o entregador e o horário de saída
        cursor.execute('INSERT INTO entregas_finalizadas (cod_entrega, cod_entregador, nome_cliente, bairro,telefone_entregador, entregador, data_entrega, horário_saida, horário_chegada,cod_cliente) VALUES (?,?,?,?,?,?,?,?,?,?)', (entrega_rota_info[0], entrega_rota_info[1], entrega_rota_info[2], entrega_rota_info[3],entrega_rota_info[4], entrega_rota_info[5],entrega_rota_info[6], entrega_rota_info[7], horario_chegada,entrega_rota_info[8]))


        #criar método de analizar cod entrega na tabela entregas em rota e apagar a entrega da tabela anterior
        ###teste
        excluir_entrega_rota_finalizadas(entrega_rota_info[0])
        ### fim do teste

        # Confirma as alterações
        conexao.commit()

        print("Entrega finalizada com sucesso.")

def pesquisa_por_data(data_entrega):
    
    limpa_terminal()
    print("Entregas finalizadas:")
    print("*" * 50)
    
    # Executa a consulta SELECT com a cláusula WHERE para filtrar por data de entrega
    cursor.execute('SELECT * FROM entregas_finalizadas WHERE data_entrega = ?', (data_entrega,))
    registros = cursor.fetchall()

    for registro in registros:
        print(registro)
    print("*" * 50)

def pesquisa_data_entregador(entregador, data_entrega ):
    
    limpa_terminal()
    print("*" * 50)

    # Executa a consulta SELECT com a cláusula WHERE para filtrar por data de entrega e cod_entregador
    cursor.execute('SELECT * FROM entregas_finalizadas WHERE data_entrega = ? AND cod_entregador = ?', (data_entrega,entregador))
    registros = cursor.fetchall()
    
    for registro in registros:
        print(registro)
    print("*" * 50)


#  *****************AVISO*****************AVISO*******************************AVISO****************************AVISO***********************

while False:  # False para servir apenas como base para o FRONTEND

#  *****************AVISO*****************AVISO*******************************AVISO****************************AVISO***********************
   
    selecao = input("""Opções:
                    [1] Adicionar
                    [2] Deletar
                    [3] Exibir
                    [4] Pesquisar
                    [5] Sair
                    Digite a opção: """)
    
    if selecao =="1":
        opções_Adicionar = input("""Opções Adicionar:
                                 
                                 [1] Adicionar Cliente
                                 [2] Adicionar entregador
                                 [3] Adicionar Entregas em Aberto
                                 [4] Adicionar Entregas em Rota
                                 [5] Adicionar Entregas Finalizadas 
                                 [6] Sair
                                 Digite a opção: """)
        
        if opções_Adicionar == "1":
                add_clientes()
        
        if opções_Adicionar == "2":
            add_entregadores()
        
        if opções_Adicionar == "3":
            add_entregas_aberto()
        
        if opções_Adicionar == "4":
            exibir_entregas_aberto()
            codigo_cliente = input("Digite o código do cliente da entrega selecionada: ")
            codigo_entregador = input("Digite o código do entregador: ")
            adicionar_entregador_rota(int(codigo_cliente), int(codigo_entregador))
        
        if opções_Adicionar == "5":
            cod_entrega_a_finalizar = input("digite o códico da entrega para finalizar: ")
            adicionar_entregas_finalizadas(cod_entrega_a_finalizar)
        
        if opções_Adicionar == "6":
            break

    if selecao == "2":
        opções_deletar = input("""Opções Deletar:
                               
                                 [1] Deletar Cliente
                                 [2] Deletar Entregador
                                 [3] Deletar Entrega Em Aberto
                                 [4] Deletar Entregas Em Rota
                                 [5] Sair
                                Digite a opção: """)
        if opções_deletar == "1":
            id_cliente_a_deletar = input("Digite o código do cliente a ser deletado: ")
            delete_cliente(id_cliente_a_deletar)   

        if opções_deletar == "2":
            id_entregador_a_deletar = input("Digite o código do entregador a ser deletado: ")
            delete_entregador(id_entregador_a_deletar)  

        if opções_deletar == "3":
            limpa_terminal()
            cod_entrega_aberto = input("Digite o código do cliente que deseja deletar a entrega em aberto: ")
            delete_entregas_aberto(cod_entrega_aberto)

        if opções_deletar == "4":
            cod_entrega_rota = input("Digite o código da entrega que deseja deletar de entregas em rota: ")
            delete_entregas_rota(cod_entrega_rota)
        
        if opções_deletar == "5":
            break

    if selecao == "3":
        opções_Exibir = input("""Opções Exibir:
                                 
                                 [1] Exibir Cliente
                                 [2] Exibir entregador
                                 [3] Exibir Entregas em Aberto
                                 [4] Exibir Entregas em Rota
                                 [5] Exibir Entregas Finalizadas 
                                 [6] Sair
                                 Digite a opção: """)
        if opções_Exibir == "1":
            exibir_clientes()
        
        if opções_Exibir == "2":
            exibir_entregadores()
        
        if opções_Exibir == "3":
             exibir_entregas_aberto()
        
        if opções_Exibir == "4":
            exibir_entregas_rota()
        
        if opções_Exibir == "5":
            exibir_entregas_finalizadas()

        if opções_Exibir == "6":
            break
    
    if selecao == "4":
        opções_pesquisa= input("""Opções pesquisa:
                                 
                                 [1] Pesquisa Entragas Finalizadas Por Data
                                 [2] Pesquisa Entregas Finalizadas Por Data E Entregador
                                 [3] Pesquisa Data Hoje
                                 [4] Sair
                                 Digite a opção: """)
        if opções_pesquisa == "1":
            data_pesquisa = input("Digite a data que deseja pesquisar (AAAA-MM-DD): ")
            pesquisa_por_data(data_pesquisa)
        
        if opções_pesquisa == "2":
            entregador_pesquisa = input("digite o código do entregador que deseja pesquisar: ")
            data_pesquisa1 = input("Digite a data que deseja pesquisar (AAAA-MM-DD): ")
            
            try:
                pesquisa_data_entregador(entregador_pesquisa, data_pesquisa1)
            except Exception as e:
                print(f"Ocorreu um erro na pesquisa: {e}")
        
        if opções_pesquisa == "3":
            data_hoje = datetime.date.today().isoformat()
            pesquisa_por_data(data_hoje)

        if opções_pesquisa == "4":
            break

    if selecao == "5":
        break    

# Fecha a conexão
#conexao.close()