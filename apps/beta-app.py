import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from scipy.special import beta as beta_func, betaln
import matplotlib.gridspec as gridspec


# Configuração da página
st.set_page_config(
    page_title="Distribuição Beta - Projeto de Laboratórios de Estatística II",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("Distribuição Beta")
st.markdown("Exploração interativa dos parâmetros, propriedades e simulações.")


# Sidebar - Parâmetros
st.sidebar.header("Parâmetros")

alpha = st.sidebar.slider("α (alpha)", min_value=0.1, max_value=10.0, value=2.0, step=0.1)
beta_param = st.sidebar.slider("β (beta)", min_value=0.1, max_value=10.0, value=5.0, step=0.1)

st.sidebar.markdown("---")
st.sidebar.header("Simulação")
n_samples = st.sidebar.slider(
    "Número de amostras (TLC)", min_value=100, max_value=3000, value=500, step=100
)
sample_size_tlc = st.sidebar.slider(
    "Tamanho de cada amostra (TLC)", min_value=5, max_value=100, value=30, step=5
)
max_n_lgn = st.sidebar.slider(
    "Tamanho máximo da amostra (LGN)", min_value=200, max_value=5000, value=1000, step=100
)

if st.sidebar.button("Nova simulação"):
    st.rerun()


# Distribuição Beta - scipy
dist = stats.beta(alpha, beta_param)

# Propriedades teóricas
mean_teorica   = alpha / (alpha + beta_param)
var_teorica    = (alpha * beta_param) / ((alpha + beta_param)**2 * (alpha + beta_param + 1))
std_teorica    = np.sqrt(var_teorica)
skewness       = dist.stats(moments='s')
kurtosis       = dist.stats(moments='k')

if alpha > 1 and beta_param > 1:
    moda = (alpha - 1) / (alpha + beta_param - 2)
    moda_str = f"{moda:.4f}"
elif alpha <= 1 and beta_param > 1:
    moda_str = "0 (fronteira)"
elif alpha > 1 and beta_param <= 1:
    moda_str = "1 (fronteira)"
else:
    moda_str = "0 e 1 (bimodal)"

quantis = {f"Q{int(p*100)}": dist.ppf(p) for p in [0.10, 0.25, 0.50, 0.75, 0.90]}


# PARTE I - Estatísticas e gráficos
st.header("Parte I - Propriedades do Modelo")

# Estatísticas em cards
col1, col2, col3, col4 = st.columns(4)
col1.metric("Média (μ)",         f"{mean_teorica:.4f}")
col2.metric("Variância (σ²)",    f"{var_teorica:.4f}")
col3.metric("Desvio padrão (σ)", f"{std_teorica:.4f}")
col4.metric("Moda",              moda_str)

col5, col6, col7, col8 = st.columns(4)
col5.metric("Assimetria",  f"{float(skewness):.4f}")
col6.metric("Curtose",     f"{float(kurtosis):.4f}")
col7.metric("α",           f"{alpha:.1f}")
col8.metric("β",           f"{beta_param:.1f}")

st.markdown("---")

# Gráficos PDF e CDF
x = np.linspace(1e-4, 1 - 1e-4, 500)
pdf_vals = dist.pdf(x)
cdf_vals = dist.cdf(x)

fig1, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
fig1.suptitle(f"Distribuição Beta(α={alpha}, β={beta_param})", fontsize=13)

# PDF
ax1.plot(x, pdf_vals, color="#3266ad", linewidth=2)
ax1.fill_between(x, pdf_vals, alpha=0.15, color="#3266ad")
ax1.set_title("Função Densidade de Probabilidade (PDF)")
ax1.set_xlabel("x")
ax1.set_ylabel("f(x)")
ax1.axvline(mean_teorica, color="#D85A30", linestyle="--", linewidth=1.5, label=f"Média = {mean_teorica:.3f}")
ax1.legend(fontsize=10)
ax1.grid(alpha=0.3)
ax1.set_xlim(0, 1)

# CDF
ax2.plot(x, cdf_vals, color="#0F6E56", linewidth=2)
ax2.set_title("Função de Distribuição Acumulada (CDF)")
ax2.set_xlabel("x")
ax2.set_ylabel("F(x)")
ax2.axhline(0.5, color="#888", linestyle=":", linewidth=1, label="F(x) = 0.5")
ax2.axvline(quantis["Q50"], color="#D85A30", linestyle="--", linewidth=1.5, label=f"Mediana = {quantis['Q50']:.3f}")
ax2.legend(fontsize=10)
ax2.grid(alpha=0.3)
ax2.set_xlim(0, 1)
ax2.set_ylim(0, 1)

plt.tight_layout()
st.pyplot(fig1)

# Quantis
st.subheader("Quantis")
q_cols = st.columns(5)
for i, (label, val) in enumerate(quantis.items()):
    q_cols[i].metric(label, f"{val:.4f}")

with st.expander("Fórmulas - PDF e CDF da Distribuição Beta"):
    st.markdown(r"""
**Função Densidade de Probabilidade (PDF)**
 
$$f(x \mid \alpha, \beta) = \frac{x^{\alpha-1}(1-x)^{\beta-1}}{B(\alpha,\beta)}, \quad x \in (0,1)$$
 
onde $B(\alpha, \beta) = \dfrac{\Gamma(\alpha)\,\Gamma(\beta)}{\Gamma(\alpha+\beta)}$ é a função Beta e $\Gamma$ é a função Gama.
 
---
 
**Função de Distribuição Acumulada (CDF)**
 
$$F(x \mid \alpha, \beta) = I_x(\alpha, \beta) = \frac{B(x;\,\alpha,\beta)}{B(\alpha,\beta)}$$
 
onde $B(x;\alpha,\beta) = \int_0^x t^{\alpha-1}(1-t)^{\beta-1}\,dt$ é a função Beta incompleta e $I_x$ é a função Beta incompleta regularizada.
 
---
 
**Propriedades:**
 
| Propriedade | Fórmula |
|---|---|
| Média | $\mu = \dfrac{\alpha}{\alpha+\beta}$ |
| Variância | $\sigma^2 = \dfrac{\alpha\beta}{(\alpha+\beta)^2(\alpha+\beta+1)}$ |
| Moda | $\dfrac{\alpha-1}{\alpha+\beta-2}$ (se $\alpha,\beta > 1$) |
""")

st.markdown("---")


# PARTE II - Simulações LGN e TLC
st.header("Parte II - Simulações")

# Lei dos Grandes Números
st.subheader("Lei dos Grandes Números (LGN)")
st.markdown(
    "À medida que o tamanho da amostra **n** aumenta, "
    "a média amostral converge para a média teórica **μ**."
)

big_sample = dist.rvs(size=max_n_lgn)
running_mean = np.cumsum(big_sample) / np.arange(1, max_n_lgn + 1)

fig2, ax = plt.subplots(figsize=(12, 4))
ax.plot(range(1, max_n_lgn + 1), running_mean, color="#3266ad", linewidth=1.2, label="Média amostral acumulada")
ax.axhline(mean_teorica, color="#D85A30", linestyle="--", linewidth=1.8, label=f"Média teórica μ = {mean_teorica:.4f}")
ax.set_title("Lei dos Grandes Números - Convergência da Média Amostral")
ax.set_xlabel("n (tamanho da amostra)")
ax.set_ylabel("Média amostral")
ax.legend(fontsize=10)
ax.grid(alpha=0.3)
plt.tight_layout()
st.pyplot(fig2)

# Teorema Limite Central
st.subheader("Teorema Limite Central (TLC)")
st.markdown(
    f"A distribuição das médias de **{n_samples}** amostras de tamanho **n={sample_size_tlc}** "
    "aproxima uma distribuição Normal."
)

sample_means = np.array([
    dist.rvs(size=sample_size_tlc).mean()
    for _ in range(n_samples)
])

mu_tlc    = mean_teorica
sigma_tlc = std_teorica / np.sqrt(sample_size_tlc)

x_norm = np.linspace(sample_means.min(), sample_means.max(), 300)
norm_pdf = stats.norm.pdf(x_norm, mu_tlc, sigma_tlc)

fig3, ax = plt.subplots(figsize=(12, 4))
ax.hist(
    sample_means, bins=40, density=True,
    color="#3266ad", alpha=0.55, edgecolor="#3266ad", linewidth=0.5,
    label="Distribuição das médias amostrais"
)
ax.plot(x_norm, norm_pdf, color="#D85A30", linewidth=2.2,
        label=f"Normal teórica N(μ={mu_tlc:.3f}, σ={sigma_tlc:.4f})")
ax.set_title("Teorema Limite Central - Distribuição das Médias Amostrais")
ax.set_xlabel("Média amostral")
ax.set_ylabel("Densidade")
ax.legend(fontsize=10)
ax.grid(alpha=0.3)
plt.tight_layout()
st.pyplot(fig3)

# Comparação estatísticas simuladas vs teóricas
st.subheader("Comparação: simulação vs teoria (TLC)")
col_a, col_b, col_c, col_d = st.columns(4)
col_a.metric("Média amostral (sim.)",  f"{sample_means.mean():.4f}", f"{sample_means.mean() - mu_tlc:+.4f} vs μ")
col_b.metric("Média teórica (μ)",      f"{mu_tlc:.4f}")
col_c.metric("Desvio padrão (sim.)",   f"{sample_means.std():.4f}",  f"{sample_means.std() - sigma_tlc:+.4f} vs σ/√n")
col_d.metric("Desvio padrão teórico",  f"{sigma_tlc:.4f}")

with st.expander("Fórmulas - Lei dos Grandes Números e Teorema Limite Central"):
    st.markdown(r"""
**Lei dos Grandes Números (LGN)**
 
Seja $X_1, X_2, \ldots, X_n$ uma sequência de variáveis aleatórias i.i.d. com média $\mu$. A média amostral é:
 
$$\bar{X}_n = \frac{1}{n}\sum_{i=1}^{n} X_i$$
 
A LGN garante que:
 
$$\bar{X}_n \xrightarrow{n \to \infty} \mu$$
 
No gráfico, a linha azul é $\bar{X}_n$ calculada acumuladamente - e converge para a linha vermelha $\mu = \dfrac{\alpha}{\alpha+\beta}$.
 
---
 
**Teorema Limite Central (TLC)**
 
Para $n$ suficientemente grande, a distribuição de $\bar{X}_n$ aproxima-se de uma Normal:
 
$$\bar{X}_n \xrightarrow{d} \mathcal{N}\!\left(\mu,\, \frac{\sigma^2}{n}\right)$$
 
ou equivalentemente, a variável estandardizada:
 
$$Z = \frac{\bar{X}_n - \mu}{\sigma / \sqrt{n}} \xrightarrow{d} \mathcal{N}(0,1)$$
 
onde $\mu$ e $\sigma^2$ são a média e variância da distribuição Beta original. O histograma mostra as médias das amostras simuladas e a curva vermelha é a Normal teórica prevista pelo TLC.
""")

st.markdown("---")
st.caption("Projeto de Laboratórios de Estatística II - Distribuição Beta | Código gerado com Python + Streamlit + SciPy + NumPy + Matplotlib")
