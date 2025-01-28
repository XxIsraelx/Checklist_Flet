import flet as ft
from flet import Text, MainAxisAlignment, CrossAxisAlignment, FontWeight, TextField
import time
import locale

def main(page: ft.Page):
    page.title = "Checklist"
    page.vertical_alignment = ft.MainAxisAlignment.START

    # Ajuste do locale para pt_BR, para garantir que as datas sejam formatadas corretamente
    try:
        locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')  # Configura para pt_BR
    except locale.Error:
        locale.setlocale(locale.LC_TIME, 'portuguese')  # Caso o anterior falhe, tenta uma alternativa

    # Lista de itens com o estado de seleção e campo de texto
    items = [
        {"name": "Estado do Pneu", "checked": False, "comment": ""},
        {"name": "Nivel do Óleo", "checked": False, "comment": ""},
        {"name": "Reservatorio de Agua", "checked": False, "comment": ""},
        {"name": "Teste de Freios:", "checked": False, "comment": ""},
        {"name": "Lanternas e Iluminação:", "checked": False, "comment": ""},
        {"name": "Bateria:", "checked": False, "comment": ""},
        {"name": "Lataria/visual:", "checked": False, "comment": ""},
        {"name": "Vazamentos:", "checked": False, "comment": ""},
        {"name": "Tacógrafo:", "checked": False, "comment": ""},
        {"name": "Thermo King:", "checked": False, "comment": ""}, 
        {"name": "Condição do baú:", "checked": False, "comment": ""},
        {"name": "Ferramentas:", "checked": False, "comment": ""},
    ]

    def create_checklist():
        checklist_controls = []
        for item in items:
            # Caixa de seleção
            checkbox = ft.Checkbox(label=item["name"], value=item["checked"])
            checkbox.on_change = lambda e, idx=item["name"]: toggle_item(idx, e.control.value)

            # Campo de texto para comentário que aparece se o item for marcado
            comment_input = ft.TextField(
                label="O que aconteceu?", 
                visible=item["checked"],  # Inicialmente escondido
                width=250,
                border_color="#696969",  # Cor da borda configurada
                border_radius=10
            )
            item["comment_input"] = comment_input  # Guardar o campo de comentário na lista de itens

            # Adiciona a caixa de seleção e o campo de texto em um container
            checklist_controls.append(
                ft.Row(
                    controls=[checkbox, comment_input],
                    alignment=MainAxisAlignment.START,
                    spacing=10
                )
            )
        return checklist_controls
    
    def toggle_item(item_name, checked):
        # Atualiza o estado de "checked" e a visibilidade do campo de texto
        for item in items:
            if item["name"] == item_name:
                item["checked"] = checked
                # Torna o campo de texto visível quando o item for marcado
                item["comment_input"].visible = checked
                item["comment_input"].value = ""  # Limpa o valor ao desmarcar (se necessário)
        
        page.update()  # Atualiza a página para refletir as mudanças

    # Campos KM atual e KM da próxima troca de óleo
    km_current_field = ft.TextField(
        label="KM Atual", 
        width=200,
        border_color="#696969",  # Cor da borda
        border_radius=10,
        on_change=lambda e: validate_km()  # Verifica ao alterar o valor
    )
    
    km_next_field = ft.TextField(
        label="KM da próxima troca de óleo", 
        width=250,
        border_color="#696969",  # Cor da borda
        border_radius=10,
        on_change=lambda e: validate_km()  # Verifica ao alterar o valor
    )

    # Campos KM row (para adicionar na tela)
    km_row = ft.Row(
        controls=[ 
            ft.Container(
                content=km_current_field,
                padding=10,  # Padding aqui
                alignment=ft.alignment.center,  
            ),
            ft.Container(
                content=km_next_field,
                padding=10,  # Padding aqui
                alignment=ft.alignment.center,  
            )
        ],
        alignment=MainAxisAlignment.CENTER,
        spacing=15
    )

    submit_button = ft.ElevatedButton(
        text="Enviar", 
        on_click=lambda e: page.add(ft.Text("Formulário Enviado!")), 
        disabled=True,  # Desabilitado inicialmente
        tooltip="Os campos KM atual e KM da próxima troca de óleo são obrigatórios."
    )

    # Adicionando data e hora no canto superior direito
    def update_time(e=None):
        # Obtém a data e hora atual no formato desejado em português
        current_time = time.strftime("%A, %d de %B de %Y %H:%M")  # Formato: Dia da semana, dia do mês, mês, ano, hora:minuto
        date_time_text.value = current_time
        page.update()

    # Exibir a hora atual
    date_time_text = ft.Text("", size=12, weight=FontWeight.BOLD)
    update_time()  # Chama a função para exibir a hora inicial

    # Atualiza a hora a cada minuto (60 segundos)
    page.on_timer = update_time  # Atualiza a hora a cada intervalo

    # Validação para os campos KM
    def validate_km():
        km_atual_value = km_current_field.value
        km_proxima_value = km_next_field.value

        if km_atual_value == "" or km_proxima_value == "":
            submit_button.disabled = True  # Botão desabilitado
            submit_button.tooltip = "Os campos KM atual e KM da próxima troca de óleo são obrigatórios."
            page.update()
        else:
            submit_button.disabled = False  # Botão habilitado
            submit_button.tooltip = ""  # Limpa o tooltip quando os campos são preenchidos
            page.update()

    # Layout da página
    page.add(
        ft.Column(
            [
                ft.Row(
                    controls=[date_time_text],
                    alignment=ft.alignment.top_right,  # Coloca no canto superior direito
                ),
                ft.Text("Selecione alguma irregularidade", size=15, weight=FontWeight.BOLD),
                *create_checklist(),
                ft.Text("Informe os KM para acompanhamento", size=15, weight=FontWeight.BOLD),
                km_row,  # Linha com os campos KM
                submit_button,  # Botão de envio
            ],
            alignment=MainAxisAlignment.CENTER, horizontal_alignment=CrossAxisAlignment.CENTER,
        )
    )

# Alteração: Permitir conexões externas com "host='0.0.0.0'"
ft.app(target=main, host="0.0.0.0", port=8550)
