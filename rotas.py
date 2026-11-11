"""Telas de rotas: rota mais segura, cadastrar, listar e remover."""

from dados import salvar_rotas, proximo_id, buscar_por_id
from validacoes import ler_texto, ler_inteiro, ler_opcao, confirmar, ler_item_existente
from interface import subtitulo, imprimir_tabela, pausar, mensagem_sucesso, mensagem_erro, mensagem_aviso
from trechos import listar_trechos, formatar_faixa
from seguranca import avaliar_rota, recomendar_rota, classificar_nota

# Linha 3-Vermelha do metrô
ESTACOES = ("Tatuapé", "Belém", "Bresser-Mooca")


def descrever_caminho(rota, trechos):
    """Devolve as ruas da rota no formato 'Rua A > Rua B'."""
    nomes = []
    for trecho_id in rota["trechos"]:
        trecho = buscar_por_id(trechos, trecho_id)
        if trecho is None:
            nomes.append("(trecho removido)")
        else:
            nomes.append(trecho["rua"])
    return " > ".join(nomes)


def listar_rotas(rotas, trechos):
    """Mostra as rotas em tabela."""
    subtitulo("ROTAS CADASTRADAS")
    cabecalhos = ("ID", "Estação", "Destino", "Caminho")
    linhas = []
    for rota in rotas:
        linhas.append((rota["id"], rota["estacao"], rota["destino"], descrever_caminho(rota, trechos)))
    imprimir_tabela(cabecalhos, linhas)


def destinos_da_estacao(rotas, estacao):
    """Devolve os destinos, sem repetir, que saem da estação."""
    destinos = []
    for rota in rotas:
        if rota["estacao"] == estacao and rota["destino"] not in destinos:
            destinos.append(rota["destino"])
    return destinos


def mostrar_avaliacao(avaliacao):
    """Mostra cada trecho da rota com sua nota."""
    rota = avaliacao["rota"]
    print(f"\nRota {rota['id']}: {rota['estacao']} -> {rota['destino']}")
    passo = 1
    for trecho, nota in avaliacao["notas"]:
        print(f"  {passo}. {trecho['rua']} ({formatar_faixa(trecho['faixa'])}): nota {nota} - {classificar_nota(nota)}")
        passo += 1
    print(f"  Nota mínima: {avaliacao['minima']} | Nota média: {avaliacao['media']}")


def tela_rota_segura(rotas, trechos, ocorrencias):
    """Compara as rotas até um destino e recomenda a mais segura."""
    subtitulo("ROTA MAIS SEGURA")
    if len(rotas) == 0:
        mensagem_aviso("Nenhuma rota cadastrada ainda.")
        return

    estacao = ler_opcao("Em qual estação você desce?", ESTACOES)
    destinos = destinos_da_estacao(rotas, estacao)
    if len(destinos) == 0:
        mensagem_aviso(f"Ainda não há rotas saindo da estação {estacao}.")
        return

    destino = ler_opcao("\nPara onde você vai?", tuple(destinos))

    avaliacoes = []
    for rota in rotas:
        if rota["estacao"] == estacao and rota["destino"] == destino:
            avaliacao = avaliar_rota(rota, trechos, ocorrencias)
            if avaliacao is None:
                mensagem_aviso(f"A rota {rota['id']} tem um trecho que não existe mais e foi ignorada.")
            else:
                avaliacoes.append(avaliacao)

    if len(avaliacoes) == 0:
        mensagem_erro("Nenhuma rota válida para esse destino.")
        return

    subtitulo(f"ROTAS DE {estacao.upper()} ATÉ {destino.upper()}")
    for avaliacao in avaliacoes:
        mostrar_avaliacao(avaliacao)

    melhor = recomendar_rota(avaliacoes)
    print()
    print("=" * 60)
    print(f"RECOMENDADA: rota {melhor['rota']['id']}")
    print(f"Caminho: {descrever_caminho(melhor['rota'], trechos)}")
    print(f"Pior trecho do caminho tem nota {melhor['minima']}: {classificar_nota(melhor['minima'])}")
    print("Critério: escolhemos a rota cujo trecho mais perigoso é o menos perigoso.")
    print("=" * 60)


def cadastrar_rota(rotas, trechos):
    """Cadastra uma rota com estação, destino e trechos em ordem."""
    subtitulo("CADASTRAR ROTA")
    if len(trechos) == 0:
        mensagem_aviso("Cadastre trechos antes de criar uma rota.")
        return

    estacao = ler_opcao("Estação de partida:", ESTACOES)
    destino = ler_texto("Nome do destino (ex.: Casa A, Escola): ")

    listar_trechos(trechos)
    print("\nDigite os ids dos trechos na ordem do caminho. Digite 0 para terminar.")
    ids_da_rota = []
    while True:
        trecho = ler_item_existente(f"Trecho {len(ids_da_rota) + 1} (0 para terminar): ", trechos)
        if trecho is None:
            if len(ids_da_rota) == 0:
                mensagem_erro("A rota precisa de pelo menos um trecho.")
                continue
            break
        if trecho["id"] in ids_da_rota:
            mensagem_erro("Esse trecho já está na rota.")
        else:
            ids_da_rota.append(trecho["id"])

    nova_rota = {
        "id": proximo_id(rotas),
        "estacao": estacao,
        "destino": destino,
        "trechos": ids_da_rota,
    }
    rotas.append(nova_rota)
    if salvar_rotas(rotas):
        mensagem_sucesso(f"Rota {nova_rota['id']} cadastrada: {descrever_caminho(nova_rota, trechos)}.")


def remover_rota(rotas, trechos):
    """Remove uma rota após confirmação."""
    subtitulo("REMOVER ROTA")
    if len(rotas) == 0:
        mensagem_aviso("Nenhuma rota cadastrada ainda.")
        return
    listar_rotas(rotas, trechos)
    rota = ler_item_existente("\nId da rota (0 para cancelar): ", rotas)
    if rota is None:
        return

    if confirmar(f"Tem certeza que deseja remover a rota {rota['id']}?"):
        rotas.remove(rota)
        if salvar_rotas(rotas):
            mensagem_sucesso("Rota removida.")
    else:
        mensagem_aviso("Remoção cancelada.")


def menu_rotas(rotas, trechos, ocorrencias):
    """Submenu de rotas."""
    while True:
        subtitulo("ROTAS")
        print("1. Descobrir a rota mais segura")
        print("2. Cadastrar rota")
        print("3. Listar rotas")
        print("4. Remover rota")
        print("0. Voltar")
        opcao = ler_inteiro("Escolha: ", 0, 4)

        match opcao:
            case 1:
                tela_rota_segura(rotas, trechos, ocorrencias)
            case 2:
                cadastrar_rota(rotas, trechos)
            case 3:
                listar_rotas(rotas, trechos)
            case 4:
                remover_rota(rotas, trechos)
            case 0:
                return
        pausar()
