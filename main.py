"""Carrega os dados e mostra o menu principal da Volta Segura."""

from dados import carregar_trechos, carregar_json, salvar_trechos, ARQUIVO_OCORRENCIAS, ARQUIVO_ROTAS
from validacoes import ler_inteiro, confirmar
from interface import titulo, subtitulo, pausar, mensagem_aviso, mensagem_sucesso, imprimir_tabela
from trechos import menu_trechos, escolher_trecho, formatar_faixa
from ocorrencias import menu_ocorrencias, criar_ocorrencia
from rotas import menu_rotas
from relatorio import mostrar_relatorio
from seguranca import calcular_nota, classificar_nota, detalhar_nota, estado_poste, LEITURA_MINIMA, LEITURA_MAXIMA


def ler_leitura_ldr():
    """Devolve a leitura do LDR, ou None se não for número."""
    # Não repete a pergunta: o valor errado deve mostrar LEITURA INVÁLIDA
    entrada = input(f"Leitura do sensor de luz LDR ({LEITURA_MINIMA} a {LEITURA_MAXIMA}): ").strip()
    try:
        return int(entrada)
    except ValueError:
        return None


def tela_simular_poste(trechos, ocorrencias):
    """Simula as leituras do poste e mostra o estado e a ação."""
    subtitulo("SIMULAR POSTE INTELIGENTE")
    print("Informe as leituras dos sensores do poste.\n")
    eh_noite = confirmar("É noite?")
    leitura = ler_leitura_ldr()
    tem_pedestre = confirmar("O sensor de presença (PIR) detectou alguém?")

    estado, intensidade, acao = estado_poste(eh_noite, leitura, tem_pedestre)

    print()
    print("=" * 60)
    print(f"Estado do poste: {estado}")
    print(f"Intensidade da luz: {intensidade}%")
    print(f"Ação: {acao}")
    print("=" * 60)

    # Lâmpada com falha: oferece registrar a ocorrência
    if estado == "APAGADO / FALHA" and len(trechos) > 0:
        if confirmar("\nRegistrar automaticamente uma ocorrência de poste apagado?"):
            trecho = escolher_trecho(trechos)
            if trecho is None:
                return
            descricao = f"Registrada pelo sensor do poste (leitura do LDR: {leitura})"
            nova = criar_ocorrencia(ocorrencias, trecho["id"], "poste_apagado", descricao)
            # Conta o poste como apagado, o que baixa a nota
            if trecho["postes_apagados"] < trecho["postes_total"]:
                trecho["postes_apagados"] += 1
                salvar_trechos(trechos)
            mensagem_sucesso(f"Ocorrência {nova['id']} registrada em {trecho['rua']}.")
            print(f"Nova nota do trecho: {calcular_nota(trecho, ocorrencias)}")


def tela_nota_trecho(trechos, ocorrencias):
    """Mostra a nota de cada trecho e o cálculo de um deles."""
    subtitulo("NOTA DE SEGURANÇA DOS TRECHOS")
    if len(trechos) == 0:
        mensagem_aviso("Nenhum trecho cadastrado ainda.")
        return

    cabecalhos = ("ID", "Rua", "Faixa", "Nota", "Classificação")
    linhas = []
    for trecho in trechos:
        nota = calcular_nota(trecho, ocorrencias)
        linhas.append((trecho["id"], trecho["rua"], formatar_faixa(trecho["faixa"]), nota, classificar_nota(nota)))
    imprimir_tabela(cabecalhos, linhas)

    print("\nPara ver o cálculo detalhado, escolha um trecho.")
    trecho = escolher_trecho(trechos)
    if trecho is None:
        return

    detalhes = detalhar_nota(trecho, ocorrencias)

    subtitulo(f"{trecho['rua']}, {formatar_faixa(trecho['faixa'])}")
    texto_postes = f"{detalhes['acesos']} de {detalhes['total']} postes acesos"
    texto_ocorrencias = f"{detalhes['ocorrencias_ativas']} ativa(s)"
    print(f"Iluminação:  {texto_postes:<28} +{detalhes['iluminacao']:.1f}")
    print(f"Calçada:     {trecho['calcada']:<28} +{detalhes['calcada']:.1f}")
    print(f"Ocorrências: {texto_ocorrencias:<28} -{detalhes['desconto']:.1f}")
    print("-" * 50)
    print(f"Nota final:  {detalhes['nota']}  {classificar_nota(detalhes['nota'])}")


def mostrar_menu_principal():
    titulo("VOLTA SEGURA")
    print("Caminho iluminado da estação até em casa".center(60))
    print()
    print("1. Trechos de rua        (cadastrar, listar, editar, remover)")
    print("2. Ocorrências           (registrar, listar, atualizar, remover)")
    print("3. Simular poste inteligente")
    print("4. Nota de segurança de um trecho")
    print("5. Rotas                 (rota mais segura, cadastrar, listar)")
    print("6. Relatório geral")
    print("0. Sair")


def main():
    # Dados ficam na memória e são salvos no JSON a cada alteração
    trechos = carregar_trechos()
    ocorrencias = carregar_json(ARQUIVO_OCORRENCIAS)
    rotas = carregar_json(ARQUIVO_ROTAS)

    while True:
        mostrar_menu_principal()
        opcao = ler_inteiro("\nEscolha uma opção: ", 0, 6)

        match opcao:
            case 1:
                menu_trechos(trechos, ocorrencias, rotas)
            case 2:
                menu_ocorrencias(ocorrencias, trechos)
            case 3:
                tela_simular_poste(trechos, ocorrencias)
                pausar()
            case 4:
                tela_nota_trecho(trechos, ocorrencias)
                pausar()
            case 5:
                menu_rotas(rotas, trechos, ocorrencias)
            case 6:
                mostrar_relatorio(trechos, ocorrencias)
                pausar()
            case 0:
                print("\nAté logo! Volte em segurança.")
                break


if __name__ == "__main__":
    # Ctrl+C fecha com mensagem em vez de erro
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\n\nPrograma encerrado. Volte em segurança.")
