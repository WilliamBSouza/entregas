import sqlite3

conexao = sqlite3.connect('entregas.db')
cursor = conexao.cursor()

  # Utilizando parâmetros na consulta SQL
cursor.execute("""
    SELECT cod, nome, telefone
    FROM entregadores 
    ORDER BY cod ASC;
    """,)

lista_entregadores = cursor.fetchall()



print(lista_entregadores)