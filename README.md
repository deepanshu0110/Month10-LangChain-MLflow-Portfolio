# Month 10 — LangChain + MLflow + Prompt Engineering Portfolio

**Student:** Deepanshu Garg | **GitHub:** [deepanshu0110](https://github.com/deepanshu0110)
**Roadmap:** Month 10 of 12 — Data Science & AI Self-Study Curriculum
**Goal:** High-value freelance practice + MSc Data Science (TU/e, September 2027)

---

## What This Month Covers

Month 10 bridges classical ML (Months 6–7) and production deployment (Month 8) with the **LLM application layer** — the stack that commands premium freelance rates in 2025–26.

| Week | Days | Focus | Key Skills |
|------|------|-------|-----------|
| W1 | 169–172 | LangChain Core | Chains, Memory, Agents, LCEL, RunnableParallel |
| W2 | 173–175 | MLflow | Experiment tracking, Model registry, Artifact logging |
| W3 | 176–178 | Ollama + Evidently | Local LLMs on Colab T4, Data drift monitoring |
| W4 | 179–180 | Prompt Engineering + Capstone | Structured prompting, End-to-end pipeline |

---

## Tech Stack

| Layer | Tools |
|-------|-------|
| LLM Backend | Groq free API — `llama-3.1-8b-instant` |
| LLM Framework | `LangChain 0.2.16` · `langchain-groq 0.1.9` · `langchain-community 0.2.16` |
| Local LLM (learning) | Ollama on Google Colab T4 |
| Vector Search | FAISS (local) |
| ML Tracking | MLflow |
| Drift Monitoring | Evidently |
| Environment | Google Colab (primary) · VS Code (scripts) |
| Data | ReviewPulse India — 600 rows, seed=155 |

---

## Dataset — ReviewPulse India

Synthetic freelancer review dataset used consistently across Months 9–10.

| Column | Type | Description |
|--------|------|-------------|
| review_id | int | Unique review identifier (1–600) |
| freelancer_id | int | Freelancer ID (1001–1200) |
| review_text | str | One of 10 standardised review texts |
| sentiment | str | positive / negative / neutral (44.5% / 25.5% / 30%) |
| rating | int | 1–5 stars (correlated with sentiment) |
| hired_again | str | Yes / No (35.67% Yes) |
| review_date | str | 2023-01-01 onwards, one per day |

**Key stats (seed=155):** 266 negative · 154 positive · 180 neutral · avg rating 2.75 · hired-again 35.67%

---

## Month 10 Scorecard

| Day | Topic | Score | Status |
|-----|-------|-------|--------|
| 169 | LangChain Chains & Memory | 80/80 + 10★ | ✅ Perfect |
| 170 | LangChain Tools & Agents | 80/80 + 10★ | ✅ Perfect |
| 171 | Document Loaders + LCEL | 80/80 + 10★ | ✅ Perfect |
| 172 | LangChain Capstone | 90/90 + 10★ | ✅ Perfect |
| 173 | MLflow Experiment Tracking | — | 🔜 |
| 174 | MLflow Model Registry | — | 🔜 |
| 175 | MLflow Capstone | — | 🔜 |
| 176 | Ollama on Colab | — | 🔜 |
| 177 | Evidently Drift Monitoring — Part 1 | — | 🔜 |
| 178 | Evidently Drift Monitoring — Part 2 | — | 🔜 |
| 179 | Prompt Engineering | — | 🔜 |
| 180 | Month 10 Capstone | — | 🔜 |
| **Running Total** | | **330/330 + 40★** | **All perfect** |

---

## Key Concepts Demonstrated

### LangChain (Days 169–172)
- **LCEL** — composable chains using the `|` pipe operator
- **RunnableParallel** — run N chains on the same input simultaneously
- **RunnableLambda / RunnablePassthrough** — wrap Python functions as chain steps
- **ReAct Agent** — `create_react_agent` + `AgentExecutor` with custom `@tool` functions
- **Memory** — `ConversationBufferMemory` for multi-turn dialogue context
- **CSVLoader** — convert tabular data into LangChain `Document` objects
- **`.batch()`** — process N inputs in one parallel call

### NRA Framework (applied to every analysis output)
Every insight in this portfolio follows the **Number + Reason + Action** standard:
- **Number** — exact value read from printed cell output, never estimated
- **Reason** — causal mechanism (WHY, not WHAT)
- **Action** — specific, committed, measurable intervention — no hedging language

---

## Repository Structure

```
Month10-LangChain-MLflow-Portfolio/
│
├── Day169_LangChain_Chains_Memory.ipynb
├── Day170_LangChain_Tools_Agents.ipynb
├── Day171_Document_Loaders_LCEL.ipynb
├── Day172_LangChain_Capstone.ipynb
│
├── Day173_MLflow_Tracking.ipynb          ← coming
├── Day174_MLflow_Registry.ipynb          ← coming
├── Day175_MLflow_Capstone.ipynb          ← coming
│
├── Day176_Ollama_Colab.ipynb             ← coming
├── Day177_Evidently_Drift_P1.ipynb       ← coming
├── Day178_Evidently_Drift_P2.ipynb       ← coming
│
├── Day179_Prompt_Engineering.ipynb       ← coming
├── Day180_Month10_Capstone.ipynb         ← coming
│
├── reviewpulse_india.csv                 ← shared dataset (seed=155)
├── auto_sync_month10.py                  ← auto-push watchdog script
└── README.md
```

---

## Previous Months

| Month | Repo | Topic | Score |
|-------|------|-------|-------|
| M1 | [excel-data-analytics](https://github.com/deepanshu0110/excel-data-analytics) | Excel | ✅ Complete |
| M2 | [Month2-SQL-Portfolio](https://github.com/deepanshu0110/Month2-SQL-Portfolio) | SQL | ✅ 119/120 |
| M3 | [Month3-Python-Portfolio](https://github.com/deepanshu0110/Month3-Python-Portfolio) | Python / Pandas | ✅ Complete |
| M4 | [Month4-PowerBI-Tableau-Portfolio](https://github.com/deepanshu0110/Month4-PowerBI-Tableau-Portfolio) | Power BI + Tableau | ✅ Complete |
| M5 | [Month5-BI-Upwork-Portfolio](https://github.com/deepanshu0110/Month5-BI-Upwork-Portfolio) | BI + Freelance | ✅ Complete |
| M6–7 | [Month6-and-7-Stats-ML-Portfolio](https://github.com/deepanshu0110/Month6-and-7-Stats-ML-Portfolio) | Stats + ML | ✅ 1659+/1660 |
| M8 | [Month8-Streamlit-FastAPI-Portfolio](https://github.com/deepanshu0110/Month8-Streamlit-FastAPI-Portfolio) | Streamlit + FastAPI | ✅ 1120/1120+140★ |
| M9 | [Month9-NLP-DeepLearning-Portfolio](https://github.com/deepanshu0110/Month9-NLP-DeepLearning-Portfolio) | NLP + Deep Learning | ✅ 1150/1150+140★ |
| **M10** | **← you are here** | **LangChain + MLflow** | **330/330+40★ running** |

---

*Auto-synced via `auto_sync_month10.py` — last updated by watchdog*
