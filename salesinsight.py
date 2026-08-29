import pandas as pd
import numpy as np
import random
import re
from datetime import datetime, timedelta


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

df_limpo, relatorio_limpeza = limpar_dados(df_bruto.copy())
print(df_limpo.head())


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

df_limpo, relatorio_limpeza = limpar_dados(df_bruto.copy())
df_transformado = criar_colunas_derivadas(df_limpo)
print(df_transformado.head())