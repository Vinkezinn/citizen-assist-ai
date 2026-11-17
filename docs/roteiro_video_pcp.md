# Roteiro do vídeo técnico de PCP (5 a 8 minutos, YouTube não listado)

Regras do enunciado: **não é pitch**, é a explicação do código **pela própria equipe**. **Todos os integrantes falam**, cada um explicando uma parte técnica. **Proibido narração com IA ou voz sintética.** Tela com código legível (fonte grande) e o programa rodando; câmera é opcional. O que passar de 8 minutos não é avaliado, e **funcionalidade não demonstrada e explicada não é pontuada**.

**Trabalhando sozinho:** você faz todas as partes (A, B e C) e fala em todo o vídeo, com a sua própria voz.

Sugestão de divisão para 3 integrantes (ajustem para o tamanho do grupo; com 2, juntem as partes):

| Tempo | Quem | Roteiro oficial | O que mostrar e explicar |
|---|---|---|---|
| 0:00 a 0:30 | A | 1. Equipe, público e problema | Nomes, "pequenos comércios", problema da conta de luz e da informação espalhada |
| 0:30 a 1:15 | A | 2. JSON | Um registro de `data/base_conhecimento.json`: cada campo, **lista de dicionários**, e onde aparecem **tuplas** (retorno de `buscar()`); campo opcional `calculo` |
| 1:15 a 2:45 | B | 3. Classes | `Orientacao`, `BaseConhecimento` e `Assistente`: atributos, métodos, **self** e **composição** (Assistente tem BaseConhecimento, que tem lista de Orientacao); `carregar()` criando objetos |
| 2:45 a 4:00 | B | 4. Busca | `normalizar()` e `pontuar()` com o **cálculo de uma pergunta real**, ex.: "O que é bandeira vermelha?" = +3 "bandeira vermelha", +3 "bandeira" = 6, ALTA. Mostrar também o caso de 3 a 5 (MÉDIA) |
| 4:00 a 5:15 | C | 5. Execução | Rodar `python main.py`: pergunta encontrada; pergunta não encontrada (ex.: "xyz"); entrada inválida (letras no menu, s/n inválido); dado pessoal bloqueado (ex.: "meu cpf é 123.456.789-00"); navegação por categoria com "0 para voltar" |
| 5:15 a 6:15 | C | 6. Alteração ao vivo | Perguntar "quero pagar menos": **não encontrei**. Abrir o JSON, incluir `"pagar menos"` em `palavras_chave` da orientação 12, salvar e perguntar de novo: passa a ser **encontrada** (confiança MÉDIA, 3 pontos) |
| 6:15 a 7:15 | A | 7. Histórico, CSV e indicadores | Abrir `data/historico.json`, exportar o CSV (menu 4) e mostrar o `atendimentos.csv`; mostrar os indicadores do teste com usuários |
| 7:15 a 8:00 | B/C | 8. Decisão técnica e limitação | Uma decisão (ex.: JSON ausente/corrompido não trava o programa; ou o módulo `energia/` separado e chamado só quando `calculo` existe) e uma limitação (busca só por palavras-chave, sem sinônimos; base pequena) |

Dicas:
- Ensaiem o passo 6 antes de gravar. Voltem o JSON ao original depois (ou usem uma cópia).
- Apaguem `data/historico.json` (deixe `[]`) antes de gravar, para os indicadores mostrarem só o teste real.
- Terminal com fonte grande; deixe o código aberto no editor enquanto explicam.
- Cada pessoa deve conseguir explicar a parte que fala sem ler: se não souber explicar algum trecho, estude-o antes.
- Publique como **Não listado** e teste o link em janela anônima.
