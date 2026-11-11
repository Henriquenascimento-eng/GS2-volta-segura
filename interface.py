"""Mostra títulos, mensagens e tabelas no terminal."""

LARGURA = 60  # caracteres por linha


def titulo(texto):
    """Mostra um título centralizado entre linhas de '='."""
    print()
    print("=" * LARGURA)
    print(texto.center(LARGURA))
    print("=" * LARGURA)


def subtitulo(texto):
    """Mostra um subtítulo sublinhado com '-'."""
    print()
    print(texto)
    print("-" * LARGURA)


def pausar():
    """Espera o usuário apertar Enter."""
    input("\nPressione Enter para continuar...")


def mensagem_sucesso(texto):
    print(f"[OK] {texto}")


def mensagem_erro(texto):
    print(f"[ERRO] {texto}")


def mensagem_aviso(texto):
    print(f"[AVISO] {texto}")


def imprimir_tabela(cabecalhos, linhas_tabela):
    """Mostra uma tabela com colunas alinhadas."""
    if len(linhas_tabela) == 0:
        print("(nenhum registro encontrado)")
        return

    # Cada coluna fica com a largura do seu maior texto
    larguras = []
    for coluna in range(len(cabecalhos)):
        maior = len(str(cabecalhos[coluna]))
        for registro in linhas_tabela:
            tamanho = len(str(registro[coluna]))
            if tamanho > maior:
                maior = tamanho
        larguras.append(maior)

    texto = ""
    for coluna in range(len(cabecalhos)):
        texto += str(cabecalhos[coluna]).ljust(larguras[coluna]) + "  "
    print(texto)

    total = 0
    for largura in larguras:
        total += largura + 2
    print("-" * total)

    for registro in linhas_tabela:
        texto = ""
        for coluna in range(len(cabecalhos)):
            texto += str(registro[coluna]).ljust(larguras[coluna]) + "  "
        print(texto)
