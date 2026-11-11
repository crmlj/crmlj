# %%
# Importar as bibliotecas de análise e visualização.
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# %%
# Ler o CSV e inspecionar as primeiras linhas, colunas, tipos e dimensões.
schools = pd.read_csv("schools.csv")
print(schools.head().to_string(index=False))
print(schools.columns)
print(schools.dtypes)
print("Linhas e colunas:", schools.shape)

# %%
# Contar os valores ausentes e os valores distintos por coluna.
print("\nValores ausentes por coluna")
print(schools.isna().sum())
print("\nValores distintos por coluna")
print(schools.nunique())

# %%
# Filtrar as escolas com média de matemática de pelo menos 80% de 800.
low_limit = 800 * 0.80
best_math_schools = schools[schools["average_math"] >= low_limit]

# Ordenar por nota e manter apenas o nome da escola e a média de matemática.
best_math_schools = best_math_schools.sort_values("average_math", ascending=False)
best_math_schools = best_math_schools[["school_name", "average_math"]]

# Somar as notas médias das três secções do SAT para cada escola.
schools["total_SAT"] = (
    schools["average_math"] + schools["average_reading"] + schools["average_writing"]
)

# Selecionar as dez escolas com maior pontuação total.
top_10_schools = schools.sort_values("total_SAT", ascending=False).head(10)
top_10_schools = top_10_schools[["school_name", "total_SAT"]]

# Calcular a contagem, a média e o desvio-padrão das pontuações por borough.
boroughs = schools.groupby("borough")["total_SAT"].agg(["count", "mean", "std"])

# Selecionar o maior desvio-padrão antes de arredondar e renomear as colunas.
largest_std_dev = (
    boroughs.sort_values("std", ascending=False)
    .head(1)
    .round(2)
    .reset_index()
    .rename(columns={
        "count": "num_schools",
        "mean": "average_SAT",
        "std": "std_SAT",
    })
)

# Apresentar os resultados das três perguntas do projeto.
print("\nMelhores notas de matemática")
print(best_math_schools.to_string(index=False))
print("\n10 maiores pontuações no SAT")
print(top_10_schools.to_string(index=False))
print("\nBorough com o maior desvio-padrão")
print(largest_std_dev.to_string(index=False))

# %%
# Associar uma cor a cada borough e criar o boxplot com Seaborn.
cores_por_borough = {
    "Manhattan": "#0072B2",
    "Staten Island": "#E69F00",
    "Bronx": "#009E73",
    "Queens": "#CC79A7",
    "Brooklyn": "#D55E00",
}
fig, ax = plt.subplots(figsize=(8, 5))
sns.boxplot(
    data=schools,
    x="borough",
    y="total_SAT",
    hue="borough",
    palette=cores_por_borough,
    legend=False,
    ax=ax,
)
ax.set(
    title="Pontuações do SAT por borough",
    xlabel="Borough (std = desvio-padrão)",
    ylabel="Pontuação total do SAT",
)

# Acrescentar o desvio-padrão abaixo do nome de cada borough.
rotulos = []
for rotulo in ax.get_xticklabels():
    borough = rotulo.get_text()
    desvio = boroughs.loc[borough, "std"]
    rotulos.append("%s\nstd: %.2f" % (borough, desvio))

# Ajustar o espaço dos rótulos e mostrar o gráfico.
ax.set_xticks(ax.get_xticks(), rotulos)
fig.tight_layout()
plt.show()
