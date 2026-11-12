#%%
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

nobel = pd.read_csv("nobel.csv")
#%%
# Encontra o gênero e o país de nascimento mais frequentes.

top_gender = nobel["sex"].value_counts().idxmax()
print(top_gender)
print(top_gender)
top_country = nobel["birth_country"].value_counts().idxmax()
print(top_country)

#%%
# Identificar a década com a maior razão de vencedores nascidos nos EUA
nobel["usa_born"] = nobel["birth_country"] == "United States of America"

# Criar coluna decade

nobel["decade"] = (np.floor(nobel["year"] / 10) * 10).astype(int)

# Retorna uma Series com as décadas no índice.
proporcoes = nobel.groupby("decade")["usa_born"].mean()

# idxmax() na Series retorna um único valor: a década de maior proporção.

max_decade_usa = int(proporcoes.idxmax())

# Retorna um DataFrame com as colunas decade e usa_born.
data = nobel.groupby("decade", as_index=False)["usa_born"].mean()

# Usa as duas colunas do DataFrame para montar o gráfico.
sns.relplot(
    data=data,
    x="decade",
    y="usa_born",
    kind="line",
)
# Qual combinação de década e categoria do Prêmio Nobel teve a maior proporção de laureadas mulheres?
#%%
nobel["sex"].value_counts(dropna=False) # coluna original

nobel["female"] = nobel["sex"] == "Female"
nobel["male"] = nobel["sex"] == "Male"

gender = nobel.groupby(["decade", "category"], as_index = False).agg(female_mean=("female", "mean"), male_mean=("male", "mean")) # as_index=False mantém decade e category como colunas do DataFrame.

nobel["female"].value_counts(dropna=False)
nobel["male"].value_counts(dropna=False)

max_female_mean = gender["female_mean"].idxmax() # retorna a linha
max_male_mean = gender["male_mean"].idxmax() # retorna a linha 

decada_female = gender.loc[max_female_mean, "decade"]
categoria_female = gender.loc[max_female_mean, "category"]

decada_male = gender.loc[max_male_mean, "decade"]
categoria_male = gender.loc[max_male_mean, "category"]

max_male_dict = {int(decada_male) : categoria_male}
max_female_dict = {int(decada_female) : categoria_female}

max_dict = {"female" : max_female_dict, "male": max_male_dict}
print(max_dict)
#%%
# %%
map_female = gender.pivot(
    index="category", columns="decade", values="female_mean") * 100

ax = sns.heatmap(map_female, cmap="Blues", vmin=0, vmax=100)
ax.set(title="Mulheres premiadas (%)", xlabel="Década", ylabel="Categoria")

# %%
map_male = gender.pivot(index="category", columns="decade", values="male_mean") * 100

ax = sns.heatmap(map_male, cmap="Blues", vmin=0, vmax=100)
ax.set(title="Homens premiados (%)", xlabel="Década", ylabel="Categoria")

ax.set_facecolor("#e5e7eb")

#%%
# Encontra a primeira mulher premiada.
laureadas = nobel[nobel["female"]]
linha_primeira_mulher = laureadas["year"].idxmin()
first_woman_name = laureadas.loc[linha_primeira_mulher, "full_name"]
first_woman_category = laureadas.loc[linha_primeira_mulher, "category"]

# Seleciona o primeiro registro masculino no ano mais antigo.
homens_premiados = nobel[nobel["male"]]
linha_primeiro_homem = homens_premiados["year"].idxmin()
first_man_name = homens_premiados.loc[linha_primeiro_homem, "full_name"]
first_man_category = homens_premiados.loc[linha_primeiro_homem, "category"]

# Guarda os nomes de quem recebeu pelo menos dois prêmios.
vencedores = nobel["full_name"].value_counts()
repeat_list = vencedores[vencedores >= 2].index.tolist()

# Exibe as respostas na janela interativa.
print("Gênero mais premiado:", top_gender)
print("País de nascimento mais frequente:", top_country)
print("Década e categoria com maior proporção de mulheres:", max_dict["female"])
print("Década e categoria com maior proporção de homens:", max_dict["male"])
print("Primeira mulher premiada:", first_woman_name, first_woman_category)
print("Homem premiado no primeiro ano:", first_man_name, first_man_category)
print("Vencedores recorrentes:", repeat_list)
# %%
