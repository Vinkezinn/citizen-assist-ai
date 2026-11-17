# Citizen Assist AI: energia para pequenos comércios

Projeto único entregue em duas disciplinas da Global Solution 2026.2 (Ciência da Computação, turmas 1CC):

- **Pensamento Computacional e Automação com Python (PCP):** o assistente em si (JSON, classes, busca por pontuação, histórico, indicadores, CSV).
- **Soluções em Energias Renováveis e Sustentáveis:** a análise de energia e as simulações integradas ao assistente (pasta [`energia/`](energia/) e [`docs/`](docs/)).

> Contribuição de Energias Renováveis e Sustentáveis: pasta `energia/`, `docs/analise_energia.md`, `docs/referencias_energia.md` e as orientações da categoria "Eficiência energética" e "Energia solar" com campo `calculo` em `data/base_conhecimento.json`.

## Integrantes

| Nome completo | RM |
|---|---|
| Kevin Rodrigues | 571777 |

## Público e problema

**Público:** donos de pequenos comércios (mercadinhos, padarias) na área de concessão da Enel SP, ligados em baixa tensão (grupo B).

**Problema:** a conta de luz pesa, a informação está espalhada e em linguagem técnica, e há muita propaganda de energia solar com promessas irreais. O dono precisa saber onde a energia é gasta, o que fazer primeiro (eficiência ou solar) e quais são os limites dessas estimativas.

**ODS relacionados:** ODS 7 (energia limpa e acessível), ODS 12 (consumo e produção responsáveis) e ODS 13 (ação contra a mudança global do clima).

## Como executar

Só Python 3.9+ (nenhuma biblioteca externa, sem interface gráfica):

```bash
python main.py                        # assistente no terminal
python -m unittest discover -s tests  # testes automatizados
python -m energia.simulacao           # tabela comparativa de energia (vídeo de Energia)
```

Menu: 1 fazer pergunta, 2 navegar por categorias, 3 indicadores, 4 exportar CSV, 0 sair (pede nota de facilidade de 1 a 5). Em todas as telas, "0" volta.

## Estrutura (PCP)

```
main.py                    menu e execução
orientacao.py              classe Orientacao (um registro do JSON; exibir())
base_conhecimento.py       classe BaseConhecimento (carregar, categorias, por_categoria, pontuar, buscar)
assistente.py              classe Assistente (perguntar, navegar, registrar, indicadores, exportar_csv)
data/base_conhecimento.json   12 orientações, 3 categorias
data/historico.json           atendimentos (gerado ao usar)
data/atendimentos.csv         exportação (gerada ao usar)
energia/                   módulo de Energia (calculos.py, simulacao.py, data/*.csv)
tests/                     testes automatizados
docs/                      análise de energia, referências, testes com usuários, roteiros dos vídeos
entregas/                  modelos dos dois arquivos .txt do portal
```

Composição: `Assistente` tem uma `BaseConhecimento`, que tem uma lista de objetos `Orientacao`.

## Regra de pontuação (PCP)

A pergunta e os textos da base são normalizados (minúsculas, sem acentos nem pontuação). Para cada orientação:

| Regra | Pontos |
|---|---|
| Palavra-chave da orientação que aparece na pergunta | +3 |
| Palavra da pergunta (4 letras ou mais) que aparece no título | +1 |

Melhor orientação com **6 pontos ou mais**: confiança ALTA. **3 a 5**: MÉDIA. **Nenhuma com 3 pontos**: "não encontrei", com sugestão de outras palavras e das categorias. `buscar()` devolve uma lista de tuplas `(pontos, orientacao)`, da maior para a menor; o assistente mostra a melhor e até duas alternativas. Exemplo: "O que é bandeira vermelha?" faz 3 pontos por "bandeira vermelha" e 3 por "bandeira": **6, ALTA**. Não alteramos os pesos do enunciado.

## Regras de atendimento

- Navegação por categorias com "0 para voltar".
- Entradas inválidas (letras, fora da faixa, vazio, s/n inválido) nunca encerram o programa.
- **Dados pessoais:** o assistente nunca pede nome, CPF, telefone ou e-mail. Texto com 8 ou mais dígitos ou com "@" é recusado e não é registrado.
- **Transparência:** toda resposta mostra fonte, data de verificação e o aviso "este assistente NÃO é um canal oficial".
- JSON ausente ou corrompido (base ou histórico) não trava o programa.
- Cada atendimento vai para `data/historico.json` (data, origem, pergunta, id da orientação, se encontrou, se ajudou, tentativas e tempo em segundos), com indicadores e exportação para CSV.

## Integração com Energia

Orientações com o campo opcional `"calculo"` (led, refrigeracao, solar, comparar) chamam `energia/simulacao.py` depois de exibir a resposta. Assim as respostas de energia saem de cálculos reais, não de texto fixo. Nas simulações de solar, o usuário pode informar o consumo mensal (kWh) para recalcular.

| Conteúdo de energia | Onde |
|---|---|
| Consumo por equipamento, eficiência, solar, Fio B, payback, CO₂ | `energia/calculos.py` |
| Dados e premissas, com origem e tipo (público ou estimado) | `energia/data/premissas.csv`, `energia/data/equipamentos.csv` |
| Cálculos, comparação (A eficiência, B solar, C combinada), sensibilidade e justificativas | `docs/analise_energia.md` |
| Referências | `docs/referencias_energia.md` e campo `fonte` de cada orientação |
| Testes com usuários e ajustes | `docs/testes_usuarios.md` |

Resultado resumido (comércio-modelo, 10 anos): eficiência R$ 18.100 com retorno em 2,7 anos; solar de 13,9 kWp R$ 41.711 com retorno em 2,8 anos; eficiência + solar menor (8,6 kWp) com o maior saldo. Valores estimados, não garantidos.

## Fontes consultadas

Páginas da ANEEL (bandeiras tarifárias, tarifa branca, conta de energia, reclamação, geração distribuída), Planalto (Lei 14.300/2022), Agência Gov (Selo Procel), AGEMS (etiqueta e refrigeração), CRESESB (irradiação), faturas públicas da Enel SP, Solfácil/Radar e MCTI. Lista com links em cada orientação do JSON e em `docs/referencias_energia.md`.

**Conferência das fontes (17/11/2026):** as 12 orientações de `data/base_conhecimento.json` têm `verificado_em` preenchido. O conteúdo de cada uma foi conferido na web contra a fonte oficial ou contra textos que a reproduzem; o que foi (e o que não foi) conferido está na coluna "Situação" de [`docs/referencias_energia.md`](docs/referencias_energia.md). Correções feitas na conferência: o reajuste da Enel SP na baixa tensão é 8,97% (10,18% é a média de todas as classes); a orientação 4 passou a apontar para a página "Reclame da Distribuidora" da ANEEL; a orientação 10 passou a dizer que os percentuais do Fio B valem para quem pediu acesso depois de 7/1/2023; as bandeiras de novembro/2026 estão verdes.

## Teste com usuários

Testado com **3 pessoas de fora da equipe, 10 atendimentos**. Uma rodada de ensaio do autor (11 atendimentos) ficou de fora dos indicadores. Detalhes e comentários em [`docs/testes_usuarios.md`](docs/testes_usuarios.md).

| Indicador | Valor |
|---|---|
| Resposta encontrada (%) | 90,0 |
| Taxa de acerto: ajudou (%) | 22,2 (2 de 9) |
| Tempo médio para encontrar | 12,1 s |
| Tentativas por atendimento | 1,30 |
| Facilidade de uso (1 a 5) | 3,0 |

**Dúvidas sem solução:** nenhuma dúvida real. Um participante colou um comando do computador por engano; o programa não travou, e o texto foi substituído no histórico por "[texto colado por engano]".

**Melhoria feita:** a pergunta "por que a luz está cara?" não era encontrada (rodada de ensaio). Foram adicionadas à orientação 1 as palavras-chave "luz esta cara", "luz cara" e "conta cara".

**Limitação revelada:** as perguntas conceituais sobre solar ("como funciona...", "é o futuro?") caem na orientação de instalação (9), que não respondeu a dúvida. Falta uma orientação conceitual com fonte oficial.

- Teste com 3 pessoas (10 atendimentos): taxa de acerto de 22,2%; o assistente responde pelo que está na base e não resolve bem perguntas conceituais sobre energia solar.
## Vídeos

- Vídeo técnico de PCP (5 a 8 minutos): _link_
- Vídeo técnico de Energia (até 3 minutos): _link_

## Uso de IA generativa

Este projeto foi desenvolvido com apoio de IA generativa. A equipe é responsável por verificar dados, cálculos, fontes e recomendações e por explicar o código no vídeo.
