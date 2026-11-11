"""Mostra o relatório geral por bairro."""

from interface import subtitulo, imprimir_tabela, mensagem_aviso
from seguranca import calcular_nota, classificar_nota, NOTA_MINIMA_VERDE, STATUS_ATIVOS
from ocorrencias import TIPOS_OCORRENCIA, formatar


def agrupar_por_bairro(trechos):
    """Devolve um dicionário bairro -> lista de trechos."""
    grupos = {}
    for trecho in trechos:
        bairro = trecho["bairro"]
        if bairro not in grupos:
            grupos[bairro] = []
        grupos[bairro].append(trecho)
    return grupos


def resumo_do_bairro(trechos_do_bairro, ocorrencias):
    """Devolve a linha da tabela de um bairro."""
    soma_notas = 0
    postes_total = 0
    postes_apagados = 0
    mais_critico = None
    nota_mais_critica = 11  # acima de 10, para a 1ª nota já ser menor

    for trecho in trechos_do_bairro:
        nota = calcular_nota(trecho, ocorrencias)
        soma_notas += nota
        postes_total += trecho["postes_total"]
        postes_apagados += trecho["postes_apagados"]
        if nota < nota_mais_critica:
            nota_mais_critica = nota
            mais_critico = trecho

    media = round(soma_notas / len(trechos_do_bairro), 1)

    if postes_total == 0:
        percentual_apagados = 0
    else:
        percentual_apagados = round(postes_apagados / postes_total * 100)

    return (
        len(trechos_do_bairro),
        media,
        f"{percentual_apagados}%",
        f"{mais_critico['rua']} ({nota_mais_critica})",
    )


def contar_ocorrencias_por_tipo(ocorrencias):
    """Devolve um dicionário tipo -> quantidade de ocorrências ativas."""
    contagem = {}
    for tipo in TIPOS_OCORRENCIA:
        contagem[tipo] = 0
    for ocorrencia in ocorrencias:
        if ocorrencia["status"] in STATUS_ATIVOS:
            contagem[ocorrencia["tipo"]] += 1
    return contagem


def mostrar_relatorio(trechos, ocorrencias):
    """Mostra o relatório completo."""
    subtitulo("RELATÓRIO GERAL - SITUAÇÃO POR BAIRRO")
    if len(trechos) == 0:
        mensagem_aviso("Nenhum trecho cadastrado ainda.")
        return

    grupos = agrupar_por_bairro(trechos)
    cabecalhos = ("Bairro", "Trechos", "Nota média", "Postes apagados", "Trecho mais crítico")
    linhas = []
    for bairro, trechos_do_bairro in grupos.items():
        quantidade, media, apagados, critico = resumo_do_bairro(trechos_do_bairro, ocorrencias)
        linhas.append((bairro, quantidade, f"{media} {classificar_nota(media).split()[0]}", apagados, critico))
    imprimir_tabela(cabecalhos, linhas)

    subtitulo("OCORRÊNCIAS ATIVAS (abertas ou em análise)")
    contagem = contar_ocorrencias_por_tipo(ocorrencias)
    total_ativas = 0
    for tipo, quantidade in contagem.items():
        print(f"  {formatar(tipo):<20} {quantidade}")
        total_ativas += quantidade
    print(f"  {'TOTAL':<20} {total_ativas}")

    verdes = 0
    for trecho in trechos:
        if calcular_nota(trecho, ocorrencias) >= NOTA_MINIMA_VERDE:
            verdes += 1
    percentual_verdes = round(verdes / len(trechos) * 100)

    subtitulo("INDICADOR DE IMPACTO")
    print(f"  {verdes} de {len(trechos)} trechos estão VERDES (seguros): {percentual_verdes}%")
    print("  Meta do projeto: aumentar essa porcentagem a cada mês,")
    print("  consertando primeiro os trechos mais críticos de cada bairro.")
