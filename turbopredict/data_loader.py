"""
data_loader.py — sem import streamlit (UI fica no app.py)
Coloque os CSVs em turbopredict/data/ ou faça upload pela tela inicial.
"""
import pandas as pd
import numpy as np
from pathlib import Path

_HERE    = Path(__file__).resolve().parent
DATA_DIR = _HERE / "data"
_FILE_BOL = DATA_DIR / "base_boletos_fiap.csv"
_FILE_AUX = DATA_DIR / "base_auxiliar_fiap.csv"


def data_files_ok() -> bool:
    return _FILE_BOL.exists() and _FILE_AUX.exists()


def save_uploaded_files(bytes_bol: bytes, bytes_aux: bytes) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    _FILE_BOL.write_bytes(bytes_bol)
    _FILE_AUX.write_bytes(bytes_aux)


def load_data():
    df_bol = pd.read_csv(_FILE_BOL, parse_dates=["dt_emissao","dt_vencimento","dt_pagamento"])
    df_aux = pd.read_csv(_FILE_AUX)

    df_bol["dpd"]        = (df_bol["dt_pagamento"] - df_bol["dt_vencimento"]).dt.days.fillna(999)
    df_bol["em_atraso"]  = df_bol["dpd"] > 0
    df_bol["atraso_30"]  = df_bol["dpd"] >= 30
    df_bol["atraso_60"]  = df_bol["dpd"] >= 60
    df_bol["atraso_90"]  = df_bol["dpd"] >= 90
    df_bol["mes_emissao"]= df_bol["dt_emissao"].dt.to_period("M").astype(str)

    agg = df_bol.groupby("id_beneficiario").agg(
        total_boletos      =("id_boleto",    "count"),
        vlr_total          =("vlr_nominal",  "sum"),
        vlr_medio          =("vlr_nominal",  "mean"),
        pct_atraso_geral   =("em_atraso",    "mean"),
        pct_atraso_30      =("atraso_30",    "mean"),
        pct_atraso_60      =("atraso_60",    "mean"),
        pct_atraso_90      =("atraso_90",    "mean"),
        dpd_medio          =("dpd", lambda x: x[x<999].mean() if (x<999).any() else 0),
        n_pagadores_unicos =("id_pagador",   "nunique"),
        primeiro_boleto    =("dt_emissao",   "min"),
        ultimo_boleto      =("dt_emissao",   "max"),
    ).reset_index()

    conc = df_bol.groupby(["id_beneficiario","id_pagador"])["vlr_nominal"].sum().reset_index()
    conc_top = (conc.sort_values("vlr_nominal", ascending=False)
                    .groupby("id_beneficiario").first().reset_index()
                    .rename(columns={"vlr_nominal":"vlr_top_pagador"}))
    total_vlr = (df_bol.groupby("id_beneficiario")["vlr_nominal"].sum()
                       .reset_index().rename(columns={"vlr_nominal":"vlr_total_ref"}))
    conc_top = conc_top.merge(total_vlr, on="id_beneficiario")
    conc_top["concentracao_top1"] = conc_top["vlr_top_pagador"] / conc_top["vlr_total_ref"]
    agg = agg.merge(conc_top[["id_beneficiario","concentracao_top1"]], on="id_beneficiario", how="left")

    df = agg.merge(df_aux, left_on="id_beneficiario", right_on="id_cnpj", how="left")

    df["score_risco"] = _score_sintetico(df)
    df["nivel_risco"] = pd.cut(df["score_risco"], bins=[0,300,600,1000],
                                labels=["Alto","Médio","Baixo"])
    df["pd_30_est"] = df["pct_atraso_30"].clip(0,1)
    df["pd_60_est"] = df["pct_atraso_60"].clip(0,1)
    df["pd_90_est"] = df["pct_atraso_90"].clip(0,1)
    df["tendencia"] = _tendencia(df)
    return df, df_bol


def _score_sintetico(df):
    s = pd.Series(500.0, index=df.index)
    s -= df["pct_atraso_30"].fillna(0.5) * 200
    s -= df["pct_atraso_60"].fillna(0.5) * 150
    s -= df["pct_atraso_90"].fillna(0.5) * 100
    s -= df["dpd_medio"].fillna(30).clip(0,120) / 120 * 80
    mat = df["score_materialidade_v2"].fillna(df["score_materialidade_v2"].median())
    qtd = df["score_quantidade_v2"].fillna(df["score_quantidade_v2"].median())
    s += (mat/1000)*120 + (qtd/1000)*80
    s += (df["sacado_indice_liquidez_1m"].fillna(0.5) - 0.5) * 100
    s -= df["concentracao_top1"].fillna(0.5).clip(0,1) * 50
    return s.clip(0,1000).round(0)


def _tendencia(df):
    tend = []
    for _, r in df.iterrows():
        evo = r.get("score_materialidade_evolucao", 500)
        atr = r.get("pct_atraso_geral", 0.5)
        evo = 500 if pd.isna(evo) else evo
        if evo > 600 and atr < 0.1:   tend.append("↑ Melhora")
        elif evo < 400 or atr > 0.3:  tend.append("↓ Piora")
        else:                          tend.append("→ Estável")
    return pd.Series(tend, index=df.index)


def get_timeseries(df_bol):
    ts = df_bol.groupby("mes_emissao").agg(
        volume_total=("vlr_nominal","sum"),
        n_boletos   =("id_boleto",  "count"),
        pct_atraso  =("em_atraso",  "mean"),
    ).reset_index()
    return ts.sort_values("mes_emissao")


def get_shap_simulado(row):
    feats = [
        {"nome":"% Atraso 30d",       "valor":row.get("pct_atraso_30",0),               "peso":-0.35,"direcao":"risco"},
        {"nome":"Score Materialidade", "valor":row.get("score_materialidade_v2",500),    "peso": 0.25,"direcao":"protecao"},
        {"nome":"Liquidez sacado",     "valor":row.get("sacado_indice_liquidez_1m",0.5), "peso": 0.20,"direcao":"protecao"},
        {"nome":"Concentração top-1",  "valor":row.get("concentracao_top1",0.5),         "peso":-0.15,"direcao":"risco"},
        {"nome":"DPD médio",           "valor":row.get("dpd_medio",0),                   "peso":-0.12,"direcao":"risco"},
        {"nome":"Score Qtd v2",        "valor":row.get("score_quantidade_v2",500),       "peso": 0.10,"direcao":"protecao"},
    ]
    for f in feats:
        v = float(f["valor"]) if not pd.isna(f["valor"]) else 0.5
        v = v/1000 if v > 1 else v
        f["magnitude"] = min(abs(f["peso"])*v*2, 1.0)
    return sorted(feats, key=lambda x: x["magnitude"], reverse=True)[:5]
