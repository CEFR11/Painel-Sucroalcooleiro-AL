# Painel Sucroalcooleiro — Alagoas

Painel interativo de monitoramento da dependência do setor sucroalcooleiro e da diversificação econômica dos 102 municípios de Alagoas, com dados da RAIS (2018–2022) e do Novo CAGED (2023–2026).

**Acesse em:** [painel-sucroalcooleiro-al.streamlit.app](https://painel-sucroalcooleiro-al-ginjdrc5ntkx25h5md6vuk.streamlit.app/)

## Contexto

Este painel é parte do trabalho:

> **Análise Quantitativa da Estrutura Produtiva e do Mercado de Trabalho Formal em Alagoas: Dependência da Cana-de-Açúcar nos Microdados da RAIS e do Novo CAGED (2018–2026)**
>
> José Pedro de Lira Barbosa, Cleverson Alves de Almeida, Carlos Eduardo Felix Ramos
>
> Curso de Sistemas de Informação — UFAL, Unidade Educacional Penedo / Campus Arapiraca

## Funcionalidades

| Aba | Descrição |
|-----|-----------|
| **Visão Estadual** | Scatter HHI × % Cana com os 102 municípios, tabela ordenável com todos os indicadores |
| **Ficha do Município** | Perfil individual: métricas, gráfico de evolução do emprego (RAIS + CAGED em séries separadas), tabela anual |
| **Comparador** | Comparação lado a lado de dois municípios |
| **Metodologia** | Fontes, quebra de série, indicadores, classificação e limitações |

## Dados

- `base_jasp_painel_completo_2018_2026.csv` — 918 linhas (102 municípios × 9 anos), com vínculos, indicadores de concentração e movimentações CAGED
- `base_jasp_municipios_consolidado_2018_2026.csv` — 102 linhas, uma por município, com valores consolidados de 2022 e saldos CAGED 2023–2026

**Fontes primárias:** RAIS via Base dos Dados / BigQuery; Novo CAGED via portal gov.br (MTE).

> ⚠️ Os níveis RAIS e CAGED **não são comparáveis** — a RAIS inclui estatutários, o Novo CAGED só cobre CLT. O painel nunca conecta as duas séries. 2026 é parcial (jan–set).

## Como rodar localmente

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Licença

Dados públicos do Ministério do Trabalho e Emprego. Código do painel disponível para fins acadêmicos.
