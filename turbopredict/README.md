# TurboPredict — MVP Sprint 3
## Challenge FIAP 2025 · Núclea · Equipe 3GCM

Dashboard de análise de risco de recebíveis com IA explicável (XGBoost + SHAP).

---

## Instalação

```bash
# 1. Clone ou baixe este repositório
cd turbopredict/

# 2. (Recomendado) Crie um ambiente virtual
python -m venv .venv
source .venv/bin/activate      # Linux/Mac
.venv\Scripts\activate         # Windows

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Coloque as bases na pasta data/
mkdir data/
cp /caminho/para/base_boletos_fiap.csv  data/
cp /caminho/para/base_auxiliar_fiap.csv data/

# 5. Execute o app
streamlit run app.py
```

O app abrirá em http://localhost:8501

---

## Estrutura do Projeto

```
turbopredict/
├── app.py               # Entrada principal + layout + CSS global
├── data_loader.py       # Carregamento, feature engineering e score sintético
├── requirements.txt
├── data/
│   ├── base_boletos_fiap.csv
│   └── base_auxiliar_fiap.csv
└── pages/
    ├── dashboard.py     # KPIs, tabela de cedentes, busca turbo, alertas
    ├── carteira.py      # Mapa de calor, distribuição de risco, top cedentes
    ├── simulacao.py     # Laboratório de cutoff, matriz financeira, z-score
    └── configuracoes.py # Parâmetros, API docs, log de auditoria
```

---

## Funcionalidades do MVP

| Funcionalidade | Status | Arquivo |
|---|---|---|
| Busca Turbo por ID de cedente | ✅ | dashboard.py |
| Score de risco 0–1000 | ✅ | data_loader.py |
| Card de risco explicável (SHAP simulado) | ✅ | dashboard.py |
| Tabela de cedentes com filtros | ✅ | dashboard.py |
| Semáforo de tendência (↑→↓) | ✅ | data_loader.py |
| Alertas preditivos por nível | ✅ | dashboard.py / carteira.py |
| Mapa de calor concentração × risco | ✅ | carteira.py |
| Slider de cutoff interativo | ✅ | simulacao.py |
| Matriz de confusão financeira | ✅ | simulacao.py |
| Detecção de anomalias (z-score) | ✅ | simulacao.py |
| Trilha de auditoria | ✅ | configuracoes.py |
| Log de decisões exportável (CSV) | ✅ | configuracoes.py |

---

## Próximos Passos (Sprint 4)

- [ ] Treinar XGBoost real com labels PD_30/60/90 e substituir score sintético
- [ ] Calcular SHAP values reais via `shap.TreeExplainer`
- [ ] Expor endpoints FastAPI (`/score`, `/search`, `/alerts`)
- [ ] Conectar Kafka para alertas em tempo real
- [ ] Deploy em container Docker

---

## Equipe 3GCM

| Membro | RM | Responsabilidade |
|---|---|---|
| Carlos Eduardo da Silva Nascimento | 568340 | EDA + Feature Engineering |
| Giovani Ribeiro Brisola | 566813 | API FastAPI + Arquitetura |
| Giovanna Liz Takamori Silva Souza | 567788 | Frontend / Streamlit |
| Guilherme Dias de Souza Matunaga | 568147 | Modelo ML + SHAP |
| Melissa Teixeira Gomes | 566713 | Apresentação + Gerenciamento |
