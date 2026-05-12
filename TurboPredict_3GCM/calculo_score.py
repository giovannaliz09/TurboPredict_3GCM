"""
calculo_score.py — Motor de score XGBoost integrado.
Carrega os 3 modelos (30/60/90 dias) e expõe funções de feature engineering.
"""
import pandas as pd
import numpy as np
import joblib
import json
from pathlib import Path

# ── Caminhos ────────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).parent / "models"

# ── Carregamento dos modelos ─────────────────────────────────────────────────
model_30 = joblib.load(BASE_DIR / "xgb_pd_30.pkl")
model_60 = joblib.load(BASE_DIR / "xgb_pd_60.pkl")
model_90 = joblib.load(BASE_DIR / "xgb_pd_90.pkl")

with open(BASE_DIR / "feature_cols.json") as f:
    FEATURE_COLS = json.load(f)


# ── Preparação da base de boletos ────────────────────────────────────────────
def preparar_base_boletos(df_bol: pd.DataFrame) -> pd.DataFrame:
    df = df_bol.copy()

    df["dt_pagamento"]  = pd.to_datetime(df["dt_pagamento"],  errors="coerce")
    df["dt_vencimento"] = pd.to_datetime(df["dt_vencimento"], errors="coerce")
    df["dt_emissao"]    = pd.to_datetime(df["dt_emissao"],    errors="coerce")

    df["dpd"]       = (df["dt_pagamento"] - df["dt_vencimento"]).dt.days.fillna(999)
    df["em_atraso"] = df["dpd"] > 0
    df["atraso_30"] = df["dpd"] >= 30
    df["atraso_60"] = df["dpd"] >= 60
    df["atraso_90"] = df["dpd"] >= 90

    df["mes_emissao"]          = df["dt_emissao"].dt.to_period("M")
    df["pct_baixa_vs_nominal"] = (df["vlr_baixa"] / df["vlr_nominal"]).clip(0, 1) \
                                 if "vlr_baixa" in df.columns else 0.0

    return df


# ── Feature engineering ──────────────────────────────────────────────────────
def build_features(df_boletos: pd.DataFrame, df_aux: pd.DataFrame = None) -> pd.DataFrame:
    df = df_boletos.copy()

    agg = df.groupby("id_beneficiario").agg(
        total_boletos       =("id_boleto",    "count"),
        vlr_total           =("vlr_nominal",  "sum"),
        vlr_medio           =("vlr_nominal",  "mean"),
        vlr_std             =("vlr_nominal",  "std"),
        pct_atraso_geral    =("em_atraso",    "mean"),
        # Renomeados para bater com feature_cols.json (treinado com sufixo _hist)
        pd_30_hist          =("atraso_30",    "mean"),
        pd_60_hist          =("atraso_60",    "mean"),
        pd_90_hist          =("atraso_90",    "mean"),
        dpd_medio           =("dpd", lambda x: x[x < 999].mean() if (x < 999).any() else 0),
        dpd_max             =("dpd", lambda x: x[x < 999].max()  if (x < 999).any() else 0),
        n_pagadores_unicos  =("id_pagador",   "nunique"),
        meses_ativo         =("mes_emissao",  "nunique"),
        n_especies          =("tipo_especie", "nunique"),
        pct_baixa_vs_nominal=("pct_baixa_vs_nominal", lambda x: x.fillna(0).mean()),
    ).reset_index()

    agg["atraso_cronico"] = (agg["dpd_medio"] > 30).astype(int)

    # Concentração em único pagador
    conc = df.groupby(["id_beneficiario", "id_pagador"])["vlr_nominal"].sum().reset_index()
    conc_top = (
        conc.sort_values("vlr_nominal", ascending=False)
            .groupby("id_beneficiario").first().reset_index()
            .rename(columns={"vlr_nominal": "vlr_top_pagador"})
    )
    total_vlr = df.groupby("id_beneficiario")["vlr_nominal"].sum().reset_index()
    conc_top  = conc_top.merge(total_vlr, on="id_beneficiario")
    conc_top["concentracao_top1"] = conc_top["vlr_top_pagador"] / conc_top["vlr_nominal"]
    agg = agg.merge(conc_top[["id_beneficiario", "concentracao_top1"]], on="id_beneficiario", how="left")

    # Recência
    ultimo = df.groupby("id_beneficiario")["dt_emissao"].max().reset_index()
    ultimo["dias_desde_ultimo"] = (df["dt_emissao"].max() - ultimo["dt_emissao"]).dt.days
    agg = agg.merge(ultimo[["id_beneficiario", "dias_desde_ultimo"]], on="id_beneficiario", how="left")

    # ── Join com base auxiliar ────────────────────────────────────────────────
    if df_aux is not None:
        aux_cols = [
            "id_cnpj", "cd_cnae_prin", "uf",
            "sacado_indice_liquidez_1m",
            "cedente_indice_liquidez_1m",
            "score_materialidade_evolucao",
            "media_atraso_dias",
            "indicador_liquidez_quantitativo_3m",
            "share_vl_inad_pag_bol_6_a_15d",
            "score_quantidade",
            "score_materialidade",
        ]
        aux = df_aux[[c for c in aux_cols if c in df_aux.columns]].copy()
        if "uf" in aux.columns:
            aux["uf_cod"] = aux["uf"].astype("category").cat.codes
            aux = aux.drop(columns=["uf"])
        if "cd_cnae_prin" in aux.columns:
            aux["cnae_cod"] = aux["cd_cnae_prin"].astype("category").cat.codes
            aux = aux.drop(columns=["cd_cnae_prin"])
        agg = agg.merge(aux, left_on="id_beneficiario", right_on="id_cnpj", how="left")
        agg = agg.drop(columns=["id_cnpj"], errors="ignore")

    return agg


# ── Score em batch para toda a carteira (usado pelo data_loader) ─────────────
def score_carteira(df_bol: pd.DataFrame, df_aux: pd.DataFrame) -> pd.DataFrame:
    """
    Roda o pipeline ML completo sobre toda a carteira.

    O score final é a média ponderada de dois componentes:
      - Score ML (60%): saída dos modelos XGBoost PD30/60/90 convertida para 0-1000
      - Score qualitativo (40%): score composto de materialidade, liquidez e concentração,
        para diferenciar os ~91% de clientes com PD histórico = 0

    Retorna DataFrame com colunas:
        id_beneficiario, score_risco (int 0-1000), nivel_risco ('Alto'|'Médio'|'Baixo'),
        pd_30_est, pd_60_est, pd_90_est
    """
    df_base = preparar_base_boletos(df_bol)
    df_feat = build_features(df_base, df_aux)

    for col in FEATURE_COLS:
        if col not in df_feat.columns:
            df_feat[col] = 0

    X = df_feat[FEATURE_COLS].copy()
    X = X.apply(pd.to_numeric, errors="coerce").fillna(0)

    pd30 = np.clip(model_30.predict(X), 0, 1)
    pd60 = np.clip(model_60.predict(X), 0, 1)
    pd90 = np.clip(model_90.predict(X), 0, 1)

    pd_final = pd30 * 0.5 + pd60 * 0.3 + pd90 * 0.2

    # Score ML puro (0-1000 linear)
    score_ml = np.clip((1 - pd_final) * 1000, 0, 1000)

    # Score qualitativo — diferencia os 91% de clientes com PD histórico = 0
    # Usa features auxiliares para rankear risco relativo dentro do grupo "adimplente"
    mat  = df_feat.get("score_materialidade",  pd.Series(500, index=df_feat.index))
    qtd  = df_feat.get("score_quantidade",      pd.Series(500, index=df_feat.index))
    liq  = df_feat.get("sacado_indice_liquidez_1m",pd.Series(0.5, index=df_feat.index))
    evo  = df_feat.get("score_materialidade_evolucao", pd.Series(500, index=df_feat.index))
    conc = df_feat.get("concentracao_top1",        pd.Series(0.5, index=df_feat.index))
    dpd  = df_feat.get("dpd_medio",                pd.Series(0,   index=df_feat.index))

    mat  = pd.to_numeric(mat,  errors="coerce").fillna(500)
    qtd  = pd.to_numeric(qtd,  errors="coerce").fillna(500)
    liq  = pd.to_numeric(liq,  errors="coerce").fillna(0.5)
    evo  = pd.to_numeric(evo,  errors="coerce").fillna(500)
    conc = pd.to_numeric(conc, errors="coerce").fillna(0.5)
    dpd  = pd.to_numeric(dpd,  errors="coerce").fillna(0)

    qualidade   = ((mat/1000)*0.4 + (qtd/1000)*0.3 + liq*0.2 + (evo/1000)*0.1) * 300
    penalidades = -((dpd.clip(0, 120)/120)*100 + conc.clip(0, 1)*100) / 2 * 0.4
    score_pd    = (1 - pd_final) * 500

    score_qualitativo = np.clip(score_pd + qualidade + penalidades, 0, 1000)

    # Score final: média ponderada ML (60%) + qualitativo (40%)
    score_final = np.clip(score_ml * 0.6 + score_qualitativo * 0.4, 0, 1000).round(0).astype(int)

    result = pd.DataFrame({
        "id_beneficiario": df_feat["id_beneficiario"].values,
        "score_risco":     score_final,
        "pd_30_est":       pd30,
        "pd_60_est":       pd60,
        "pd_90_est":       pd90,
    })

    # ── CORREÇÃO CRÍTICA: classificação por percentis (não bins fixos) ──────
    # Antes os bins eram [0, 400, 700, 1000], mas como os scores XGBoost
    # ficam concentrados em 657-911, NINGUÉM caía em "Alto" e quase ninguém
    # em "Médio". Agora usa percentis 30/70 para distribuir os cedentes
    # proporcionalmente entre Alto/Médio/Baixo, garantindo que sempre exista uma população em cada nível para análise de risco.
    p30 = result["score_risco"].quantile(0.30)
    p70 = result["score_risco"].quantile(0.70)

    def classificar(score):
        if score <= p30:
            return "Alto"
        elif score <= p70:
            return "Médio"
        else:
            return "Baixo"

    result["nivel_risco"] = result["score_risco"].apply(classificar)

    return result


# ── Score para um único cliente ──────────────────────────────────────────────
def calcular_score_cliente(row, df_bol: pd.DataFrame, df_aux: pd.DataFrame = None):
    """
    Retorna (score: int, erro: str|None).
    Score de 0 a 1000 — quanto maior, menor o risco.
    """
    try:
        df_base = preparar_base_boletos(df_bol)
        df_feat = build_features(df_base, df_aux)

        cliente_id = row["id_beneficiario"]
        df_feat = df_feat[df_feat["id_beneficiario"] == cliente_id]

        if df_feat.empty:
            return 200, "Sem histórico suficiente"

        for col in FEATURE_COLS:
            if col not in df_feat.columns:
                df_feat[col] = 0

        X = df_feat[FEATURE_COLS].copy()
        X = X.apply(pd.to_numeric, errors="coerce").fillna(0)

        p30 = float(np.clip(model_30.predict(X)[0], 0, 1))
        p60 = float(np.clip(model_60.predict(X)[0], 0, 1))
        p90 = float(np.clip(model_90.predict(X)[0], 0, 1))

        pd_final = p30 * 0.5 + p60 * 0.3 + p90 * 0.2
        score = int(np.clip((1 - pd_final) * 1000, 0, 1000))

        return score, None

    except Exception as e:
        return 200, f"Erro: {str(e)}"
