"""Classe BaseConhecimento: o conjunto de todas as orientações (lê o JSON e faz a busca)."""
import json

from orientacao import Orientacao

ACENTOS = {"á": "a", "à": "a", "ã": "a", "â": "a", "é": "e", "ê": "e",
           "í": "i", "ó": "o", "õ": "o", "ô": "o", "ú": "u", "ç": "c"}

CAMPOS = ["id", "categoria", "titulo", "palavras_chave", "resposta",
          "documentos", "onde", "fonte", "verificado_em"]


def normalizar(texto):
    """minúsculas, sem acentos e sem pontuação; com espaço no início e no fim."""
    texto = texto.lower().strip()
    for letra, troca in ACENTOS.items():
        texto = texto.replace(letra, troca)
    for sinal in "?!.,;:()":
        texto = texto.replace(sinal, " ")
    return " " + " ".join(texto.split()) + " "


class BaseConhecimento:
    def __init__(self, caminho):
        self.caminho = caminho
        self.orientacoes = []

    def carregar(self):
        """Lê o JSON e cria os objetos Orientacao. Devolve (True/False, mensagem).
        Arquivo ausente, corrompido ou com campos faltando NÃO trava o programa."""
        self.orientacoes = []
        try:
            with open(self.caminho, encoding="utf-8") as f:
                dados = json.load(f)
        except FileNotFoundError:
            return False, f"Arquivo não encontrado: {self.caminho}"
        except (json.JSONDecodeError, UnicodeDecodeError):
            return False, f"Arquivo corrompido (JSON inválido): {self.caminho}"
        if not isinstance(dados, list):
            return False, "A base deve ser uma lista de orientações."
        ignoradas = 0
        for d in dados:
            if isinstance(d, dict) and all(c in d for c in CAMPOS):
                self.orientacoes.append(Orientacao.de_dicionario(d))
            else:
                ignoradas += 1
        if not self.orientacoes:
            return False, "Nenhuma orientação válida na base."
        msg = f"{len(self.orientacoes)} orientações carregadas."
        if ignoradas:
            msg += f" ({ignoradas} registro(s) inválido(s) ignorado(s).)"
        return True, msg

    def categorias(self):
        """Lista de categorias, sem repetir, na ordem em que aparecem."""
        cats = []
        for o in self.orientacoes:
            if o.categoria not in cats:
                cats.append(o.categoria)
        return cats

    def por_categoria(self, categoria):
        return [o for o in self.orientacoes if o.categoria == categoria]

    def pontuar(self, pergunta, orientacao):
        """+3 por palavra-chave que aparece na pergunta; +1 por palavra da pergunta
        (4 letras ou mais) que aparece no título."""
        p = normalizar(pergunta)
        pontos = 0
        for chave in orientacao.palavras_chave:
            if normalizar(chave) in p:
                pontos += 3
        palavras_titulo = set(normalizar(orientacao.titulo).split())
        for palavra in set(p.split()):
            if len(palavra) >= 4 and palavra in palavras_titulo:
                pontos += 1
        return pontos

    def buscar(self, pergunta):
        """Lista de tuplas (pontos, orientacao), da maior para a menor pontuação.
        Só entram orientações com pelo menos 1 ponto."""
        resultados = []
        for o in self.orientacoes:
            pontos = self.pontuar(pergunta, o)
            if pontos > 0:
                resultados.append((pontos, o))
        resultados.sort(key=lambda t: (-t[0], t[1].id))
        return resultados
