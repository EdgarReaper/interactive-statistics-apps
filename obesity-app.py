import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from scipy import stats


# Configuração da página

st.set_page_config(
    page_title="Análise Exploratória - Obesidade",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("Análise Exploratória - Dataset de Obesidade")
st.markdown("Análise interativa de variáveis quantitativas com intervalos de confiança.")


# Carregar dados

@st.cache_data
def load_data():
    df = pd.read_csv("Obesity.csv")
    return df

df = load_data()


# Dicionário de nomes legíveis para as colunas

VAR_LABELS = {
    "Weight": "Peso (kg)",
    "Age":    "Idade (anos)",
    "Height": "Altura (m)",
    "FCVC":   "Frequência de consumo de vegetais (1–3)",
    "NCP":    "Nº de refeições principais por dia",
    "CH2O":   "Consumo de água por dia (1–3)",
    "FAF":    "Frequência de atividade física (0–3)",
    "TUE":    "Tempo de uso de tecnologia por dia (0–2)",
}

OBESITY_ORDER = [
    "Insufficient_Weight",
    "Normal_Weight",
    "Overweight_Level_I",
    "Overweight_Level_II",
    "Obesity_Type_I",
    "Obesity_Type_II",
    "Obesity_Type_III",
]

OBESITY_LABELS = {
    "Insufficient_Weight":  "Peso Insuficiente",
    "Normal_Weight":        "Peso Normal",
    "Overweight_Level_I":   "Excesso Peso I",
    "Overweight_Level_II":  "Excesso Peso II",
    "Obesity_Type_I":       "Obesidade I",
    "Obesity_Type_II":      "Obesidade II",
    "Obesity_Type_III":     "Obesidade III",
}

COLORS = ["#4e9af1","#57c785","#f0a500","#f06f40","#c94040","#8e2323","#4b0f0f"]


# Sidebar

st.sidebar.header("Opções")

variavel = st.sidebar.selectbox(
    "Variável a analisar",
    options=list(VAR_LABELS.keys()),
    format_func=lambda x: VAR_LABELS[x]
)

confianca = st.sidebar.slider(
    "Nível de confiança do IC (%)",
    min_value=80, max_value=99, value=95, step=1
)

filtrar_grupo = st.sidebar.checkbox("Filtrar por nível de obesidade", value=False)
grupo_sel = None
if filtrar_grupo:
    grupo_sel = st.sidebar.selectbox(
        "Nível de obesidade",
        options=OBESITY_ORDER,
        format_func=lambda x: OBESITY_LABELS[x]
    )

st.sidebar.markdown("---")
st.sidebar.markdown("**Sobre o dataset**")
st.sidebar.markdown(f"- **{len(df)}** observações")
st.sidebar.markdown(f"- **{df.shape[1]}** variáveis")
st.sidebar.markdown("- Fonte: UCI Machine Learning Repository")


# Filtrar dados se necessário

if filtrar_grupo and grupo_sel:
    dados = df[df["NObeyesdad"] == grupo_sel][variavel].dropna()
    label_grupo = f" - {OBESITY_LABELS[grupo_sel]}"
else:
    dados = df[variavel].dropna()
    label_grupo = " - Toda a amostra"

n        = len(dados)
media    = dados.mean()
mediana  = dados.median()
dp       = dados.std()
variancia= dados.var()
minimo   = dados.min()
maximo   = dados.max()
q1       = dados.quantile(0.25)
q3       = dados.quantile(0.75)
iqr      = q3 - q1
assimetria = dados.skew()
curtose    = dados.kurt()


# SECÇÃO 1 - Estatísticas descritivas

st.header(f"1. Estatísticas Descritivas - {VAR_LABELS[variavel]}{label_grupo}")

c1, c2, c3, c4 = st.columns(4)
c1.metric("Média",         f"{media:.3f}")
c2.metric("Mediana",       f"{mediana:.3f}")
c3.metric("Desvio Padrão", f"{dp:.3f}")
c4.metric("Variância",     f"{variancia:.3f}")

c5, c6, c7, c8 = st.columns(4)
c5.metric("Mínimo",        f"{minimo:.3f}")
c6.metric("Máximo",        f"{maximo:.3f}")
c7.metric("Amplitude IQR", f"{iqr:.3f}")
c8.metric("Nº Observações",f"{n}")

c9, c10 = st.columns(2)
c9.metric("Assimetria",  f"{assimetria:.4f}")
c10.metric("Curtose",    f"{curtose:.4f}")

st.markdown("---")


# SECÇÃO 2 - Histograma e Boxplot

st.header("2. Gráficos Exploratórios")

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 4))
fig.suptitle(f"{VAR_LABELS[variavel]}{label_grupo}", fontsize=13)

#  Histograma 
valores_unicos = dados.nunique()
n_bins = min(40, max(10, n // 20)) if valores_unicos > 10 else valores_unicos
ax1.hist(dados, bins=n_bins, color="#3266ad", alpha=0.7, edgecolor="#3266ad", linewidth=0.4, density=True)

# Curva KDE - só se os dados tiverem variação suficiente
kde_possivel = dp > 1e-10 and valores_unicos > 5
if kde_possivel:
    kde_x = np.linspace(minimo, maximo, 300)
    kde = stats.gaussian_kde(dados)
    ax1.plot(kde_x, kde(kde_x), color="#D85A30", linewidth=2, label="Densidade estimada (KDE)")
else:
    ax1.text(0.5, 0.92, "KDE não disponível (dados com pouca variação)",
             transform=ax1.transAxes, ha="center", fontsize=8, color="#D85A30",
             style="italic")

ax1.axvline(media,  color="#D85A30", linestyle="--", linewidth=1.5, label=f"Média = {media:.2f}")
ax1.axvline(mediana,color="#0F6E56", linestyle=":",  linewidth=1.5, label=f"Mediana = {mediana:.2f}")
ax1.set_xlabel(VAR_LABELS[variavel])
ax1.set_ylabel("Densidade")
ax1.set_title("Histograma com KDE")
ax1.legend(fontsize=9)
ax1.grid(alpha=0.3)

#  Boxplot 
bp = ax2.boxplot(dados, vert=True, patch_artist=True,
                 boxprops=dict(facecolor="#3266ad", alpha=0.5),
                 medianprops=dict(color="#D85A30", linewidth=2),
                 whiskerprops=dict(linewidth=1.5),
                 capprops=dict(linewidth=1.5),
                 flierprops=dict(marker="o", markersize=3, alpha=0.4, color="#3266ad"))
ax2.set_ylabel(VAR_LABELS[variavel])
ax2.set_title("Boxplot")
ax2.set_xticks([])
ax2.grid(alpha=0.3, axis="y")

# Anotações no boxplot
for val, lbl, col in [(q1,"Q1","#555"), (mediana,"Mediana","#D85A30"), (q3,"Q3","#555"), (media,"Média","#c00")]:
    ax2.axhline(val, color=col, linestyle=":", linewidth=0.8, alpha=0.6)
    ax2.text(1.32, val, f"{lbl} = {val:.2f}", va="center", fontsize=8, color=col)

plt.tight_layout()
st.pyplot(fig)

st.markdown("---")


# SECÇÃO 3 - Intervalo de Confiança

st.header(f"3. Intervalo de Confiança para a Média - {confianca}%")

alpha_ic = 1 - confianca / 100
t_crit   = stats.t.ppf(1 - alpha_ic / 2, df=n - 1)
erro_pad = dp / np.sqrt(n)
ic_inf   = media - t_crit * erro_pad
ic_sup   = media + t_crit * erro_pad
margem   = t_crit * erro_pad

# Cards do IC
ca, cb, cc, cd = st.columns(4)
ca.metric("Limite Inferior",  f"{ic_inf:.4f}")
cb.metric("Média amostral",   f"{media:.4f}")
cc.metric("Limite Superior",  f"{ic_sup:.4f}")
cd.metric("Margem de erro",   f"± {margem:.4f}")

ce, cf, cg = st.columns(3)
ce.metric("Erro padrão (σ/√n)", f"{erro_pad:.4f}")
cf.metric("t crítico",          f"{t_crit:.4f}")
cg.metric("Graus de liberdade", f"{n-1}")

# Gráfico do IC
fig2, ax = plt.subplots(figsize=(10, 3))

# Distribuição t centrada na média
x_t = np.linspace(media - 4*erro_pad, media + 4*erro_pad, 500)
y_t = stats.norm.pdf(x_t, media, erro_pad)

ax.plot(x_t, y_t, color="#3266ad", linewidth=2)

# Área do IC a sombreado
mask_ic = (x_t >= ic_inf) & (x_t <= ic_sup)
ax.fill_between(x_t, y_t, where=mask_ic, color="#3266ad", alpha=0.2,
                label=f"IC {confianca}% = [{ic_inf:.3f}, {ic_sup:.3f}]")

# Linhas verticais
ax.axvline(media,  color="#D85A30", linewidth=2,   linestyle="-",  label=f"Média = {media:.3f}")
ax.axvline(ic_inf, color="#3266ad", linewidth=1.5, linestyle="--", label=f"Inf = {ic_inf:.3f}")
ax.axvline(ic_sup, color="#3266ad", linewidth=1.5, linestyle="--", label=f"Sup = {ic_sup:.3f}")

ax.set_xlabel(VAR_LABELS[variavel])
ax.set_ylabel("Densidade")
ax.set_title(f"Intervalo de Confiança {confianca}% para a Média - {VAR_LABELS[variavel]}{label_grupo}")
ax.legend(fontsize=9)
ax.grid(alpha=0.3)
plt.tight_layout()
st.pyplot(fig2)

# Interpretação automática
st.info(
    f"**Interpretação:** Com um nível de confiança de {confianca}%, estimamos que a média populacional "
    f"de **{VAR_LABELS[variavel]}** se encontra entre **{ic_inf:.3f}** e **{ic_sup:.3f}**. "
    f"A margem de erro é de ±{margem:.3f}, calculada com base numa amostra de {n} observações."
)

st.markdown("---")


# SECÇÃO 4 - Distribuição por nível de obesidade

st.header(f"4. Comparação por Nível de Obesidade - {VAR_LABELS[variavel]}")

grupos_data = [
    df[df["NObeyesdad"] == g][variavel].dropna().values
    for g in OBESITY_ORDER
]
labels_pt = [OBESITY_LABELS[g] for g in OBESITY_ORDER]

fig3, (ax_box, ax_bar) = plt.subplots(1, 2, figsize=(14, 5))
fig3.suptitle(f"{VAR_LABELS[variavel]} por Nível de Obesidade", fontsize=13)

#  Boxplot por grupo 
bps = ax_box.boxplot(grupos_data, patch_artist=True,
                     medianprops=dict(color="white", linewidth=2),
                     whiskerprops=dict(linewidth=1.2),
                     capprops=dict(linewidth=1.2),
                     flierprops=dict(marker="o", markersize=2, alpha=0.3))
for patch, color in zip(bps["boxes"], COLORS):
    patch.set_facecolor(color)
    patch.set_alpha(0.75)
for flier, color in zip(bps["fliers"], COLORS):
    flier.set_markerfacecolor(color)

ax_box.set_xticklabels(labels_pt, rotation=30, ha="right", fontsize=8)
ax_box.set_ylabel(VAR_LABELS[variavel])
ax_box.set_title("Boxplot por grupo")
ax_box.grid(alpha=0.3, axis="y")

#  Médias com IC 95% 
medias_g  = [np.mean(g) for g in grupos_data]
ic_g      = [stats.t.interval(0.95, df=len(g)-1, loc=np.mean(g), scale=stats.sem(g)) for g in grupos_data]
ic_inf_g  = [ic[0] for ic in ic_g]
ic_sup_g  = [ic[1] for ic in ic_g]
erros_inf = [m - i for m, i in zip(medias_g, ic_inf_g)]
erros_sup = [s - m for m, s in zip(medias_g, ic_sup_g)]

bars = ax_bar.bar(labels_pt, medias_g, color=COLORS, alpha=0.75, edgecolor="white", linewidth=0.5)
ax_bar.errorbar(labels_pt, medias_g,
                yerr=[erros_inf, erros_sup],
                fmt="none", color="black", capsize=5, linewidth=1.5, capthick=1.5)
ax_bar.set_xticklabels(labels_pt, rotation=30, ha="right", fontsize=8)
ax_bar.set_ylabel(f"Média de {VAR_LABELS[variavel]}")
ax_bar.set_title("Média com IC 95% por grupo")
ax_bar.grid(alpha=0.3, axis="y")

plt.tight_layout()
st.pyplot(fig3)

st.markdown("---")
st.caption("Projeto de Laboratórios de Estatística II - Análise Exploratória do Dataset de Obesidade | Código gerado com Python + Streamlit + SciPy")