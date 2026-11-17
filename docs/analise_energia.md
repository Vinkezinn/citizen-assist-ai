# Análise de consumo e comparação de alternativas

## 1. Contexto

Comércio-modelo (mercadinho de bairro, Enel SP, grupo B). Necessidade: reduzir o custo de refrigeração e iluminação. Período de referência comum: **10 anos**. Todos os valores são calculados por `energia/calculos.py` a partir de `energia/data/`.

## 2. Consumo (dados estimados)

Fórmula: **E (kWh/mês) = qtd × P (W) × horas/dia × fator de uso × dias ÷ 1000**

| Equipamento | Qtd | P (W) | h/dia | Fator de uso | kWh/mês | Parte |
|---|---|---|---|---|---|---|
| Lâmpada tubular fluorescente 40 W + reator | 40 | 45 | 12 | 1,0 | 648 | 42% |
| Câmara fria pequena | 1 | 1.500 | 24 | 0,4 | 432 | 28% |
| Expositor vertical refrigerado | 2 | 400 | 24 | 0,5 | 288 | 19% |
| Freezer horizontal | 1 | 300 | 24 | 0,5 | 108 | 7% |
| Computador/PDV/balança | 3 | 100 | 12 | 0,7 | 76 | 5% |
| **Total** | | | | | **1.552** | |

Potências, horas e fatores de uso são **estimados** (o grupo deve substituir por medições, etiquetas ou a fatura do comércio escolhido). Custo mensal: 1.552 × R$ 0,93 = ~R$ 1.443.

## 3. Alternativas

**A. Eficiência energética.** LED 18 W no lugar das tubulares; expositores e freezer eficientes (−30%); vedação e termostato da câmara fria (−15%). Consumo cai de 1.552 para **979 kWh/mês** (−572 kWh). Investimento estimado: R$ 18.100.

**B. Energia solar fotovoltaica (fonte renovável).** Dimensionada para cobrir o consumo menos o custo de disponibilidade (50 kWh): 1.502 kWh/mês ÷ (4,5 × 30 × 0,80) = **13,9 kWp**. Investimento: 13,9 kWp × R$ 3,00/Wp = R$ 41.711.

**C. Eficiência + solar menor.** Faz A primeiro e dimensiona o solar para 979 kWh/mês: **8,6 kWp**.

### Modelo de fluxo de caixa (anos 1 a 10)

- Tarifa do ano t = 0,93 × 1,04^(t−1).
- Geração cai 0,5%/ano. Energia compensada = mínimo entre geração e necessidade.
- **Fio B** sobre a energia injetada (50% da geração): injetado × tarifa × 25% × percentual (75% no ano 1 = 2027; 90% depois).
- Manutenção do solar: 1% do investimento por ano.
- Payback simples (sem desconto), com interpolação dentro do ano.

## 4. Resultados (caso-base)

| Alternativa | Investimento | Economia 1º ano | Retorno | Saldo em 10 anos | CO₂ evitado/ano |
|---|---|---|---|---|---|
| A. Eficiência | R$ 18.100 | R$ 6.388 | 2,7 anos | R$ 58.595 | 0,26 t |
| B. Solar | R$ 41.711 | R$ 14.770 | 2,8 anos | R$ 128.747 | 0,69 t |
| C. Eficiência + solar | R$ 43.911 | R$ 15.528 | 2,8 anos | R$ 138.264 | 0,69 t |

## 5. Sensibilidade (retorno em anos / saldo em 10 anos, R$)

| Cenário | A | B | C |
|---|---|---|---|
| Caso-base | 2,7 / 58.595 | 2,8 / 128.747 | 2,8 / 138.264 |
| Solar a R$ 4,00/Wp | 2,7 / 58.595 | 3,7 / 113.453 | 3,3 / 128.800 |
| Solar a R$ 2,45/Wp | 2,7 / 58.595 | 2,3 / 137.159 | 2,5 / 143.470 |
| Tarifa R$ 0,75/kWh | 3,3 / 43.751 | 3,4 / 94.948 | 3,4 / 102.505 |
| Tarifa R$ 1,00/kWh | 2,6 / 64.368 | 2,6 / 141.891 | 2,6 / 152.171 |
| Tarifa R$ 1,01/kWh (com reajuste da baixa tensão de 8,97%) | 2,5 / 65.192 | 2,6 / 143.769 | 2,5 / 154.157 |
| Sem reajuste da tarifa | 2,8 / 45.780 | 2,9 / 99.856 | 2,9 / 107.571 |
| Fio B = 40% da tarifa | 2,7 / 58.595 | 3,0 / 115.678 | 2,9 / 130.177 |
| Irradiação 4,0 kWh/m².dia | 2,7 / 58.595 | 3,1 / 123.012 | 3,0 / 134.715 |
| Desempenho (PR) 0,70 | 2,7 / 58.595 | 3,2 / 122.192 | 3,0 / 134.208 |

## 6. Justificativas das recomendações

- **Custo.** A eficiência custa menos e se paga em prazo parecido com o solar. O solar gera o maior saldo no longo prazo.
- **Viabilidade.** A eficiência não depende de telhado nem de aprovação da distribuidora. O solar depende de área, sombra, estrutura, projeto e homologação.
- **Impacto ambiental.** O fator de emissão do SIN é baixo (38,5 kgCO₂/MWh em 2023), então o CO₂ evitado é pequeno (0,26 a 0,69 t/ano). O argumento principal é financeiro; o ambiental é secundário. Emissões de fabricação não foram incluídas.
- **Ordem recomendada (C).** Reduzir o consumo primeiro diminui o solar de 13,9 para 8,6 kWp e evita superdimensionar.

## 7. Limitações

1. Consumo dos equipamentos, preços e percentuais de economia são estimados.
2. Tarifa de março/2026 (faturas residenciais da Enel SP, sem bandeira). Em 04/07/2026 houve reajuste médio de 8,97% na baixa tensão (10,18% é a média de todas as classes): a linha "Tarifa R$ 1,01" da sensibilidade mostra o efeito. O comércio pode ser da classe B3, com tarifa diferente: confirmar na fatura real.
3. Retorno simples, sem juros, financiamento, impostos, depreciação ou troca de inversor.
4. Fio B: parcela de 25% da tarifa é estimativa; regra após 2029 depende da ANEEL.
5. Os resultados são estimativas, não garantias de economia, geração ou custo.
6. O retorno de ~2,7 anos é sensível ao preço dos equipamentos e à tarifa: valide com orçamentos reais antes de apresentar como conclusão.

7. A irradiação de 4,5 kWh/m².dia é estimada e não foi reconferida no CRESESB; com 4,0 o retorno do solar passa de 2,8 para 3,1 anos (veja a sensibilidade).
8. O percentual do Fio B (60% em 2026, 75% em 2027, 90% em 2028) vale para quem pediu acesso depois de 7/1/2023; de 2029 em diante a regra depende da ANEEL e foi mantida em 90%.
9. A tarifa de ~R$ 0,93 não inclui a bandeira tarifária (verde em novembro de 2026); em bandeira amarela ou vermelha o kWh fica mais caro e a economia, maior.
