# SalesInsight PY

## Sobre o projeto

Este é um miniprojeto para uma empresa de varejo fictícia, onde analisei
como as vendas evoluem ao longo dos meses e trimestres, quais produtos
estão gerando mais receitas, qual a região que melhor vende e quem são
nossos clientes mais valiosos.

Este script:
- Gera e carrega os dados de vendas
- Inspeciona formatos, tipos de dado e valores nulos
- Limpa e trata os dados
- Cria novas colunas derivadas
- Calcula métricas agregadas
- Segmenta os clientes
- Realiza cálculos com NumPy
- Gera 4 gráficos
- Exporta os resultados

## Como executar


## Conceitos aplicados

Python basico
- Variaveis, tipos de dados (int, float, str, bool)
- Condicionais (if/elif/else) na classificacao de segmento de cliente, faixa de receita e perfil de volume
- Lacos (for) na geracao do dataset sintetico
- Funcoes com parametros, retorno e docstring em todo o fluxo
- Funcoes lambda em pelo menos dois contextos distintos (segmentacao de clientes e processar_coluna)
- Funcao de ordem superior: processar_coluna recebe outra funcao como argumento

Manipulacao de arquivos e dados
- Leitura e escrita de CSV (pd.read_csv, .to_csv())
- Leitura e escrita de JSON (json.dump, json.load)
- Modulo datetime para extrair mes, trimestre e ano
- Expressoes regulares (re.sub, re.compile) na padronizacao do nome do cliente

Pandas
- Series e DataFrames
- Filtros e selecoes com condicoes booleanas
- groupby com .agg() para metricas por mes, produto, categoria e regiao
- Tratamento de dados sujos: nulos, datas invalidas, espacos extras

NumPy
- Conversao de coluna para array (.to_numpy())
- Operacoes vetorizadas (media, mediana, desvio padrao, soma)
- Broadcasting na normalizacao dos valores para o intervalo 0-1
- Filtragem booleana de array
- np.select para transformacao condicional vetorizada

Visualizacao
- Matplotlib para o grafico de linha
- Seaborn para os graficos de barras e dispersao
- Subplots (plt.subplots(2, 2)) com fig.suptitle() para o painel resumo
- Customizacao: titulo, rotulos, legenda, paleta de cores, figsize e tight_layout()

Orientacao a objetos
- Classe AnalisadorDeVendas com __init__, atributos de instancia e metodos usando self

Versionamento
- Git e GitHub com branches por funcionalidade, commits descritivos e Pull Requests seguindo o GitHub Flow simplificado

## Decisões técnicas

Por que reconstruir o nome do cliente em vez de so limpar caracteres especiais

O gerador de dados cria ruidos como "CLIENTE-001" e "cliente#001". Se a limpeza apenas remover os caracteres invalidos com re.sub, sobra algo como "cliente001", que ainda nao bate com o padrao exigido "Cliente_NNN". A solucao usada foi extrair somente os digitos do texto com regex e remontar o nome do zero no formato correto. Isso evita que o mesmo cliente seja contado duas vezes na segmentacao por causa de pequenas variacoes de escrita.

Por que remover registros invalidos em vez de tentar corrigi-los

Datas invalidas e valores nulos em quantidade ou preco foram descartados com dropna, em vez de receberem um valor estimado. Sem um contexto de negocio real, inventar um numero para preencher esses campos distorceria a receita total, que e a metrica central de todo o relatorio. Estrategias de imputacao fazem parte de conteudos futuros do curso e nao foram aplicadas aqui de proposito.

Por que usar np.select em vez de um laco for

A classificacao da faixa de receita de cada linha foi feita com np.select, que aplica a condicao a coluna inteira de uma vez (vetorizacao). Um laco for percorreria o DataFrame linha por linha, o que fica muito mais lento conforme o volume de dados cresce.

Observacao sobre desvio padrao

O np.std() do NumPy usa por padrao ddof=0 (populacional), enquanto o .std() do pandas usa ddof=1 (amostral). Os dois calculos produzem valores ligeiramente diferentes para o mesmo conjunto de dados, e essa diferenca e esperada, nao um erro de implementacao.

## Vídeo de demonstração
*(link a adicionar após a gravação)*