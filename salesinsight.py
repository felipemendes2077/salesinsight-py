import pandas as pd
import numpy as np
import random
import re
import matplotlib.pyplot as plt
import seaborn as sns
import os
from datetime import datetime, timedelta

sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams["figure.figsize"] = (12, 6)
plt.rcParams["axes.titlesize"] = 14

def gerar_dataset_vendas(n_registros=200, seed=42):
    """Gera um dataset sintetico de vendas com dados sujos."""
    random.seed(seed)
    np.random.seed(seed)
    produtos = ["Notebook", "Smartphone", "Tablet", "Monitor",
                "Teclado", "Mouse", "Headset"]
    categorias = {"Notebook": "Computadores", "Smartphone": "Celulares",
                  "Tablet": "Celulares", "Monitor": "Computadores",
                  "Teclado": "Perifericos", "Mouse": "Perifericos",
                  "Headset": "Perifericos"}
    precos = {"Notebook": 3500, "Smartphone": 2200, "Tablet": 1800,
              "Monitor": 1200, "Teclado": 250, "Mouse": 120,
              "Headset": 350}
    regioes = ["Sudeste", "Sul", "Nordeste", "Centro-Oeste", "Norte"]
    data_inicio = datetime(2025, 1, 1)
    dados = []
    for i in range(n_registros):
        produto = random.choice(produtos)
        categoria = categorias[produto]
        quantidade = random.randint(1, 10)
        preco = round(precos[produto] * random.uniform(0.85, 1.15), 2)
        data = data_inicio + timedelta(days=random.randint(0, 364))
        data_txt = data.strftime("%Y-%m-%d")
        cliente = f"Cliente_{random.randint(1, 50):03d}"
        # --- sujeira proposital para a etapa de limpeza ---
        if random.random() < 0.05:
            quantidade = None                    # valor nulo
        if random.random() < 0.04:
            preco = None                         # valor nulo
        if random.random() < 0.06:
            produto = "  " + produto + " "       # espacos extras
        if random.random() < 0.03:
            data_txt = "DATA INVALIDA"           # data invalida
        if random.random() < 0.10:
            cliente = random.choice([            # ruido no nome
                cliente.upper().replace("_", "-"),
                cliente + "!!",
                "  " + cliente,
                cliente.replace("Cliente_", "cliente#"),
            ])
        dados.append({
            "id_venda": i + 1,
            "data_venda": data_txt,
            "cliente": cliente,
            "produto": produto,
            "categoria": categoria,
            "regiao": random.choice(regioes),
            "quantidade": quantidade,
            "preco_unitario": preco,
        })
    return pd.DataFrame(dados)


# Gerar e salvar o CSV bruto
df_bruto = gerar_dataset_vendas()
df_bruto.to_csv("vendas.csv", index=False)
print(f"Dataset gerado com {len(df_bruto)} registros.")
print(df_bruto.head())


def inspecionar_dados(df):
    """Exibe as informacoes estruturais do DataFrame."""
    print("\n=== INSPECAO INICIAL DO DATASET ===")
    print(f"Shape: {df.shape}")
    print(f"\nColunas: {list(df.columns)}")
    print(f"\nTipos de dados:\n{df.dtypes}")
    print(f"\nValores nulos por coluna:\n{df.isnull().sum()}")
    print(f"\nPrimeiros registros:\n{df.head()}")
    return df


inspecionar_dados(df_bruto)


def limpar_dados(df):
    """
    Limpa e trata o DataFrame de vendas.
    Retorna: (df_limpo, relatorio), onde relatorio e um dicionario
    com as contagens de registros iniciais, removidos e finais.
    """
    total_inicial = len(df)

    # 1. remover espacos extras nas colunas de texto
    colunas_texto = ["data_venda", "cliente", "produto", "categoria", "regiao"]
    for coluna in colunas_texto:
        df[coluna] = df[coluna].str.strip()

    # 2. converter data_venda e descartar datas invalidas
    df["data_venda"] = pd.to_datetime(df["data_venda"], errors="coerce")
    removidos_data_invalida = df["data_venda"].isna().sum()
    df = df.dropna(subset=["data_venda"])

    # 3. descartar nulos em quantidade e preco_unitario
    antes_dropna = len(df)
    df = df.dropna(subset=["quantidade", "preco_unitario"])
    removidos_nulos = antes_dropna - len(df)

    # 4. ajustar os tipos numericos
    df["quantidade"] = df["quantidade"].astype(int)
    df["preco_unitario"] = df["preco_unitario"].astype(float)

    # 5. padronizar o nome do cliente
    def padronizar_cliente(valor):
        digitos = re.sub(r"\D", "", str(valor))
        if digitos:
            return f"Cliente_{int(digitos):03d}"
        return valor

    df["cliente"] = df["cliente"].apply(padronizar_cliente)
    padrao_cliente = re.compile(r"^Cliente_\d{3}$")
    fora_do_padrao = (~df["cliente"].apply(lambda c: bool(padrao_cliente.match(c)))).sum()

    # 6. relatorio de limpeza
    total_final = len(df)
    relatorio = {
        "total_inicial": total_inicial,
        "removidos_data_invalida": int(removidos_data_invalida),
        "removidos_nulos": int(removidos_nulos),
        "clientes_fora_do_padrao": int(fora_do_padrao),
        "total_final": total_final,
    }

    print("\n=== RELATORIO DE LIMPEZA ===")
    print(f"Registros iniciais: {relatorio['total_inicial']}")
    print(f"Removidos por data invalida: {relatorio['removidos_data_invalida']}")
    print(f"Removidos por nulos criticos: {relatorio['removidos_nulos']}")
    print(f"Clientes fora do padrao apos padronizacao: {relatorio['clientes_fora_do_padrao']}")
    print(f"Registros finais: {relatorio['total_final']}")

    return df, relatorio


def criar_colunas_derivadas(df):
    """Cria colunas derivadas a partir do dataset limpo."""
    df = df.copy()

    # receita_total
    df["receita_total"] = df["quantidade"] * df["preco_unitario"]

    # mes, mes_nome, trimestre, ano
    df["mes"] = df["data_venda"].dt.month
    nomes_meses = {
        1: "Janeiro", 2: "Fevereiro", 3: "Marco", 4: "Abril",
        5: "Maio", 6: "Junho", 7: "Julho", 8: "Agosto",
        9: "Setembro", 10: "Outubro", 11: "Novembro", 12: "Dezembro",
    }
    df["mes_nome"] = df["mes"].map(nomes_meses)
    df["trimestre"] = "Q" + df["data_venda"].dt.quarter.astype(str)
    df["ano"] = df["data_venda"].dt.year

    # faixa_receita_item (transformacao condicional vetorizada)
    condicoes = [
        df["receita_total"] < 500,
        (df["receita_total"] >= 500) & (df["receita_total"] < 5000),
        df["receita_total"] >= 5000,
    ]
    faixas = ["Baixo Valor", "Medio Valor", "Alto Valor"]
    df["faixa_receita_item"] = np.select(condicoes, faixas, default="Nao Classificado")

    return df


def calcular_metricas(df):
    """
    Calcula as metricas agregadas do dataset.
    Retorna um dicionario no formato {nome_da_metrica: DataFrame}.
    """
    metricas = {}

    # por mes
    por_mes = df.groupby("mes").agg(
        receita_total=("receita_total", "sum"),
        quantidade=("quantidade", "sum"),
        n_vendas=("id_venda", "count"),
    ).reset_index()
    metricas["por_mes"] = por_mes

    # top produtos (top 5)
    top_produtos = df.groupby("produto").agg(
        receita_total=("receita_total", "sum")
    ).reset_index().sort_values("receita_total", ascending=False).head(5)
    metricas["top_produtos"] = top_produtos

    # por categoria
    por_categoria = df.groupby("categoria").agg(
        receita_total=("receita_total", "sum")
    ).reset_index().sort_values("receita_total", ascending=False)
    metricas["por_categoria"] = por_categoria

    # por regiao (receita total e ticket medio)
    por_regiao = df.groupby("regiao").agg(
        receita_total=("receita_total", "sum"),
        ticket_medio=("receita_total", "mean"),
    ).reset_index().sort_values("receita_total", ascending=False)
    metricas["por_regiao"] = por_regiao

    print("\n=== POR MES ===")
    print(por_mes)
    print("\n=== TOP PRODUTOS ===")
    print(top_produtos)
    print("\n=== POR CATEGORIA ===")
    print(por_categoria)
    print("\n=== POR REGIAO ===")
    print(por_regiao)

    return metricas


def segmentar_clientes(df):
    """
    Agrupa por cliente, soma a receita e classifica em
    Bronze / Prata / Ouro.
    Retorna um DataFrame com: cliente, total_gasto, segmento.
    """
    por_cliente = df.groupby("cliente").agg(
        total_gasto=("receita_total", "sum")
    ).reset_index()

    por_cliente["segmento"] = por_cliente["total_gasto"].apply(
        lambda gasto: "Bronze" if gasto < 5000
        else ("Prata" if gasto < 15000 else "Ouro")
    )

    top_10 = por_cliente.sort_values("total_gasto", ascending=False).head(10)
    distribuicao = por_cliente["segmento"].value_counts()

    print("\n=== TOP 10 CLIENTES ===")
    print(top_10)
    print("\n=== DISTRIBUICAO POR SEGMENTO ===")
    print(distribuicao)

    return por_cliente


def calcular_estatisticas_numpy(df):
    """
    Aplica operacoes NumPy sobre a coluna receita_total.
    Retorna um dicionario com os valores agregados calculados.
    """
    receitas = df["receita_total"].to_numpy()

    media = np.mean(receitas)
    mediana = np.median(receitas)
    desvio_padrao = np.std(receitas)
    soma_total = np.sum(receitas)

    # broadcasting: escalonar o array para o intervalo 0-1
    receitas_normalizadas = (receitas - receitas.min()) / (receitas.max() - receitas.min())

    # filtragem booleana: vendas acima da media
    vendas_acima_media = receitas[receitas > media]
    qtd_acima_media = len(vendas_acima_media)

    estatisticas = {
        "media": float(media),
        "mediana": float(mediana),
        "desvio_padrao": float(desvio_padrao),
        "soma_total": float(soma_total),
        "qtd_vendas_acima_media": int(qtd_acima_media),
    }

    print("\n=== ESTATISTICAS NUMPY (receita_total) ===")
    print(f"Media: {estatisticas['media']:.2f}")
    print(f"Mediana: {estatisticas['mediana']:.2f}")
    print(f"Desvio padrao: {estatisticas['desvio_padrao']:.2f}")
    print(f"Soma total: {estatisticas['soma_total']:.2f}")
    print(f"Vendas acima da media: {estatisticas['qtd_vendas_acima_media']} de {len(receitas)}")
    print(f"Exemplo de receitas normalizadas (0-1): {receitas_normalizadas[:5]}")

    return estatisticas

def gerar_grafico_receita_por_mes(metricas):
    """Gera o grafico de linha: receita total por mes."""
    por_mes = metricas["por_mes"]
    os.makedirs("outputs/graficos", exist_ok=True)

    fig, ax = plt.subplots()
    ax.plot(por_mes["mes"], por_mes["receita_total"],
            marker="o", linewidth=2, color="#2c6e91")
    ax.set_title("Receita Total por Mes")
    ax.set_xlabel("Mes")
    ax.set_ylabel("Receita Total (R$)")
    ax.set_xticks(por_mes["mes"])
    plt.tight_layout()
    plt.savefig("outputs/graficos/receita_por_mes.png", dpi=150)
    plt.close()
    print("Grafico salvo: outputs/graficos/receita_por_mes.png")

def gerar_grafico_top_produtos(metricas):
    """Gera o grafico de barras: top 5 produtos por receita."""
    top_produtos = metricas["top_produtos"]

    fig, ax = plt.subplots()
    sns.barplot(data=top_produtos, y="produto", x="receita_total",
                hue="produto", legend=False, palette="Blues_d", ax=ax)
    ax.set_title("Top 5 Produtos por Receita")
    ax.set_xlabel("Receita Total (R$)")
    ax.set_ylabel("Produto")
    plt.tight_layout()
    plt.savefig("outputs/graficos/top_produtos.png", dpi=150)
    plt.close()
    print("Grafico salvo: outputs/graficos/top_produtos.png")

def gerar_grafico_dispersao(df):
    """Gera o grafico de dispersao: quantidade x receita_total, por categoria."""
    fig, ax = plt.subplots()
    sns.scatterplot(data=df, x="quantidade", y="receita_total",
                     hue="categoria", palette="deep", s=70, ax=ax)
    ax.set_title("Quantidade vs Receita Total por Categoria")
    ax.set_xlabel("Quantidade")
    ax.set_ylabel("Receita Total (R$)")
    ax.legend(title="Categoria")
    plt.tight_layout()
    plt.savefig("outputs/graficos/quantidade_vs_receita.png", dpi=150)
    plt.close()
    print("Grafico salvo: outputs/graficos/quantidade_vs_receita.png")

def gerar_painel_resumo(metricas, df):
    """Gera um painel 2x2 combinando as principais visualizacoes."""
    por_mes = metricas["por_mes"]
    top_produtos = metricas["top_produtos"]
    por_regiao = metricas["por_regiao"]

    fig, axes = plt.subplots(2, 2, figsize=(14, 9))

    # [0,0] linha - receita por mes
    axes[0, 0].plot(por_mes["mes"], por_mes["receita_total"],
                     marker="o", linewidth=2, color="#2c6e91")
    axes[0, 0].set_title("Receita Total por Mes")
    axes[0, 0].set_xlabel("Mes")
    axes[0, 0].set_ylabel("Receita Total (R$)")

    # [0,1] barras - top produtos
    sns.barplot(data=top_produtos, y="produto", x="receita_total",
                hue="produto", legend=False, palette="Blues_d", ax=axes[0, 1])
    axes[0, 1].set_title("Top 5 Produtos por Receita")
    axes[0, 1].set_xlabel("Receita Total (R$)")
    axes[0, 1].set_ylabel("Produto")

    # [1,0] dispersao - quantidade x receita por categoria
    sns.scatterplot(data=df, x="quantidade", y="receita_total",
                     hue="categoria", palette="deep", s=50, ax=axes[1, 0])
    axes[1, 0].set_title("Quantidade vs Receita por Categoria")
    axes[1, 0].set_xlabel("Quantidade")
    axes[1, 0].set_ylabel("Receita Total (R$)")
    axes[1, 0].legend(title="Categoria", fontsize=8)

    # [1,1] barras - receita por regiao
    sns.barplot(data=por_regiao, y="regiao", x="receita_total",
                hue="regiao", legend=False, palette="Greens_d", ax=axes[1, 1])
    axes[1, 1].set_title("Receita Total por Regiao")
    axes[1, 1].set_xlabel("Receita Total (R$)")
    axes[1, 1].set_ylabel("Regiao")

    fig.suptitle("SalesInsight PY - Painel Resumo", fontsize=16)
    plt.tight_layout()
    plt.savefig("outputs/graficos/painel_resumo.png", dpi=150)
    plt.close()
    print("Grafico salvo: outputs/graficos/painel_resumo.png")

def processar_coluna(df, coluna, funcao_transformacao, nome_saida=None):
    """
    Aplica uma funcao de transformacao a uma coluna do DataFrame.
    Demonstra o uso de funcoes como argumento (funcao de ordem superior).
    """
    nome_saida = nome_saida or f"{coluna}_transformado"
    df[nome_saida] = df[coluna].apply(funcao_transformacao)
    return df

class AnalisadorDeVendas:
    """Encapsula o fluxo de analise dos dados de vendas."""

    def __init__(self, caminho_arquivo):
        self.caminho_arquivo = caminho_arquivo
        self.df_bruto = None
        self.df_limpo = None
        self.metricas = {}
        self.clientes = None
        self.estatisticas_numpy = {}
        self.relatorio_limpeza = {}

    def carregar(self):
        """Le o CSV e guarda o DataFrame bruto."""
        self.df_bruto = pd.read_csv(self.caminho_arquivo)
        print(f"\n[Analisador] {len(self.df_bruto)} registros lidos.")

    def limpar(self):
        """Limpa os dados reaproveitando limpar_dados()."""
        self.df_limpo, self.relatorio_limpeza = limpar_dados(self.df_bruto.copy())

    def transformar(self):
        """Cria as colunas derivadas reaproveitando criar_colunas_derivadas()."""
        self.df_limpo = criar_colunas_derivadas(self.df_limpo)

    def analisar(self):
        """Calcula metricas, segmentacao e operacoes NumPy."""
        self.metricas = calcular_metricas(self.df_limpo)
        self.clientes = segmentar_clientes(self.df_limpo)
        self.estatisticas_numpy = calcular_estatisticas_numpy(self.df_limpo)

    def visualizar(self):
        """Gera e exporta as quatro figuras."""
        gerar_grafico_receita_por_mes(self.metricas)
        gerar_grafico_top_produtos(self.metricas)
        gerar_grafico_dispersao(self.df_limpo)
        gerar_painel_resumo(self.metricas, self.df_limpo)

    def resumo(self):
        """Imprime um resumo executivo do que foi processado."""
        print("\n=== RESUMO EXECUTIVO ===")
        print(f"Registros analisados: {len(self.df_limpo)}")
        print(f"Receita total: R$ {self.estatisticas_numpy['soma_total']:.2f}")
        print(f"Clientes segmentados: {len(self.clientes)}")

df_limpo, relatorio_limpeza = limpar_dados(df_bruto.copy())
df_transformado = criar_colunas_derivadas(df_limpo)
metricas = calcular_metricas(df_transformado)
clientes_segmentados = segmentar_clientes(df_transformado)
estatisticas_numpy = calcular_estatisticas_numpy(df_transformado)
gerar_grafico_receita_por_mes(metricas)
gerar_grafico_top_produtos(metricas)
gerar_grafico_dispersao(df_transformado)
gerar_painel_resumo(metricas, df_transformado)

df_transformado = processar_coluna(df_transformado, "receita_total",
                                    lambda x: round(x / 1000, 2),
                                    nome_saida="receita_em_milhares")
df_transformado = processar_coluna(df_transformado, "quantidade",
                                    lambda q: "Alto Volume" if q > 5 else "Baixo Volume",
                                    nome_saida="perfil_volume")
print(df_transformado[["receita_total", "receita_em_milhares", "quantidade", "perfil_volume"]].head())


