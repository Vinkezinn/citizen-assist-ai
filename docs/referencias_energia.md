# Referências

Dados e fontes usados em `energia/data/premissas.csv` e nas orientações de `data/base_conhecimento.json`. Conferência feita em **17/11/2026**. A coluna "Situação" diz o que foi realmente conferido e como.

| # | Dado | Fonte | Situação |
|---|---|---|---|
| 1 | Tarifa com tributos: TUSD 0,55485 + TE 0,37556 R$/kWh (mar/2026) | Faturas Enel SP publicadas em camara.leg.br/cota-parlamentar (documentos públicos de 2026) | Conferido em várias faturas de mar/2026 (valores de 0,55434 a 0,55486 e 0,37525 a 0,37559) |
| 2 | Reajuste Enel SP, vigência 04/07/2026: média 10,18% (todas as classes), 8,97% na baixa tensão, 9,02% nos residenciais | ANEEL, via Agência Brasil, InfoMoney, Cenário Energia | Conferido em várias notícias |
| 3 | Bandeiras (por 100 kWh): amarela R$ 1,885, vermelha 1 R$ 4,463, vermelha 2 R$ 7,877; novembro/2026 verde | ANEEL, via Agência Brasil e imprensa | Conferido |
| 4 | Fio B: 60% (2026), 75% (2027), 90% (2028); 2029 pelo art. 17; quem pediu acesso até 7/1/2023 tem regra anterior | Lei 14.300/2022, art. 27 (planalto.gov.br) | Conferido em textos que reproduzem o artigo; a página do Planalto não foi aberta |
| 5 | Custo de disponibilidade: 30/50/100 kWh | REN ANEEL 1.000/2021, art. 291 | Conferido em várias fontes que citam o artigo |
| 6 | Fator de emissão do SIN: 38,5 kgCO₂/MWh (2023); 21,5 a 28,9 kg/MWh (mar e abr/2025) | MCTI (SIRENE), via eixos.com.br e canalsolar.com.br | Conferido |
| 7 | Irradiação solar, capital de SP, 4,5 a 4,8 kWh/m².dia | CRESESB SunData (cresesb.cepel.br/sundata) | **Não reconferido.** Tratado como estimado; sensibilidade com 4,0 |
| 8 | Preço médio solar residencial R$ 2,45/Wp (1º tri/2026) | Radar Solfácil, via Cenário Energia | Da pesquisa anterior, **não reconferido** nesta rodada; usado só como cenário |
| 9 | Selo Procel (voluntário, em geral classe A) e etiqueta ENCE (A a G) | Agência Gov (set/2023); CLASP; Agência Minas | Conferido |
| 10 | LED: eficiência luminosa, potência (W) e etiqueta ENCE | Cartilha do Inmetro sobre lâmpadas LED (gov.br/inmetro) | Conferido |
| 11 | Tarifa branca: ponta, intermediário e fora de ponta; fins de semana e feriados fora de ponta | ANEEL, via Agência iNFRA e EDP | Conferido |
| 12 | Reclamação: Consumidor.gov.br e app ANEEL Consumidor | Página "Reclame da Distribuidora", gov.br/aneel | Página aberta e lida |
| 13 | Microgeração até 75 kW; solicitação e parecer de acesso | Lei 14.300/2022 e FAQ da ANEEL | Conferido em textos da lei e da regulação |

**Dados que NÃO têm fonte** (estimados pelo grupo): potência e uso dos equipamentos, economia de 30% e 15% dos modelos eficientes, preços dos equipamentos e do LED, R$ 3,00/Wp comercial, simultaneidade (50%), parcela do Fio B na tarifa (25%, ordem de grandeza coerente com notícias que citam R$ 0,12 por kWh para 60% do Fio B), reajuste anual da tarifa (4%), desempenho (0,80), degradação (0,5%/ano). Estão marcados como `estimado` nos CSV.
