import flet as ft

tb_tabela = ft.Ref[ft.DataTable]()

# Define the create_datatable function
# data=None, styles=None, events=None
def create_datatable():

    # Create the DataTable with the specified parameters
    data_table = ft.DataTable(
        # width=1490,
        # height=55,
        data_row_max_height=35, # Tamanho máximo da tabela.
        # bgcolor="yellow",
        border=ft.border.all(2, "red"),
        border_radius=10,
        vertical_lines=ft.border.BorderSide(3, "blue"),
        horizontal_lines=ft.border.BorderSide(1, "green"),
        sort_column_index=0,
        sort_ascending=True,
        heading_row_color=ft.colors.BLACK12,
        heading_row_height=55,
        data_row_color={"hovered": "0x30FF0000"},
        show_checkbox_column=True,
        divider_thickness=0,
        # column_spacing=200,
        ref=tb_tabela,
        columns=[
            ft.DataColumn(ft.Text("Código", width=50), on_sort=lambda e: print(f"{e.column_index}, {e.ascending}"),),
            ft.DataColumn(ft.Text("Status", width=40), on_sort=lambda e: print(f"{e.column_index}, {e.ascending}"),),
            ft.DataColumn(ft.Text("Data Emissao", width=150), on_sort=lambda e: print(f"{e.column_index}, {e.ascending}"),),
            ft.DataColumn(ft.Text("Data Entrega", width=150)),
            ft.DataColumn(ft.Text("Descricao", width=70), on_sort=lambda e: print(f"{e.column_index}, {e.ascending}"),),
            ft.DataColumn(ft.Text("Observacao", width=240), numeric=True,  on_sort=lambda e: print(f"{e.column_index}, {e.ascending}"),), 
        ],
        rows=[],
    )
    
    # Return the DataTable instance
    return data_table