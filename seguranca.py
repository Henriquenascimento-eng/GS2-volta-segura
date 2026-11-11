"""Cálculos da nota, da rota mais segura e do poste (sem input nem print)."""

# --- Nota de segurança ---

PESO_ILUMINACAO = 6  # pontos máximos da iluminação, de 10

PONTOS_CALCADA = {
    "boa": 2.5,
    "regular": 1.5,
    "ruim": 0.5,
}

DESCONTO_POR_OCORRENCIA = 0.5
DESCONTO_MAXIMO = 1.5

STATUS_ATIVOS = ("aberta", "em_analise")  # ainda contam como problema

NOTA_MINIMA_VERDE = 7
NOTA_MINIMA_AMARELA = 4

# --- Poste inteligente ---
# Mesmos valores do ESP32 (pasta edge/)

LEITURA_MINIMA = 0      # LDR no escuro total
LEITURA_MAXIMA = 1023   # LDR com muita luz

LIMITE_LAMPADA_APAGADA = 200  # à noite, abaixo disso a lâmpada falhou

LUZ_PEDESTRE = 100   # % de luz com alguém passando
LUZ_ECONOMIA = 30    # % de luz com a rua vazia


# --- Nota do trecho ---

def contar_ocorrencias_ativas(trecho_id, ocorrencias):
    """Devolve quantas ocorrências do trecho não foram resolvidas."""
    quantidade = 0
    for ocorrencia in ocorrencias:
        if ocorrencia["trecho_id"] == trecho_id and ocorrencia["status"] in STATUS_ATIVOS:
            quantidade += 1
    return quantidade


def detalhar_nota(trecho, ocorrencias):
    """Devolve a nota do trecho (0 a 10) e cada parte do cálculo."""
    total = trecho["postes_total"]
    acesos = total - trecho["postes_apagados"]

    if total == 0:
        iluminacao = 0
    else:
        iluminacao = acesos / total * PESO_ILUMINACAO

    calcada = PONTOS_CALCADA[trecho["calcada"]]

    ativas = contar_ocorrencias_ativas(trecho["id"], ocorrencias)
    desconto = ativas * DESCONTO_POR_OCORRENCIA
    if desconto > DESCONTO_MAXIMO:
        desconto = DESCONTO_MAXIMO

    nota = iluminacao + calcada - desconto

    if nota < 0:
        nota = 0
    elif nota > 10:
        nota = 10

    return {
        "acesos": acesos,
        "total": total,
        "iluminacao": round(iluminacao, 1),
        "calcada": calcada,
        "ocorrencias_ativas": ativas,
        "desconto": desconto,
        "nota": round(nota, 1),
    }


def calcular_nota(trecho, ocorrencias):
    """Devolve a nota de segurança do trecho (0 a 10)."""
    detalhes = detalhar_nota(trecho, ocorrencias)
    return detalhes["nota"]


def classificar_nota(nota):
    """Devolve VERDE, AMARELO ou VERMELHO conforme a nota."""
    if nota >= NOTA_MINIMA_VERDE:
        return "VERDE (seguro)"
    elif nota >= NOTA_MINIMA_AMARELA:
        return "AMARELO (atenção)"
    else:
        return "VERMELHO (evitar)"


# --- Rota mais segura ---

def avaliar_rota(rota, trechos, ocorrencias):
    """Devolve as notas, a mínima e a média da rota (None se faltar trecho)."""
    notas_dos_trechos = []
    for trecho_id in rota["trechos"]:
        trecho_encontrado = None
        for trecho in trechos:
            if trecho["id"] == trecho_id:
                trecho_encontrado = trecho
        if trecho_encontrado is None:
            return None
        nota = calcular_nota(trecho_encontrado, ocorrencias)
        notas_dos_trechos.append((trecho_encontrado, nota))

    if len(notas_dos_trechos) == 0:
        return None

    minima = notas_dos_trechos[0][1]
    soma = 0
    for trecho, nota in notas_dos_trechos:
        if nota < minima:
            minima = nota
        soma += nota
    media = round(soma / len(notas_dos_trechos), 1)

    return {
        "rota": rota,
        "notas": notas_dos_trechos,
        "minima": minima,
        "media": media,
    }


def recomendar_rota(avaliacoes):
    """Devolve a avaliação da rota mais segura."""
    # Vence a maior nota mínima: um só trecho escuro já torna o caminho inseguro
    # Empate: vence a maior média
    melhor = None
    for avaliacao in avaliacoes:
        if melhor is None:
            melhor = avaliacao
        elif avaliacao["minima"] > melhor["minima"]:
            melhor = avaliacao
        elif avaliacao["minima"] == melhor["minima"] and avaliacao["media"] > melhor["media"]:
            melhor = avaliacao
    return melhor


# --- Poste inteligente ---

def estado_poste(eh_noite, leitura, tem_pedestre):
    """Devolve (estado, intensidade em %, ação) do poste."""
    if leitura is None or leitura < LEITURA_MINIMA or leitura > LEITURA_MAXIMA:
        return ("LEITURA INVÁLIDA", 0, "Verificar o sensor de luz (LDR).")
    elif not eh_noite:
        return ("DESLIGADO (DIA)", 0, "Lâmpada desligada durante o dia.")
    elif leitura < LIMITE_LAMPADA_APAGADA:
        return ("APAGADO / FALHA", 0, "Alerta enviado: a lâmpada não está acendendo.")
    elif tem_pedestre:
        return ("PEDESTRE", LUZ_PEDESTRE, "Pedestre detectado: luz no máximo.")
    else:
        return ("ECONOMIA", LUZ_ECONOMIA, "Rua vazia: luz reduzida para economizar energia.")
