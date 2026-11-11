"""Cadastra, lista, edita e remove trechos de rua."""

from dados import salvar_trechos, proximo_id
from validacoes import ler_texto, ler_inteiro, ler_opcao, confirmar, ler_item_existente
from interface import subtitulo, imprimir_tabela, pausar, mensagem_sucesso, mensagem_erro, mensagem_aviso

CONDICOES_CALCADA = ("boa", "regular", "ruim")

MAXIMO_POSTES = 200  # por trecho


def formatar_faixa(faixa):
    """Devolve a faixa no formato '100 a 400'."""
    inicio, fim = faixa
    return f"{inicio} a {fim}"


def ler_faixa():
    """Devolve a faixa (inicio, fim) digitada."""
    inicio = ler_inteiro("Número inicial do trecho: ", 0)
    # Mínimo inicio + 1 garante fim maior que inicio
    fim = ler_inteiro("Número final do trecho: ", inicio + 1)
    return (inicio, fim)


def ler_postes():
    """Devolve (total, apagados) dos postes digitados."""
    total = ler_inteiro("Quantidade de postes no trecho: ", 0, MAXIMO_POSTES)
    apagados = ler_inteiro("Quantos estão apagados: ", 0, total)
    return (total, apagados)


def cadastrar_trecho(trechos):
    """Cadastra e salva um novo trecho."""
    subtitulo("CADASTRAR TRECHO")
    bairro = ler_texto("Bairro: ")
    rua = ler_texto("Rua: ")
    faixa = ler_faixa()
    postes_total, postes_apagados = ler_postes()
    calcada = ler_opcao("Condição da calçada:", CONDICOES_CALCADA)

    novo_trecho = {
        "id": proximo_id(trechos),
        "bairro": bairro,
        "rua": rua,
        "faixa": faixa,
        "postes_total": postes_total,
        "postes_apagados": postes_apagados,
        "calcada": calcada,
    }
    trechos.append(novo_trecho)

    if salvar_trechos(trechos):
        mensagem_sucesso(f"Trecho {novo_trecho['id']} cadastrado: {rua}, {formatar_faixa(faixa)}.")


def montar_linhas_trechos(trechos):
    """Devolve as linhas da tabela de trechos."""
    linhas = []
    for trecho in trechos:
        acesos = trecho["postes_total"] - trecho["postes_apagados"]
        linhas.append((
            trecho["id"],
            trecho["bairro"],
            trecho["rua"],
            formatar_faixa(trecho["faixa"]),
            f"{acesos}/{trecho['postes_total']} acesos",
            trecho["calcada"],
        ))
    return linhas


def listar_trechos(trechos):
    """Mostra os trechos em tabela."""
    subtitulo("TRECHOS CADASTRADOS")
    cabecalhos = ("ID", "Bairro", "Rua", "Faixa", "Postes", "Calçada")
    imprimir_tabela(cabecalhos, montar_linhas_trechos(trechos))


def escolher_trecho(trechos):
    """Devolve o trecho escolhido, ou None."""
    if len(trechos) == 0:
        mensagem_aviso("Nenhum trecho cadastrado ainda.")
        return None
    listar_trechos(trechos)
    return ler_item_existente("\nId do trecho (0 para cancelar): ", trechos)


def editar_trecho(trechos):
    """Altera um campo de um trecho."""
    subtitulo("EDITAR TRECHO")
    trecho = escolher_trecho(trechos)
    if trecho is None:
        return

    print(f"\nEditando: {trecho['rua']}, {formatar_faixa(trecho['faixa'])}")
    print("1. Bairro")
    print("2. Rua")
    print("3. Faixa de numeração")
    print("4. Postes (total e apagados)")
    print("5. Condição da calçada")
    print("0. Cancelar")
    campo = ler_inteiro("O que deseja alterar? ", 0, 5)

    match campo:
        case 1:
            trecho["bairro"] = ler_texto("Novo bairro: ")
        case 2:
            trecho["rua"] = ler_texto("Nova rua: ")
        case 3:
            trecho["faixa"] = ler_faixa()
        case 4:
            total, apagados = ler_postes()
            trecho["postes_total"] = total
            trecho["postes_apagados"] = apagados
        case 5:
            trecho["calcada"] = ler_opcao("Nova condição da calçada:", CONDICOES_CALCADA)
        case 0:
            mensagem_aviso("Edição cancelada.")
            return

    if salvar_trechos(trechos):
        mensagem_sucesso("Trecho atualizado.")


def remover_trecho(trechos, ocorrencias, rotas):
    """Remove um trecho que não esteja em uso."""
    subtitulo("REMOVER TRECHO")
    trecho = escolher_trecho(trechos)
    if trecho is None:
        return

    qtd_ocorrencias = 0
    for ocorrencia in ocorrencias:
        if ocorrencia["trecho_id"] == trecho["id"]:
            qtd_ocorrencias += 1

    qtd_rotas = 0
    for rota in rotas:
        if trecho["id"] in rota["trechos"]:
            qtd_rotas += 1

    # Em uso, ocorrências e rotas ficariam apontando para um trecho inexistente
    if qtd_ocorrencias > 0 or qtd_rotas > 0:
        mensagem_erro(
            f"Não é possível remover: o trecho tem {qtd_ocorrencias} ocorrência(s) "
            f"e está em {qtd_rotas} rota(s). Remova-as antes."
        )
        return

    if confirmar(f"Tem certeza que deseja remover {trecho['rua']}?"):
        trechos.remove(trecho)
        if salvar_trechos(trechos):
            mensagem_sucesso("Trecho removido.")
    else:
        mensagem_aviso("Remoção cancelada.")


def menu_trechos(trechos, ocorrencias, rotas):
    """Submenu de trechos de rua."""
    while True:
        subtitulo("TRECHOS DE RUA")
        print("1. Cadastrar trecho")
        print("2. Listar trechos")
        print("3. Editar trecho")
        print("4. Remover trecho")
        print("0. Voltar")
        opcao = ler_inteiro("Escolha: ", 0, 4)

        match opcao:
            case 1:
                cadastrar_trecho(trechos)
            case 2:
                listar_trechos(trechos)
            case 3:
                editar_trecho(trechos)
            case 4:
                remover_trecho(trechos, ocorrencias, rotas)
            case 0:
                return
        pausar()
