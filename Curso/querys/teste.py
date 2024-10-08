# import os
# import pymssql

# USER = os.getenv('DB_USER', 'sa')
# PASSWORD = os.getenv('DB_PASSWORD', 'Abc*123')
# HOST = os.getenv('DB_HOST', '192.168.254.1')
# DATABASE = os.getenv('DB_NAME', 'ALTERDATA_TESTE')

# # Configuração da conexão
# connection_string = f'mssql+pymssql://{USER}:{PASSWORD}@{HOST}/{DATABASE}'

# from sqlalchemy import create_engine, text, Column, update, insert, select, desc, func, and_
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy import text

# engine = create_engine(connection_string)
# Session = sessionmaker(bind=engine)
# session = Session()



# def execute_stored_procedure(entity, column, value):
#     result = session.execute(text("EXEC stp_GetMultiCode :entity, :column, :value"),
#                             {'entity': entity, 
#                                 'column': column, 
#                                 'value': value})
#     return result

# result = execute_stored_procedure('PedidoDeCompra', 'IdPedidoDeCompra', 1)
# for row in result:
#     print(row)

# session.close()






# import pymssql

# # Configuração da conexão
# USER = 'sa'
# PASSWORD = 'Abc*123'
# HOST = '192.168.254.1'
# DATABASE = 'ALTERDATA_TESTE'

# # Função para executar a stored procedure com pymssql
# def execute_stored_procedure():
#     try:
#         # Conecta ao banco de dados
#         with pymssql.connect(server=HOST, user=USER, password=PASSWORD, database=DATABASE) as conn:
#             with conn.cursor() as cursor:
#                 # Chama a stored procedure com parâmetros de entrada e captura o de saída
#                 cursor.execute("""
#                     DECLARE @OutputParam INT;
#                     EXEC stp_GetMultiCode @TableName = %s, @FieldName = %s, @NrCodigos = %s;
#                 """, ('PedidoDeCompra', 'IdPedidoDeCompra', 1))

#                 # Captura o valor retornado
#                 output_value = cursor.fetchall()  # fetchall() para múltiplos códigos, caso a stored procedure retorne mais de um

#                 # Verifica se há resultados
#                 if output_value:
#                     print("Output Param:", output_value)
#                 else:
#                     print("Nenhum código retornado.")

#                 # Retorna os resultados
#                 return output_value

#     except pymssql.DatabaseError as e:
#         print(f"Erro ao acessar o banco de dados: {e}")
#         return None

# # Executa a função
# result = execute_stored_procedure()

# # Exibe os resultados
# print(result)





# import pymssql

# # Configuração da conexão
# USER = 'sa'
# PASSWORD = 'Abc*123'
# HOST = '192.168.254.1'
# DATABASE = 'ALTERDATA_TESTE'

# # Função para executar a stored procedure com pymssql
# def execute_stored_procedure(entity, column, value):
#     try:
#         # Conecta ao banco de dados
#         with pymssql.connect(server=HOST, user=USER, password=PASSWORD, database=DATABASE) as conn:
#             with conn.cursor() as cursor:
#                 # Executa a stored procedure diretamente com callproc
#                 cursor.callproc('stp_GetMultiCode', (entity, column, value))

#                 # Recupera os resultados da primeira tabela retornada
#                 result = cursor.fetchall()
                
#                 # Retorna os resultados
#                 return result
#     except pymssql.DatabaseError as e:
#         print(f"Erro ao acessar o banco de dados: {e}")
#         return None

# # Executa a função
# result = execute_stored_procedure('PedidoDeCompra', 'IdPedidoDeCompra', 1)

# # Exibe os resultados
# for row in result:
#     print(row)


# ---------------------------------------------------------------------------------------------------------------
# import flet as ft

# def main(page):
#     # Configurando o modo claro para o tema da página
#     page.theme_mode = ft.ThemeMode.LIGHT

#     # Função que será chamada ao carregar o arquivo
#     def on_upload(e):
#         # Mostrando o nome do arquivo carregado
#         uploaded_file = e.files[0]
#         page.add(ft.Text(f"Arquivo carregado: {uploaded_file.name}"))

#     # Função para simular o carregamento do arquivo
#     def start_upload(e):
#         # Indicador de atividade enquanto o upload está ocorrendo
#         upload_indicator = ft.CupertinoActivityIndicator(radius=50, color=ft.colors.RED, animating=True)
#         page.add(upload_indicator)
        
#         # Simulando o tempo de upload
#         page.update()  # Atualizando a página para exibir o indicador de atividade
#         page.snack_bar = ft.SnackBar(ft.Text("Carregando arquivo..."))
#         page.snack_bar.open = True
#         page.update()

#         # Simulando uma espera para o "upload"
#         import time
#         time.sleep(2)

#         # Removendo o indicador de atividade após o upload
#         page.remove(upload_indicator)
#         page.snack_bar.open = False
#         page.update()

#     # Botão para selecionar o arquivo e iniciar o upload
#     file_picker = ft.FilePicker(on_result=on_upload)
#     page.overlay.append(file_picker)

#     page.add(
#         ft.Column(
#             controls=[
#                 ft.ElevatedButton("Selecionar Arquivo", icon=ft.icons.UPLOAD_FILE, on_click=lambda _: file_picker.pick_files()),
#                 ft.ElevatedButton("Iniciar Upload", on_click=start_upload),
#             ]
#         )
#     )

# # Iniciando a aplicação
# ft.app(target=main)
# ------------------------------------------------------------------------------------------------------------------
# import flet as ft

# def main(page: ft.Page):
#     page.add(
#         ft.DataTable(
#         width=700,
#         bgcolor="yellow",
#         border=ft.border.all(2, "red"),
#         border_radius=10,
#         vertical_lines=ft.BorderSide(3, "blue"),
#         horizontal_lines=ft.BorderSide(1, "green"),
#         sort_column_index=0,
#         sort_ascending=True,
#         heading_row_color=ft.colors.BLACK12,
#         heading_row_height=100,
#         data_row_color={"hovered": "0x30FF0000"},
#         show_checkbox_column=True,
#         divider_thickness=0,
#         column_spacing=200,
#         columns=[
#             ft.DataColumn(
#                 ft.Text("Column 1"),
#                 on_sort=lambda e: [# Select the column itself
#                                    e.control.parent.__setattr__("sort_column_index" , e.column_index) ,
#                                    # Toggle the sort (ascending / descending)
#                                    e.control.parent.__setattr__("sort_ascending" , False) if e.control.parent.sort_ascending else e.control.parent.__setattr__("sort_ascending" , True) ,
#                                    # Sort the table rows according above
#                                    e.control.parent.rows.sort(key=lambda x: x.cells[e.column_index].content.value,reverse = e.control.parent.sort_ascending) ,
#                                    # Update table
#                                    e.control.parent.update()
#                                   ],
#             ),
#             ft.DataColumn(
#                 ft.Text("Column 2"),
#                 tooltip="This is a second column",
#                 numeric=True,
#                 on_sort=lambda e: print(f"{e.column_index}, {e.ascending}"),
#             ),
#         ],
#         rows=[
#             ft.DataRow(
#                 [ft.DataCell(ft.Text("A")), ft.DataCell(ft.Text("1"))],
#                 selected=True,
#                 on_select_changed=lambda e: print(f"row select changed: {e.data}"),
#             ),
#             ft.DataRow([ft.DataCell(ft.Text("B")), ft.DataCell(ft.Text("2"))]),
#         ],
#     ),
# )

# ft.app(target=main)
# ------------------------------------------------------------------------------------------------------------------

# import flet as ft

# def main(page: ft.Page):

#     # Dados iniciais da tabela
#     data = [
#         ["Ana", 25, "Engenheira"],
#         ["Bruno", 30, "Designer"],
#         ["Carlos", 22, "Desenvolvedor"],
#         ["Daniela", 28, "Gerente"],
#     ]

#     # Estado para controle da ordenação
#     ascending = True

#     # Função que reordena as linhas com base na coluna clicada
#     def sort_table(e, column_index):
#         nonlocal ascending, data
#         data.sort(key=lambda x: x[column_index], reverse=not ascending)
#         ascending = not ascending
#         update_table()

#     # Função para atualizar a tabela
#     def update_table():
#         table.rows.clear()

#         for row in data:
#             table.rows.append(ft.DataRow(cells=[
#                 ft.DataCell(ft.Text(row[0])),
#                 ft.DataCell(ft.Text(str(row[1]))),
#                 ft.DataCell(ft.Text(row[2])),
#             ]))
            
#         page.update()

#     # Definindo a tabela
#     table = ft.DataTable(
#         columns=[
#             ft.DataColumn(ft.Text("Nome"), on_sort=lambda e: sort_table(e, 0)),
#             ft.DataColumn(ft.Text("Idade"), on_sort=lambda e: sort_table(e, 1)),
#             ft.DataColumn(ft.Text("Profissão"), on_sort=lambda e: sort_table(e, 2)),
#         ],
#         rows=[]
#     )

#     # Carregando os dados iniciais na tabela
#     update_table()

#     # Adicionando a tabela à página
#     page.add(table)

# ft.app(target=main)
# ------------------------------------------------------------------------------------------------------------------
import flet as ft

def main(page: ft.Page):
    def sort_column(e):
        # Definir o índice da coluna a ser ordenada
        e.control.parent.__setattr__("sort_column_index", e.column_index)
        # Alternar a ordenação entre ascendente e descendente
        e.control.parent.__setattr__("sort_ascending", not e.control.parent.sort_ascending)
        # Ordenar as linhas da tabela com base no valor da célula
        e.control.parent.rows.sort(key=lambda x: x.cells[e.column_index].content.value, reverse=not e.control.parent.sort_ascending)
        # Atualizar a tabela
        e.control.parent.update()

    page.add(
        ft.DataTable(
            width=700,
            bgcolor="yellow",
            border=ft.border.all(2, "red"),
            border_radius=10,
            vertical_lines=ft.BorderSide(3, "blue"),
            horizontal_lines=ft.BorderSide(1, "green"),
            sort_column_index=0,
            sort_ascending=True,
            heading_row_color=ft.colors.BLACK12,
            heading_row_height=100,
            data_row_color={"hovered": "0x30FF0000"},
            show_checkbox_column=True,
            divider_thickness=0,
            column_spacing=200,
            columns=[
                ft.DataColumn(
                    ft.Text("Column 1"),
                    on_sort=sort_column,  # Reutilizar a função genérica
                ),
                ft.DataColumn(
                    ft.Text("Column 2"),
                    tooltip="This is a second column",
                    numeric=True,
                    on_sort=sort_column,  # Reutilizar a função genérica
                ),
            ],
            rows=[
                ft.DataRow(
                    [ft.DataCell(ft.Text("A")), ft.DataCell(ft.Text("1"))],
                    selected=True,
                    on_select_changed=lambda e: print(f"row select changed: {e.data}"),
                ),
                ft.DataRow([ft.DataCell(ft.Text("B")), ft.DataCell(ft.Text("2"))]),
            ],
        ),
    )

ft.app(target=main)

# ------------------------------------------------------------------------------------------------------------------

# from time import sleep
# import flet as ft

# def main(page: ft.Page):
#     def button_click(e):
#         loading = ft.AlertDialog(
#             content=ft.Container(
#                 content=ft.ProgressRing(),
#                 alignment=ft.alignment.center,
#             ),
#             bgcolor=ft.colors.TRANSPARENT,
#             modal=True,
#             disabled=True,
#         )
#         page.open(loading)
#         sleep(3)
#         page.close(loading)

#     btn = ft.ElevatedButton("Executar tarefa!", on_click=button_click)
#     page.add(btn)

# ft.app(target=main)


# ------------------- FUNCIONANDO -----------------------------------------
# import pyodbc

# # Configuração da conexão
# USER = 'sa'
# PASSWORD = 'Abc*123'
# HOST = '192.168.254.1'
# DATABASE = 'ALTERDATA_TESTE'

# # String de conexão
# connection_string = (
#     'DRIVER={ODBC Driver 17 for SQL Server};'
#     f'SERVER={HOST};DATABASE={DATABASE};UID={USER};PWD={PASSWORD}'
# )

# # Função para executar a stored procedure com pyodbc
# def execute_stored_procedure(entity, column, value):
#     try:
#         # Conecta ao banco de dados
#         with pyodbc.connect(connection_string) as conn:
#             with conn.cursor() as cursor:
#                 # Executa a stored procedure diretamente
#                 cursor.execute("{CALL stp_GetMultiCode(?, ?, ?)}", (entity, column, value))
                
#                 # Recupera os resultados
#                 result = cursor.fetchall()
#                 return result
#     except pyodbc.DatabaseError as e:
#         print(f"Erro ao acessar o banco de dados: {e}")
#         return None

# # Executa a função
# result = execute_stored_procedure('PedidoDeCompra', 'IdPedidoDeCompra', 1)

# # Exibe os resultados
# for row in result:
#     print(row)

