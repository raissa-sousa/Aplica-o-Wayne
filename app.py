import flet as ft
import time
import json

# SENHAS PARA CADA TIPO DE USUÁRIO
SENHAS = {
    "Funcionário": "123",
    "Gerente": "456",
    "ADM_SEGURANÇA": "789"
}


# Página anterior para navegação
pagina_anterior = None


# PÁGINA DE LOGIN

def login(page):
    usuario_input = ft.Dropdown(
        label="Escolha o Tipo de Usuário",
        options=[
            ft.dropdown.Option("Funcionário"),
            ft.dropdown.Option("Gerente"),
            ft.dropdown.Option("ADM_SEGURANÇA")
        ],
        width=250,
        autofocus=True
    )
    
    senha_input = ft.TextField(label="Senha", password=True, width=250)

    def verificar_login(e):
        usuario = usuario_input.value
        senha = senha_input.value
        if usuario and senha and SENHAS.get(usuario) == senha:
            page.clean()
            exibir_menu(page, usuario)  # Passar o tipo de usuário
        else:
            page.add(ft.Text("Senha incorreta ou usuário inválido", color="red"))

    login_button = ft.OutlinedButton("Login", on_click=verificar_login)
    page.add(ft.Column(
            [
                usuario_input,
                senha_input,
                login_button
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20  # Ajuste no espaçamento entre os componentes
        )
    )

#------------------------------------------------------------------------------------------------------------------------------------------------------

# PÁGINA DO MENU

# Função para renderizar o menu com base no tipo de usuário
def exibir_menu(page, usuario):
    page.title = "Indústrias Wayne"
    page.padding = 0
    page.scroll = ft.ScrollMode.AUTO

    img = ft.Image(src="IMAGENS/image01.png", width=700, height=400)

    # Exibir o texto solicitando ao usuário escolher a área
    texto_instrucoes = ft.Text("ESCOLHA A ÁREA QUE DESEJA ACESSAR:", size=20, weight="bold", color="white")

    # Menu com as opções
    row = ft.Row(
        [
            ft.Container(
                content=ft.Image(src="IMAGENS/recursos.png"),
                margin=2,
                padding=2,
                alignment=ft.alignment.center,
                width=250,
                height=200,
                border_radius=10,
                on_click=lambda e: verificar_acesso(page, usuario, "RECURSOS"),
            ),
            ft.Container(
                content=ft.Image(src="IMAGENS/segurança.png"),
                margin=2,
                padding=2,
                alignment=ft.alignment.center,
                width=250,
                height=200,
                border_radius=10,
                on_click=lambda e: verificar_acesso(page, usuario, "SEGURANÇA"),
            ),
            ft.Container(
                content=ft.Image(src="IMAGENS/atividades.png"),
                margin=2,
                padding=2,
                alignment=ft.alignment.center,
                width=250,
                height=200,
                border_radius=10,
                on_click=lambda e: verificar_acesso(page, usuario, "ATIVIDADES"),
            ),
        ],
        alignment=ft.MainAxisAlignment.CENTER  # Centralizar horizontalmente os botões
    )

    botao_sair = ft.OutlinedButton("Sair", on_click=lambda e: sair_e_abrir_login(page))  # Voltar à tela de login
    
    # Organizar todos os elementos em uma única coluna
    layout = ft.Column(
        [
            img,  # Imagem no topo
            texto_instrucoes,  # Texto de instruções
            row,  # Linha com os botões
            botao_sair  # Botão Sair no final
        ],
        alignment=ft.MainAxisAlignment.CENTER,  # Centralizar todos os itens verticalmente
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,  # Centralizar todos os itens horizontalmente
        expand=True  # Expandir para ocupar a altura total da página
    )
    
    # Limpar a página e adicionar o layout centralizado
    page.clean()
    page.add(layout)

    # Função para a ação do botão "Sair" (limpar a página de menu e voltar ao login)
def sair_e_abrir_login(page):
    page.clean()  # Limpar a página de menu
    time.sleep(0.1)  # Pausa de meio segundo (100 ms) antes de reabrir a página de login
    main(page)  # Chamar a função de login para reabrir a tela de login

# Função para verificar o acesso aos menus
def verificar_acesso(page, usuario, menu):
    global pagina_anterior  # Usar variável global para controlar a página anterior
    pagina_anterior = menu  # Armazenar a página atual como anterior
    page.clean()

    # Se o menu for "SEGURANÇA" ou "ATIVIDADES" e o usuário for um "Funcionário", negar o acesso
    if (menu == "SEGURANÇA" or menu == "ATIVIDADES") and usuario == "Funcionário":
        # Exibir a mensagem de ACESSO NEGADO! em uma janela pop-up
        exibir_popup_acesso_negado(page, usuario)
    else:
        # Se o usuário tiver permissão, mostrar os respectivos conteúdos
        if menu == "SEGURANÇA":
            exibir_SEGURANCA(page, usuario)
        elif menu == "ATIVIDADES":
            exibir_atividades(page, usuario)
        elif menu == "RECURSOS":
            exibir_RECURSOS(page, usuario)

# Função para exibir a janela pop-up de ACESSO NEGADO!
def exibir_popup_acesso_negado(page, usuario):
    acesso_negado_dialog = ft.AlertDialog(
        title=ft.Text("ACESSO NEGADO!"),
        content=ft.Text("Você não tem permissão para acessar esta área."),
        actions=[
            ft.TextButton("Fechar", on_click=lambda e: fechar_pop_up_e_voltar(page, usuario))  # Fechar o pop-up e voltar ao menu
        ]
    )
    page.dialog = acesso_negado_dialog
    page.dialog.open = True
    page.update()

# Função para fechar o pop-up e voltar ao menu
def fechar_pop_up_e_voltar(page, usuario):
    if page.dialog:
        page.dialog.open = False
        page.update()
        time.sleep(0.1)  # Pequeno atraso para garantir a atualização visual
        page.dialog = None
    exibir_menu(page, usuario)
    page.update()


#-------------------------------------------------------------------------------------------------------------------------------------------

# PÁGINA DE RECURSOS

# Caminho do arquivo JSON
ARQUIVO_DADOS = "dados.json"

# Funções para carregar e salvar dados
def carregar_dados():
    try:
        with open(ARQUIVO_DADOS, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {
            "equipamentos": [{"id": 1, "nome": "Computador", "tipo": "Tecnologia", "status": "Ativo"}],
            "veiculos": [{"id": 1, "nome": "Batmóvel", "tipo": "Veículo", "status": "Ativo"}],
            "seguranca": [{"id": 1, "nome": "Câmera", "tipo": "SEGURANÇA", "status": "Ativa"}]
        }

def salvar_dados(dados):
    with open(ARQUIVO_DADOS, "w") as f:
        json.dump(dados, f, indent=4)

# Carregando os dados ao iniciar a aplicação
RECURSOS = carregar_dados()

# Função para renderizar os RECURSOS
def exibir_RECURSOS(page, usuario):

    # Inserindo imagem no background
    background = ft.Container(
        width="100%",
        height="100%",
        content=ft.Image(
            src="IMAGENS/fundo1.png",
            fit=ft.ImageFit.COVER,
            repeat=ft.ImageRepeat.REPEAT,
        ),
        alignment=ft.alignment.top_left,
        expand=True,
    )

    def atualizar_tabela(nome_tabela):
        return ft.Container(
            content=ft.DataTable(
                columns=[
                    ft.DataColumn(ft.Text("ID")),
                    ft.DataColumn(ft.Text("Nome")),
                    ft.DataColumn(ft.Text("Tipo")),
                    ft.DataColumn(ft.Text("Status")),
                    ft.DataColumn(ft.Text("Ações")),
                ],
                rows=[
                    ft.DataRow(cells=[
                        ft.DataCell(ft.Text(str(item["id"]))),
                        ft.DataCell(ft.Text(item["nome"])),
                        ft.DataCell(ft.Text(item["tipo"])),
                        ft.DataCell(ft.Text(item["status"])),
                        ft.DataCell(
                            ft.Row([
                                ft.IconButton(
                                    icon=ft.icons.EDIT,
                                    on_click=lambda e, item=item: editar_item(nome_tabela, item, page)
                                ),
                                ft.IconButton(
                                    icon=ft.icons.DELETE,
                                    on_click=lambda e, item=item: remover_item(nome_tabela, item, page)
                                )
                            ])
                        )
                    ]) for item in RECURSOS[nome_tabela]
                ]
            ),
            border=ft.border.all(3, ft.colors.WHITE),  # Adicionando borda de 3px e cor branca
            padding=10,  # Adicionando um pouco de padding
            margin=10,  # Espaçamento externo
            border_radius=10
        )

    def editar_item(nome_tabela, item, page):
        def salvar_edicao(e):
            item["nome"] = input_nome.value
            item["tipo"] = input_tipo.value
            item["status"] = input_status.value
            salvar_dados(RECURSOS)  # Salvar alterações no arquivo
            fechar_dialog()  # Fechar o diálogo após salvar
            exibir_RECURSOS(page, usuario)

        def fechar_dialog():
            page.dialog.open = False  # Fechar o diálogo
            page.update()  # Atualizar a página
            time.sleep(0.1)  # Adicionando atraso para garantir a atualização visual

        input_nome = ft.TextField(label="Nome", value=item["nome"])
        input_tipo = ft.TextField(label="Tipo", value=item["tipo"])
        input_status = ft.TextField(label="Status", value=item["status"])

        dialog = ft.AlertDialog(
            title=ft.Text("Editar Item"),
            content=ft.Column([input_nome, input_tipo, input_status]),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: fechar_dialog()),  # Fechar diálogo ao cancelar
                ft.TextButton("Salvar", on_click=salvar_edicao),  # Fechar diálogo ao salvar
            ]
        )
        page.dialog = dialog
        page.dialog.open = True
        page.update()  # Garantir a atualização da página para refletir as mudanças

    def adicionar_item(nome_tabela):
        def salvar_adicao(e):
            novo_id = max([item["id"] for item in RECURSOS[nome_tabela]]) + 1 if RECURSOS[nome_tabela] else 1
            RECURSOS[nome_tabela].append({
                "id": novo_id,
                "nome": input_nome.value,
                "tipo": input_tipo.value,
                "status": input_status.value,
            })
            salvar_dados(RECURSOS)  # Salvar alterações no arquivo
            fechar_dialog()  # Fechar o diálogo após salvar
            exibir_RECURSOS(page, usuario)

        def fechar_dialog():
            page.dialog.open = False  # Fechar o diálogo
            page.update()  # Atualizar a página
            time.sleep(0.1)  # Adicionando atraso para garantir a atualização visual

        input_nome = ft.TextField(label="Nome")
        input_tipo = ft.TextField(label="Tipo")
        input_status = ft.TextField(label="Status")

        dialog = ft.AlertDialog(
            title=ft.Text("Adicionar Item"),
            content=ft.Column([input_nome, input_tipo, input_status]),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: fechar_dialog()),  # Fechar diálogo ao cancelar
                ft.TextButton("Salvar", on_click=salvar_adicao),  # Fechar diálogo ao salvar
            ]
        )
        page.dialog = dialog
        page.dialog.open = True
        page.update()  # Garantir a atualização da página para refletir as mudanças

    def remover_item(nome_tabela, item, page):
        RECURSOS[nome_tabela].remove(item)
        salvar_dados(RECURSOS)  # Salvar alterações no arquivo
        exibir_RECURSOS(page,usuario)

    # Layout da página com as tabelas
    page.clean()
    content = ft.Column([
        ft.Container(
            content=ft.Text("GESTÃO DE RECURSOS", size=24, weight="bold"),
            padding=25
        ),
        ft.Divider(color=ft.colors.GREY, thickness=2, height=20),

        ft.Text("EQUIPAMENTOS", size=20, weight="bold"),
        atualizar_tabela("equipamentos"),
        ft.OutlinedButton("Adicionar Equipamento", on_click=lambda e: adicionar_item("equipamentos")),

        ft.Divider(color=ft.colors.GREY, thickness=2, height=20),

        ft.Text("VEÍCULOS", size=20, weight="bold"),
        atualizar_tabela("veiculos"),
        ft.OutlinedButton("Adicionar Veículo", on_click=lambda e: adicionar_item("veiculos")),

        ft.Divider(color=ft.colors.GREY, thickness=2, height=20),

        ft.Text("RECURSOS de SEGURANÇA", size=20, weight="bold"),
        atualizar_tabela("seguranca"),
        ft.OutlinedButton("Adicionar Recurso de Segurança", on_click=lambda e: adicionar_item("seguranca")),

        ft.Divider(color=ft.colors.GREY, thickness=2, height=20),

        ft.OutlinedButton("Voltar", on_click=lambda e: voltar(page, usuario))
    ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER,)

    layout = ft.Stack([background, content])

    page.add(layout)

#--------------------------------------------------------------------------------------------------------------------------------------------------------------

# PÁGINA DE SEGURANÇA

# Caminho do arquivo json de segurança
ARQUIVO_SEGURANCA = "seguranca_dados.json"

# Função para carregar os dados de segurança
def carregar_dados_seguranca():
    try:
        with open(ARQUIVO_SEGURANCA, "r", encoding='utf-8') as f:  # Adicionando encoding='utf-8'
            return json.load(f)
    except FileNotFoundError:
        return SEGURANCA


# Função para salvar os dados de segurança no arquivo
def salvar_dados_seguranca(dados):
    with open(ARQUIVO_SEGURANCA, "w", encoding='utf-8') as f:  # Adicionando encoding='utf-8'
        json.dump(dados, f, indent=4),

# Carregando os dados ao iniciar a aplicação
SEGURANCA = carregar_dados_seguranca()

# Função para renderizar SEGURANÇA
def exibir_SEGURANCA(page, usuario):

    # Inserindo imagem no background
    background = ft.Container(
        width=page.window_width,
        height=page.window_height,
        image_src="IMAGENS/fundo1.png",  # Caminho para a imagem
        image_fit=ft.ImageFit.COVER,  # Ajusta como a imagem é exibida
        alignment=ft.alignment.center,
    )

    # Função para salvar os dados editados
    def salvar_edicao(index, novo_valor):
        try:
            # Garantir que o valor é numérico
            novo_valor = int(novo_valor)

            # Encontra o dado com base no índice (id) e atualiza o valor
            SEGURANCA['dados'][index]['valor'] = novo_valor

            # Atualiza os dados no arquivo JSON
            salvar_dados_seguranca(SEGURANCA)   # Salvar alterações no arquivo
            fechar_dialog_SEGURANCA()  # Fechar o diálogo após salvar
            exibir_SEGURANCA(page, usuario)
        
        except ValueError:
            # Em caso de erro, exibe uma mensagem de erro (se o valor não for um número válido)
            page.dialog.content = ft.Text("Por favor, insira um número válido!")
            page.update()

    # Fechar o pop-up após salvar os dados
    def fechar_dialog_SEGURANCA():
        page.dialog.open = False  # Fechar o diálogo
        page.controls.clear()
        page.update()  # Atualizar a página
        time.sleep(0.1)  # Adicionando atraso para garantir a atualização visual     
        exibir_SEGURANCA(page, usuario)
        
    # Função para abrir o pop-up de edição
    def abrir_edicao(index, dados):
        # Campo de edição - somente números serão permitidos
        input_field = ft.TextField(value=dados, label="Editar dado", keyboard_type=ft.KeyboardType.NUMBER)

        # Pop-up de edição
        pop_up = ft.AlertDialog(
            title=ft.Text("Editar Dados de Segurança"),
            content=ft.Column(
                [
                    input_field,
                    ft.Row(
                        [
                            ft.OutlinedButton("Salvar", on_click=lambda e: salvar_edicao(index, input_field.value)),
                            ft.OutlinedButton("Cancelar", on_click=lambda e: fechar_dialog_SEGURANCA()),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=10,
                    ),
                ],
                tight=True,
            ),
        )

        # Adiciona e abre o pop-up
        page.dialog = pop_up  # Associa o diálogo à página
        pop_up.open = True     # Abre o diálogo
        page.update()          # Atualiza a página para exibir o pop-up

    # Atualizar a lista de contêineres para refletir os dados atualizados
    conteineres = [
        ft.Container(
            content=ft.Stack(   # Para sobrepor o texto à imagem
                [
                    ft.Image(src="IMAGENS/borda.png", width=300, height=250),
                    ft.Column(  # Column para empilhar o texto e o botão
                        [
                            # Concatenando nome, valor e tipo em uma única string
                            ft.Text(
                                f"{dados['nome']}:",
                                size=16,
                                weight=ft.FontWeight.BOLD,
                                text_align=ft.TextAlign.CENTER,
                                color=ft.colors.WHITE,
                                opacity=1,
                                max_lines=2,  
                                overflow=ft.TextOverflow.ELLIPSIS,  # Adiciona '...' se o texto for muito longo
                                width=200,  # Limita a largura do texto
                            ),
                            ft.Text(
                                f"Valor: {dados['valor']}{dados['tipo']}",
                                size=16,
                                weight=ft.FontWeight.BOLD,
                                text_align=ft.TextAlign.CENTER,
                                color=ft.colors.WHITE,
                                opacity=1,
                                max_lines=1,  # Garantir que não quebre a linha de forma inesperada
                                width=200,
                            ),
                            ft.IconButton(
                                icon=ft.icons.EDIT,
                                icon_size=24,
                                on_click=lambda e, index=i: abrir_edicao(index, dados['valor']),  # Passa o índice e valor para edição
                                icon_color=ft.colors.WHITE,
                                tooltip="Editar",
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,  # Alinha o conteúdo do Column no centro
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,  # Centraliza o conteúdo horizontalmente
                        spacing=10,  # Espaçamento entre o texto e o botão
                    ),
                ],
                alignment=ft.alignment.center,  # Alinha o conteúdo do Stack no centro
            ),
            padding=10,
            bgcolor="rgba(0, 0, 0, 0.7)", 
            border_radius=10,
            margin=10,
            width=300,  
            height=250, 
        )
        for i, dados in enumerate(SEGURANCA['dados'])  # Iterando sobre a lista de 'dados' no dicionário
    ]

    # Dividir os contêineres em linhas (3 contêineres por linha)
    linhas = [
        ft.Row(conteineres[i:i + 3], alignment=ft.MainAxisAlignment.CENTER, spacing=10)
        for i in range(0, len(conteineres), 3)
    ]

    # Título da seção
    painel_titulo = ft.Column(
        [
            ft.Text(
                "DADOS DE SEGURANÇA",
                size=24,
                weight=ft.FontWeight.BOLD,
                color=ft.colors.WHITE,
                text_align=ft.TextAlign.CENTER,
            ),
            *linhas,
            ft.OutlinedButton("Voltar", on_click=lambda e: voltar(page, usuario)),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=20,
    )

    # Usando Stack para sobrepor o conteúdo ao fundo
    layout = ft.Stack(
        [
            background,  # Fundo da página
            ft.Container(
                content=painel_titulo,
                top=100,  # Ajuste de posicionamento no topo
                left=0,  # Deixa o conteúdo centralizado horizontalmente
                right=0,  # Deixa o conteúdo centralizado horizontalmente
                expand=True,  # O painel de SEGURANÇA se ajusta ao tamanho da página
            ),
        ]
    )

    # Adiciona o layout à página
    page.add(layout)

    # Atualiza a página para refletir a nova estrutura de contêineres
    page.update()


#--------------------------------------------------------------------------------------------------------------------------------------------------------------------


# PÁGINA DE ATIVIDADES

# Caminho do arquivo JSON de atividades
ARQUIVO_ATIVIDADES = "atividades_dados.json"

# Função para carregar os dados de atividades
def carregar_dados_atividades():
    try:
        with open(ARQUIVO_ATIVIDADES, "r", encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

# Função para salvar os dados de atividades
def salvar_dados_atividades(atividades):
    with open(ARQUIVO_ATIVIDADES, "w", encoding='utf-8') as f:
        json.dump(atividades, f, ensure_ascii=False, indent=4)

# Função para criar uma tabela de atividades
def criar_tabela_atividades(categoria, atividades_lista, on_status_change):
    return ft.Container(
        content=ft.DataTable(
            width=500,  # Ajuste da largura da tabela
            columns=[
                ft.DataColumn(label=ft.Text("Atividade", text_align=ft.TextAlign.CENTER, font_family="Neue Machina")),
                ft.DataColumn(label=ft.Text("Status", text_align=ft.TextAlign.CENTER, font_family="Neue Machina"))
            ],
            rows=[
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text(atividade["nome"], text_align=ft.TextAlign.CENTER, font_family="Neue Machina")),
                    ft.DataCell(ft.Container(
                        content=ft.Dropdown(
                            options=[ft.dropdown.Option("Ativo"), ft.dropdown.Option("Inativo")],
                            value=atividade["status"],
                            on_change=lambda e, atv=atividade["nome"]: on_status_change(categoria, atv, e.control.value)
                        ),
                        width=100,  # Ajuste da largura do dropdown
                        alignment=ft.alignment.center
                    ))
                ]) for atividade in atividades_lista
            ],
        ),
        border=ft.border.all(3, ft.colors.WHITE),  # Adicionando borda de 3px e cor branca
        padding=10,  # Adicionando padding interno
        margin=10,  # Adicionando margem externa
        border_radius=10
    )

# Função para renderizar as tabelas de atividades
def exibir_atividades(page, usuario):
    # Carregar os dados de atividades a partir do arquivo JSON
    atividades = carregar_dados_atividades()

    # Função para atualizar o status e salvar no arquivo JSON
    def atualizar_status(categoria, atividade_nome, novo_status):
        for atividade in atividades[categoria]:
            if atividade["nome"] == atividade_nome:
                atividade["status"] = novo_status
                break
        salvar_dados_atividades(atividades)

    # Inserindo imagem no background
    background = ft.Container(
        width="100%",
        height="100%",
        content=ft.Image(
            src="IMAGENS/fundo1.png",
            fit=ft.ImageFit.COVER,
            repeat=ft.ImageRepeat.REPEAT,
        ),
        alignment=ft.alignment.top_left,
        expand=True,
    )

    # Título da página
    titulo = ft.Container(
        content=ft.Text(
            "GERENCIAMENTO DE ATIVIDADES",
            size=24,
            weight=ft.FontWeight.BOLD,
            color=ft.colors.WHITE,
            text_align=ft.TextAlign.CENTER,
            font_family="Neue Machina"
        ),
        padding=20
    )

    # Criar tabelas organizadas em pares (2 tabelas lado a lado) com títulos centralizados
    tabelas = list(atividades.items())
    linha1 = [
        ft.Container(
            content=ft.Column(
                [
                    ft.Text(tabelas[0][0], size=20, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE, text_align=ft.TextAlign.CENTER),
                    criar_tabela_atividades(tabelas[0][0], tabelas[0][1], atualizar_status)
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            ),
            alignment=ft.alignment.center
        ),
        ft.Container(
            content=ft.Column(
                [
                    ft.Text(tabelas[1][0], size=20, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE, text_align=ft.TextAlign.CENTER),
                    criar_tabela_atividades(tabelas[1][0], tabelas[1][1], atualizar_status)
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            ),
            alignment=ft.alignment.center
        )
    ]
    linha2 = [
        ft.Container(
            content=ft.Column(
                [
                    ft.Text(tabelas[2][0], size=20, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE, text_align=ft.TextAlign.CENTER),
                    criar_tabela_atividades(tabelas[2][0], tabelas[2][1], atualizar_status)
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            ),
            alignment=ft.alignment.center
        ),
        ft.Container(
            content=ft.Column(
                [
                    ft.Text(tabelas[3][0], size=20, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE, text_align=ft.TextAlign.CENTER),
                    criar_tabela_atividades(tabelas[3][0], tabelas[3][1], atualizar_status)
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            ),
            alignment=ft.alignment.center
        )
    ]

    # Layout geral usando Rows para as linhas
    content = ft.Column(
        controls=[
            titulo,
            ft.Row(linha1, spacing=20, alignment=ft.MainAxisAlignment.CENTER),
            ft.Row(linha2, spacing=20, alignment=ft.MainAxisAlignment.CENTER),
            ft.Container(
                content=ft.OutlinedButton(
                    "Voltar",
                    on_click=lambda e: voltar(page, usuario)
                ),
                width=150,
                height=50,
                alignment=ft.alignment.center,
                margin=5
            )
        ],
        alignment=ft.MainAxisAlignment.START,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )

    # Adiciona o layout configurado dentro de um Stack
    page.clean()
    page.add(
        ft.Stack([
            background,
            ft.Container(
                content=content,
                padding=20,
                expand=True
            )
        ])
    )
    page.update()  # Atualiza a página


#---------------------------------------------------------------------------------------------------------------------------------------------------------------


# Função para voltar à página anterior
def voltar(page, usuario):
    if pagina_anterior == "RECURSOS":
        exibir_menu(page, usuario)
    elif pagina_anterior == "SEGURANÇA":
        exibir_menu(page, usuario)
    elif pagina_anterior == "ATIVIDADES":
        exibir_menu(page, usuario)
    else:
        login(page)  # Volta para a tela de login caso nenhuma página anterior esteja definida


#--------------------------------------------------------------------------------------------------------------------------------------------------------------

# Função principal do Flet
def main(page: ft.Page):
    page.title = "Indústrias Wayne"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 30
    page.scroll = ft.ScrollMode.AUTO
    page.margin = ft.Margin(top=0, left=0, right=0, bottom=0)
    page.theme = ft.Theme(font_family="Neue Machina")
    page.window_maximized = True

    # Inserindo a imagem
    img_container = ft.Container(
        content=ft.Image(
            src="IMAGENS/logo.png",
            width=700,
            height=350,
            fit=ft.ImageFit.CONTAIN,
        ),
        padding=0,  # Sem espaçamento interno
        margin=0,  # Sem espaçamento externo
        alignment=ft.alignment.center,  # Centraliza a imagem no contêiner
    )

    page.theme = ft.Theme(font_family="Neue Machina",
                color_scheme=ft.ColorScheme(
                primary=ft.colors.WHITE,
                secondary=ft.colors.GREY,
                background=ft.colors.BLACK,
                surface=ft.colors.BLUE,
                ))

    # Inserindo o texto com um container para ajustar a margem
    page.add(
        img_container,
        ft.Container(
            content=ft.Text("CONTROLE DE ACESSO", size=25, weight="bold"),
            margin=ft.Margin(top=0, left=0, right=0, bottom=20),  # Ajustando o espaçamento superior
            padding=ft.Padding(top=0, right=0, bottom=0, left=0),
        ),
    )

    # Iniciar com a tela de login
    login(page)

# Executando a aplicação
ft.app(target=main)





