"""Simulações de energia exibidas pelo assistente (contribuição de Energias Renováveis e Sustentáveis).

Cada função devolve um texto curto montado a partir de energia/calculos.py,
de modo que o que o assistente diz é sempre coerente com os cálculos.
"""
import re

from . import calculos as c

AVISO = ("Estimativa com premissas simplificadas, não é garantia de economia, geração ou custo. "
         "Confira sua fatura e peça orçamentos reais.")
FONTES = ("Fontes das premissas: faturas Enel SP (mar/2026), CRESESB, Lei 14.300/2022, "
          "Solfácil/Radar (1º tri/2026), MCTI. Detalhes em docs/referencias_energia.md.")


def _brl(v):
    return "R$ " + f"{v:,.0f}".replace(",", ".")


def _anos(v, horizonte):
    return f"{v:.1f} anos" if v is not None else f"mais de {horizonte} anos"


def _virgula(texto):
    """Decimais no padrão brasileiro (1 ou 2 casas após o ponto vira vírgula)."""
    return re.sub(r"(\d)\.(\d{1,2})(?!\d)", r"\1,\2", texto)


class Simulador:
    def __init__(self):
        self.p = c.carregar_premissas()
        self.eq = c.carregar_equipamentos()
        self.h = int(self.p["horizonte_anos"])
        self.base = c.consumo_mensal(self.eq)
        self.ef, self.fv, self.cb = c.comparar(self.eq, self.p, self.h)

    def led(self):
        e = next(x for x in self.eq if "tubular" in x["nome"].lower())
        antes = c.energia_mensal_kwh(e["qtd"], e["potencia_w"], e["horas_dia"], e["fator_uso"], e["dias_mes"])
        dep = c.energia_mensal_kwh(e["qtd"], e["potencia_w_eficiente"], e["horas_dia"], e["fator_uso"], e["dias_mes"])
        custo = e["qtd"] * e["custo_troca_unit"]
        eco = (antes - dep) * self.p["tarifa_kwh"]
        retorno = custo / eco if eco else None
        return (f"Simulação (comércio-modelo, dados estimados): {int(e['qtd'])} lâmpadas tubulares de "
                f"{e['potencia_w']:.0f} W (com reator) trocadas por LED de {e['potencia_w_eficiente']:.0f} W, "
                f"12 h por dia. Economia: {antes - dep:.0f} kWh/mês, cerca de {_brl(eco)}/mês "
                f"(tarifa R$ {self.p['tarifa_kwh']:.2f}/kWh). Custo das lâmpadas: {_brl(custo)}, "
                f"retorno em {retorno:.1f} meses, sem contar a instalação.")

    def refrigeracao(self):
        refrig = [e for e in self.eq if any(k in e["nome"].lower() for k in ("expositor", "freezer", "câmara", "camara"))]
        antes = sum(c.energia_mensal_kwh(e["qtd"], e["potencia_w"], e["horas_dia"], e["fator_uso"], e["dias_mes"]) for e in refrig)
        dep = sum(c.energia_mensal_kwh(e["qtd"], e["potencia_w_eficiente"], e["horas_dia"], e["fator_uso"], e["dias_mes"]) for e in refrig)
        custo = sum(e["qtd"] * e["custo_troca_unit"] for e in refrig)
        eco = (antes - dep) * self.p["tarifa_kwh"]
        return (f"Simulação (comércio-modelo, dados estimados): a refrigeração consome {antes:.0f} kWh/mês "
                f"({antes / self.base:.0%} do total). Com modelos eficientes e vedação/termostato da câmara fria, "
                f"cairia para {dep:.0f} kWh/mês, economia de cerca de {_brl(eco)}/mês. Investimento estimado "
                f"{_brl(custo)} (retorno em {_anos(custo / eco / 12 if eco else None, self.h)}). "
                "Os percentuais de economia (30% e 15%) e os preços são estimados.")

    def solar(self):
        d = self.fv.detalhes
        return (f"Simulação (comércio-modelo, {self.base:.0f} kWh/mês): sistema de cerca de {d['kwp']:.1f} kWp "
                f"(irradiação {self.p['irradiacao_hsp']} kWh/m².dia, desempenho {self.p['performance_ratio']:.0%}), "
                f"investimento estimado {_brl(self.fv.investimento)} (R$ {self.p['custo_wp']:.2f}/Wp, estimado), "
                f"economia no 1º ano {_brl(self.fv.economia_ano1)} já descontado o Fio B, retorno em "
                f"{_anos(self.fv.payback_anos, self.h)}. Não inclui troca de inversor nem financiamento.")

    def comparar(self):
        linhas = []
        for r in (self.ef, self.fv, self.cb):
            linhas.append(f"- {r.nome}: investimento {_brl(r.investimento)}, economia no 1º ano "
                          f"{_brl(r.economia_ano1)}, saldo em {self.h} anos {_brl(r.saldo)}, retorno em "
                          f"{_anos(r.payback_anos, self.h)}, CO₂ evitado {r.co2_evitado_t_ano1:.2f} t/ano")
        rec = (f"Recomendação: comece pela eficiência; assim o sistema solar cai de "
               f"{self.fv.detalhes['kwp']:.1f} para {self.cb.detalhes['kwp']:.1f} kWp. O CO₂ evitado é pequeno "
               "porque a rede brasileira já é majoritariamente renovável: o argumento principal é financeiro.")
        return (f"Simulação (comércio-modelo, mesmo período de {self.h} anos):\n" + "\n".join(linhas) + "\n" + rec)

    def personalizado(self, kwh):
        s = c.analisar_solar(kwh, self.p, self.h)
        d = s.detalhes
        custo_mes = kwh * self.p["tarifa_kwh"]
        pct = self.ef.detalhes["kwh_mes_poupados"] / self.base
        return (f"Com {kwh:.0f} kWh/mês, sua conta seria cerca de {_brl(custo_mes)}/mês (tarifa "
                f"R$ {self.p['tarifa_kwh']:.2f}/kWh, ajuste se a sua for diferente). Um sistema solar teria "
                f"~{d['kwp']:.1f} kWp, investimento estimado {_brl(s.investimento)} e retorno em "
                f"{_anos(s.payback_anos, self.h)}. Se sua redução com eficiência for parecida com a do "
                f"comércio-modelo ({pct:.0%}), economizaria ~{kwh * pct:.0f} kWh/mês antes do solar (suposição).")

    def simular(self, tipo, kwh=None):
        if tipo == "personalizado":
            texto = self.personalizado(kwh)
        else:
            funcoes = {"led": self.led, "refrigeracao": self.refrigeracao,
                       "solar": self.solar, "comparar": self.comparar}
            texto = funcoes[tipo]()
        return _virgula(texto + "\n" + AVISO + "\n" + FONTES)


if __name__ == "__main__":
    # python -m energia.simulacao  -> tabela comparativa das alternativas (usada no vídeo de Energia)
    s = Simulador()
    print(f"Consumo-base: {s.base:.1f} kWh/mês | Horizonte: {s.h} anos\n")
    print(f"{'Alternativa':45} {'Invest.':>10} {'Eco. 1º ano':>12} {'Saldo':>10} {'Payback':>9} {'tCO2/ano':>9}")
    for r in (s.ef, s.fv, s.cb):
        pb = f"{r.payback_anos:.1f}" if r.payback_anos is not None else f">{s.h}"
        print(f"{r.nome:45} {r.investimento:10,.0f} {r.economia_ano1:12,.0f} {r.saldo:10,.0f} {pb:>9} {r.co2_evitado_t_ano1:9.2f}")
