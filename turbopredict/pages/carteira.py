"""pages/carteira.py — Monitoramento estratégico da carteira."""
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
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
            <div class="turbo-logo">📂 Monitoramento de Carteira</div>
            <div class="turbo-subtitle">Análise consolidada e saúde dos ativos · {n} cedentes ativos</div>
        </div>
    </div>
    """.replace("{n}", str(len(df))), unsafe_allow_html=True)

    # ── KPIs ─────────────────────────────────────────────────────────────────
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.metric("Exposição Total", f"R$ {df['vlr_total'].sum()/1e6:.1f}M")
    with k2:
        inad = df_bol[df_bol["dpd"] >= 30]["vlr_nominal"].sum() / df_bol["vlr_nominal"].sum()
        st.metric("Inadimplência D+30", f"{inad*100:.1f}%", f"{inad*100 - 2.5:.1f}pp vs meta")
    with k3:
        st.metric("Ticket Médio", f"R$ {df_bol['vlr_nominal'].mean():,.0f}")
    with k4:
        st.metric("Cedentes em Alerta", f"{(df['nivel_risco']=='Alto').sum()} críticos")

    st.markdown("---")
    col_esq, col_dir = st.columns([2, 3])

    # ── Distribuição por score ────────────────────────────────────────────────
    with col_esq:
        st.markdown('<div class="section-title">Distribuição por Score</div>', unsafe_allow_html=True)
        contagem = df["nivel_risco"].value_counts()
        cores_pizza = {"Baixo": "#66bb6a", "Médio": "#ffc107", "Alto": "#ef5350"}
        fig_pizza = go.Figure(go.Pie(
            labels=contagem.index,
            values=contagem.values,
            hole=0.55,
            marker_colors=[cores_pizza.get(l, "#8fadc8") for l in contagem.index],
            textinfo="percent+label",
            textfont=dict(size=12, family="IBM Plex Mono"),
        ))
        fig_pizza.update_layout(**PLOTLY_DARK, height=260, showlegend=False)
        st.plotly_chart(fig_pizza, use_container_width=True)

        st.markdown('<div class="section-title">Volume por Nível de Risco</div>', unsafe_allow_html=True)
        vol_risco = df.groupby("nivel_risco")["vlr_total"].sum().reindex(["Alto", "Médio", "Baixo"])
        fig_vol = go.Figure(go.Bar(
            x=["Alto", "Médio", "Baixo"],
            y=vol_risco.values / 1e6,
            marker_color=["#ef5350", "#ffc107", "#66bb6a"],
        ))
        fig_vol.update_layout(**PLOTLY_DARK, height=200, showlegend=False,
                              yaxis_ticksuffix="M", bargap=0.3)
        st.plotly_chart(fig_vol, use_container_width=True)

    # ── Mapa de calor Concentração × Risco ───────────────────────────────────
    with col_dir:
        st.markdown('<div class="section-title">Mapa de Calor — Concentração × Score</div>', unsafe_allow_html=True)

        df_hm = df.dropna(subset=["concentracao_top1", "score_risco"]).copy()
        df_hm["conc_bin"] = pd.cut(df_hm["concentracao_top1"], bins=5,
                                    labels=["Muito Baixa","Baixa","Média","Alta","Muito Alta"])
        df_hm["score_bin"] = pd.cut(df_hm["score_risco"], bins=5,
                                     labels=["0-200","200-400","400-600","600-800","800-1000"])

        pivot = df_hm.groupby(["conc_bin","score_bin"]).size().unstack(fill_value=0)

        fig_hm = go.Figure(go.Heatmap(
            z=pivot.values,
            x=list(pivot.columns),
            y=list(pivot.index),
            colorscale=[[0,"#0d1b35"],[0.3,"#1e3a5f"],[0.6,"#ffc107"],[1,"#ef5350"]],
            showscale=True,
            texttemplate="%{z}",
            textfont=dict(size=12, family="IBM Plex Mono"),
        ))
        fig_hm.update_layout(
            **PLOTLY_DARK, height=300,
            xaxis_title="Score de Risco",
            yaxis_title="Concentração Top-1 Pagador",
        )
        st.plotly_chart(fig_hm, use_container_width=True)

        # Top 5 cedentes por exposição
        st.markdown('<div class="section-title">Top 5 Cedentes por Exposição</div>', unsafe_allow_html=True)
        top5 = df.nlargest(5, "vlr_total")[["id_beneficiario","vlr_total","nivel_risco","pct_atraso_30","tendencia"]]

        rows = ""
        for _, r in top5.iterrows():
            nivel = str(r["nivel_risco"])
            badge_cls = "badge-green" if nivel == "Baixo" else ("badge-yellow" if nivel == "Médio" else "badge-red")
            tend = r["tendencia"]
            tend_cls = "tend-up" if "Piora" in tend else ("tend-down" if "Melhora" in tend else "tend-stab")
            rows += f"""
            <tr style='border-bottom:1px solid #132035;'>
              <td style='padding:8px 12px; font-family:IBM Plex Mono,monospace; font-size:11px; color:#8fadc8;'>{r['id_beneficiario'][:20]}...</td>
              <td style='padding:8px 12px; font-size:13px;'>R$ {r['vlr_total']/1e3:,.0f}k</td>
              <td style='padding:8px 12px;'><span class='score-badge {badge_cls}'>{nivel}</span></td>
              <td style='padding:8px 12px; font-size:13px;'>{r['pct_atraso_30']*100:.1f}%</td>
              <td style='padding:8px 12px;'><span class='{tend_cls}'>{tend}</span></td>
            </tr>"""

        st.markdown(f"""
        <table style='width:100%; border-collapse:collapse; background:#0d1b35; border-radius:10px; border:1px solid #1e3a5f;'>
          <thead>
            <tr style='background:#132035;'>
              <th style='padding:8px 12px; text-align:left; font-size:11px; color:#607d9e;'>CEDENTE</th>
              <th style='padding:8px 12px; text-align:left; font-size:11px; color:#607d9e;'>VOLUME</th>
              <th style='padding:8px 12px; text-align:left; font-size:11px; color:#607d9e;'>RISCO</th>
              <th style='padding:8px 12px; text-align:left; font-size:11px; color:#607d9e;'>ATRASO 30D</th>
              <th style='padding:8px 12px; text-align:left; font-size:11px; color:#607d9e;'>TENDÊNCIA</th>
            </tr>
          </thead>
          <tbody>{rows}</tbody>
        </table>
        """, unsafe_allow_html=True)

    # ── Alertas críticos da carteira ─────────────────────────────────────────
    st.markdown('<div class="section-title">Alertas Críticos da Carteira</div>', unsafe_allow_html=True)

    col_a1, col_a2 = st.columns(2)

    with col_a1:
        # Cedentes com tendência de piora
        em_piora = df[df["tendencia"] == "↓ Piora"].nlargest(3, "vlr_total")
        st.markdown("**Deterioração Detectada por Média Móvel**")
        for _, r in em_piora.iterrows():
            st.markdown(f"""
            <div class="alert-yellow">
                <div class="alert-title">🟡 {r['id_beneficiario'][:28]}...</div>
                <div class="alert-desc">Vol: R$ {r['vlr_total']/1e3:.0f}k · Atraso 30d: {r['pct_atraso_30']*100:.1f}% · Score: {int(r['score_risco'])}</div>
            </div>
            """, unsafe_allow_html=True)

    with col_a2:
        # Alta concentração
        alta_conc = df[df["concentracao_top1"] > 0.7].nlargest(3, "vlr_total")
        st.markdown("**Alta Concentração em Único Pagador (>70%)**")
        for _, r in alta_conc.iterrows():
            st.markdown(f"""
            <div class="alert-red">
                <div class="alert-title">🔴 {r['id_beneficiario'][:28]}...</div>
                <div class="alert-desc">Concentração: {r['concentracao_top1']*100:.0f}% em único pagador · Vol: R$ {r['vlr_total']/1e3:.0f}k</div>
            </div>
            """, unsafe_allow_html=True)

    # ── Evolução de inadimplência por espécie ─────────────────────────────────
    st.markdown('<div class="section-title">Inadimplência por Tipo de Espécie</div>', unsafe_allow_html=True)
    by_esp = df_bol.groupby("tipo_especie").agg(
        pct_atraso=("atraso_30", "mean"),
        volume=("vlr_nominal", "sum"),
    ).reset_index().sort_values("pct_atraso", ascending=True)

    fig_esp = go.Figure(go.Bar(
        x=by_esp["pct_atraso"] * 100,
        y=by_esp["tipo_especie"].str[:30],
        orientation="h",
        marker_color="#4fc3f7",
        marker_line_color="#1e3a5f",
        marker_line_width=1,
    ))
    fig_esp.update_layout(**PLOTLY_DARK, height=200, showlegend=False,
                          xaxis_ticksuffix="%", bargap=0.3)
    st.plotly_chart(fig_esp, use_container_width=True)
