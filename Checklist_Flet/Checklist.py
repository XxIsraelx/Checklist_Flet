import flet as ft
from flet import Text, MainAxisAlignment, CrossAxisAlignment, FontWeight, TextField, AlertDialog, Dropdown
import time
import locale

# Lista de motoristas e placas de caminhões (pode ser alterado conforme necessário)
motoristas = [
            "Anderson Alves", "André", "Danisete", "Erick", "Fernando", 
            "Gilmar", "Igor", "Israel", "Joao Victor", "Jilson", "Marco Antonio", 
            "Manoel", "Mario", "Nilton", "Reginaldo", "Washigton", "Vitor Hugo", 
            "Josue", "Juliano", "Oseias", "Valdinei"
            ]

placas = [
        "2E21", "8H52", "3833", "0048", "2645", "1270",
        "1079", "6D17", "7J38", "7246", "9004", "1528",
        "9C47", "0D86", "9543", "8847", "6179", "8G63",
        "6062", "2H13", "9701", "3125", "9H71", "3J16" 
        ]

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
        on_click=lambda e: show_confirm_pop_up(),  # Abre o pop-up de confirmação ao clicar
        disabled=True,  # Desabilitado inicialmente
        tooltip="Os campos KM atual e KM da próxima troca de óleo são obrigatórios."
    )

    cancel_button = ft.ElevatedButton(
        text="Cancelar", 
        on_click=lambda e: show_cancel_confirmation_dialog(),
    )

    # Função para exibir o pop-up de confirmação de cancelamento
    def show_cancel_confirmation_dialog():
        dialog = AlertDialog(
            title=Text("Deseja cancelar o envio do formulário?"),
            content=Text("Você tem certeza que deseja cancelar?"),
            actions=[
                ft.TextButton(text="Sim", on_click=lambda e: cancel_form(dialog)),  # Cancela e fecha o app
                ft.TextButton(text="Não", on_click=lambda e: close_dialog(dialog)),  # Fecha o pop sem cancelar
            ]
        )
        page.add(dialog)
        dialog.open = True
        page.update()

    def cancel_form(dialog):
        # Fecha a aplicação se o usuário clicar "Sim"
        dialog.open = False
        page.update()
        page.window.destroy()

    def close_dialog(dialog):
        # Apenas fecha o pop-up
        dialog.open = False
        page.update()

    # Função para exibir o pop-up de confirmação de envio
    def show_confirm_pop_up():
        # Exclui a mensagem "Formulário Enviado!"
        for control in page.controls:
            if isinstance(control, ft.Text) and control.value == "Formulário Enviado!":
                page.controls.remove(control)

        # Criação do pop-up com altura ajustada
        dialog = AlertDialog(
            title=ft.Row(
                controls=[ft.Text("Confirmar envio", size=18, weight=FontWeight.BOLD)],  # Coloca o título dentro de uma Row
                alignment=ft.MainAxisAlignment.CENTER,  # Alinha o título no centro
            ),
            content=ft.Column(
                controls=[
                    ft.Text("Escolha o motorista:", size=15),
                    ft.Dropdown(
                        options=[ft.dropdown.Option(motorista) for motorista in motoristas],
                        width=250,
                        value=None,
                        label="Motorista",
                        height=40,  # Ajusta a altura do dropdown
                    ),
                    ft.Text("Escolha a placa do caminhão:", size=15),
                    ft.Dropdown(
                        options=[ft.dropdown.Option(placa) for placa in placas],
                        width=250,
                        value=None,
                        label="Placa do caminhão",
                        height=40,  # Ajusta a altura do dropdown
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=5  # Ajusta o espaçamento entre os controles
            ),
            actions=[
                ft.TextButton(text="Enviar", on_click=lambda e: send_form(dialog)),
                ft.TextButton(text="Cancelar", on_click=lambda e: close_dialog(dialog)),
            ],
        )
    
        # Ajuste o tamanho da coluna de conteúdo diretamente para controlar a altura
        dialog.content.height = 200  # Limitando a altura do conteúdo
    
        page.add(dialog)
        dialog.open = True
        page.update()

    def send_form(dialog):
        # Aqui você pode adicionar a lógica de envio do formulário (salvar ou enviar os dados)
        page.add(ft.Text("Formulário Enviado!"))
        close_dialog(dialog)  # Fecha o pop-up após o envio

    def close_dialog(dialog):
        # Apenas fecha o pop-up
        dialog.open = False
        page.update()

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

        # Verifica se algum dos campos de KM está vazio
        if km_atual_value == "" or km_proxima_value == "":
            submit_button.disabled = True  # Desabilita o botão de envio
            submit_button.tooltip = "Os campos KM atual e KM da próxima troca de óleo são obrigatórios."
            page.update()
            return  # Não prossegue com a validação se algum campo estiver vazio

        try:
            # Tenta converter os valores para float (considerando números decimais também)
            km_atual_value = float(km_atual_value)
            km_proxima_value = float(km_proxima_value)

            # Verifica se o KM da próxima troca é maior que o KM atual
            if km_proxima_value <= km_atual_value:
                return  # Não prossegue com o envio se houver erro

            # Se passou nas validações, habilita o botão de envio
            submit_button.disabled = False
            submit_button.tooltip = ""  # Limpa o tooltip de erro
            page.update()
        
        except ValueError:
            # Se algum valor não for convertido corretamente (por exemplo, letras em vez de números)
            show_alert("Valor informado inválido", "Por favor, insira números válidos para os campos KM.")
            submit_button.disabled = True  # Desabilita o botão de envio em caso de erro
            submit_button.tooltip = "Os campos KM devem ser numéricos."
            page.update()

    def show_alert(title, message):
        # Função para exibir o pop-up de erro
        dialog = AlertDialog(
            title=Text(title),
            content=Text(message),
            actions=[
                ft.TextButton(text="OK", on_click=lambda e: close_alert(dialog))  # Usando a função close_alert
            ]
        )
        page.add(dialog)
        dialog.open = True
        page.update()

    def close_alert(dialog):
        # Função para fechar o alerta
        dialog.open = False
        page.update()  # Atualiza a página para refletir a mudança

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
                ft.Row(controls=[submit_button, cancel_button], spacing=10),  # Botões lado a lado
            ],
            alignment=MainAxisAlignment.CENTER, horizontal_alignment=CrossAxisAlignment.CENTER,
        )
    )

# Alteração: Permitir conexões externas com "host='0.0.0.0'"
ft.app(target=main, host="0.0.0.0", port=8550)
