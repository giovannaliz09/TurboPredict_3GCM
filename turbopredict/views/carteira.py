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

    # ── Alertas Preditivos — Média Móvel e Z-Score (Giovani) ─────────────────
    st.markdown('<div class="section-title">Alertas Preditivos — Semáforo de Tendência</div>', unsafe_allow_html=True)

    # Calcula média móvel de 7 dias por mês de emissão
    ts_alerta = df_bol.groupby("mes_emissao").agg(
        pct_atraso=("em_atraso", "mean"),
        volume=("vlr_nominal", "sum"),
    ).reset_index().sort_values("mes_emissao")

    ts_alerta["media_movel_7"] = ts_alerta["pct_atraso"].rolling(window=7, min_periods=1).mean()

    # Z-score para detectar spikes
    media = ts_alerta["pct_atraso"].mean()
    std   = ts_alerta["pct_atraso"].std()
    ts_alerta["z_score"] = (ts_alerta["pct_atraso"] - media) / (std + 1e-9)

    # Semáforo do último mês
    ultimo = ts_alerta.iloc[-1]
    penultimo = ts_alerta.iloc[-2] if len(ts_alerta) > 1 else ultimo

    if ultimo["pct_atraso"] > penultimo["pct_atraso"] * 1.1:
        semaforo = "↑ Piora"
        cor_sem = "#ef5350"
        emoji = "🔴"
    elif ultimo["pct_atraso"] < penultimo["pct_atraso"] * 0.9:
        semaforo = "↓ Melhora"
        cor_sem = "#66bb6a"
        emoji = "🟢"
    else:
        semaforo = "→ Estável"
        cor_sem = "#ffc107"
        emoji = "🟡"

    # KPIs do semáforo
    col_s1, col_s2, col_s3 = st.columns(3)
    with col_s1:
        st.markdown(f"""
        <div style='background:#0d1b35; border:1px solid #1e3a5f; border-radius:12px; padding:16px; text-align:center;'>
            <div style='font-size:11px; color:#607d9e; margin-bottom:8px;'>TENDÊNCIA ATUAL</div>
            <div style='font-size:32px;'>{emoji}</div>
            <div style='font-size:16px; color:{cor_sem}; font-weight:600; margin-top:4px;'>{semaforo}</div>
        </div>
        """, unsafe_allow_html=True)
    with col_s2:
        st.markdown(f"""
        <div style='background:#0d1b35; border:1px solid #1e3a5f; border-radius:12px; padding:16px; text-align:center;'>
            <div style='font-size:11px; color:#607d9e; margin-bottom:8px;'>ATRASO ÚLTIMO MÊS</div>
            <div style='font-family:IBM Plex Mono; font-size:28px; color:#c8d6ea;'>{ultimo["pct_atraso"]*100:.1f}%</div>
            <div style='font-size:11px; color:#607d9e; margin-top:4px;'>Média móvel 7m: {ultimo["media_movel_7"]*100:.1f}%</div>
        </div>
        """, unsafe_allow_html=True)
    with col_s3:
        z = ultimo["z_score"]
        cor_z = "#ef5350" if abs(z) > 2 else ("#ffc107" if abs(z) > 1 else "#66bb6a")
        st.markdown(f"""
        <div style='background:#0d1b35; border:1px solid #1e3a5f; border-radius:12px; padding:16px; text-align:center;'>
            <div style='font-size:11px; color:#607d9e; margin-bottom:8px;'>Z-SCORE (ANOMALIA)</div>
            <div style='font-family:IBM Plex Mono; font-size:28px; color:{cor_z};'>{z:.2f}σ</div>
            <div style='font-size:11px; color:#607d9e; margin-top:4px;'>{"⚠ Spike detectado!" if abs(z) > 2 else "Normal"}</div>
        </div>
        """, unsafe_allow_html=True)

    # Gráfico média móvel
    fig_mm = go.Figure()
    fig_mm.add_trace(go.Scatter(
        x=ts_alerta["mes_emissao"],
        y=ts_alerta["pct_atraso"] * 100,
        name="% Atraso Real",
        line=dict(color="#4fc3f7", width=2),
        mode="lines+markers",
        marker=dict(size=5),
    ))
    fig_mm.add_trace(go.Scatter(
        x=ts_alerta["mes_emissao"],
        y=ts_alerta["media_movel_7"] * 100,
        name="Média Móvel 7m",
        line=dict(color="#ffc107", width=2, dash="dash"),
    ))
    fig_mm.update_layout(
        **PLOTLY_DARK,
        height=250,
        yaxis_ticksuffix="%",
        legend=dict(orientation="h", y=1.08, bgcolor="rgba(0,0,0,0)"),
        xaxis_tickangle=-45,
    )
    st.plotly_chart(fig_mm, use_container_width=True)

    # Alertas por z-score
    meses_spike = ts_alerta[ts_alerta["z_score"].abs() > 2].sort_values("z_score", ascending=False)
    if not meses_spike.empty:
        st.markdown("**Spikes Detectados por Z-Score (> 2σ)**")
        for _, r in meses_spike.iterrows():
            cor_alerta = "alert-red" if r["z_score"] > 3 else "alert-yellow"
            nivel_z = "🔴 Anomalia forte" if r["z_score"] > 3 else "🟡 Anomalia moderada"
            st.markdown(f"""
            <div class="{cor_alerta}">
                <div class="alert-title">{nivel_z} — {r["mes_emissao"]}</div>
                <div class="alert-desc">Z-score: {r["z_score"]:.2f}σ · Atraso: {r["pct_atraso"]*100:.1f}% · Média da carteira: {media*100:.1f}%</div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="alert-info">
            <div class="alert-title">✅ Nenhum spike detectado</div>
            <div class="alert-desc">Z-score menor que 2σ em todos os meses.</div>
        </div>
        """, unsafe_allow_html=True)
