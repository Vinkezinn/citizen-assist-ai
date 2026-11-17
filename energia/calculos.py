"""Cálculos de energia: consumo, eficiência energética e solar fotovoltaica.

Todas as premissas vêm de data/premissas.csv e data/equipamentos.csv.
Os resultados são ESTIMATIVAS, não garantias.
"""
import csv
import os
from dataclasses import dataclass, field
from typing import List, Optional

RAIZ = os.path.dirname(os.path.abspath(__file__))
DADOS = os.path.join(RAIZ, "data")


def carregar_premissas(caminho: Optional[str] = None) -> dict:
    """Lê premissas.csv e devolve {chave: valor float}."""
    caminho = caminho or os.path.join(DADOS, "premissas.csv")
    with open(caminho, encoding="utf-8", newline="") as f:
        return {l["chave"]: float(l["valor"]) for l in csv.DictReader(f)}


def carregar_equipamentos(caminho: Optional[str] = None) -> List[dict]:
    caminho = caminho or os.path.join(DADOS, "equipamentos.csv")
    campos = ["qtd", "potencia_w", "horas_dia", "fator_uso", "dias_mes",
              "potencia_w_eficiente", "custo_troca_unit"]
    with open(caminho, encoding="utf-8", newline="") as f:
        linhas = list(csv.DictReader(f))
    for l in linhas:
        for c in campos:
            l[c] = float(l[c])
    return linhas


def energia_mensal_kwh(qtd, potencia_w, horas_dia, fator_uso, dias_mes) -> float:
    """E (kWh/mês) = qtd x P(W) x h/dia x fator de uso x dias / 1000."""
    return qtd * potencia_w * horas_dia * fator_uso * dias_mes / 1000.0


def consumo_mensal(equipamentos: List[dict], eficiente: bool = False) -> float:
    total = 0.0
    for e in equipamentos:
        p = e["potencia_w_eficiente"] if eficiente else e["potencia_w"]
        total += energia_mensal_kwh(e["qtd"], p, e["horas_dia"], e["fator_uso"], e["dias_mes"])
    return total


def investimento_eficiencia(equipamentos: List[dict]) -> float:
    return sum(e["qtd"] * e["custo_troca_unit"] for e in equipamentos)


@dataclass
class Resultado:
    nome: str
    investimento: float
    economia_ano1: float
    economia_total: float
    saldo: float
    payback_anos: Optional[float]
    kwh_evitados_ano1: float
    co2_evitado_t_ano1: float
    detalhes: dict = field(default_factory=dict)


def _payback(investimento: float, fluxos: List[float]) -> Optional[float]:
    """Payback simples com interpolação dentro do ano. None se não ocorre no horizonte."""
    if investimento <= 0:
        return 0.0
    acumulado = 0.0
    for i, f in enumerate(fluxos):
        if acumulado + f >= investimento:
            return i + (investimento - acumulado) / f if f > 0 else float(i + 1)
        acumulado += f
    return None


def _avaliar(nome, investimento, fluxos, kwh_ano1, p, detalhes) -> Resultado:
    total = sum(fluxos)
    return Resultado(
        nome=nome,
        investimento=investimento,
        economia_ano1=fluxos[0],
        economia_total=total,
        saldo=total - investimento,
        payback_anos=_payback(investimento, fluxos),
        kwh_evitados_ano1=kwh_ano1,
        co2_evitado_t_ano1=kwh_ano1 / 1000.0 * p["fator_emissao_t_mwh"],
        detalhes=detalhes,
    )


def _tarifa(p, t):  # t = 1..N
    return p["tarifa_kwh"] * (1 + p["reajuste_tarifa_anual"]) ** (t - 1)


def dimensionar_solar(consumo_kwh_mes: float, p: dict) -> dict:
    """Dimensiona o sistema para cobrir (consumo - custo de disponibilidade)."""
    necessidade = max(consumo_kwh_mes - p["custo_disponibilidade_kwh"], 0.0)
    kwh_por_kwp_mes = p["irradiacao_hsp"] * 30 * p["performance_ratio"]
    kwp = necessidade / kwh_por_kwp_mes
    return {"necessidade_kwh_mes": necessidade, "kwp": kwp,
            "geracao_kwh_mes": kwp * kwh_por_kwp_mes}


def fluxos_solar(consumo_kwh_mes: float, p: dict, anos: int):
    """Economia anual (R$) do solar, já descontados Fio B e manutenção."""
    dim = dimensionar_solar(consumo_kwh_mes, p)
    capex = dim["kwp"] * 1000 * p["custo_wp"]
    fluxos = []
    for t in range(1, anos + 1):
        geracao_mes = dim["geracao_kwh_mes"] * (1 - p["degradacao_anual"]) ** (t - 1)
        compensado = min(geracao_mes, dim["necessidade_kwh_mes"])
        injetado = geracao_mes * (1 - p["simultaneidade"])
        pct = p["fio_b_ano1"] if t == 1 else p["fio_b_ano2_em_diante"]
        tarifa = _tarifa(p, t)
        fio_b = injetado * tarifa * p["fio_b_parcela_tarifa"] * pct
        economia_mes = compensado * tarifa - fio_b
        fluxos.append(economia_mes * 12 - capex * p["om_solar_pct"])
    return dim, capex, fluxos


def fluxos_eficiencia(equipamentos: List[dict], p: dict, anos: int):
    antes = consumo_mensal(equipamentos)
    depois = consumo_mensal(equipamentos, eficiente=True)
    poupado = antes - depois
    fluxos = [poupado * 12 * _tarifa(p, t) for t in range(1, anos + 1)]
    return antes, depois, poupado, investimento_eficiencia(equipamentos), fluxos


def analisar_eficiencia(equipamentos, p, anos=None) -> Resultado:
    anos = int(anos or p["horizonte_anos"])
    antes, depois, poupado, capex, fluxos = fluxos_eficiencia(equipamentos, p, anos)
    return _avaliar("Alternativa A: eficiência energética", capex, fluxos, poupado * 12, p,
                    {"consumo_antes": antes, "consumo_depois": depois, "kwh_mes_poupados": poupado})


def analisar_solar(consumo_kwh_mes, p, anos=None) -> Resultado:
    anos = int(anos or p["horizonte_anos"])
    dim, capex, fluxos = fluxos_solar(consumo_kwh_mes, p, anos)
    return _avaliar("Alternativa B: energia solar fotovoltaica", capex, fluxos,
                    dim["geracao_kwh_mes"] * 12, p,
                    {**dim, "consumo_base": consumo_kwh_mes})


def analisar_combinada(equipamentos, p, anos=None) -> Resultado:
    """Eficiência primeiro; solar dimensionado para o consumo que sobra."""
    anos = int(anos or p["horizonte_anos"])
    antes, depois, poupado, capex_ef, fl_ef = fluxos_eficiencia(equipamentos, p, anos)
    dim, capex_fv, fl_fv = fluxos_solar(depois, p, anos)
    fluxos = [a + b for a, b in zip(fl_ef, fl_fv)]
    return _avaliar("Alternativa C: eficiência + solar menor", capex_ef + capex_fv, fluxos,
                    (poupado + dim["geracao_kwh_mes"]) * 12, p,
                    {**dim, "consumo_antes": antes, "consumo_depois": depois})


def comparar(equipamentos=None, p=None, anos=None) -> List[Resultado]:
    equipamentos = equipamentos or carregar_equipamentos()
    p = p or carregar_premissas()
    base = consumo_mensal(equipamentos)
    return [analisar_eficiencia(equipamentos, p, anos),
            analisar_solar(base, p, anos),
            analisar_combinada(equipamentos, p, anos)]
