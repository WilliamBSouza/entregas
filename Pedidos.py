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

def configurações_sistema ():

    configurações = Tk()
    configurações.geometry("270x300")
    configurações.title('configurações')

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

    def janela_cadastrar_clientes():

        def mostrar_clientes():
            conn, cursor = conecta_bd_clientes()

            # Executar a consulta para obter os clientes cadastrados
            cursor.execute("SELECT * FROM clientes")
            clientes = cursor.fetchall()

            desconectar_bd(conn)

            if clientes:
                for cliente in clientes:
                    print("Código:", cliente[0])
                    print("Nome:", cliente[1])
                    print("Telefone:", cliente[2])
                    print("Bairro:", cliente[3])
                    print("--------------------")
            else:
                print("Não há clientes cadastrados.")

        def adicionar_cliente():
            nome = entry_nome.get()
            telefone = entry_telefone.get()
            bairro = entry_bairro.get()

            conn, cursor = conecta_bd_clientes()

            try:
                # Executar a inserção dos dados do cliente
                cursor.execute("INSERT INTO clientes (nome_cliente, telefone, bairro) VALUES (?, ?, ?)",
                            (nome, telefone, bairro))
                conn.commit()
                status_label.config(text="Cliente adicionado com sucesso!", fg="green")
            except Exception as e:
                status_label.config(text="Erro ao adicionar cliente: " + str(e), fg="red")
            finally:
                desconectar_bd(conn)

        janela_add_clientes = Tk()
        janela_add_clientes.geometry("320x160")
        janela_add_clientes.title('Cadastro de Cliente')

        label_nome_cliente = Label(janela_add_clientes, text="Nome do cliente:")
        label_nome_cliente.place(x=10, y=5)

        label_telefone = Label(janela_add_clientes, text="Telefone:")
        label_telefone.place(x=10, y=25)

        label_bairro = Label(janela_add_clientes, text="Bairro:")
        label_bairro.place(x=10, y=45)

        status_label = Label(janela_add_clientes, text="")
        status_label.place(x=10, y=130)

        entry_nome = Entry(janela_add_clientes)
        entry_nome.place(x=110, y=5, width=200)

        entry_telefone = Entry(janela_add_clientes)
        entry_telefone.place(x=110, y=25)

        entry_bairro = Entry(janela_add_clientes)
        entry_bairro.place(x=110, y=45)

        btn_adicionar_cliente = Button(janela_add_clientes, text="Adicionar Cliente", command=adicionar_cliente)
        btn_adicionar_cliente.place(x=50, y=75)

        btn_mostrar_clientes = Button(janela_add_clientes, text="Mostrar Clientes", command=mostrar_clientes)
        btn_mostrar_clientes.place(x=50, y=105)

        janela_add_clientes.mainloop()

    # janela entregador
    def janela_entregador():

        def excluir_entregador():
            codigo = entry_codigo_entregador.get()

            conn, cursor = conecta_bd_entregadores()

            # Executar a exclusão do entregador com o código especificado
            cursor.execute("DELETE FROM entregadores WHERE cod = ?", (codigo,))
            conn.commit()

            if cursor.rowcount > 0:
                status_label.config(text="Entregador excluído com sucesso!", fg="green")
            else:
                status_label.config(text="Entregador não encontrado.", fg="red")

            desconectar_bd(conn)

        def adicionar_entregador():
            nome = entry_nome_entregador.get()

            conn, cursor = conecta_bd_entregadores()

            try:
                # Executar a inserção dos dados do entregador
                cursor.execute("INSERT INTO entregadores (nome_entregador) VALUES (?)", (nome,))
                conn.commit()
                status_label.config(text="Entregador adicionado com sucesso!", fg="green")
            except Exception as e:
                status_label.config(text="Erro ao adicionar entregador: " + str(e), fg="red")
            finally:
                desconectar_bd(conn)
        def mostrar_entregadores():
            conn, cursor = conecta_bd_entregadores()

            # Executar a consulta para obter os entregadores cadastrados
            cursor.execute("SELECT * FROM entregadores")
            entregadores = cursor.fetchall()

            desconectar_bd(conn)

            if entregadores:
                for entregador in entregadores:
                    print("Código:", entregador[0])
                    print("Nome:", entregador[1])
                    print("--------------------")
            else:
                print("Não há entregadores cadastrados.")       


        janela_Entregadores = Tk()
        janela_Entregadores.geometry("320x320")
        janela_Entregadores.title('Entregadores')

        status_label = Label(janela_Entregadores, text="")
        status_label.place(x=10, y=130)

        label_codigo_entregador = Label(janela_Entregadores, text="Código:")
        label_codigo_entregador.place(x=10, y=180)

        entry_codigo_entregador = Entry(janela_Entregadores)
        entry_codigo_entregador.place(x=70, y=180)

        btn_excluir_entregador = Button(janela_Entregadores, text="Excluir Entregador", command=excluir_entregador)
        btn_excluir_entregador.place(x=80, y=220)

        label_nome_entregador = Label(janela_Entregadores, text="Nome do Entregador:")
        label_nome_entregador.place(x=10, y=10)

        entry_nome_entregador = Entry(janela_Entregadores)
        entry_nome_entregador.place(x=130, y= 10)

        btn_adicionar_entregador = Button(janela_Entregadores, text="Adicionar Entregador", command=adicionar_entregador)
        btn_adicionar_entregador.place(x=80, y=40)

        btn_mostrar_entregadores = Button(janela_Entregadores, text="Mostrar Entregadores", command=mostrar_entregadores)
        btn_mostrar_entregadores.place(x=80, y=70)

        janela_Entregadores.mainloop()

    # janela excluir clientes
    def janela_excluir_clientes():
        def excluir_cliente():
            codigo = entry_codigo.get()

            conn, cursor = conecta_bd_clientes()

            # Executar a exclusão do cliente com o código especificado
            cursor.execute("DELETE FROM clientes WHERE cod = ?", (codigo,))
            conn.commit()

            if cursor.rowcount > 0:
                status_label.config(text="Cliente excluído com sucesso!", fg="green")
            else:
                status_label.config(text="Cliente não encontrado.", fg="red")

            desconectar_bd(conn)

        janela_apagar_clientes = Tk()
        janela_apagar_clientes.geometry("320x160")
        janela_apagar_clientes.title('Apagar clientes')

        status_label = Label(janela_apagar_clientes, text="")
        status_label.place(x=10, y=130)

        label_codigo = Label(janela_apagar_clientes, text="Código:")
        label_codigo.place(x=10, y=65)

        entry_codigo = Entry(janela_apagar_clientes)
        entry_codigo.place(x=110, y=65)

        btn_excluir_cliente = Button(janela_apagar_clientes, text="Excluir Cliente", command=excluir_cliente)
        btn_excluir_cliente.place(x=110, y=100)

        janela_apagar_clientes.mainloop()

    btn_cadastrar_clientes = Button(configurações, text='Cadastrar cliente', command=janela_cadastrar_clientes)
    btn_cadastrar_clientes.place(x=10, y=20,width=250)

    btn_apagar_clientes = Button(configurações, text='Apagar cliente', command=janela_excluir_clientes)
    btn_apagar_clientes.place(x=10, y=50,width=250)

    btn_Entregadores = Button(configurações, text='Entregadores', command=janela_entregador)
    btn_Entregadores.place(x=10, y=80,width=250)


    configurações.mainloop()

def janela_pedidos():
        def conecta_bd_pedidos():
            conn = sqlite3.connect("pedidos.bd")
            cursor = conn.cursor()
            return conn, cursor
        # Função para adicionar pedidos
        def adicionar_pedido():
            entregador = entry_entregador.get()
            clientes = entry_clientes.get()

            # Separar os IDs dos clientes em uma lista
            clientes = clientes.split(",")

            # Inserir os pedidos na tabela de pedidos
            conn, cursor = conecta_bd_pedidos()

            try:
                # Executar a inserção dos dados do pedido
                for cliente in clientes:
                    cursor.execute("INSERT INTO pedidos (entregador, cliente) VALUES (?, ?)", (entregador, cliente))
                conn.commit()
                status_label.config(text="Pedido adicionado com sucesso!", fg="green")
            except Exception as e:
                status_label.config(text="Erro ao adicionar pedido: " + str(e), fg="red")
            finally:
                desconectar_bd(conn)

        janela_pedidos = Tk()
        janela_pedidos.geometry("320x160")
        janela_pedidos.title('Gerenciamento de Pedidos')

        label_entregador = Label(janela_pedidos, text="Entregador:")
        label_entregador.place(x=10, y=5)

        label_clientes = Label(janela_pedidos, text="Clientes (separados por vírgula):")
        label_clientes.place(x=10, y=25)

        status_label = Label(janela_pedidos, text="")
        status_label.place(x=10, y=130)

        entry_entregador = Entry(janela_pedidos)
        entry_entregador.place(x=110, y=5, width=200)

        entry_clientes = Entry(janela_pedidos)
        entry_clientes.place(x=160, y=25, width=150)

        btn_adicionar_pedido = Button(janela_pedidos, text="Adicionar Pedido", command=adicionar_pedido)
        btn_adicionar_pedido.place(x=50, y=75)

        janela_pedidos.mainloop()

janela = Tk()
janela.geometry("290x300")
janela.title('Controle de pedidos')

btn_configuração = Button(janela, text='Configurações', command=configurações_sistema)
btn_configuração.place(x=10, y=10,width=270)

btn_pedidos = Button(janela, text='pedidos', command=janela_pedidos)
btn_pedidos.place(x=10, y=40,width=270)

janela.mainloop()