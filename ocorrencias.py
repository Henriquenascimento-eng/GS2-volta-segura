"""Cadastra, lista, atualiza e remove ocorrências dos trechos."""

from dados import salvar_ocorrencias, proximo_id, buscar_por_id
from validacoes import ler_texto, ler_inteiro, ler_opcao, confirmar, ler_item_existente
from interface import subtitulo, imprimir_tabela, pausar, mensagem_sucesso, mensagem_aviso
from trechos import escolher_trecho

TIPOS_OCORRENCIA = ("poste_apagado", "calcada_quebrada", "rua_escura", "outro")
STATUS_OCORRENCIA = ("aberta", "em_analise", "resolvida")


def formatar(texto):
    """Devolve o texto com '_' trocado por espaço."""
    return texto.replace("_", " ")


def orientacao_por_tipo(tipo):
    """Devolve o órgão para onde encaminhar a ocorrência."""
    match tipo:
        case "poste_apagado":
            return "Encaminhar para a concessionária de iluminação pública."
        case "calcada_quebrada":
            return "Encaminhar para a subprefeitura (zeladoria de calçadas)."
        case "rua_escura":
            return "Solicitar estudo de novos pontos de iluminação para a prefeitura."
        case _:
            return "Analisar a ocorrência e definir o órgão responsável."


def criar_ocorrencia(ocorrencias, trecho_id, tipo, descricao):
    """Cria e salva uma ocorrência aberta. Devolve a ocorrência."""
    nova = {
        "id": proximo_id(ocorrencias),
        "trecho_id": trecho_id,
        "tipo": tipo,
        "descricao": descricao,
        "status": "aberta",
    }
    ocorrencias.append(nova)
    salvar_ocorrencias(ocorrencias)
    return nova


def registrar_ocorrencia(ocorrencias, trechos):
    """Pede os dados e registra uma ocorrência."""
    subtitulo("REGISTRAR OCORRÊNCIA")
    trecho = escolher_trecho(trechos)
    if trecho is None:
        return

    tipo = ler_opcao("\nTipo de ocorrência:", TIPOS_OCORRENCIA)
    descricao = ler_texto("Descreva o problema (ex.: poste em frente ao 250): ")

    nova = criar_ocorrencia(ocorrencias, trecho["id"], tipo, descricao)
    mensagem_sucesso(f"Ocorrência {nova['id']} registrada em {trecho['rua']}.")
    print(f"Encaminhamento: {orientacao_por_tipo(tipo)}")


def nome_da_rua(trechos, trecho_id):
    """Devolve o nome da rua do trecho."""
    trecho = buscar_por_id(trechos, trecho_id)
    if trecho is None:
        return "(trecho removido)"
    return trecho["rua"]


def listar_ocorrencias(ocorrencias, trechos):
    """Mostra as ocorrências em tabela."""
    subtitulo("OCORRÊNCIAS")
    cabecalhos = ("ID", "Rua", "Tipo", "Status", "Descrição")
    linhas = []
    for ocorrencia in ocorrencias:
        linhas.append((
            ocorrencia["id"],
            nome_da_rua(trechos, ocorrencia["trecho_id"]),
            formatar(ocorrencia["tipo"]),
            formatar(ocorrencia["status"]),
            ocorrencia["descricao"],
        ))
    imprimir_tabela(cabecalhos, linhas)


def escolher_ocorrencia(ocorrencias, trechos):
    """Devolve a ocorrência escolhida, ou None."""
    if len(ocorrencias) == 0:
        mensagem_aviso("Nenhuma ocorrência registrada ainda.")
        return None
    listar_ocorrencias(ocorrencias, trechos)
    return ler_item_existente("\nId da ocorrência (0 para cancelar): ", ocorrencias)


def atualizar_status(ocorrencias, trechos):
    """Muda o status de uma ocorrência."""
    subtitulo("ATUALIZAR STATUS")
    ocorrencia = escolher_ocorrencia(ocorrencias, trechos)
    if ocorrencia is None:
        return

    print(f"\nStatus atual: {formatar(ocorrencia['status'])}")
    novo_status = ler_opcao("Novo status:", STATUS_OCORRENCIA)

    if novo_status == ocorrencia["status"]:
        mensagem_aviso("O status escolhido é igual ao atual. Nada foi alterado.")
        return

    ocorrencia["status"] = novo_status
    salvar_ocorrencias(ocorrencias)
    mensagem_sucesso(f"Ocorrência {ocorrencia['id']} agora está: {formatar(novo_status)}.")


def remover_ocorrencia(ocorrencias, trechos):
    """Remove uma ocorrência após confirmação."""
    subtitulo("REMOVER OCORRÊNCIA")
    ocorrencia = escolher_ocorrencia(ocorrencias, trechos)
    if ocorrencia is None:
        return

    if confirmar(f"Tem certeza que deseja remover a ocorrência {ocorrencia['id']}?"):
        ocorrencias.remove(ocorrencia)
        salvar_ocorrencias(ocorrencias)
        mensagem_sucesso("Ocorrência removida.")
    else:
        mensagem_aviso("Remoção cancelada.")


def menu_ocorrencias(ocorrencias, trechos):
    """Submenu de ocorrências."""
    while True:
        subtitulo("OCORRÊNCIAS")
        print("1. Registrar ocorrência")
        print("2. Listar ocorrências")
        print("3. Atualizar status")
        print("4. Remover ocorrência")
        print("0. Voltar")
        opcao = ler_inteiro("Escolha: ", 0, 4)

        match opcao:
            case 1:
                registrar_ocorrencia(ocorrencias, trechos)
            case 2:
                listar_ocorrencias(ocorrencias, trechos)
            case 3:
                atualizar_status(ocorrencias, trechos)
            case 4:
                remover_ocorrencia(ocorrencias, trechos)
            case 0:
                return
        pausar()
