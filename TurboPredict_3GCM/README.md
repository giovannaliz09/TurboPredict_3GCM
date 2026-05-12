# ⚡ TurboPredict

> Sistema inteligente de análise de risco de recebíveis para FIDCs

Solução desenvolvida pelo grupo **3GCM** no Challenge Enterprise FIAP em parceria com a **Núclea (2026)**.
O TurboPredict transforma a análise de risco de recebíveis — historicamente manual, lenta e subjetiva — em um processo padronizado, rápido e preditivo, utilizando modelos de Machine Learning e explicabilidade via SHAP.

---

## 🎯 Problema

Análises de risco em FIDCs sofrem com:
- **Lentidão** nas consultas e decisões
- **Subjetividade** dos analistas e critérios inconsistentes
- **Falta de indicadores preditivos** sobre deterioração da carteira
- **Dificuldade** em identificar tendências e anomalias

## 💡 Solução

O TurboPredict entrega um MVP funcional que padroniza o processo end-to-end:

- ⚡ **Busca Turbo** — localização instantânea de cedentes por ID parcial
- 🤖 **Score de Risco automatizado** — XGBoost treinado para PD 30/60/90 dias
- 🔍 **Explicabilidade SHAP** — mostra os principais fatores que influenciam cada decisão
- 📊 **Dashboard interativo** — KPIs, distribuições e tabelas em tempo real
- 🧪 **Laboratório de Simulação** — ajuste de cutoffs e apetite ao risco
- 🚨 **Alertas Preditivos** — semáforo de tendência, média móvel e z-score para anomalias

---

## 🛠️ Stack Técnica

| Camada | Tecnologia |
|--------|-----------|
| Interface | Streamlit |
| Modelos ML | XGBoost (PD 30/60/90) |
| Manipulação de dados | Pandas, NumPy |
| Visualização | Plotly |
| Persistência | CSV / Parquet |

---

## 📂 Estrutura do Projeto

```
turbopredict/
├── app.py                      # Entrypoint do Streamlit
├── data_loader.py              # Carregamento e processamento dos dados
├── calculo_score.py            # Motor de score XGBoost + qualitativo
├── data/                       # Bases da Núclea
│   ├── base_boletos_fiap.csv
│   └── base_auxiliar_fiap.csv
├── models/                     # Modelos XGBoost treinados
│   ├── xgb_pd_30.pkl
│   ├── xgb_pd_60.pkl
│   ├── xgb_pd_90.pkl
│   └── feature_cols.json
├── views/                      # Páginas do app
│   ├── dashboard.py
│   ├── carteira.py
│   ├── simulacao.py
│   └── configuracoes.py
├── turbopredict_modelo_credito_v3.ipynb   # Notebook EDA + treino
└── requirements.txt
```

---

## 🚀 Como Rodar

**1. Instalar dependências:**
```bash
pip install -r requirements.txt
```

**2. Executar o app:**
```bash
streamlit run app.py
```

**3. Abrir no navegador:**
O Streamlit abrirá automaticamente em `http://localhost:8501`

---

## 👥 Equipe 3GCM

| Integrante | Função |
|-----------|--------|
| **Giovani Ribeiro** | EDA, Busca Turbo, Alertas Preditivos e Estabilização do MVP |
| **Carlos** | Feature Engineering e Análise Exploratória |
| **Guilherme** | Modelagem XGBoost (PD 30/60/90) e Validação Técnica |
| **Giovanna** | Frontend, Integração com API e Ajustes de Código |
| **Melissa** | Apresentação, Gerenciamento de Projeto e Demonstração |

---

## 📅 Sprints

| Sprint | Entrega |
|--------|---------|
| Sprint 1 | Contextualização e proposta de solução |
| Sprint 2 | Arquitetura e desenho inicial |
| Sprint 3 | MVP preliminar funcional |
| Sprint 4 | Solução final, vídeo pitch e estabilização |

---

## 📊 Dados

Base anonimizada fornecida pela **Núclea** contendo:
- 7.118 boletos com datas de emissão, vencimento e pagamento
- 4.612 CNPJs com scores de materialidade, liquidez e inadimplência
- Cruzamento via `id_beneficiario` ↔ `id_cnpj`

---

## 🏫 Contexto Acadêmico

Projeto desenvolvido como parte do **Challenge Enterprise FIAP 2026** — disciplina integradora que conecta estudantes a problemas reais de empresas parceiras.

**Empresa parceira:** Núclea
**Curso:** Faculdade de Tecnologia em Análise e Desenvolvimento de Sistemas

---

*Desenvolvido com ⚡ pelo grupo 3GCM*
