"""Lê e grava os arquivos JSON e busca itens por id."""

import json
import os

# Caminho relativo a este arquivo, para funcionar rodando de qualquer pasta
PASTA_PROJETO = os.path.dirname(os.path.abspath(__file__))
PASTA_DADOS = os.path.join(PASTA_PROJETO, "data")

ARQUIVO_TRECHOS = os.path.join(PASTA_DADOS, "trechos.json")
ARQUIVO_OCORRENCIAS = os.path.join(PASTA_DADOS, "ocorrencias.json")
ARQUIVO_ROTAS = os.path.join(PASTA_DADOS, "rotas.json")


def carregar_json(caminho):
    """Devolve a lista do arquivo JSON (vazia se ele não existir ou estiver corrompido)."""
    try:
        with open(caminho, "r", encoding="utf-8") as arquivo:
            conteudo = json.load(arquivo)
        return conteudo
    except FileNotFoundError:
        print(f"[AVISO] Arquivo {os.path.basename(caminho)} não encontrado. Criando um novo.")
        salvar_json(caminho, [])
        return []
    except json.JSONDecodeError:
        print(f"[AVISO] Arquivo {os.path.basename(caminho)} está corrompido. Começando com lista vazia.")
        return []


def salvar_json(caminho, conteudo):
    """Grava a lista no arquivo JSON. Devolve True se salvou."""
    try:
        os.makedirs(PASTA_DADOS, exist_ok=True)
        with open(caminho, "w", encoding="utf-8") as arquivo:
            # ensure_ascii=False mantém os acentos
            json.dump(conteudo, arquivo, ensure_ascii=False, indent=2)
        return True
    except OSError:
        print(f"[ERRO] Não foi possível salvar o arquivo {os.path.basename(caminho)}.")
        return False


def carregar_trechos():
    """Devolve a lista de trechos lida do JSON."""
    trechos = carregar_json(ARQUIVO_TRECHOS)
    for trecho in trechos:
        # O JSON não tem tupla: a faixa volta como lista
        trecho["faixa"] = tuple(trecho["faixa"])
    return trechos


def salvar_trechos(trechos):
    """Grava os trechos no JSON. Devolve True se salvou."""
    copia = []
    for trecho in trechos:
        # Cópia para não trocar a faixa dos trechos em uso
        trecho_para_salvar = dict(trecho)
        trecho_para_salvar["faixa"] = list(trecho["faixa"])
        copia.append(trecho_para_salvar)
    return salvar_json(ARQUIVO_TRECHOS, copia)


def salvar_ocorrencias(ocorrencias):
    return salvar_json(ARQUIVO_OCORRENCIAS, ocorrencias)


def salvar_rotas(rotas):
    return salvar_json(ARQUIVO_ROTAS, rotas)


def proximo_id(lista):
    """Devolve o maior id da lista + 1."""
    maior = 0
    for item in lista:
        if item["id"] > maior:
            maior = item["id"]
    return maior + 1


def buscar_por_id(lista, id_procurado):
    """Devolve o item com esse id, ou None."""
    for item in lista:
        if item["id"] == id_procurado:
            return item
    return None
