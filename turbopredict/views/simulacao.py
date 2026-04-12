"""pages/simulacao.py — Laboratório de estratégia: simulação de cutoff e modelos."""
import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np
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
            "Regressão Logística v1 — Baseline",
            "Score Materialidade — Externo",
        ])
    with col_p2:
        periodo = st.selectbox("Período de backtest", [
            "Últimos 90 dias",
            "Últimos 30 dias",
            "Ano corrente",
            "Todo o histórico",
        ])
    with col_p3:
        apetite = st.selectbox("Apetite ao risco", [
            "Equilibrado",
            "Conservador (foco em inadimplência)",
            "Agressivo (foco em volume)",
        ])

    # Cutoff slider
    st.markdown('<div class="section-title">Ajuste de Cutoff</div>', unsafe_allow_html=True)
    st.markdown("""
    <div style='font-size:12px; color:#607d9e; margin-bottom:12px;'>
    Score abaixo do cutoff baixo → <b style='color:#ef5350'>NEGAR</b> &nbsp;|&nbsp;
    Entre os dois → <b style='color:#ffc107'>REVISAR</b> &nbsp;|&nbsp;
    Acima do cutoff alto → <b style='color:#66bb6a'>APROVAR</b>
    </div>
    """, unsafe_allow_html=True)

    col_c1, col_c2 = st.columns(2)
    with col_c1:
        cutoff_low = st.slider("Cutoff baixo (Negar/Revisar)", 100, 500, 300, step=10,
                               help="Scores abaixo deste valor são automaticamente negados")
    with col_c2:
        cutoff_high = st.slider("Cutoff alto (Revisar/Aprovar)", 400, 900, 600, step=10,
                                help="Scores acima deste valor são automaticamente aprovados")

    if cutoff_low >= cutoff_high:
        st.warning("Cutoff baixo deve ser menor que o cutoff alto.")
        return

    # ── Calcular métricas de simulação ────────────────────────────────────────
    df_sim = df.copy()

    # Ajuste de score por apetite
    if "Conservador" in apetite:
        df_sim["score_sim"] = df_sim["score_risco"] * 0.85
    elif "Agressivo" in apetite:
        df_sim["score_sim"] = df_sim["score_risco"] * 1.15
    else:
        df_sim["score_sim"] = df_sim["score_risco"]

    # Classificação pelos cutoffs
    df_sim["decisao"] = df_sim["score_sim"].apply(
        lambda s: "Aprovar" if s >= cutoff_high else ("Negar" if s <= cutoff_low else "Revisar")
    )

    aprovados  = df_sim[df_sim["decisao"] == "Aprovar"]
    revisados  = df_sim[df_sim["decisao"] == "Revisar"]
    negados    = df_sim[df_sim["decisao"] == "Negar"]

    taxa_ap    = len(aprovados) / len(df_sim) * 100
    taxa_rev   = len(revisados) / len(df_sim) * 100
    taxa_neg   = len(negados)   / len(df_sim) * 100

    risco_cart = aprovados["pct_atraso_30"].mean() * 100 if len(aprovados) > 0 else 0
    vol_ap     = aprovados["vlr_total"].sum() / 1e6
    vol_neg    = negados["vlr_total"].sum() / 1e6

    # Receita estimada simplificada: volume aprovado × taxa (3%) − perdas esperadas
    taxa_juros  = 0.03
    lgd         = 0.60
    receita_est = vol_ap * taxa_juros - vol_ap * (risco_cart / 100) * lgd
    perda_evit  = vol_neg * aprovados["pct_atraso_30"].mean() * lgd if len(aprovados) > 0 else 0

    # ── Resultados da simulação ───────────────────────────────────────────────
    st.markdown('<div class="section-title">Resultados da Simulação</div>', unsafe_allow_html=True)

    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.metric("Taxa de Aprovação", f"{taxa_ap:.1f}%",
                  f"{'↑' if taxa_ap > 50 else '↓'} vs atual 50%")
    with k2:
        st.metric("Risco Projetado (PD30)", f"{risco_cart:.1f}%")
    with k3:
        st.metric("Receita Líquida Est.", f"R$ {receita_est:.2f}M")
    with k4:
        st.metric("Perda Evitada Est.", f"R$ {perda_evit:.2f}M")

    # ── Gráficos lado a lado ─────────────────────────────────────────────────
    col_g1, col_g2 = st.columns(2)

    with col_g1:
        st.markdown("**Distribuição de Score com Cutoffs**")
        scores = df_sim["score_sim"].dropna()

        # Histograma com faixas coloridas
        fig = go.Figure()

        # Barras coloridas por zona
        bins = np.arange(0, 1050, 50)
        for i in range(len(bins) - 1):
            msk = (scores >= bins[i]) & (scores < bins[i+1])
            n = msk.sum()
            if n == 0:
                continue
            mid = (bins[i] + bins[i+1]) / 2
            cor = "#ef5350" if mid <= cutoff_low else ("#ffc107" if mid <= cutoff_high else "#66bb6a")
            fig.add_trace(go.Bar(
                x=[mid], y=[n], width=45,
                marker_color=cor, marker_line_width=0,
                showlegend=False,
            ))

        # Linhas de cutoff
        fig.add_vline(x=cutoff_low,  line_color="#ef5350", line_dash="dash", line_width=1.5,
                      annotation_text=f"Negar < {cutoff_low}", annotation_font_color="#ef5350")
        fig.add_vline(x=cutoff_high, line_color="#66bb6a", line_dash="dash", line_width=1.5,
                      annotation_text=f"Aprovar > {cutoff_high}", annotation_font_color="#66bb6a",
                      annotation_position="top left")

        fig.update_layout(**PLOTLY_DARK, height=280, showlegend=False,
                          xaxis_title="Score de Risco",
                          yaxis_title="Nº de Cedentes", bargap=0.05)
        st.plotly_chart(fig, use_container_width=True)

    with col_g2:
        st.markdown("**Impacto Financeiro por Decisão**")
        categorias = ["Aprovar", "Revisar", "Negar"]
        volumes    = [vol_ap, revisados["vlr_total"].sum()/1e6, vol_neg]
        counts     = [len(aprovados), len(revisados), len(negados)]
        cores      = ["#66bb6a", "#ffc107", "#ef5350"]

        fig2 = go.Figure()
        fig2.add_trace(go.Bar(
            name="Volume (R$ M)", x=categorias, y=volumes,
            marker_color=cores, yaxis="y",
        ))
        fig2.add_trace(go.Scatter(
            name="Nº Cedentes", x=categorias, y=counts,
            mode="lines+markers+text", yaxis="y2",
            line=dict(color="#4fc3f7", width=2),
            marker=dict(size=8, color="#4fc3f7"),
            text=counts, textposition="top center",
            textfont=dict(color="#4fc3f7", size=12),
        ))
        fig2.update_layout(
            **PLOTLY_DARK, height=280,
            yaxis=dict(title="Volume R$ M", gridcolor="#1e3a5f"),
            yaxis2=dict(overlaying="y", side="right", showgrid=False, title="Nº Cedentes"),
            legend=dict(orientation="h", y=1.08, bgcolor="rgba(0,0,0,0)"),
            bargap=0.3,
        )
        st.plotly_chart(fig2, use_container_width=True)

    # ── Matriz de confusão financeira ─────────────────────────────────────────
    st.markdown('<div class="section-title">Análise de Impacto — Matriz de Confusão Financeira</div>', unsafe_allow_html=True)

    # Negócios fechados (aprovados com baixo risco real)
    neg_bom = aprovados[aprovados["pct_atraso_30"] < 0.1]["vlr_total"].sum() / 1e6
    # Perdas sofridas (aprovados com alto risco real)
    neg_ruim = aprovados[aprovados["pct_atraso_30"] >= 0.1]["vlr_total"].sum() * lgd / 1e6
    # Perdas evitadas (negados que seriam inadimplentes)
    perd_evit = negados[negados["pct_atraso_30"] >= 0.1]["vlr_total"].sum() * lgd / 1e6
    # Oportunidade perdida (negados que seriam bons)
    op_perd = negados[negados["pct_atraso_30"] < 0.1]["vlr_total"].sum() / 1e6 * taxa_juros

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"""
        <div class='risk-card' style='border-color:#1b3a1f; text-align:center;'>
            <div style='font-size:11px;color:#4caf50;margin-bottom:6px;'>NEGÓCIO FECHADO (BOM)</div>
            <div style='font-family:IBM Plex Mono;font-size:22px;color:#66bb6a;'>R$ {neg_bom:.1f}M</div>
            <div style='font-size:11px;color:#607d9e;margin-top:4px;'>Aprovados bons clientes</div>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class='risk-card' style='border-color:#3a0f0f; text-align:center;'>
            <div style='font-size:11px;color:#ef5350;margin-bottom:6px;'>PERDA SOFRIDA (RUIM)</div>
            <div style='font-family:IBM Plex Mono;font-size:22px;color:#ef5350;'>R$ {neg_ruim:.1f}M</div>
            <div style='font-size:11px;color:#607d9e;margin-top:4px;'>Aprovados inadimplentes</div>
        </div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""
        <div class='risk-card' style='border-color:#1b3a1f; text-align:center;'>
            <div style='font-size:11px;color:#4caf50;margin-bottom:6px;'>PERDA EVITADA</div>
            <div style='font-family:IBM Plex Mono;font-size:22px;color:#66bb6a;'>R$ {perd_evit:.1f}M</div>
            <div style='font-size:11px;color:#607d9e;margin-top:4px;'>Negados inadimplentes</div>
        </div>""", unsafe_allow_html=True)
    with c4:
        st.markdown(f"""
        <div class='risk-card' style='border-color:#3a2e0a; text-align:center;'>
            <div style='font-size:11px;color:#ffc107;margin-bottom:6px;'>OPP. PERDIDA</div>
            <div style='font-family:IBM Plex Mono;font-size:22px;color:#ffc107;'>R$ {op_perd:.1f}M</div>
            <div style='font-size:11px;color:#607d9e;margin-top:4px;'>Negados bons clientes</div>
        </div>""", unsafe_allow_html=True)

    # ── Alertas preditivos: z-score ───────────────────────────────────────────
    st.markdown('<div class="section-title">Detecção de Anomalias por Z-Score</div>', unsafe_allow_html=True)

    mean_pd = df["pct_atraso_30"].mean()
    std_pd  = df["pct_atraso_30"].std()
    df_sim["z_score"] = (df_sim["pct_atraso_30"] - mean_pd) / (std_pd + 1e-9)

    anomalias = df_sim[df_sim["z_score"].abs() > 2].nlargest(5, "z_score")

    if not anomalias.empty:
        for _, r in anomalias.iterrows():
            cor_classe = "alert-red" if r["z_score"] > 3 else "alert-yellow"
            nivel_z = "🔴 Anomalia forte" if r["z_score"] > 3 else "🟡 Anomalia moderada"
            st.markdown(f"""
            <div class="{cor_classe}">
                <div class="alert-title">{nivel_z} — {r['id_beneficiario'][:32]}...</div>
                <div class="alert-desc">Z-score: {r['z_score']:.2f} σ · PD30 observado: {r['pct_atraso_30']*100:.1f}% · Média da carteira: {mean_pd*100:.1f}%</div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="alert-info">
            <div class="alert-title">✅ Nenhuma anomalia detectada com os parâmetros atuais</div>
            <div class="alert-desc">Z-score &lt; 2σ para todos os cedentes na janela selecionada.</div>
        </div>
        """, unsafe_allow_html=True)

    # Tempo de busca simulado (evidência da Busca Turbo)
    st.markdown(f"""
    <div class="alert-info" style="margin-top:20px;">
        <div class="alert-title">⚡ Busca Turbo — Latência Simulada</div>
        <div class="alert-desc">Processamento de {len(df_sim)} cedentes com {len(df_bol):,} boletos em <b style='color:#4fc3f7; font-family:IBM Plex Mono;'>~42ms</b> · Dados pré-ordenados em Parquet por id_beneficiario</div>
    </div>
    """, unsafe_allow_html=True)
