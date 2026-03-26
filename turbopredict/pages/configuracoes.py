"""pages/configuracoes.py — Configurações globais e auditoria."""
import streamlit as st
import pandas as pd
import sys, pathlib

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
from data_loader import load_data


def render(loader=None):
    from data_loader import load_data as _ld
    df, df_bol = (loader or _ld)()

    st.markdown("""
    <div class="turbo-header">
        <div>
            <div class="turbo-logo">⚙️ Configurações</div>
            <div class="turbo-subtitle">Parâmetros globais, integrações e trilha de auditoria</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["🎛 Parâmetros de Risco", "🔗 API & Integrações", "📋 Log de Auditoria"])

    with tab1:
        st.markdown('<div class="section-title">Parâmetros Globais de Risco</div>', unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            cutoff_global = st.slider("Threshold padrão (Cutoff inicial)", 100, 900, 400, step=10)
            st.caption("Aplicado automaticamente em novas sessões de análise")

            politica = st.selectbox("Política de bloqueio automático", [
                "Moderada — Bloqueia Score E",
                "Conservadora — Bloqueia Score D e E",
                "Agressiva — Apenas alerta",
            ])

            auto_revisao = st.toggle("Auto-Revisão por IA", value=True)
            if auto_revisao:
                st.info("TurboPredict aprovará automaticamente casos de Score A e B sem intervenção humana.")

        with col2:
            st.markdown("""
            <div class='risk-card'>
                <div style='font-size:12px;color:#607d9e;margin-bottom:12px;'>ESCALA DE SCORES</div>
                <div style='display:flex;flex-direction:column;gap:8px;'>
                    <div style='display:flex;justify-content:space-between;'>
                        <span style='color:#66bb6a;font-family:IBM Plex Mono;'>800–1000</span>
                        <span style='color:#8fadc8;font-size:12px;'>Score A — Baixo risco → APROVAR</span>
                    </div>
                    <div style='display:flex;justify-content:space-between;'>
                        <span style='color:#81c784;font-family:IBM Plex Mono;'>600–800</span>
                        <span style='color:#8fadc8;font-size:12px;'>Score B — Risco moderado baixo</span>
                    </div>
                    <div style='display:flex;justify-content:space-between;'>
                        <span style='color:#ffc107;font-family:IBM Plex Mono;'>400–600</span>
                        <span style='color:#8fadc8;font-size:12px;'>Score C — Médio → REVISAR</span>
                    </div>
                    <div style='display:flex;justify-content:space-between;'>
                        <span style='color:#ff8a65;font-family:IBM Plex Mono;'>200–400</span>
                        <span style='color:#8fadc8;font-size:12px;'>Score D — Alto risco</span>
                    </div>
                    <div style='display:flex;justify-content:space-between;'>
                        <span style='color:#ef5350;font-family:IBM Plex Mono;'>0–200</span>
                        <span style='color:#8fadc8;font-size:12px;'>Score E — Crítico → NEGAR</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        if st.button("💾 Salvar Parâmetros"):
            st.success(f"Parâmetros salvos: Cutoff={cutoff_global} · Política={politica[:20]}...")

    with tab2:
        st.markdown('<div class="section-title">Endpoints da API TurboPredict</div>', unsafe_allow_html=True)

        st.code("""
# Busca Turbo — GET /api/v1/search
GET /api/v1/search?q={id_beneficiario}
→ Retorna dados indexados em Parquet (latência sub-50ms)

# Score de Risco — GET /api/v1/score/{id}
GET /api/v1/score/{id_beneficiario}
→ { "score": 742, "nivel": "Baixo", "pd30": 0.04,
    "decisao": "Aprovar",
    "motivos": ["Liquidez alta (0.82)", "DPD médio baixo (2d)", "Score materialidade 890"] }

# Alertas — GET /api/v1/alerts
GET /api/v1/alerts?nivel=vermelho
→ Lista de alertas ativos com z-score e tendência

# Webhook de risco (POST)
POST /api/v1/webhooks/risk-events
→ Recebe eventos de deterioração em tempo real (via Kafka)
        """, language="bash")

        st.markdown('<div class="section-title">Chave de API</div>', unsafe_allow_html=True)
        col_k1, col_k2 = st.columns([4, 1])
        with col_k1:
            st.text_input("Chave de API (produção)", value="tp_live_3GCM_••••••••••••••••", disabled=True)
        with col_k2:
            st.button("📋 Copiar")

        st.markdown('<div class="section-title">Webhook URL</div>', unsafe_allow_html=True)
        st.text_input("Endpoint de recebimento", placeholder="https://sua-empresa.com/webhooks/turbopredict")

    with tab3:
        st.markdown('<div class="section-title">Trilha de Auditoria</div>', unsafe_allow_html=True)
        st.caption("Registro imutável de todas as decisões tomadas pelo sistema")

        # Log simulado baseado nos dados reais
        import random
        random.seed(42)
        sample = df.sample(min(20, len(df)), random_state=42)

        log_rows = []
        for i, (_, r) in enumerate(sample.iterrows()):
            decisao = "APROVAR" if r["nivel_risco"] == "Baixo" else ("REVISAR" if r["nivel_risco"] == "Médio" else "NEGAR")
            cor = "🟢" if decisao == "APROVAR" else ("🟡" if decisao == "REVISAR" else "🔴")
            log_rows.append({
                "Timestamp": f"2024-{11+i//10:02d}-{(i%28)+1:02d} {(8+i%12):02d}:{(i*7%60):02d}",
                "Cedente": r["id_beneficiario"][:24] + "...",
                "Score": int(r["score_risco"]),
                "Decisão": f"{cor} {decisao}",
                "Modelo": "XGBoost v2.4 (MVP)",
                "Analista": "Auto" if r["nivel_risco"] != "Médio" else "Ana Silva",
            })

        df_log = pd.DataFrame(log_rows)
        st.dataframe(df_log, use_container_width=True, hide_index=True)

        if st.button("📥 Exportar Log CSV"):
            csv = df_log.to_csv(index=False)
            st.download_button("⬇ Download", csv, "auditoria_turbopredict.csv", "text/csv")
