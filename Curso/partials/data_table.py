import flet as ft
# Tem que importar na view para poder funcionar a ordenação.
def sort_column(e):
    # Definir o índice da coluna a ser ordenada
    e.control.parent.__setattr__("sort_column_index", e.column_index)
    # Alternar a ordenação entre ascendente e descendente
    e.control.parent.__setattr__("sort_ascending", not e.control.parent.sort_ascending)
    # Ordenar as linhas da tabela com base no valor da célula
    e.control.parent.rows.sort(key=lambda x: x.cells[e.column_index].content.value, reverse=not e.control.parent.sort_ascending)
    # Atualizar a tabela
    e.control.parent.update()

# Define the create_datatable function
# data=None, styles=None, events=None
def create_datatable(ref=None, campos=None):

    # Create the DataTable with the specified parameters
    data_table = ft.DataTable(
        # width=1490,
        # height=55,
        data_row_max_height=25, # Tamanho máximo da tabela.
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
        ref=ref,
        columns=campos,
        data_row_min_height=15, # Ajuste da altura mínima das linhas
        rows=[],
    )
    # Return the DataTable instance
    return data_table

def my_table(datatable=None):
    # Para existência de um Scroll na tabela
    mytable = ft.Column(
        expand=True,
        controls=[
            ft.Row( 
                controls = [datatable], 
                scroll = ft.ScrollMode.ALWAYS
            )
        ],
        scroll=ft.ScrollMode.ALWAYS, # Define a existência de um Scroll
        on_scroll_interval=0, # Define o intervalo de exibição da fo.Column o padrão é 100 milissegundos           
    )
    return mytable