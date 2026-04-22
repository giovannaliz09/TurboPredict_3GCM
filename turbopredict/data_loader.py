import pandas as pd
import numpy as np
from pathlib import Path

_HERE    = Path(__file__).resolve().parent
DATA_DIR = _HERE / "data"
_FILE_BOL = DATA_DIR / "base_boletos_fiap.csv"
_FILE_AUX = DATA_DIR / "base_auxiliar_fiap.csv"
_FILE_PROCESSADO = DATA_DIR / "base_final_processada.csv"

def data_files_ok() -> bool:
    return _FILE_BOL.exists() and _FILE_AUX.exists()

def save_uploaded_files(bytes_bol: bytes, bytes_aux: bytes) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    _FILE_BOL.write_bytes(bytes_bol)
    _FILE_AUX.write_bytes(bytes_aux)


def _enrich_df_bol(df_bol: pd.DataFrame) -> pd.DataFrame:
    """
    Garante que df_bol sempre tenha as colunas derivadas necessárias:
      - dpd          (dias de atraso; NaN de pagamento → 999)
      - em_atraso    (bool: dpd > 0)
      - mes_emissao  (período mensal como string)
    Seguro chamar mesmo que as colunas já existam.
    """
    if "dpd" not in df_bol.columns:
        df_bol["dpd"] = (
            df_bol["dt_pagamento"] - df_bol["dt_vencimento"]
        ).dt.days.fillna(999)

    if "em_atraso" not in df_bol.columns:
        df_bol["em_atraso"] = df_bol["dpd"] > 0

    if "mes_emissao" not in df_bol.columns:
        df_bol["mes_emissao"] = (
            df_bol["dt_emissao"].dt.to_period("M").astype(str)
        )

    return df_bol


def _enrich_df(df: pd.DataFrame, df_bol: pd.DataFrame) -> pd.DataFrame:
    """
    Garante que df (nível beneficiário) sempre tenha pct_atraso_30,
    calculada a partir de df_bol quando ausente.
    """
    if "pct_atraso_30" not in df.columns:
        atraso30 = (
            df_bol.assign(flag=df_bol["dpd"] >= 30)
            .groupby("id_beneficiario")["flag"]
            .mean()
            .rename("pct_atraso_30")
            .reset_index()
        )
        df = df.merge(atraso30, on="id_beneficiario", how="left")
        df["pct_atraso_30"] = df["pct_atraso_30"].fillna(0.0)

    return df


def load_data():
    if _FILE_PROCESSADO.exists():
        df = pd.read_csv(_FILE_PROCESSADO)
        df_bol = pd.read_csv(
            _FILE_BOL,
            parse_dates=["dt_emissao", "dt_vencimento", "dt_pagamento"],
        )

        # CORREÇÃO Erros 1 e 2: sempre enriquecer df_bol
        df_bol = _enrich_df_bol(df_bol)

        # CORREÇÃO Erro 3: garantir pct_atraso_30 em df
        df = _enrich_df(df, df_bol)

        return df, df_bol

    # ── Caminho sem arquivo processado ────────────────────────────────────────
    df_bol = pd.read_csv(
        _FILE_BOL,
        parse_dates=["dt_emissao", "dt_vencimento", "dt_pagamento"],
    )
    df_aux = pd.read_csv(_FILE_AUX)

    # CORREÇÃO Erros 1 e 2: enriquecer df_bol antes de qualquer uso
    df_bol = _enrich_df_bol(df_bol)

    df = df_bol.groupby("id_beneficiario").agg(
        vlr_total=("vlr_nominal", "sum"),
        total_boletos=("id_boleto", "count"),
    ).reset_index()

    df = df.merge(df_aux, left_on="id_beneficiario", right_on="id_cnpj", how="left")

    df["score"] = 0
    df["nivel_risco"] = "Não Processado"

    # CORREÇÃO Erro 3: calcular pct_atraso_30 a partir do df_bol enriquecido
    df = _enrich_df(df, df_bol)

    return df, df_bol


def _tendencia(df):
    tend = []
    for _, r in df.iterrows():
        evo = r.get("score_evolucao_v2", 500)
        atr = r.get("pct_atraso_30", 0)
        if evo > 600 and atr < 0.1:    tend.append("↑ Melhora")
        elif evo < 400 or atr > 0.3:   tend.append("↓ Piora")
        else:                           tend.append("→ Estável")
    return pd.Series(tend, index=df.index)


def get_timeseries(df_bol):
    # df_bol já chegará enriquecido (mes_emissao garantida por _enrich_df_bol)
    ts = df_bol.groupby("mes_emissao").agg(
        volume_total=("vlr_nominal", "sum"),
        n_boletos   =("id_boleto",   "count"),
        pct_atraso  =("em_atraso",   "mean"),
    ).reset_index()
    return ts.sort_values("mes_emissao")
