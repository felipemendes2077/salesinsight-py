# Kanban — SalesInsight PY

**Projeto:** Mini-Projeto Avaliativo M1.1 — Desenvolvedor(a) em IA para Análise Preditiva [T3]
**Prazo:** 31/08/2026, 22h
**Alvo interno de conclusão:** 29/08/2026 (dias 30 e 31 são folga)
**Formato:** Individual

---

## Cronograma

| Dia | Foco | Tarefas |
|---|---|---|
| Sex 21/08 | Setup do projeto | 01–04 |
| Sáb 22/08 | Dataset e inspeção (RF01–RF02) | 05–06 |
| Dom 23/08 | Limpeza e regex (RF03) — dia mais difícil | 07 |
| Seg 24/08 | Colunas derivadas (RF04) | 08 |
| Ter 25/08 | Métricas com groupby (RF05) | 09 |
| Qua 26/08 | Segmentação e NumPy (RF06–RF07) | 10–12 |
| Qui 27/08 | As 4 figuras (RF08) — dia mais longo | 13–16 |
| Sex 28/08 | Exportação, classe e main (RF09–RF11) | 17–19 |
| Sáb 29/08 | Teste do zero, README final, vídeo | 20–22 |
| Dom 30/08 | Bônus B03/B04 (opcional) + revisar código para o vídeo | — |
| Seg 31/08 | Conferir links e submeter no AVA | 23 |

**Regra:** commit ao fim de cada dia. O critério 2 avalia se o histórico reflete a evolução do trabalho — os timestamps aparecem no GitHub.

---

## Backlog

| # | Tarefa | RF | Branch | Commit sugerido |
|---|---|---|---|---|
| 01 | Criar repositório público `salesinsight-py` no GitHub | — | `main` | `chore: cria estrutura inicial do repositorio` |
| 02 | Criar `develop` a partir da `main` | — | `develop` | — |
| 03 | Criar README.md esqueleto (objetivo + estrutura) | — | `docs/readme` | `docs: adiciona readme inicial` |
| 04 | Montar este quadro Kanban | — | `develop` | `docs: adiciona planejamento kanban` |
| 05 | Implementar `gerar_dataset_vendas()` e salvar `vendas.csv` | RF01 | `feat/dataset-inspecao` | `feat: adiciona geracao do dataset sintetico de vendas` |
| 06 | Implementar `inspecionar_dados()` (shape, dtypes, isnull, head) | RF02 | `feat/dataset-inspecao` | `feat: adiciona inspecao estrutural do dataframe` |
| 07 | Implementar `limpar_dados()` — strip, datas, nulos, tipos, regex, relatório | RF03 | `feat/limpeza-dados` | `feat: implementa limpeza com datetime e regex` |
| 08 | Implementar `criar_colunas_derivadas()` — receita, mês, trimestre, ano, np.select | RF04 | `feat/transformacoes` | `feat: adiciona colunas derivadas com np.select` |
| 09 | Implementar `calcular_metricas()` — groupby por mês, produto, categoria, região | RF05 | `feat/metricas-agregadas` | `feat: implementa metricas agregadas com groupby` |
| 10 | Implementar `segmentar_clientes()` — Bronze/Prata/Ouro com lambda | RF06 | `feat/metricas-agregadas` | `feat: adiciona segmentacao de clientes com lambda` |
| 11 | Implementar `calcular_estatisticas_numpy()` — vetorização, broadcasting, filtro booleano | RF07 | `feat/numpy` | `feat: adiciona operacoes vetorizadas com numpy` |
| 12 | Implementar `processar_coluna()` (função de ordem superior) + 2 usos de lambda | RF09-A | `feat/numpy` | `feat: adiciona funcao de ordem superior processar_coluna` |
| 13 | Gráfico de linha — `receita_por_mes.png` | RF08 | `feat/visualizacoes` | `feat: cria grafico de linha de receita por mes` |
| 14 | Gráfico de barras — `top_produtos.png` | RF08 | `feat/visualizacoes` | `feat: cria grafico de barras dos top produtos` |
| 15 | Gráfico de dispersão — `quantidade_vs_receita.png` | RF08 | `feat/visualizacoes` | `feat: cria grafico de dispersao quantidade x receita` |
| 16 | Painel 2x2 com subplots — `painel_resumo.png` | RF08 | `feat/visualizacoes` | `feat: adiciona painel de subplots e exportacao em png` |
| 17 | Implementar `exportar_resultados()` — CSV, JSON e releitura do JSON | RF10 | `feat/exportacao` | `feat: implementa exportacao em csv e json` |
| 18 | Criar classe `AnalisadorDeVendas` (init, atributos, métodos) | RF09-B | `feat/classe-analisador` | `feat: cria classe AnalisadorDeVendas` |
| 19 | Criar `main()` e bloco `if __name__ == "__main__":` | RF11 | `feat/classe-analisador` | `feat: adiciona ponto de entrada main` |
| 20 | Rodar o fluxo do zero (apagar `vendas.csv` e `outputs/`) e validar | — | `develop` | `fix: ajustes apos teste do fluxo completo` |
| 21 | Finalizar README (execução, conceitos aplicados, decisões técnicas, link do vídeo) | — | `docs/readme` | `docs: atualiza readme com instrucoes e conceitos` |
| 22 | Gravar vídeo de até 5 min e publicar com acesso por link | — | — | — |
| 23 | Merge de tudo em `develop` → `main` e submeter links no AVA | — | `main` | `chore: merge develop para main` |

---

## A Fazer

_(mover aqui as tarefas do dia)_

## Em Andamento

_(máximo 1–2 tarefas por vez)_

## Concluído

_(mover ao terminar, marcando a data)_

---

## Roteiro do vídeo (máx. 5 min)

Cronometrar antes de gravar. Sugestão de divisão:

| Tempo | Conteúdo |
|---|---|
| 0:00–0:30 | Objetivo do projeto e o problema de negócio |
| 0:30–1:00 | O que instalar/configurar (`pip install pandas numpy matplotlib seaborn`) |
| 1:00–1:30 | Como organizei as tarefas: mostrar o Kanban na tela |
| 1:30–2:00 | Branches criadas e o objetivo de cada uma |
| 2:00–3:30 | Execução do fluxo do início ao fim (rodar ao vivo ou gravado) |
| 3:30–4:15 | **Uma decisão técnica** explicada com segurança |
| 4:15–5:00 | O que poderia ser melhorado |

Requisitos de gravação: rosto visível, boa iluminação, áudio audível. Vertical ou horizontal.

### Candidatos a "decisão técnica" (escolher UM e dominar)

1. **Por que reconstruir o nome do cliente em vez de só limpar caracteres.** Ruídos como `CLIENTE-001` e `cliente#001` sobrevivem a um `re.sub` simples e continuam fora do padrão `^Cliente_\d{3}$`. Extrair os dígitos e remontar o nome garante que o mesmo cliente não seja contado duas vezes na segmentação.
2. **Por que remover registros inválidos em vez de imputar.** Sem contexto de negócio, inventar valor de quantidade ou preço distorce a receita — que é a métrica central do relatório. Imputação é conteúdo da Semana 10.
3. **Por que `np.select` em vez de um laço `for`.** Vetorização opera sobre o array inteiro de uma vez; um laço em Python percorre linha a linha e fica ordens de magnitude mais lento conforme o dataset cresce.
4. **A diferença entre `np.std()` (ddof=0) e `Series.std()` (ddof=1).** Os valores não batem e isso é esperado — populacional vs. amostral.

---

## Checklist de armadilhas

- [ ] `quantidade` vira `float64` por causa dos `None` — aplicar `.astype(int)` depois do `dropna()`
- [ ] Nome do mês em português via dicionário, **não** `.dt.strftime("%B")`
- [ ] Em `sns.barplot`, usar `palette` **sempre** junto com `hue=` e `legend=False`
- [ ] Toda a limpeza acontece **antes** das transformações, agregações e gráficos
- [ ] Todas as 4 figuras: título, rótulos nos 2 eixos, legenda, `figsize`, paleta escolhida, `tight_layout()`, `dpi>=100`
- [ ] Pelo menos 5 commits (individual), com mensagens descritivas
- [ ] Repositório **público**
- [ ] Vídeo acessível por qualquer pessoa com o link
- [ ] Links do repositório, do Kanban e do vídeo enviados no AVA
