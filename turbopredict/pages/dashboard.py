"""pages/dashboard.py — Tela principal com KPIs, tabela de cedentes e alertas."""
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
import sys, pathlib

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
from data_loader import load_data, get_timeseries, get_shap_simulado

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
    ts = get_timeseries(df_bol)

    # ── Header ───────────────────────────────────────────────────────────────
    st.markdown("""
    <div class="turbo-header">
        <div>
            <div class="turbo-logo">⚡ TurboPredict</div>
            <div class="turbo-subtitle">Dashboard de Risco · Análise de Recebíveis FIAP/Núclea 2025</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Barra de busca ───────────────────────────────────────────────────────
    busca = st.text_input(
        "🔍  Busca Turbo",
        placeholder="Buscar por ID do beneficiário...",
        label_visibility="collapsed",
    )
    if busca:
        resultados = df[df["id_beneficiario"].str.contains(busca[:8], case=False, na=False)]
        if not resultados.empty:
            st.success(f"{len(resultados)} cedente(s) encontrado(s)")
            _render_cedente_card(resultados.iloc[0])
            return
        else:
            st.warning("Nenhum cedente encontrado para essa busca.")

    # ── KPIs ─────────────────────────────────────────────────────────────────
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.metric("Volume Total Analisado", f"R$ {df['vlr_total'].sum()/1e6:.1f}M", "↑ 7% vs mês anterior")
    with k2:
        taxa_ap = (df["nivel_risco"] == "Baixo").mean()
        st.metric("Taxa de Aprovação", f"{taxa_ap*100:.1f}%", f"Cutoff atual: 400 pts")
    with k3:
        risco_pond = df["pct_atraso_30"].mean()
        st.metric("Risco Ponderado (PD30)", f"{risco_pond*100:.1f}%", "Estável")
    with k4:
        alertas_crit = (df["nivel_risco"] == "Alto").sum()
        st.metric("Alertas TurboPredict", f"{int(alertas_crit)} Críticos", "⚠ Requer atenção")

    st.markdown("---")

    # ── Gráficos ─────────────────────────────────────────────────────────────
    col_esq, col_dir = st.columns([3, 2])

    with col_esq:
        st.markdown('<div class="section-title">Evolução Mensal de Volume e Atraso</div>', unsafe_allow_html=True)
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=ts["mes_emissao"], y=ts["volume_total"] / 1e3,
            name="Volume (R$ mil)", marker_color="#1e3a5f", marker_line_color="#2d5a8f", marker_line_width=1,
        ))
        fig.add_trace(go.Scatter(
            x=ts["mes_emissao"], y=ts["pct_atraso"] * 100,
            name="% Atraso", yaxis="y2", line=dict(color="#ef5350", width=2),
            mode="lines+markers", marker=dict(size=5),
        ))
        fig.update_layout(
            **PLOTLY_DARK,
            height=280,
            yaxis2=dict(overlaying="y", side="right", showgrid=False, ticksuffix="%", color="#ef5350"),
            legend=dict(orientation="h", y=1.08, x=0, bgcolor="rgba(0,0,0,0)"),
            yaxis_tickprefix="R$", yaxis_ticksuffix="k",
            bargap=0.25,
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_dir:
        st.markdown('<div class="section-title">Distribuição de Score de Risco</div>', unsafe_allow_html=True)
        bins = pd.cut(df["score_risco"], bins=10)
        contagem = bins.value_counts().sort_index()
        cores = ["#ef5350" if i < 3 else ("#ffc107" if i < 7 else "#66bb6a") for i in range(len(contagem))]
        fig2 = go.Figure(go.Bar(
            x=[str(b) for b in contagem.index],
            y=contagem.values,
            marker_color=cores,
        ))
        fig2.update_layout(**PLOTLY_DARK, height=280, showlegend=False,
                           xaxis_tickangle=-45, bargap=0.1)
        st.plotly_chart(fig2, use_container_width=True)

    # ── Tabela de cedentes ────────────────────────────────────────────────────
    st.markdown('<div class="section-title">Cedentes — Visão Geral de Risco</div>', unsafe_allow_html=True)

    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1:
        filtro_risco = st.selectbox("Filtrar por risco", ["Todos", "Alto", "Médio", "Baixo"])
    with col_f2:
        filtro_tend = st.selectbox("Filtrar por tendência", ["Todas", "↑ Melhora", "→ Estável", "↓ Piora"])
    with col_f3:
        ordenar = st.selectbox("Ordenar por", ["Score (↑ risco primeiro)", "Volume total", "% Atraso 30d"])

    df_tab = df.copy()
    if filtro_risco != "Todos":
        df_tab = df_tab[df_tab["nivel_risco"] == filtro_risco]
    if filtro_tend != "Todas":
        df_tab = df_tab[df_tab["tendencia"] == filtro_tend]

    if ordenar == "Score (↑ risco primeiro)":
        df_tab = df_tab.sort_values("score_risco")
    elif ordenar == "Volume total":
        df_tab = df_tab.sort_values("vlr_total", ascending=False)
    else:
        df_tab = df_tab.sort_values("pct_atraso_30", ascending=False)

    df_tab = df_tab.head(50)

    # Renderizar tabela HTML estilizada
    rows_html = ""
    for _, row in df_tab.iterrows():
        score = int(row["score_risco"])
        nivel = row["nivel_risco"]
        badge_cls = "badge-green" if nivel == "Baixo" else ("badge-yellow" if nivel == "Médio" else "badge-red")
        tend = row["tendencia"]
        tend_cls = "tend-up" if "Piora" in tend else ("tend-down" if "Melhora" in tend else "tend-stab")
        vlr = f"R$ {row['vlr_total']:,.0f}"
        atr30 = f"{row['pct_atraso_30']*100:.1f}%"
        dpd = f"{row['dpd_medio']:.0f}d"
        boletos = int(row["total_boletos"])
        cedente_id = row["id_beneficiario"][:16] + "..."

        rows_html += f"""
        <tr style='border-bottom:1px solid #132035;'>
          <td style='padding:10px 12px; font-family:IBM Plex Mono,monospace; font-size:12px; color:#8fadc8;'>{cedente_id}</td>
          <td style='padding:10px 12px;'><span class='score-badge {badge_cls}'>{score}</span></td>
          <td style='padding:10px 12px; font-size:13px;'>{vlr}</td>
          <td style='padding:10px 12px; font-size:13px;'>{atr30}</td>
          <td style='padding:10px 12px; font-size:13px;'>{dpd}</td>
          <td style='padding:10px 12px; font-size:13px;'>{boletos}</td>
          <td style='padding:10px 12px;'><span class='{tend_cls}'>{tend}</span></td>
        </tr>"""

    st.markdown(f"""
    <div style='overflow-x:auto; border-radius:10px; border:1px solid #1e3a5f;'>
    <table style='width:100%; border-collapse:collapse; background:#0d1b35;'>
      <thead>
        <tr style='background:#132035; border-bottom:1px solid #1e3a5f;'>
          <th style='padding:10px 12px; text-align:left; font-size:11px; color:#607d9e; letter-spacing:.06em;'>ID BENEFICIÁRIO</th>
          <th style='padding:10px 12px; text-align:left; font-size:11px; color:#607d9e; letter-spacing:.06em;'>SCORE IA</th>
          <th style='padding:10px 12px; text-align:left; font-size:11px; color:#607d9e; letter-spacing:.06em;'>VOLUME</th>
          <th style='padding:10px 12px; text-align:left; font-size:11px; color:#607d9e; letter-spacing:.06em;'>ATRASO 30D</th>
          <th style='padding:10px 12px; text-align:left; font-size:11px; color:#607d9e; letter-spacing:.06em;'>DPD MÉDIO</th>
          <th style='padding:10px 12px; text-align:left; font-size:11px; color:#607d9e; letter-spacing:.06em;'>BOLETOS</th>
          <th style='padding:10px 12px; text-align:left; font-size:11px; color:#607d9e; letter-spacing:.06em;'>TENDÊNCIA</th>
        </tr>
      </thead>
      <tbody>{rows_html}</tbody>
    </table>
    </div>
    """, unsafe_allow_html=True)

    # ── Alertas laterais ─────────────────────────────────────────────────────
    st.markdown('<div class="section-title">Alertas TurboPredict Ativos</div>', unsafe_allow_html=True)

    criticos = df[df["nivel_risco"] == "Alto"].nlargest(3, "pct_atraso_30")
    medios   = df[(df["nivel_risco"] == "Médio") & (df["tendencia"] == "↓ Piora")].head(2)

    for _, row in criticos.iterrows():
        st.markdown(f"""
        <div class="alert-red">
            <div class="alert-title">🔴 Risco Crítico — {row['id_beneficiario'][:24]}...</div>
            <div class="alert-desc">Score {int(row['score_risco'])} · Atraso 30d: {row['pct_atraso_30']*100:.1f}% · DPD médio: {row['dpd_medio']:.0f}d · Tendência: {row['tendencia']}</div>
        </div>
        """, unsafe_allow_html=True)

    for _, row in medios.iterrows():
        st.markdown(f"""
        <div class="alert-yellow">
            <div class="alert-title">🟡 Deterioração Detectada — {row['id_beneficiario'][:24]}...</div>
            <div class="alert-desc">Score {int(row['score_risco'])} · Tendência de piora identificada pelos algoritmos de média móvel e z-score.</div>
        </div>
        """, unsafe_allow_html=True)


def _render_cedente_card(row):
    """Card detalhado de risco ao buscar um cedente específico."""
    from data_loader import get_shap_simulado

    score = int(row["score_risco"])
    nivel = str(row["nivel_risco"])
    circle_cls = "circle-green" if nivel == "Baixo" else ("circle-yellow" if nivel == "Médio" else "circle-red")
    decisao = "✅ APROVAR" if nivel == "Baixo" else ("⚠ REVISAR" if nivel == "Médio" else "❌ NEGAR")
    dec_cor = "#66bb6a" if nivel == "Baixo" else ("#ffc107" if nivel == "Médio" else "#ef5350")

    shap = get_shap_simulado(row)

    bars_html = ""
    for f in shap:
        pct = int(f["magnitude"] * 100)
        cor = "#ef5350" if f["direcao"] == "risco" else "#4caf50"
        v = f["valor"]
        v_str = f"{v:.2f}" if isinstance(v, float) and v < 10 else f"{v:.0f}"
        bars_html += f"""
        <div class="shap-bar-container">
            <div class="shap-label">{f['nome']} = {v_str} {'▲ aumenta risco' if f['direcao']=='risco' else '▼ reduz risco'}</div>
            <div class="shap-bar-bg"><div class="shap-bar-fill {'shap-pos' if f['direcao']=='risco' else 'shap-neg'}" style="width:{pct}%"></div></div>
        </div>"""

    st.markdown(f"""
    <div class="risk-card">
        <div class="risk-card-header">
            <div>
                <div style="font-size:13px; color:#607d9e; margin-bottom:4px;">CARD DE RISCO EXPLICÁVEL</div>
                <div style="font-family:IBM Plex Mono,monospace; font-size:14px; color:#c8d6ea;">{row['id_beneficiario'][:48]}...</div>
                <div style="font-size:13px; color:{dec_cor}; margin-top:8px; font-weight:600;">{decisao}</div>
            </div>
            <div class="risk-score-circle {circle_cls}">{score}</div>
        </div>
        <div style="display:grid; grid-template-columns:1fr 1fr 1fr; gap:12px; margin:16px 0; padding:14px 0; border-top:1px solid #1e3a5f; border-bottom:1px solid #1e3a5f;">
            <div><div style="font-size:11px;color:#607d9e;">Atraso 30d</div><div style="font-family:IBM Plex Mono;font-size:18px;">{row['pct_atraso_30']*100:.1f}%</div></div>
            <div><div style="font-size:11px;color:#607d9e;">DPD Médio</div><div style="font-family:IBM Plex Mono;font-size:18px;">{row['dpd_medio']:.0f}d</div></div>
            <div><div style="font-size:11px;color:#607d9e;">Volume Total</div><div style="font-family:IBM Plex Mono;font-size:18px;">R$ {row['vlr_total']/1e3:.0f}k</div></div>
        </div>
        <div style="font-size:12px; color:#8fadc8; margin-bottom:10px; font-weight:500;">PRINCIPAIS FATORES (SHAP simulado)</div>
        {bars_html}
    </div>
    """, unsafe_allow_html=True)
