"""Classe Assistente: faz o atendimento, guarda o histórico e calcula os indicadores."""
import csv
import json
import re
import time
from datetime import datetime

CAMPOS_CSV = ["data", "origem", "pergunta", "id_orientacao", "encontrou",
              "ajudou", "tentativas", "tempo_segundos", "facilidade"]


class Assistente:
    def __init__(self, nome, base, caminho_historico="data/historico.json",
                 caminho_csv="data/atendimentos.csv"):
        self.nome = nome
        self.base = base
        self.caminho_historico = caminho_historico
        self.caminho_csv = caminho_csv
        self.historico = []
        self.simulador = None  # módulo de energia, criado só quando necessário
        self._carregar_historico()

    # ---------- histórico ----------
    def _carregar_historico(self):
        """Histórico ausente ou corrompido não trava o programa: começa vazio."""
        try:
            with open(self.caminho_historico, encoding="utf-8") as f:
                dados = json.load(f)
            self.historico = dados if isinstance(dados, list) else []
        except FileNotFoundError:
            self.historico = []
        except (json.JSONDecodeError, UnicodeDecodeError, OSError):
            print("Aviso: histórico ilegível, começando um novo.")
            self.historico = []

    def _salvar_historico(self):
        try:
            with open(self.caminho_historico, "w", encoding="utf-8") as f:
                json.dump(self.historico, f, ensure_ascii=False, indent=2)
        except OSError:
            print("Aviso: não foi possível salvar o histórico.")

    def registrar(self, origem, pergunta, id_orientacao, encontrou, ajudou, tentativas, tempo):
        atendimento = {
            "data": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "origem": origem,
            "pergunta": pergunta,
            "id_orientacao": id_orientacao,
            "encontrou": encontrou,
            "ajudou": ajudou,
            "tentativas": tentativas,
            "tempo_segundos": tempo,
            "facilidade": None,
        }
        self.historico.append(atendimento)
        self._salvar_historico()

    # ---------- entradas seguras ----------
    @staticmethod
    def tem_dado_pessoal(texto):
        """8 ou mais dígitos (CPF, telefone, etc.) ou '@' (e-mail)."""
        return len(re.findall(r"\d", texto)) >= 8 or "@" in texto

    @staticmethod
    def ler_sim_nao(mensagem):
        while True:
            r = input(mensagem).strip().lower()
            if r in ("s", "n"):
                return r == "s"
            print("Resposta inválida. Digite s ou n.")

    @staticmethod
    def ler_opcao(mensagem, maximo):
        """Lê um número de 0 a maximo; qualquer outra entrada é recusada sem encerrar."""
        while True:
            r = input(mensagem).strip()
            if r.isdigit() and 0 <= int(r) <= maximo:
                return int(r)
            print(f"Opção inválida. Digite um número de 0 a {maximo}.")

    # ---------- atendimento ----------
    def _extras_energia(self, orientacao):
        """Se a orientação tem simulação de energia, exibe e oferece usar o consumo do usuário."""
        if not orientacao.calculo:
            return
        if self.simulador is None:
            from energia.simulacao import Simulador
            self.simulador = Simulador()
        print()
        print(self.simulador.simular(orientacao.calculo))
        if orientacao.calculo in ("solar", "comparar"):
            print()
            while True:
                r = input("Quer simular com o seu consumo mensal? Digite os kWh do mês "
                          "(ex.: 900) ou 0 para pular: ").strip().replace(",", ".")
                if r == "0":
                    return
                if self.tem_dado_pessoal(r):
                    print("Atenção: não digite CPF, telefone ou e-mail.")
                    continue
                try:
                    kwh = float(r)
                except ValueError:
                    print("Entrada inválida. Digite apenas o número de kWh.")
                    continue
                if not 50 <= kwh <= 100000:
                    print("Digite um consumo entre 50 e 100000 kWh.")
                    continue
                print(self.simulador.simular("personalizado", kwh))
                return

    def _mostrar(self, orientacao):
        orientacao.exibir()
        self._extras_energia(orientacao)

    def perguntar(self):
        """Pergunta em texto livre. Usa base.buscar() e orientacao.exibir()."""
        inicio = time.time()
        tentativas = 0
        ultima = ""
        while True:
            texto = input("\nDigite sua dúvida (0 para voltar): ").strip()
            if texto == "0":
                if tentativas:  # desistiu depois de tentar: dúvida sem solução
                    self.registrar("pergunta", ultima, None, False, False, tentativas,
                                   round(time.time() - inicio, 1))
                return
            if not texto:
                print("Escreva sua dúvida ou digite 0 para voltar.")
                continue
            if self.tem_dado_pessoal(texto):
                print("Atenção: não digite CPF, telefone ou e-mail. Reescreva.")
                continue  # não conta como tentativa e não é registrado
            tentativas += 1
            ultima = texto
            resultados = self.base.buscar(texto)
            if not resultados or resultados[0][0] < 3:
                print("\nNão encontrei uma orientação para essa dúvida.")
                print("Tente outras palavras ou navegue pelas categorias:")
                for cat in self.base.categorias():
                    print(f"  - {cat}")
                continue
            pontos, melhor = resultados[0]
            confianca = "ALTA" if pontos >= 6 else "MÉDIA"
            print(f"\nConfiança da resposta: {confianca} ({pontos} pontos)\n")
            self._mostrar(melhor)
            alternativas = [o for _, o in resultados[1:3]]
            if alternativas:
                print("\nTalvez ajude também:")
                for o in alternativas:
                    print(f"  - {o.titulo}")
            ajudou = self.ler_sim_nao("\nEssa orientação respondeu sua dúvida? (s/n): ")
            self.registrar("pergunta", texto, melhor.id, True, ajudou, tentativas,
                           round(time.time() - inicio, 1))
            return

    def navegar(self):
        """Navegação por categorias, com '0 para voltar' em todas as telas."""
        categorias = self.base.categorias()
        while True:
            print("\n=== Categorias ===")
            for i, cat in enumerate(categorias, 1):
                print(f"{i}. {cat}")
            print("0. Voltar")
            op = self.ler_opcao("Escolha uma categoria: ", len(categorias))
            if op == 0:
                return
            lista = self.base.por_categoria(categorias[op - 1])
            while True:
                print(f"\n=== {categorias[op - 1]} ===")
                for i, o in enumerate(lista, 1):
                    print(f"{i}. {o.titulo}")
                print("0. Voltar")
                sel = self.ler_opcao("Escolha uma orientação: ", len(lista))
                if sel == 0:
                    break
                inicio = time.time()
                escolhida = lista[sel - 1]
                print()
                self._mostrar(escolhida)
                ajudou = self.ler_sim_nao("\nEssa orientação respondeu sua dúvida? (s/n): ")
                self.registrar("categoria", escolhida.titulo, escolhida.id, True, ajudou, 1,
                               round(time.time() - inicio, 1))

    # ---------- indicadores ----------
    def indicadores(self):
        """Dicionário com os indicadores calculados a partir do histórico."""
        n = len(self.historico)
        if n == 0:
            return None
        encontrados = [a for a in self.historico if a["encontrou"]]
        ajudaram = [a for a in encontrados if a["ajudou"]]
        notas = [a["facilidade"] for a in self.historico if a.get("facilidade")]
        return {
            "atendimentos": n,
            "encontrada_pct": 100 * len(encontrados) / n,
            "ajudou_pct": 100 * len(ajudaram) / len(encontrados) if encontrados else 0.0,
            "tempo_medio": (sum(a["tempo_segundos"] for a in encontrados) / len(encontrados)
                            if encontrados else 0.0),
            "tentativas_media": sum(a["tentativas"] for a in self.historico) / n,
            "facilidade_media": sum(notas) / len(notas) if notas else None,
            "sem_solucao": [a["pergunta"] for a in self.historico if not a["encontrou"]],
        }

    def exibir_indicadores(self):
        ind = self.indicadores()
        print("\n=== Indicadores ===")
        if ind is None:
            print("Ainda não há atendimentos registrados.")
            return
        print(f"Atendimentos registrados:       {ind['atendimentos']}")
        print(f"Resposta encontrada (%):        {ind['encontrada_pct']:.1f}")
        print(f"Taxa de acerto: ajudou (%):     {ind['ajudou_pct']:.1f}")
        print(f"Tempo médio para encontrar:     {ind['tempo_medio']:.1f} s")
        print(f"Tentativas por atendimento:     {ind['tentativas_media']:.2f}")
        fac = ind["facilidade_media"]
        print(f"Facilidade de uso (1 a 5):      {fac:.1f}" if fac is not None
              else "Facilidade de uso (1 a 5):      sem notas ainda")
        print("Dúvidas sem solução:")
        if ind["sem_solucao"]:
            for p in ind["sem_solucao"]:
                print(f"  - {p}")
        else:
            print("  nenhuma")

    def exportar_csv(self):
        """Exporta o histórico para CSV com csv.DictWriter."""
        if not self.historico:
            print("Não há atendimentos para exportar.")
            return
        try:
            with open(self.caminho_csv, "w", encoding="utf-8", newline="") as f:
                escritor = csv.DictWriter(f, fieldnames=CAMPOS_CSV, extrasaction="ignore")
                escritor.writeheader()
                escritor.writerows(self.historico)
            print(f"{len(self.historico)} atendimentos exportados para {self.caminho_csv}")
        except OSError:
            print("Não foi possível gravar o CSV (feche o arquivo se estiver aberto).")

    def pedir_nota_facilidade(self, desde):
        """Ao sair, pede nota de 1 a 5 e guarda no último atendimento da sessão."""
        if len(self.historico) <= desde:
            return
        while True:
            r = input("\nDe 1 a 5, qual a facilidade de usar o assistente? ").strip()
            if r in ("1", "2", "3", "4", "5"):
                self.historico[-1]["facilidade"] = int(r)
                self._salvar_historico()
                return
            print("Nota inválida. Digite um número de 1 a 5.")
