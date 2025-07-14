import flet as ft
import types # Importado para usar types.SimpleNamespace na simulação de eventos do teclado


ACCENT_BLUE = "#00ccff" # Azul Vibrante
ACCENT_GREEN = "#00ff99" # Verde Neon
ACCENT_PURPLE = "#8a2be2" # Roxo usado no gradiente do nome no portfólio
DARK_BG = "#0e0e0e" # Fundo principal bem escuro
MID_DARK_BG = "#1a1a1a" # Fundo de containers e caixas
LIGHT_DARK_BG = "#222222" # Fundo de botões e campos de input
TEXT_LIGHT = "#f0f0f0" # Cor principal para o texto claro
TEXT_MEDIUM = "#ccc" # Cor secundária para o texto
TEXT_DARK = "#0e0e0e" # Cor do texto em elementos de fundo claro

class CalculatorApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "Minha Calculadora Flet Avançada" # Título da janela do aplicativo
        self.page.vertical_alignment = ft.MainAxisAlignment.END # Alinha o conteúdo principal ao final da página
        self.page.window_width = 340 # Largura definida para a janela da calculadora
        self.page.window_height = 560 # Altura definida para a janela da calculadora
        self.page.window_resizable = False # Impede que o usuário redimensione a janela
        self.page.bgcolor = DARK_BG # Define a cor de fundo da janela

        self.current_expression = "0" # Armazena a expressão atual no display
        self.last_result = None # Guarda o último resultado após o cálculo para continuar operações

        # Configuração do campo de texto de exibição da calculadora
        self.txt_number = ft.TextField(
            width=300, 
            height=60, # Altura maior para o display
            text_align=ft.TextAlign.CENTER, # Alinhamento central do texto no display
            multiline=False, # Impede múltiplas linhas no display
            value="0", # Valor inicial do display
            read_only=True, # Torna o campo de texto somente leitura (usuário não pode digitar direto)
            border_color=LIGHT_DARK_BG, # Cor da borda do campo
            text_size=40, # Tamanho da fonte do texto no display
            color=TEXT_LIGHT, # Cor do texto no display
            content_padding=10, # Espaçamento interno do conteúdo
        )

        self.setup_ui() # Chama a função para montar a interface
        self.setup_keyboard_events() # Ativa o reconhecimento de eventos do teclado

    def setup_ui(self):
        # Texto para exibir o histórico de operações (acima do display principal)
        self.operation_history_text = ft.Text(value="", size=14, color=TEXT_MEDIUM, text_align=ft.TextAlign.RIGHT, width=300)

        # Contêiner que agrupa o histórico e o display numérico
        display_container = ft.Column(
            [
                self.operation_history_text,
                self.txt_number,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.END, # Alinha o display e histórico à direita
            spacing=5, # Espaçamento entre os elementos do display
            width=320 # Garante a largura para alinhamento correto
        )
        
        # Definição do layout dos botões da calculadora em uma lista de listas
        buttons_layout = [
            ["AC", "DEL", "%", "/"],
            ["7", "8", "9", "x"],
            ["4", "5", "6", "-"],
            ["1", "2", "3", "+"],
            ["0", ".", "="]
        ]

        # Processa o layout e cria as linhas de botões Flet
        rows = []
        for row_values in buttons_layout:
            controls = []
            for value in row_values:
                btn = self.create_button(value) # Cria cada botão individualmente
                controls.append(btn)
            
            # Adiciona a linha de botões à lista de linhas da página, com alinhamento e espaçamento
            rows.append(ft.Row(controls=controls, alignment=ft.MainAxisAlignment.CENTER, spacing=5))

        # Adiciona os elementos de interface à página Flet
        self.page.add(
            ft.Container(
                content=display_container,
                padding=ft.padding.all(10), # Espaçamento ao redor do contêiner do display
                alignment=ft.alignment.center # Alinha o contêiner do display ao centro da página
            ),
            ft.Column(controls=rows, alignment=ft.MainAxisAlignment.START, spacing=5) # Coluna que organiza as linhas de botões verticalmente
        )
        self.page.update() # Atualiza a interface para mostrar os elementos

    def create_button(self, value):
        # Estilo base para todos os botões, definindo forma e padding
        button_base_style = ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=8), # Cantos levemente arredondados
            padding=15, # Espaçamento interno do botão
            animation_duration=150, # Duração da animação ao clicar
        )

        # Define o estilo e comportamento de cada botão com base no seu valor
        if value.isdigit() or value == ".":
            return ft.ElevatedButton(
                text=value, 
                width=70, height=70, # Tamanho padrão dos botões numéricos
                on_click=self.button_clicked, # Chama a função ao clicar
                style=button_base_style,
                bgcolor=LIGHT_DARK_BG, # Cor de fundo para dígitos e ponto
                color=TEXT_LIGHT, # Cor do texto do botão
                on_hover=lambda e: self.on_button_hover(e, is_number=True) # Efeito visual ao passar o mouse
            )
        elif value == "AC":
            return ft.ElevatedButton(
                text=value, 
                width=70, height=70,
                on_click=self.clear_all_click, # Chama função para limpar tudo
                style=button_base_style,
                bgcolor=ACCENT_GREEN, # Cor verde neon para o botão "AC"
                color=TEXT_DARK, # Texto escuro no botão verde
                on_hover=lambda e: self.on_button_hover(e, is_operator=True)
            )
        elif value == "DEL":
            return ft.ElevatedButton(
                text=value, 
                width=70, height=70,
                on_click=self.backspace_click, # Chama função para apagar último caractere
                style=button_base_style,
                bgcolor=ft.Colors.GREY_700, # Cor cinza escuro para o botão "DEL"
                color=TEXT_LIGHT,
                on_hover=lambda e: self.on_button_hover(e, is_operator=True)
            )
        elif value in ["/", "x", "-", "+", "%"]: # Botões de operação
            return ft.ElevatedButton(
                text=value, 
                width=70, height=70,
                on_click=self.operation_click, # Chama função para operadores
                style=button_base_style,
                bgcolor=ACCENT_BLUE, # Cor azul vibrante para operadores
                color=TEXT_DARK, # Texto escuro no botão azul
                on_hover=lambda e: self.on_button_hover(e, is_operator=True)
            )
        elif value == "=":
            # Botão de igual com largura expandida e cor de destaque
            return ft.ElevatedButton(
                text=value, 
                width=155, height=70, # Ocupa largura de dois botões
                on_click=self.calculate_click, # Chama função de cálculo
                style=button_base_style,
                bgcolor=ACCENT_GREEN, # Verde Neon para o botão de igual
                color=TEXT_DARK,
                on_hover=lambda e: self.on_button_hover(e, is_operator=True)
            )
        elif value == "0":
            # Botão zero com largura expandida
            return ft.ElevatedButton(
                text=value, 
                width=155, height=70, # Ocupa largura de dois botões
                on_click=self.button_clicked,
                style=button_base_style,
                bgcolor=LIGHT_DARK_BG, 
                color=TEXT_LIGHT,
                on_hover=lambda e: self.on_button_hover(e, is_number=True)
            )
        else: # Caso haja algum botão não mapeado (segurança)
            return ft.ElevatedButton(text=value, on_click=self.button_clicked)

    def on_button_hover(self, e, is_number=False, is_operator=False):
        # Implementa um efeito de sombra e elevação ao passar o mouse sobre os botões
        if e.data == "true": # Mouse entrou no botão
            e.control.elevation = 8 # Aumenta a elevação (efeito 3D)
            e.control.shadow = ft.BoxShadow( # Adiciona uma sombra colorida
                spread_radius=1, blur_radius=6,
                color=ACCENT_BLUE if is_operator else (ACCENT_GREEN if is_number else ft.Colors.WHITE),
                offset=ft.Offset(0, 0),
                blur_style=ft.ShadowBlurStyle.OUTER,
            )
        else: # Mouse saiu do botão
            e.control.elevation = 2 # Volta à elevação normal
            e.control.shadow = None # Remove a sombra
        self.page.update() # Atualiza a página para mostrar a mudança visual

    # --- Lógica da Calculadora (Funções de Click e Teclado) ---
    def button_clicked(self, e):
        # Lida com cliques nos botões numéricos e ponto decimal
        if self.txt_number.value == "0" or self.txt_number.value == "Erro" or \
           self.txt_number.value == "Div/0!" or self.last_result:
            self.txt_number.value = e.control.text # Substitui o "0" ou erro pelo novo número
            self.last_result = None # Limpa o último resultado guardado
        else:
            self.txt_number.value += e.control.text # Adiciona o número ao final da expressão
        self.page.update() # Atualiza o display

    def clear_all_click(self, e):
        # Limpa o display principal e o histórico de operações
        self.txt_number.value = "0"
        self.operation_history_text.value = ""
        self.last_result = None
        self.page.update()

    def backspace_click(self, e):
        # Apaga o último caractere do display
        if self.txt_number.value == "0" or self.txt_number.value == "Erro" or self.txt_number.value == "Div/0!":
            return # Não faz nada se já for "0" ou erro
        if len(self.txt_number.value) > 1:
            self.txt_number.value = self.txt_number.value[:-1] # Remove o último caractere
        else:
            self.txt_number.value = "0" # Volta para "0" se só houver um caractere
        self.page.update()

    def calculate_click(self, e):
        # Realiza o cálculo da expressão
        try:
            expression = self.txt_number.value.replace("x", "*") # Substitui 'x' por '*' para que 'eval' entenda

            # Lógica para evitar divisão por zero explícita antes do eval (melhora a mensagem de erro)
            if "/0" in expression and not "/0." in expression: # Verifica se é algo como "5/0", mas não "5/0.5"
                raise ZeroDivisionError 
            
            # Salva a expressão atual no histórico antes de mostrar o resultado
            self.operation_history_text.value = self.txt_number.value + " ="
            
            result = str(eval(expression)) # Usa eval() para calcular a expressão (atenção: eval() pode ser perigoso com inputs não confiáveis)
            self.txt_number.value = result # Exibe o resultado
            self.last_result = result # Armazena o resultado para futuras operações
        except ZeroDivisionError:
            self.txt_number.value = "Div/0!" # Mensagem específica para divisão por zero
            self.last_result = None
        except SyntaxError:
            self.txt_number.value = "Sintaxe Erro!" # Mensagem para erros de sintaxe na expressão
            self.last_result = None
        except Exception: # Captura outros erros genéricos que podem ocorrer (ex: operador no final da expressão)
            self.txt_number.value = "Erro!" # Mensagem genérica de erro
            self.last_result = None
        self.page.update()

    def operation_click(self, e):
        # Lida com cliques nos botões de operação (+, -, x, /)
        op = e.control.text # Pega o operador clicado
        
        # Não permite adicionar operador se o display está vazio (exceto para sinal negativo inicial)
        if not self.txt_number.value and op != "-":
            return 
        
        # Se o último caractere já é um operador, substitui-o pelo novo
        if self.txt_number.value and self.txt_number.value[-1] in ["+", "-", "x", "/"] and op in ["+", "-", "x", "/"]:
            self.txt_number.value = self.txt_number.value[:-1] + op 
        # Se um resultado anterior foi exibido, o operador se aplica a esse resultado
        elif self.last_result:
            self.txt_number.value = self.last_result + op
            self.last_result = None # Limpa o último resultado para uma nova expressão
        else:
            self.txt_number.value += op # Adiciona o operador
        self.page.update()

    def setup_keyboard_events(self):
        # Configura o manipulador de eventos de teclado para a página
        self.page.on_keyboard_event = self.on_keyboard_input

    def on_keyboard_input(self, e: ft.KeyboardEvent):
        key = e.key # Pega a tecla pressionada

        # Ignora eventos de teclas de controle (Ctrl, Alt, Shift sozinhas) para evitar comportamento indesejado
        if e.ctrl or e.alt or e.shift:
            return

        # Cria um objeto de evento simples que imita a estrutura de um clique de botão
        # Isso permite que as funções de clique (button_clicked, operation_click) sejam reutilizadas
        class DummyControl:
            def __init__(self, text):
                self.text = text

        # Mapeamento de teclas do teclado para ações da calculadora
        if key.isdigit() or key == ".":
            self.button_clicked(types.SimpleNamespace(control=DummyControl(key))) # Simula clique de botão numérico
        elif key == "+" or key == "-" or key == "/":
            self.operation_click(types.SimpleNamespace(control=DummyControl(key))) # Simula clique de operador
        elif key == "*": # O teclado usa '*' para multiplicação, mapeia para 'x' da UI
            self.operation_click(types.SimpleNamespace(control=DummyControl("x"))) 
        elif key == "Enter": # Tecla Enter para calcular
            self.calculate_click(None)
        elif key == "Backspace": # Tecla Backspace para apagar
            self.backspace_click(None)
        elif key == "Escape": # Tecla Escape para limpar tudo
            self.clear_all_click(None)
        
        # Impede que o navegador processe a ação padrão de certas teclas (ex: Backspace voltar página, Enter submeter form)
        if key == "Enter" or key == "Escape" or key == "Backspace":
            e.page.prevent_default_action = True 
            
        self.page.update() # Atualiza a interface para refletir a ação do teclado

# A linha abaixo inicia a aplicação Flet
# ft.app(target=main_app_instance) # Para rodar como desktop app (requer flet.exe no PATH e configurado)

def main_app_instance(page: ft.Page):
    CalculatorApp(page)

# Rodar a aplicação Flet
# Use a linha abaixo se o seu 'flet run calculadora.py' estiver funcionando e abrindo no desktop:
ft.app(target=main_app_instance) 

# Se o acima não funcionar ou preferir no navegador (com hot reload):
# ft.app(target=main_app_instance, view=ft.AppView.WEB_BROWSER)
