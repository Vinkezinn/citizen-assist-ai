import builtins
import contextlib
import io
import json
import os
import sys
import tempfile
import unittest
from unittest import mock

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, RAIZ)

from assistente import Assistente  # noqa: E402
from base_conhecimento import BaseConhecimento, normalizar  # noqa: E402
from energia import calculos as c  # noqa: E402
from energia.simulacao import Simulador  # noqa: E402

BASE = os.path.join(RAIZ, "data", "base_conhecimento.json")


def criar(tmp):
    base = BaseConhecimento(BASE)
    assert base.carregar()[0]
    return Assistente("Teste", base, os.path.join(tmp, "h.json"), os.path.join(tmp, "a.csv"))


def rodar(func, entradas):
    """Executa func simulando input() e devolve o texto impresso."""
    it = iter(entradas)
    saida = io.StringIO()
    with mock.patch.object(builtins, "input", lambda _="": next(it)), contextlib.redirect_stdout(saida):
        func()
    return saida.getvalue()


class TestBase(unittest.TestCase):
    def setUp(self):
        self.base = BaseConhecimento(BASE)
        self.base.carregar()

    def test_requisitos_minimos_da_base(self):
        self.assertGreaterEqual(len(self.base.orientacoes), 10)
        self.assertGreaterEqual(len(self.base.categorias()), 3)
        for o in self.base.orientacoes:
            self.assertGreaterEqual(len(o.palavras_chave), 3, o.titulo)
            self.assertTrue(o.fonte.startswith("http"), o.titulo)
            self.assertTrue(o.verificado_em, o.titulo)

    def test_ids_unicos(self):
        ids = [o.id for o in self.base.orientacoes]
        self.assertEqual(len(ids), len(set(ids)))

    def test_normalizar(self):
        self.assertEqual(normalizar("  Cartão do SUS?! "), " cartao do sus ")

    def test_pontuacao_exemplo(self):
        # "bandeira vermelha" (+3) e "bandeira" (+3) = 6, confiança ALTA
        o = next(x for x in self.base.orientacoes if x.id == 2)
        self.assertEqual(self.base.pontuar("O que é bandeira vermelha?", o), 6)

    def test_pontos_do_titulo(self):
        o = next(x for x in self.base.orientacoes if x.id == 7)
        # "lampadas" ("lâmpadas" no título) +1 pelo título, +3 pela chave "lampadas"
        self.assertEqual(self.base.pontuar("lâmpadas", o), 4)

    def test_buscar_devolve_tuplas_ordenadas(self):
        r = self.base.buscar("quanto custa solar e o fio b")
        self.assertTrue(all(isinstance(t, tuple) and len(t) == 2 for t in r))
        pontos = [t[0] for t in r]
        self.assertEqual(pontos, sorted(pontos, reverse=True))

    def test_pergunta_sem_resultado(self):
        self.assertEqual(self.base.buscar("qualquer coisa sem relacao"), [])

    def test_alteracao_ao_vivo_no_json(self):
        # roteiro do vídeo: "quero pagar menos" não é encontrada; com a palavra-chave nova, passa a ser
        antes = self.base.buscar("quero pagar menos")
        self.assertTrue(not antes or antes[0][0] < 3)
        next(o for o in self.base.orientacoes if o.id == 12).palavras_chave.append("pagar menos")
        depois = self.base.buscar("quero pagar menos")
        self.assertGreaterEqual(depois[0][0], 3)
        self.assertEqual(depois[0][1].id, 12)

    def test_json_ausente_e_corrompido_nao_travam(self):
        ok, msg = BaseConhecimento("nao_existe.json").carregar()
        self.assertFalse(ok)
        with tempfile.TemporaryDirectory() as t:
            p = os.path.join(t, "x.json")
            with open(p, "w") as f:
                f.write("{ quebrado")
            ok, msg = BaseConhecimento(p).carregar()
            self.assertFalse(ok)
            self.assertIn("corrompido", msg)


class TestAssistente(unittest.TestCase):
    def test_dado_pessoal(self):
        self.assertTrue(Assistente.tem_dado_pessoal("meu cpf é 123.456.789-00"))
        self.assertTrue(Assistente.tem_dado_pessoal("a@b.com"))
        self.assertTrue(Assistente.tem_dado_pessoal("telefone 11987654321"))
        self.assertFalse(Assistente.tem_dado_pessoal("consumo de 900 kwh"))

    def test_pergunta_encontrada_e_registrada(self):
        with tempfile.TemporaryDirectory() as t:
            a = criar(t)
            saida = rodar(a.perguntar, ["O que é bandeira vermelha?", "s"])
            self.assertIn("Confiança da resposta: ALTA", saida)
            self.assertIn("NÃO é um canal oficial", saida)
            self.assertIn("verificado em", saida)
            self.assertEqual(len(a.historico), 1)
            h = a.historico[0]
            self.assertTrue(h["encontrou"] and h["ajudou"])
            self.assertEqual(h["id_orientacao"], 2)
            with open(os.path.join(t, "h.json"), encoding="utf-8") as f:
                self.assertEqual(len(json.load(f)), 1)

    def test_dado_pessoal_bloqueado_e_nao_registrado(self):
        with tempfile.TemporaryDirectory() as t:
            a = criar(t)
            saida = rodar(a.perguntar, ["meu cpf é 123.456.789-00", "0"])
            self.assertIn("não digite CPF", saida)
            self.assertEqual(a.historico, [])
            with open(a.caminho_historico if os.path.exists(a.caminho_historico) else os.devnull) as f:
                self.assertNotIn("123.456", f.read())

    def test_nao_encontrada_vira_duvida_sem_solucao(self):
        with tempfile.TemporaryDirectory() as t:
            a = criar(t)
            saida = rodar(a.perguntar, ["xyz abc", "0"])
            self.assertIn("Não encontrei", saida)
            self.assertFalse(a.historico[0]["encontrou"])
            self.assertEqual(a.indicadores()["sem_solucao"], ["xyz abc"])

    def test_entradas_invalidas_nao_encerram(self):
        with tempfile.TemporaryDirectory() as t:
            a = criar(t)
            saida = rodar(a.navegar, ["abc", "", "9", "-1", "0"])
            self.assertEqual(saida.count("Opção inválida"), 4)
            saida = rodar(a.perguntar, ["", "0"])
            self.assertIn("Escreva sua dúvida", saida)

    def test_sim_nao_invalido(self):
        with mock.patch.object(builtins, "input", side_effect=["talvez", "", "s"]), \
                contextlib.redirect_stdout(io.StringIO()):
            self.assertTrue(Assistente.ler_sim_nao("? "))

    def test_navegacao_registra_atendimento(self):
        with tempfile.TemporaryDirectory() as t:
            a = criar(t)
            # categoria 1, orientação 2 (bandeiras), ajudou s, voltar, voltar
            rodar(a.navegar, ["1", "2", "s", "0", "0"])
            self.assertEqual(len(a.historico), 1)
            self.assertEqual(a.historico[0]["origem"], "categoria")
            self.assertEqual(a.historico[0]["id_orientacao"], 2)

    def test_indicadores_e_csv(self):
        with tempfile.TemporaryDirectory() as t:
            a = criar(t)
            rodar(a.perguntar, ["O que é bandeira vermelha?", "s"])
            rodar(a.perguntar, ["xyz abc", "0"])
            rodar(a.perguntar, ["O que é bandeira vermelha?", "n"])
            ind = a.indicadores()
            self.assertEqual(ind["atendimentos"], 3)
            self.assertAlmostEqual(ind["encontrada_pct"], 200 / 3)
            self.assertAlmostEqual(ind["ajudou_pct"], 50.0)
            rodar(lambda: a.pedir_nota_facilidade(0), ["7", "x", "4"])
            self.assertEqual(a.indicadores()["facilidade_media"], 4)
            a.exportar_csv()
            with open(a.caminho_csv, encoding="utf-8") as f:
                linhas = f.read().strip().splitlines()
            self.assertEqual(len(linhas), 4)
            self.assertTrue(linhas[0].startswith("data,origem,pergunta"))

    def test_historico_corrompido_nao_trava(self):
        with tempfile.TemporaryDirectory() as t:
            with open(os.path.join(t, "h.json"), "w") as f:
                f.write("###")
            with contextlib.redirect_stdout(io.StringIO()):
                a = criar(t)
            self.assertEqual(a.historico, [])

    def test_simulacao_de_energia_integrada(self):
        with tempfile.TemporaryDirectory() as t:
            a = criar(t)
            saida = rodar(a.perguntar, ["quanto custa solar?", "900", "s"])
            self.assertIn("kWp", saida)
            self.assertIn("Estimativa", saida)
            self.assertIn("Com 900 kWh/mês", saida)


class TestEnergia(unittest.TestCase):
    def setUp(self):
        self.p = c.carregar_premissas()
        self.eq = c.carregar_equipamentos()

    def test_energia_mensal(self):
        self.assertAlmostEqual(c.energia_mensal_kwh(2, 400, 24, 0.5, 30), 288.0)

    def test_consumo_base_e_eficiente(self):
        self.assertAlmostEqual(c.consumo_mensal(self.eq), 1551.6, places=1)
        self.assertAlmostEqual(c.consumo_mensal(self.eq, eficiente=True), 979.2, places=1)

    def test_dimensionamento_solar(self):
        dim = c.dimensionar_solar(1000, self.p)
        self.assertAlmostEqual(dim["kwp"] * 4.5 * 30 * 0.8, 950, places=6)

    def test_payback_interpolado(self):
        self.assertAlmostEqual(c._payback(150, [100, 100, 100]), 1.5)
        self.assertIsNone(c._payback(1000, [100, 100]))

    def test_comparacao_coerente(self):
        ef, fv, cb = c.comparar(self.eq, self.p)
        self.assertLess(cb.detalhes["kwp"], fv.detalhes["kwp"])
        for r in (ef, fv, cb):
            self.assertAlmostEqual(r.saldo, r.economia_total - r.investimento)

    def test_fio_b_reduz_economia_solar(self):
        sem = dict(self.p, fio_b_parcela_tarifa=0.0)
        self.assertGreater(c.analisar_solar(1500, sem).economia_total,
                           c.analisar_solar(1500, self.p).economia_total)

    def test_textos_da_simulacao(self):
        s = Simulador()
        for tipo in ("led", "refrigeracao", "solar", "comparar"):
            texto = s.simular(tipo)
            self.assertIn("Estimativa", texto, tipo)
            self.assertNotRegex(texto, r"\d\.\d(?!\d)", tipo)  # decimais com vírgula
        self.assertIn("900 kWh", s.simular("personalizado", 900))


if __name__ == "__main__":
    unittest.main()
