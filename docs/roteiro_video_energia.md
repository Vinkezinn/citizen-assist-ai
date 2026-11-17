# Roteiro do vídeo de Energia (máximo 3 minutos, YouTube não listado)

Este é um vídeo **separado** do vídeo técnico de PCP (5 a 8 minutos). O enunciado de Energia pede quatro coisas, nesta ordem: público e necessidade; análise de consumo e comparação das alternativas (com a renovável); demonstração no assistente; principais recomendações e limitações.

**Antes de gravar:** `data/historico.json` em `[]`; terminal com fonte grande; abas prontas: `docs/analise_energia.md`, o terminal em `python -m energia.simulacao` e o terminal em `python main.py`. Fale com a sua voz e leia em ritmo normal: o texto falado abaixo tem cerca de 325 palavras, o que dá de 2:10 a 2:30 e deixa folga para as demonstrações no terminal.

| Tempo | O que aparece na tela | O que falar |
|---|---|---|
| 0:00 a 0:20 | Título do repositório e depois o README (seção Público e problema) | "Eu sou o Kevin Rodrigues de Melo. Esta é a contribuição de Energias Renováveis ao Citizen Assist AI. O público são donos de pequenos comércios, como mercadinhos e padarias, na área da Enel São Paulo. A necessidade é reduzir a conta de luz, onde refrigeração e iluminação pesam mais." |
| 0:20 a 1:00 | `docs/analise_energia.md`, tabela da seção 2 | "Para o comércio-modelo, calculei o consumo de cada equipamento com a fórmula energia igual a quantidade vezes potência, vezes horas por dia, vezes fator de uso, vezes dias. Dá 1.552 quilowatts-hora por mês, cerca de 1.443 reais, a tarifa de 93 centavos vindo de faturas públicas da Enel. A iluminação é 42% do consumo e a refrigeração, 54%. Potências e horas são estimadas, e estão marcadas como estimadas nos arquivos CSV." |
| 1:00 a 1:50 | Terminal: `python -m energia.simulacao`, depois a tabela de resultados da seção 4 da análise | "Comparei três caminhos no mesmo período de 10 anos. A, eficiência: troca por LED, equipamentos eficientes e vedação da câmara fria. Investe 18 mil reais e se paga em 2,7 anos. B, solar, que é a fonte renovável: 13,9 quilowatts-pico, 41,7 mil reais, retorno em 2,8 anos e o maior saldo isolado. C, eficiência primeiro e um solar menor, de 8,6 quilowatts-pico: o maior saldo de todos. O cálculo já desconta o Fio B da Lei 14.300 e a manutenção. O CO₂ evitado é pequeno, de 0,26 a 0,69 tonelada por ano, porque a rede brasileira já é quase toda renovável: o argumento aqui é financeiro." |
| 1:50 a 2:35 | Terminal: `python main.py`, opção 1, digitar `quanto custa solar?`, depois `900`, depois `s` | "No assistente, pergunto: quanto custa solar? A busca por pontos acha a orientação com confiança alta e a resposta vem dos mesmos cálculos. Informo 900 quilowatts-hora do meu comércio e ele recalcula: sistema de uns 7,9 quilowatts-pico. Toda resposta traz a fonte, a data de verificação e o aviso de que não é canal oficial." |
| 2:35 a 3:00 | `docs/analise_energia.md`, seção 7 (Limitações) | "As recomendações são estimativas, não garantias. Dependem da fatura real, de orçamentos e do telhado. Se a irradiação for menor, ou a tarifa, o retorno muda, e eu mostro isso na tabela de sensibilidade. Referências, dados e registros dos testes estão no repositório. Obrigado." |

## Conferir antes de enviar
- O vídeo tem **até 3:00**. Cronometre.
- Os números falados batem com a tela (rode `python -m energia.simulacao` antes e compare).
- Mostre as três respostas do assistente sem cortar o aviso e a fonte.
- Publique como **Não listado** e teste o link em janela anônima.
- Depois de gravar, apague o que o ensaio gerou: `data/historico.json` volta para `[]` e `data/atendimentos.csv` é apagado.
