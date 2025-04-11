
import flet as ft
from flet import AppBar, Text, ElevatedButton, View, Margin, Dropdown
from flet.core.colors import  Colors
from flet.core.dropdown import Option
from flet.core.types import MainAxisAlignment, CrossAxisAlignment
from datetime import datetime


def main(page: ft.Page):
    #Configuração das páginas
    page.title = "Minha Aplicação Flet"
    page.theme_mode = ft.ThemeMode.LIGHT #ou ft.ThemeMode.FFDF9B
    page.window.width = 375
    page.window.height = 667

    def gerenciar_rotas(e):
        page.views.clear()
        page.views.append(
            View(
                "/",
                (
                    ft.Container(
                        ft.Image(src="INSS.png"),
                        margin=30,
                    ),

                    ElevatedButton(text="Simular",
                                       color=ft.Colors.WHITE,
                                       on_click=lambda _: page.go("/simular"),
                                       bgcolor=Colors.BLACK),

                    ElevatedButton(
                        text="Ver regras",
                        color=ft.Colors.BLACK,
                        on_click=lambda _: page.go("/regras"),
                        bgcolor=Colors.WHITE,
                    ),

                ),
                bgcolor='#FFDF9B',
                horizontal_alignment=CrossAxisAlignment.CENTER,
            )
        )

        if page.route == "/simular":
            page.views.append(
                View(
                    "/simular",
                    [
                        AppBar(title=Text("Simular"), bgcolor="#FFDF9B"),
                        input_idade,
                        genero,
                        input_contribuicao,
                        input_salarial,
                        categoria,
                        txt_resultado,
                        ElevatedButton(text="Enviar",
                                       color=ft.Colors.WHITE,
                                       on_click=lambda _: calcular(e),
                                       bgcolor=Colors.BLACK,
                                       width=page.window.width)

                    ],
                    bgcolor = '#FFDF9B',
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                )
            )

        elif page.route == "/regras":
            page.views.append(
                View(
                    "/regras",
                    [
                        AppBar(title=Text("Regras"), bgcolor="#FFDF9B"),
                        ft.Container(
                            content=ft.Text("2.1. Aposentadoria por Idade:\n  2.1.1. Homens: 65"
                             " anos de idade e pelo menos 15 anos de contribuição.\n 2.1.2. Mulheres: 62 anos de idade"
                                            " e pelo menos 15 anos de contribuição.\n"),
                            margin=10,
                            padding=10,
                            alignment=ft.alignment.center,
                            bgcolor=ft.Colors.WHITE,
                            width=300,
                            height=150,
                            border_radius=10,
                        ),
                        ft.Container(
                            content=ft.Text("2.2. Aposentadoria por Tempo de Contribuição:\n"
                                            " 2.2.1. Homens: 35 anos de contribuição.\n "
                                            "2.2.2. Mulheres: 30 anos de contribuição.\n "),
                            margin=10,
                            padding=10,
                            alignment=ft.alignment.center,
                            bgcolor=ft.Colors.WHITE,
                            width=300,
                            height=150,
                            border_radius=10,
                        ),

                        ft.Container(
                            content=ft.Text("2.3. Valor Estimado do Benefício:\n   O valor da aposentadoria será uma média "
                                            "de 60% da média salarial informada,\n acrescido de 2% por ano que exceder o"
                                            " tempo mínimo de contribuição."),
                            margin=10,
                            padding=10,
                            alignment=ft.alignment.center,
                            bgcolor=ft.Colors.WHITE,
                            width=300,
                            height=150,
                            border_radius=10,
                        ),
                    ],
                    bgcolor = '#FFDF9B',
                )
            )

        elif page.route == "/resultado":
            page.views.append(
                View(
                    "/resultado",
                    [

                        AppBar(title=Text("Resultado"), bgcolor="#FFDF9B"),
                        txt_data,
                        txt_valor

                    ],
                    bgcolor = '#FFDF9B',
                )
            )
        page.update()

    def voltar(e):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = gerenciar_rotas
    page.on_view_pop = voltar
    page.go(page.route)

    def conta(e):
        try:
            valor_contri = int(input_contribuicao.value)
            valor_salario = int(input_salarial.value)
            media = (valor_salario * 60)/100
            print(media)
            if valor_contri > 15:
                diferenca = (valor_contri - 15) * 2
                acrescentado = (valor_salario * diferenca) / 100
                resultado = (acrescentado + media)
                return resultado
            else:
                return media

        except Exception as e:
            txt_resultado.value = "As informações devem ser números inteiros."
        except TypeError:
            txt_resultado.value = "fffffffffffff"


    def calcular(e):
        try:
            idade = input_idade.value
            contribuicao = input_contribuicao.value
            salario = input_salarial.value
            teste = not idade.isnumeric()
            print("idade: ",teste)
            if not idade.isnumeric():
                input_idade.error = True
                input_idade.error_text = "Preencha este campo com números inteiros"
                page.update()
            if not contribuicao.isnumeric():
                input_contribuicao.error = True
                input_contribuicao.error_text = "Preencha este campo com números inteiros"
                page.update()
            if not salario.isnumeric():
                input_salarial.error = True
                input_salarial.error_text = "Preencha este campo com números inteiros"
                page.update()


            if not idade:
                idade.error = True
                idade.error_text = "Preencha esse campo"
                page.update()

            if not salario:
                salario.error = True
                salario.error_text = "Preencha esse campo"
                page.update()

            if not contribuicao:
                contribuicao.error = True
                contribuicao.error_text = "Preencha esse campo"
                page.update()

            if not genero.value:
                genero.error = True
                genero.error_text = "Preencha esse campo"
                page.update()

            if not categoria.value:
                categoria.error = True
                categoria.error_text = "Preencha esse campo"
                page.update()

            valor_idade = input_idade.value
            valor_contribuicao = int(input_contribuicao.value)
            valor_salario = int(input_salarial.value)
            resultado_conta = conta(e)


            if genero.value == "masc" and categoria.value == "idade":
                if valor_idade >= 65 and valor_contribuicao >= 15:
                    txt_data.value = "Já atingiu os requisitos para se aposentar."
                    txt_valor.value = f'O valor estimado é R$ {resultado_conta}'

                else:
                    diferenca_idade = abs(valor_idade - 65)
                    diferenca_contribuicao = abs(valor_contribuicao - 15)
                    ano_atual = datetime.today().year
                    data_prevista = abs(ano_atual + diferenca_idade) or abs(ano_atual + diferenca_contribuicao)
                    txt_data.value = f'A data estimada é {data_prevista}'
                    txt_valor.value = f'O valor estimado é R$ {resultado_conta}'

            elif genero.value == "fem" and categoria.value == "idade":
                if valor_idade >= 62 and valor_contribuicao >= 15:
                    txt_data.value = "Já atingiu os requisitos para se aposentar."
                    txt_valor.value = f'O valor estimado é R$ {resultado_conta}'
                else:
                    diferenca_idade = abs(valor_idade - 62)
                    diferenca_contribuicao = abs(valor_contribuicao - 15)
                    ano_atual = datetime.today().year
                    data_prevista = abs(ano_atual + diferenca_idade) or abs(ano_atual + diferenca_contribuicao)
                    txt_data.value = f'A data estimada é {data_prevista}'
                    txt_valor.value = f'O valor estimado é R$ {resultado_conta}'

            if genero.value == "fem" and categoria.value == "tempo":
                if valor_contribuicao >= 30:
                    media = (valor_salario * 60)/100
                    if valor_contribuicao > 30:
                        diferenca = (valor_contribuicao - 30) * 2
                        acrescentado = media * diferenca
                        txt_data.value = "Já atingiu os requisitos para se aposentar."
                        txt_valor.value = f'O valor estimado é R$ {acrescentado}'
                else:
                    diferenca_contribuicao = abs(valor_contribuicao - 15)
                    ano_atual = datetime.today().year
                    data_prevista = abs(ano_atual + diferenca_contribuicao)
                    txt_data.value = f'A data estimada é {data_prevista}'
                    txt_valor.value = f'O valor estimado é R$ {resultado_conta}'


            if genero.value == "masc" and categoria.value == "tempo":
                if valor_contribuicao >= 35:
                    media = (valor_salario * 60)/100
                    if valor_contribuicao > 35:
                        diferenca = (valor_contribuicao - 35) * 2
                        acrescentado = media * diferenca
                        txt_data.value = "Já atingiu os requisitos para se aposentar."
                        txt_valor.value = f'O valor estimado é R$ {acrescentado}'
                else:
                    diferenca_contribuicao = abs(valor_contribuicao - 15)
                    ano_atual = datetime.today().year
                    data_prevista = abs(ano_atual + diferenca_contribuicao)
                    txt_data.value = f'A data estimada é {data_prevista}'
                    txt_valor.value = f'O valor estimado é R$ {resultado_conta}'
            page.go("/resultado")
            page.update()

        except Exception as e:
            txt_resultado.value = str(e)
                #"Os valores estão incorretos, tente novamente, lembrando que tem que ser números inteiros."
            page.update()
        except TypeError:
            txt_resultado.value = "Idade, tempo de contribuição e salário deve ser números inteiros."
            page.update()



    input_idade = ft.TextField(label="Idade Atual", hint_text="Digite sua idade", bgcolor=Colors.WHITE)
    input_contribuicao = ft.TextField(label="Tempo de Contribuição", hint_text="Digite o tempo de contribuição",
                                      bgcolor=Colors.WHITE)
    input_salarial = ft.TextField(label="Média Salarial", hint_text="Digite a média salarial", bgcolor=Colors.WHITE)
    categoria = ft.Dropdown(label="Categoria da aposentadoria", bgcolor=Colors.WHITE,
                            options=[Option(key="idade", text="Aposentadoria por idade"),
                                     Option(key="tempo", text="Aposentadoria por tempo de contribuição")], fill_color=Colors.WHITE, filled=True)
    genero = ft.Dropdown(label="Genero", width=page.window.width,
                         options=[Option(key="masc", text="Masculino"),
                                  Option(key="fem", text="Feminino")], fill_color=Colors.WHITE, filled=True)

    txt_resultado = ft.Text(value="")
    txt_data = ft.TextField(value="", bgcolor=Colors.WHITE)
    txt_valor = ft.TextField(value="", bgcolor=Colors.WHITE)

ft.app(main)
