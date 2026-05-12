"""pages/simulacao.py — Laboratório de estratégia: simulação de cutoff e modelos."""
import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import timedelta
import sys, pathlib

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
from data_loader import load_data

PLOTLY_DARK = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(13,27,53,0.6)",
    font=dict(family="IBM Plex Mono", color="#8fadc8", size=12),
    xaxis=dict(gridcolor="#1e3a5f", linecolor="#1e3a5f", zerolinecolor="#1e3a5f"),
    yaxis=dict(gridcolor="#1e3a5f", linecolor="#1e3a5f", zerolinecolor="#1e3a5f"),
    margin=dict(l=10, r=10, t=30, b=10),
)


def render(loader=None):
    from data_loader import load_data as _ld
    df, df_bol = (loader or _ld)()

    st.markdown("""
    <div class="turbo-header">
        <div>
            <div class="turbo-logo">🧪 Laboratório de Estratégia</div>
            <div class="turbo-subtitle">Simule o impacto de cutoffs e parâmetros antes de aplicar em produção</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Painel de controles ───────────────────────────────────────────────────
    st.markdown('<div class="section-title">Parâmetros da Simulação</div>', unsafe_allow_html=True)

    col_p1, col_p2, col_p3 = st.columns(3)
    with col_p1:
        modelo = st.selectbox("Modelo de risco (IA)", [
            "XGBoost v2.4 — Atual (MVP)",
        ])
    with col_p2:
        periodo = st.selectbox("Período de backtest", [
            "Todo o histórico",
            "Últimos 90 dias",
            "Últimos 30 dias",
            "Ano corrente",
        ])
    with col_p3:
        apetite = st.selectbox("Apetite ao risco", [
            "Equilibrado",
            "Conservador (foco em inadimplência)",
            "Agressivo (foco em volume)",
        ])

    # ── CORREÇÃO 1: Filtro de período funcionando ─────────────────────────────
    # MOTIVO: antes o selectbox de período não filtrava nada nos dados
    hoje = df_bol["dt_emissao"].max()
    if periodo == "Últimos 30 dias":
        df_bol_filt = df_bol[df_bol["dt_emissao"] >= hoje - timedelta(days=30)]
    elif periodo == "Últimos 90 dias":
        df_bol_filt = df_bol[df_bol["dt_emissao"] >= hoje - timedelta(days=90)]
    elif periodo == "Ano corrente":
        df_bol_filt = df_bol[df_bol["dt_emissao"].dt.year == hoje.year]
    else:
        df_bol_filt = df_bol.copy()

    # Mantém apenas cedentes que têm boletos no período filtrado
    cedentes_no_periodo = df_bol_filt["id_beneficiario"].unique()
    df_filt = df[df["id_beneficiario"].isin(cedentes_no_periodo)].copy()

    # Mostra info do filtro aplicado
    st.caption(f"📅 Período: {periodo} · {len(df_filt)} cedentes · {len(df_bol_filt):,} boletos analisados")

    if len(df_filt) == 0:
        st.warning("Nenhum cedente encontrado para o período selecionado.")
        return

    # ── CORREÇÃO 2: Sliders dinâmicos baseados no range real ─────────────────
    # MOTIVO: antes os sliders iam de 100-600 e 500-900, mas o score mínimo
    # real é ~675, então o slider baixo não tinha efeito prático
    score_min = int(df_filt["score_risco"].min())
    score_max = int(df_filt["score_risco"].max())

    # Garante um range mínimo para o slider funcionar mesmo com poucos dados
    if score_max - score_min < 20:
        score_min = max(0, score_min - 50)
        score_max = min(1000, score_max + 50)

    # Valores iniciais: 30% e 70% do range
    cutoff_low_default  = int(score_min + (score_max - score_min) * 0.3)
    cutoff_high_default = int(score_min + (score_max - score_min) * 0.7)

    st.markdown('<div class="section-title">Ajuste de Cutoff</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div style='font-size:12px; color:#607d9e; margin-bottom:12px;'>
    Score abaixo do cutoff baixo → <b style='color:#ef5350'>NEGAR</b> &nbsp;|&nbsp;
    Entre os dois → <b style='color:#ffc107'>REVISAR</b> &nbsp;|&nbsp;
    Acima do cutoff alto → <b style='color:#66bb6a'>APROVAR</b><br>
    <span style='color:#4fc3f7;'>Range real dos scores: {score_min} a {score_max}</span>
    </div>
    """, unsafe_allow_html=True)

    col_c1, col_c2 = st.columns(2)
    with col_c1:
        cutoff_low = st.slider(
            "Cutoff baixo (Negar/Revisar)",
            score_min, score_max, cutoff_low_default, step=1,
            help="Scores abaixo deste valor são automaticamente negados"
        )
    with col_c2:
        cutoff_high = st.slider(
            "Cutoff alto (Revisar/Aprovar)",
            score_min, score_max, cutoff_high_default, step=1,
            help="Scores acima deste valor são automaticamente aprovados"
        )

    if cutoff_low >= cutoff_high:
        st.warning("Cutoff baixo deve ser menor que o cutoff alto.")
        return

    # ── Simulação — usa score_risco já calculado pelo modelo ML no load_data ──
    df_sim = df_filt.copy()

    # Aplica fator de apetite ao risco sobre o score do modelo
    if "Conservador" in apetite:
        df_sim["score_sim"] = (df_sim["score_risco"] * 0.85).clip(0, 1000)
    elif "Agressivo" in apetite:
        df_sim["score_sim"] = (df_sim["score_risco"] * 1.15).clip(0, 1000)
    else:
        df_sim["score_sim"] = df_sim["score_risco"]

    # ── Decisão por cutoff ────────────────────────────────────────────────────
    df_sim["decisao"] = df_sim["score_sim"].apply(
        lambda s: "Aprovar" if s >= cutoff_high else ("Negar" if s <= cutoff_low else "Revisar")
    )

    aprovados = df_sim[df_sim["decisao"] == "Aprovar"]
    revisados = df_sim[df_sim["decisao"] == "Revisar"]
    negados   = df_sim[df_sim["decisao"] == "Negar"]

    taxa_ap  = len(aprovados) / len(df_sim) * 100
    taxa_rev = len(revisados) / len(df_sim) * 100
    taxa_neg = len(negados)   / len(df_sim) * 100

    risco_cart = aprovados["pct_atraso_30"].mean() * 100 if len(aprovados) > 0 else 0
    vol_ap  = aprovados["vlr_total"].sum() / 1e6
    vol_neg = negados["vlr_total"].sum() / 1e6

    taxa_juros = 0.03
    lgd        = 0.60
    receita_est = vol_ap * taxa_juros - vol_ap * (risco_cart / 100) * lgd

    if len(negados) > 0:
        perda_evit  = vol_neg * negados["pct_atraso_30"].mean() * lgd
        perda_label = "Perda Evitada Est."
    else:
        perda_evit  = vol_ap * (risco_cart / 100) * lgd
        perda_label = "Exposicao a Perdas Est."

    # ── KPIs ──────────────────────────────────────────────────────────────────
    st.markdown('<div class="section-title">Resultados da Simulação</div>', unsafe_allow_html=True)

    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Taxa de Aprovação",      f"{taxa_ap:.1f}%")
    k2.metric("Risco Projetado (PD30)", f"{risco_cart:.1f}%")
    k3.metric("Receita Líquida Est.",   f"R$ {receita_est:.2f}M")
    k4.metric(perda_label,              f"R$ {perda_evit:.2f}M")

    # ── Gráfico — distribuição de score com linhas de cutoff ─────────────────
    col_g1, col_g2 = st.columns(2)

    with col_g1:
        st.markdown("**Distribuição de Score com Cutoffs**")
        scores = df_sim["score_sim"].dropna()

        # Bins dinâmicos baseados no range real
        bin_step = max(1, (score_max - score_min) // 20)
        bins = np.arange(score_min, score_max + bin_step, bin_step)

        fig = go.Figure()
        for i in range(len(bins) - 1):
            msk = (scores >= bins[i]) & (scores < bins[i + 1])
            n   = msk.sum()
            if n == 0:
                continue
            mid = (bins[i] + bins[i + 1]) / 2
            cor = "#ef5350" if mid <= cutoff_low else ("#ffc107" if mid <= cutoff_high else "#66bb6a")
            fig.add_trace(go.Bar(x=[mid], y=[n], width=bin_step*0.9, marker_color=cor, showlegend=False))

        fig.add_vline(x=cutoff_low,  line_color="#ef5350", line_dash="dash")
        fig.add_vline(x=cutoff_high, line_color="#66bb6a", line_dash="dash")
        fig.update_layout(**PLOTLY_DARK, height=280)
        st.plotly_chart(fig, use_container_width=True)

    with col_g2:
        st.markdown("**Decisões por Faixa de Score**")
        fig2 = go.Figure(go.Bar(
            x=["Negar", "Revisar", "Aprovar"],
            y=[len(negados), len(revisados), len(aprovados)],
            marker_color=["#ef5350", "#ffc107", "#66bb6a"],
        ))
        fig2.update_layout(**PLOTLY_DARK, height=280, showlegend=False, bargap=0.3)
        st.plotly_chart(fig2, use_container_width=True)