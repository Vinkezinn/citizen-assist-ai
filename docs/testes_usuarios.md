# Testes com usuários (PCP e Energia)

## Como foi o teste

- **3 participantes de fora da equipe**, somando **10 atendimentos**. Cada um usou o assistente no terminal (`python main.py`) e saiu pelo menu 0, informando a nota de facilidade (1 a 5).
- Nenhum nome ou dado pessoal foi registrado.
- Antes dos testes, o autor fez uma rodada de ensaio (11 atendimentos). Ela **não entra** nos indicadores abaixo.
- Um participante colou por engano um comando do computador no campo de dúvida. O programa não travou e registrou o atendimento como dúvida sem solução. O texto foi substituído por "[texto colado por engano]" porque continha dados do computador.

## Registro das pessoas

| Participante | Atendimentos | Nota de facilidade | Situações testadas | Comentário e compreensão |
|---|---|---|---|---|
| 1 | 4 | 3 | Pergunta livre sobre como funciona a energia solar; refrigeração; troca por LED; tarifa branca | [PREENCHER: o que disse, se entendeu, se achou a economia garantida] |
| 2 | 4 | 3 | Texto colado por engano; troca por LED; refrigeração; instalação de energia solar | Sem comentário registrado; apenas os dados do programa. |
| 3 | 2 | 3 | Pergunta livre "energia solar é o futuro?" (2 tentativas); Fio B | Sem comentário registrado; apenas os dados do programa. |

## Indicadores obtidos (menu 3 do programa, 10 atendimentos)

| Indicador | Valor |
|---|---|
| Resposta encontrada (%) | 90,0 |
| Taxa de acerto: ajudou (%) | 22,2 (2 de 9) |
| Tempo médio para encontrar (s) | 12,1 |
| Tentativas por atendimento | 1,30 |
| Facilidade de uso (1 a 5) | 3,0 |

## Dúvidas sem solução

- Nenhuma dúvida real. A única registrada foi a entrada colada por engano.

## O que os registros mostram

- A taxa de acerto foi baixa: das 9 respostas encontradas, 7 não ajudaram. Com 10 atendimentos não dá para generalizar.
- A orientação 9 (instalação e ligação à rede) foi aberta 3 vezes e não ajudou em nenhuma. As duas perguntas livres sobre solar eram conceituais ("como funciona...", "...é o futuro?"), e a orientação 9 trata de instalação. O assistente respondeu com a orientação mais próxima que a base tem.
- "Energia solar é o futuro?" precisou de 2 tentativas e 43 s.
- As orientações de energia com simulação (LED e refrigeração) ajudaram em 2 de 4 aberturas.

## Melhorias e ajustes

| Problema observado | Ajuste feito |
|---|---|
| "Por que a luz está cara?" não foi encontrada (rodada de ensaio da equipe) | Palavras-chave "luz esta cara", "luz cara" e "conta cara" na orientação 1. A pergunta passa a ser respondida com confiança MÉDIA (3 pontos). |
| Perguntas conceituais sobre solar caem na orientação de instalação | **Não corrigido.** Próximo passo: criar uma orientação com fonte oficial verificada. Não foi feita para não inventar informação. |

## Limitações do teste

- Apenas 3 pessoas e 10 atendimentos.
- Os comentários acima são das pessoas testadas e não representam todos os donos de comércio.