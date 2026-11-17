"""Classe Orientacao: uma informação da base de conhecimento (um registro do JSON)."""

AVISO = "Aviso: este assistente NÃO é um canal oficial."
PENDENTE = "A CONFERIR"


class Orientacao:
    def __init__(self, id, categoria, titulo, palavras_chave, resposta,
                 documentos, onde, fonte, verificado_em, calculo=None):
        self.id = id
        self.categoria = categoria
        self.titulo = titulo
        self.palavras_chave = palavras_chave
        self.resposta = resposta
        self.documentos = documentos
        self.onde = onde
        self.fonte = fonte
        self.verificado_em = verificado_em
        self.calculo = calculo  # opcional: nome da simulação do módulo de energia

    @classmethod
    def de_dicionario(cls, d):
        """Cria um Orientacao a partir de um dicionário do JSON."""
        return cls(d["id"], d["categoria"], d["titulo"], d["palavras_chave"], d["resposta"],
                   d["documentos"], d["onde"], d["fonte"], d["verificado_em"], d.get("calculo"))

    @property
    def pendente(self):
        """True se a equipe ainda não conferiu a fonte (data de verificação pendente)."""
        return self.verificado_em == PENDENTE

    def exibir(self):
        print(f">> {self.titulo}  [{self.categoria}]")
        print(self.resposta)
        if self.documentos:
            print("Documentos necessários:")
            for doc in self.documentos:
                print(f"  - {doc}")
        else:
            print("Documentos necessários: nenhum documento específico")
        print(f"Onde: {self.onde}")
        print(f"Fonte: {self.fonte} (verificado em {self.verificado_em})")
        print(AVISO)
