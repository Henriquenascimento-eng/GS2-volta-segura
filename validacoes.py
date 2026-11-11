"""Lê dados do usuário e repete a pergunta até a entrada ser válida."""

from interface import mensagem_erro
from dados import buscar_por_id


def ler_texto(mensagem):
    """Devolve um texto não vazio."""
    while True:
        texto = input(mensagem).strip()
        if texto != "":
            return texto
        mensagem_erro("Este campo não pode ficar vazio.")


def ler_inteiro(mensagem, minimo, maximo=None):
    """Devolve um inteiro entre minimo e maximo (None = sem limite)."""
    while True:
        entrada = input(mensagem).strip()

        try:
            numero = int(entrada)
        except ValueError:
            mensagem_erro("Digite um número inteiro válido.")
            continue

        if numero < minimo:
            mensagem_erro(f"O valor mínimo é {minimo}.")
        elif maximo is not None and numero > maximo:
            mensagem_erro(f"O valor máximo é {maximo}.")
        else:
            return numero


def ler_opcao(mensagem, opcoes):
    """Mostra as opções numeradas e devolve a escolhida."""
    print(mensagem)
    for posicao in range(len(opcoes)):
        texto_opcao = str(opcoes[posicao]).replace("_", " ")
        print(f"  {posicao + 1}. {texto_opcao}")
    escolha = ler_inteiro("Escolha: ", 1, len(opcoes))
    return opcoes[escolha - 1]


def confirmar(mensagem):
    """Devolve True para sim e False para não."""
    while True:
        resposta = input(f"{mensagem} (s/n): ").strip().lower()
        if resposta in ("s", "sim"):
            return True
        elif resposta in ("n", "nao", "não"):
            return False
        else:
            mensagem_erro("Responda com s ou n.")


def ler_item_existente(mensagem, lista):
    """Devolve o item do id digitado, ou None se digitar 0."""
    while True:
        id_digitado = ler_inteiro(mensagem, 0)
        if id_digitado == 0:
            return None
        item = buscar_por_id(lista, id_digitado)
        if item is not None:
            return item
        mensagem_erro(f"Não existe registro com id {id_digitado}.")
