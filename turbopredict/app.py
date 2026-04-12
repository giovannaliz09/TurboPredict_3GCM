import streamlit as st
from data_loader import data_files_ok, save_uploaded_files

st.set_page_config(
    page_title="TurboPredict",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:wght@300;400;500;600&display=swap');
html, body, [class*="css"] { font-family: 'IBM Plex Sans', sans-serif; }
section[data-testid="stSidebar"] { background:#0a0f1e; border-right:1px solid #1e2d4a; }
section[data-testid="stSidebar"] * { color:#c8d6ea !important; }
.turbo-header { background:linear-gradient(135deg,#0a0f1e,#0d1b35,#0a1628); border:1px solid #1e3a5f; border-radius:12px; padding:20px 28px; margin-bottom:24px; }
.turbo-logo { font-family:'IBM Plex Mono',monospace; font-size:26px; font-weight:500; color:#4fc3f7; letter-spacing:-1px; }
.turbo-subtitle { font-size:13px; color:#607d9e; margin-top:2px; }
.score-badge { display:inline-block; padding:3px 10px; border-radius:20px; font-size:12px; font-weight:500; font-family:'IBM Plex Mono',monospace; }
.badge-green  { background:#1b3a1f; color:#66bb6a; border:1px solid #2d5c31; }
.badge-yellow { background:#3a2e0a; color:#ffca28; border:1px solid #5c4a14; }
.badge-red    { background:#3a0f0f; color:#ef5350; border:1px solid #5c1a1a; }
.risk-card { background:#0d1b35; border:1px solid #1e3a5f; border-radius:12px; padding:20px; margin-bottom:16px; }
.shap-bar-container { margin:8px 0; }
.shap-label { font-size:12px; color:#8fadc8; margin-bottom:3px; }
.shap-bar-bg { background:#132035; border-radius:4px; height:8px; overflow:hidden; }
.shap-bar-fill { height:100%; border-radius:4px; }
.shap-pos { background:#ef5350; }
.shap-neg { background:#4caf50; }
.alert-red    { background:#2d0f0f; border:1px solid #5c1a1a; border-left:4px solid #ef5350; border-radius:8px; padding:12px 16px; margin-bottom:10px; }
.alert-yellow { background:#2d1f00; border:1px solid #5c3a00; border-left:4px solid #ffc107; border-radius:8px; padding:12px 16px; margin-bottom:10px; }
.alert-info   { background:#0d1f35; border:1px solid #1e3a5f; border-left:4px solid #4fc3f7; border-radius:8px; padding:12px 16px; margin-bottom:10px; }
.alert-title  { font-size:13px; font-weight:600; margin-bottom:3px; }
.alert-desc   { font-size:12px; color:#8fadc8; }
.section-title { font-size:13px; font-weight:600; color:#4fc3f7; text-transform:uppercase; letter-spacing:.1em; margin:20px 0 12px; display:flex; align-items:center; gap:8px; }
.section-title::after { content:''; flex:1; height:1px; background:#1e3a5f; }
.tend-up   { color:#ef5350; font-weight:600; }
.tend-down { color:#4caf50; font-weight:600; }
.tend-stab { color:#ffc107; font-weight:600; }
div[data-testid="stToolbar"] { display:none; }
button[data-testid="baseButton-headerNoPadding"] { display:none !important; }
</style>
""", unsafe_allow_html=True)

# ── Verificação de dados (antes de qualquer cache) ────────────────────────────
if not data_files_ok():
    st.markdown("""
    <div class="turbo-header">
        <div class="turbo-logo">⚡ TurboPredict</div>
        <div class="turbo-subtitle">Configuração inicial — faça upload das bases de dados</div>
    </div>
    """, unsafe_allow_html=True)

    st.info(
        "📂 Arquivos não encontrados em `turbopredict/data/`.\n\n"
        "**Opção 1 (recomendada):** copie os dois CSVs para a pasta `data/` e reinicie o app.\n\n"
        "**Opção 2:** faça upload direto abaixo."
    )

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**base_boletos_fiap.csv**")
        f_bol = st.file_uploader("boletos", type="csv", key="bol", label_visibility="collapsed")
    with col2:
        st.markdown("**base_auxiliar_fiap.csv**")
        f_aux = st.file_uploader("auxiliar", type="csv", key="aux", label_visibility="collapsed")

    if f_bol and f_aux:
        with st.spinner("Salvando arquivos..."):
            save_uploaded_files(f_bol.read(), f_aux.read())
        st.success("Arquivos salvos! Recarregando...")
        st.rerun()
    else:
        st.stop()

# ── Cache dos dados ───────────────────────────────────────────────────────────
@st.cache_data(show_spinner="Carregando dados...")
def _cached_load():
    from data_loader import load_data
    return load_data()

_cached_load()  # aquece o cache

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center;padding:20px 0 30px;'>
        <div style='font-family:IBM Plex Mono,monospace;font-size:22px;color:#4fc3f7;font-weight:500;'>⚡ TurboPredict</div>
        <div style='font-size:11px;color:#607d9e;margin-top:4px;'>Risk Intelligence v0.1 MVP</div>
    </div>
    """, unsafe_allow_html=True)

    pagina = st.radio(
        "nav",
        ["🏠  Dashboard", "📂  Carteira", "🧪  Simulação", "⚙️  Configurações"],
        label_visibility="collapsed",
    )
    st.markdown("<hr style='border-color:#1e3a5f;margin:20px 0;'>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:11px;color:#607d9e;padding:0 4px;'>Dados: Núclea · Challenge FIAP 2025<br>Equipe 3GCM · Sprint 3 MVP</div>", unsafe_allow_html=True)

# ── Roteamento ────────────────────────────────────────────────────────────────
if "Dashboard" in pagina:
    from views import dashboard
    dashboard.render(_cached_load)
elif "Carteira" in pagina:
    from views import carteira
    carteira.render(_cached_load)
elif "Simulação" in pagina:
    from views import simulacao
    simulacao.render(_cached_load)
else:
    from views import configuracoes
    configuracoes.render(_cached_load)