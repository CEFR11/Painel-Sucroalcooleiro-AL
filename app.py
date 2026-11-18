import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Painel Sucroalcooleiro — Alagoas", layout="wide", page_icon="🏭")

# ── CSS ──
st.markdown("""
<style>
    .metric-card {
        background: rgba(128,128,128,0.1); border-radius: 10px; padding: 18px; text-align: center;
        border: 1px solid rgba(128,128,128,0.25); margin-bottom: 10px;
    }
    .metric-card h3 { margin: 0; font-size: 14px; color: #888; }
    .metric-card p { margin: 4px 0 0; font-size: 28px; font-weight: 700; color: #1a1a2e; }
    @media (prefers-color-scheme: dark) {
        .metric-card p { color: #f0f0f0; }
        .metric-card h3 { color: #aaa; }
    }
    [data-theme="dark"] .metric-card p { color: #f0f0f0; }
    [data-theme="dark"] .metric-card h3 { color: #aaa; }
    .aviso { background: #fff3cd; border: 1px solid #ffc107; border-radius: 8px; padding: 12px; font-size: 13px; }
    .polo-tag { display: inline-block; padding: 3px 10px; border-radius: 12px; font-size: 12px; font-weight: 600; }
    .polo-polo { background: #555; color: #fff; }
    .polo-baixa { background: #1b9e77; color: #fff; }
</style>
""", unsafe_allow_html=True)

VERDE = "#1b9e77"
CINZA = "#555555"
CANA_CNAES = "0113-0 (Cultivo de cana), 1071-6 (Fabricação de açúcar), 1931-4 (Fabricação de álcool)"

@st.cache_data
def load_data():
    painel = pd.read_csv("base_jasp_painel_completo_2018_2026.csv")
    consolidado = pd.read_csv("base_jasp_municipios_consolidado_2018_2026.csv")
    return painel, consolidado

painel, consolidado = load_data()

def fmt(v, decimals=1, suffix="", prefix=""):
    if pd.isna(v):
        return "Dado indisponível"
    if isinstance(v, float):
        return f"{prefix}{v:,.{decimals}f}{suffix}".replace(",", "X").replace(".", ",").replace("X", ".")
    return f"{prefix}{v}{suffix}"

def fmt_int(v):
    if pd.isna(v):
        return "Dado indisponível"
    return f"{int(v):,}".replace(",", ".")

def grupo_label(g):
    if g == "Polo_Sucroalcooleiro":
        return '<span class="polo-tag polo-polo">Polo Sucroalcooleiro</span>'
    return '<span class="polo-tag polo-baixa">Baixa Dependência</span>'

def grupo_cor(g):
    return CINZA if g == "Polo_Sucroalcooleiro" else VERDE

def metric_card(titulo, valor):
    return f'<div class="metric-card"><h3>{titulo}</h3><p>{valor}</p></div>'

# ── Gráfico de evolução emprego com quebra de série ──
def grafico_evolucao(mun_painel, nome):
    rais = mun_painel[mun_painel["fonte_dados"] == "RAIS_2018_2022"].sort_values("ano")
    caged = mun_painel[mun_painel["fonte_dados"] == "Novo_CAGED_2023_2026"].sort_values("ano")

    fig = go.Figure()

    # RAIS trace (solid)
    if not rais.empty:
        y_rais = rais["estoque_unificado"]
        fig.add_trace(go.Scatter(
            x=rais["ano"], y=y_rais, mode="lines+markers", name="RAIS (2018–2022)",
            line=dict(color="#2c7fb8", width=2.5), marker=dict(size=7, color="#2c7fb8"),
            hovertemplate="%{x}: %{y:,.0f} vínculos<extra>RAIS</extra>"
        ))

    # CAGED trace (dashed)
    if not caged.empty:
        y_vals = []
        markers_color = []
        markers_symbol = []
        for _, r in caged.iterrows():
            val = r["estoque_final_caged"] if pd.notna(r["estoque_final_caged"]) else r["estoque_unificado"]
            y_vals.append(val if pd.notna(val) else None)
            if r["ano"] == 2026:
                markers_color.append("white")
                markers_symbol.append("circle-open")
            else:
                markers_color.append("#e34a33")
                markers_symbol.append("circle")
        fig.add_trace(go.Scatter(
            x=caged["ano"], y=y_vals, mode="lines+markers", name="CAGED (2023–2026)",
            line=dict(color="#e34a33", width=2.5, dash="dash"),
            marker=dict(size=8, color=markers_color, symbol=markers_symbol,
                        line=dict(color="#e34a33", width=2)),
            connectgaps=False,
            hovertemplate="%{x}: %{y:,.0f} vínculos<extra>CAGED</extra>"
        ))

    # Vertical break line
    fig.add_vline(x=2022.5, line_dash="dot", line_color="#999", line_width=1.5,
                  annotation_text="Quebra de série", annotation_position="top")

    fig.update_layout(
        title=f"Evolução do Emprego Formal — {nome}",
        xaxis_title="Ano", yaxis_title="Vínculos / Estoque",
        xaxis=dict(tickmode="linear", dtick=1),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
        height=420, margin=dict(l=60, r=30, t=60, b=40),
        hovermode="x unified"
    )
    return fig

# ── TABS ──
st.title("🏭 Painel Sucroalcooleiro — Alagoas")
st.caption("Dependência do setor sucroalcooleiro e diversificação econômica nos 102 municípios")

tab1, tab2, tab3, tab4 = st.tabs(["📊 Visão Estadual", "🏙️ Ficha do Município", "⚖️ Comparador", "📖 Metodologia"])

# ═══════════════════════════════════════════
# TAB 1 — Visão Estadual
# ═══════════════════════════════════════════
with tab1:
    n_polo = len(consolidado[consolidado["grupo_cana"] == "Polo_Sucroalcooleiro"])
    n_baixa = len(consolidado[consolidado["grupo_cana"] == "Baixa_Dependencia"])

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Municípios", "102")
    col2.metric("Polo Sucroalcooleiro", str(n_polo))
    col3.metric("Baixa Dependência", str(n_baixa))
    media_pct = consolidado["pct_cana_2022"].mean()
    col4.metric("% Cana médio (2022)", fmt(media_pct, 2, "%"))

    st.subheader("Ranking — % Emprego Cana (2022)")
    ranking = consolidado[["nome_municipio", "pct_cana_2022", "grupo_cana", "vinculos_rais_2022",
                           "hhi_2022", "shannon_2022"]].copy()
    ranking = ranking.sort_values("pct_cana_2022", ascending=False).reset_index(drop=True)
    ranking.index = ranking.index + 1
    ranking.columns = ["Município", "% Cana 2022", "Grupo", "Vínculos RAIS 2022", "HHI 2022", "Shannon 2022"]
    st.dataframe(ranking.style.format({
        "% Cana 2022": lambda v: fmt(v, 2, "%"),
        "Vínculos RAIS 2022": lambda v: fmt_int(v),
        "HHI 2022": lambda v: fmt(v, 4),
        "Shannon 2022": lambda v: fmt(v, 4)
    }), use_container_width=True, height=500)

    # Scatter HHI vs Shannon
    st.subheader("Concentração (HHI) vs Diversificação (Shannon) — 2022")
    fig_scatter = go.Figure()
    for grupo, cor, label in [("Polo_Sucroalcooleiro", CINZA, "Polo"), ("Baixa_Dependencia", VERDE, "Baixa Dep.")]:
        sub = consolidado[consolidado["grupo_cana"] == grupo]
        fig_scatter.add_trace(go.Scatter(
            x=sub["hhi_2022"], y=sub["shannon_2022"], mode="markers", name=label,
            marker=dict(color=cor, size=8, opacity=0.7),
            text=sub["nome_municipio"],
            hovertemplate="%{text}<br>HHI: %{x:.4f}<br>Shannon: %{y:.4f}<extra></extra>"
        ))
    fig_scatter.update_layout(
        xaxis_title="HHI (maior = mais concentrado)",
        yaxis_title="Shannon (maior = mais diversificado)",
        height=450, legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5)
    )
    st.plotly_chart(fig_scatter, use_container_width=True, key="scatter_visao")

    # Saldo CAGED acumulado
    st.subheader("Saldo CAGED Acumulado 2023–2026")
    saldo_df = consolidado[["nome_municipio", "grupo_cana", "saldo_acumulado_2023_2026",
                            "crescimento_emprego_2023_2026_pct"]].copy()
    saldo_df = saldo_df.sort_values("saldo_acumulado_2023_2026", ascending=False).reset_index(drop=True)
    saldo_df.index = saldo_df.index + 1
    saldo_df.columns = ["Município", "Grupo", "Saldo Acumulado", "Crescimento (%)"]
    st.dataframe(saldo_df.style.format({
        "Saldo Acumulado": lambda v: fmt_int(v),
        "Crescimento (%)": lambda v: fmt(v, 2, "%")
    }), use_container_width=True, height=400)

# ═══════════════════════════════════════════
# TAB 2 — Ficha do Município
# ═══════════════════════════════════════════
with tab2:
    municipios = sorted(consolidado["nome_municipio"].unique())
    sel = st.selectbox("Selecione o município", municipios)
    mun = consolidado[consolidado["nome_municipio"] == sel].iloc[0]
    mun_p = painel[painel["nome_municipio"] == sel]

    grupo = mun["grupo_cana"]
    st.markdown(f"### {sel} {grupo_label(grupo)}", unsafe_allow_html=True)

    # Métricas principais
    c1, c2, c3, c4 = st.columns(4)
    c1.markdown(metric_card("Vínculos RAIS 2022", fmt_int(mun["vinculos_rais_2022"])), unsafe_allow_html=True)
    c2.markdown(metric_card("% Cana 2022", fmt(mun["pct_cana_2022"], 2, "%")), unsafe_allow_html=True)
    c3.markdown(metric_card("HHI 2022", fmt(mun["hhi_2022"], 4)), unsafe_allow_html=True)
    c4.markdown(metric_card("Shannon 2022", fmt(mun["shannon_2022"], 4)), unsafe_allow_html=True)

    c5, c6, c7, c8 = st.columns(4)
    c5.markdown(metric_card("Setores (2022)", fmt_int(mun["n_setores_2022"])), unsafe_allow_html=True)
    c6.markdown(metric_card("Remuneração Média (SM)", fmt(mun["remuneracao_media_sm_2022"], 2)), unsafe_allow_html=True)
    c7.markdown(metric_card("Saldo CAGED 23–26", fmt_int(mun["saldo_acumulado_2023_2026"])), unsafe_allow_html=True)
    c8.markdown(metric_card("Crescimento 23–26", fmt(mun["crescimento_emprego_2023_2026_pct"], 2, "%")), unsafe_allow_html=True)

    # Avisos
    estoque_2022 = mun["vinculos_rais_2022"]
    if pd.notna(estoque_2022) and estoque_2022 < 200:
        st.markdown('<div class="aviso">⚠️ Município com estoque inferior a 200 vínculos. Variações percentuais podem ser instáveis.</div>', unsafe_allow_html=True)

    canapi_check = mun["id_municipio"] == 2701605
    if canapi_check:
        st.markdown('<div class="aviso">⚠️ Canapi: dados de estoque CAGED indisponíveis para 2023 e 2024. Salto atípico em 2026 (147→1.241) deve ser interpretado com cautela.</div>', unsafe_allow_html=True)

    # Gráfico evolução
    st.plotly_chart(grafico_evolucao(mun_p, sel), use_container_width=True, key="evolucao_ficha")

    # Tabela anual
    st.subheader("Dados Anuais")
    tabela = mun_p[["ano", "fonte_dados", "vinculos_rais", "estoque_final_caged", "estoque_unificado",
                     "pct_cana", "hhi", "shannon", "n_setores", "remuneracao_media_sm",
                     "saldo_caged"]].copy()
    tabela.columns = ["Ano", "Fonte", "Vínculos RAIS", "Estoque CAGED", "Estoque Unificado",
                      "% Cana", "HHI", "Shannon", "Setores", "Rem. Média (SM)", "Saldo CAGED"]
    tabela = tabela.sort_values("Ano").reset_index(drop=True)
    st.dataframe(tabela.style.format({
        "Vínculos RAIS": lambda v: fmt_int(v),
        "Estoque CAGED": lambda v: fmt_int(v),
        "Estoque Unificado": lambda v: fmt_int(v),
        "% Cana": lambda v: fmt(v, 2, "%"),
        "HHI": lambda v: fmt(v, 4),
        "Shannon": lambda v: fmt(v, 4),
        "Setores": lambda v: fmt_int(v),
        "Rem. Média (SM)": lambda v: fmt(v, 2),
        "Saldo CAGED": lambda v: fmt_int(v)
    }), use_container_width=True)

# ═══════════════════════════════════════════
# TAB 3 — Comparador
# ═══════════════════════════════════════════
with tab3:
    st.subheader("Compare dois municípios")
    col_a, col_b = st.columns(2)
    with col_a:
        mun_a = st.selectbox("Município A", municipios, index=0, key="cmp_a")
    with col_b:
        mun_b = st.selectbox("Município B", municipios, index=min(1, len(municipios)-1), key="cmp_b")

    da = consolidado[consolidado["nome_municipio"] == mun_a].iloc[0]
    db = consolidado[consolidado["nome_municipio"] == mun_b].iloc[0]

    campos = [
        ("Grupo", "grupo_cana", None),
        ("Vínculos RAIS 2022", "vinculos_rais_2022", "int"),
        ("% Cana 2022", "pct_cana_2022", "pct"),
        ("HHI 2022", "hhi_2022", "f4"),
        ("Shannon 2022", "shannon_2022", "f4"),
        ("Setores 2022", "n_setores_2022", "int"),
        ("Rem. Média (SM) 2022", "remuneracao_media_sm_2022", "f2"),
        ("Saldo CAGED 23–26", "saldo_acumulado_2023_2026", "int"),
        ("Crescimento 23–26 (%)", "crescimento_emprego_2023_2026_pct", "pct"),
    ]

    def fmt_campo(v, tipo):
        if tipo is None:
            return v.replace("_", " ") if isinstance(v, str) else str(v)
        if tipo == "int":
            return fmt_int(v)
        if tipo == "pct":
            return fmt(v, 2, "%")
        if tipo == "f4":
            return fmt(v, 4)
        if tipo == "f2":
            return fmt(v, 2)
        return str(v)

    rows = []
    for label, col, tipo in campos:
        rows.append({"Indicador": label, mun_a: fmt_campo(da[col], tipo), mun_b: fmt_campo(db[col], tipo)})
    st.table(pd.DataFrame(rows))

    # Gráficos lado a lado
    pa = painel[painel["nome_municipio"] == mun_a]
    pb = painel[painel["nome_municipio"] == mun_b]
    gc1, gc2 = st.columns(2)
    with gc1:
        st.plotly_chart(grafico_evolucao(pa, mun_a), use_container_width=True, key="evolucao_comp_a")
    with gc2:
        st.plotly_chart(grafico_evolucao(pb, mun_b), use_container_width=True, key="evolucao_comp_b")

# ═══════════════════════════════════════════
# TAB 4 — Metodologia
# ═══════════════════════════════════════════
with tab4:
    st.header("Metodologia")

    st.subheader("Fontes de Dados")
    st.markdown("""
- **RAIS (2018–2022)**: Relação Anual de Informações Sociais do Ministério do Trabalho. Inclui vínculos CLT, estatutários e militares.
- **Novo CAGED (2023–2026)**: Cadastro Geral de Empregados e Desempregados. Captura apenas movimentações CLT — **não inclui estatutários**.
- **2026**: dados parciais (janeiro a setembro). Marcado com indicador oco nos gráficos.
""")

    st.subheader("Quebra de Série RAIS → CAGED")
    st.markdown("""
⚠️ **Os níveis de emprego RAIS e CAGED não são diretamente comparáveis.**

A RAIS captura o universo completo de vínculos formais, incluindo servidores estatutários. O Novo CAGED
registra apenas movimentações CLT. Portanto, municípios com grande proporção de emprego público (estatutários)
podem apresentar queda aparente no nível de emprego a partir de 2023 que **não reflete perda real de postos de trabalho**.

No painel, a transição é sinalizada por:
- Linha vertical pontilhada em 2022.5
- Linha sólida (RAIS) vs tracejada (CAGED)
- Legenda explícita com as duas fontes
""")

    st.subheader("Indicadores de Concentração / Diversificação")
    st.markdown(f"""
- **HHI (Herfindahl-Hirschman)**: soma dos quadrados das participações setoriais. Varia de ~0 (diversificado) a 1 (monopólio). Calculado sobre vínculos RAIS 2022.
- **Entropia de Shannon**: mede a diversidade setorial. Maior = mais diversificado. Calculado sobre vínculos RAIS 2022.
- **% Cana**: participação dos CNAEs sucroalcooleiros ({CANA_CNAES}) no total de vínculos RAIS 2022.

⚠️ **Limitação — Administração pública**: em municípios pequenos, a administração pública municipal
costuma concentrar grande parte dos vínculos formais, inflando o HHI e reduzindo a entropia de Shannon
independentemente da presença sucroalcooleira. Ao interpretar esses indicadores, considere que valores
altos de HHI podem refletir dependência do setor público, e não necessariamente do setor canavieiro.
""")

    st.subheader("Classificação dos Municípios")
    st.markdown("""
- **Polo Sucroalcooleiro**: municípios com % cana ≥ 10% nos vínculos RAIS 2022. São **20** municípios.
- **Baixa Dependência**: municípios com % cana < 10%. São **82** municípios.

O limiar de 10% foi definido com base na distribuição bimodal do indicador e na literatura sobre dependência setorial.
""")

    st.subheader("Tratamento de Dados Faltantes")
    st.markdown("""
- Valores ausentes são exibidos como **"Dado indisponível"**, nunca como zero.
- **Canapi (2701605)**: estoque CAGED indisponível para 2023 e 2024. Salto atípico em 2026 (147 → 1.241 vínculos) deve ser interpretado com cautela.
- Municípios com estoque < 200 vínculos recebem aviso sobre instabilidade de variações percentuais.
""")

    st.subheader("Estoque Unificado")
    st.markdown("""
Para permitir visualização contínua, o campo `estoque_unificado` utiliza:
- **2018–2022**: `vinculos_rais` (total RAIS)
- **2023–2026**: `estoque_final_caged` (estoque CAGED ao final do período)

Essa série **não deve ser interpretada como contínua em nível absoluto** devido à mudança de fonte.
""")

    st.markdown("---")
    st.caption("Painel Sucroalcooleiro — Alagoas | Dados: RAIS & Novo CAGED | Desenvolvido com Streamlit")
