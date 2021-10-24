# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import json
import numpy as np
import pandas as pd
import requests


# %%
def get_json(api_url):
	response = requests.get(api_url)
	if response.status_code == 200:
		return json.loads(response.content.decode('utf-8'))
	else:
		return None
		


# %%
#Reformat Data Frame
pd.set_option("display.max_columns", None)

covid_url = "D:\\downloads\\DATASET-DATASCIENCE-20211015T124508Z-001\\Analisis Data COVID19 di Dunia & ASEAN\\covid19_worldwide_2020.json"
df_covid_worldwide = pd.read_json(covid_url)

print("Informasi data frame awal:")
df_covid_worldwide.info()

df_covid_worldwide = df_covid_worldwide.set_index("date").sort_index()

print("\nInformasi data frame setelah set index kolom date:")
df_covid_worldwide.info()


# %%
#Missing Value di DataFrame
print("Jumlah missing value tiap kolom:")
print(df_covid_worldwide.isna().sum())

df_covid_worldwide.dropna(inplace=True)

print("\nJumlah missing value tiap kolom setelah didrop:")
print(df_covid_worldwide.isna().sum())


# %%
#membaca data countries
countries_url = "D:\\downloads\\DATASET-DATASCIENCE-20211015T124508Z-001\\Analisis Data COVID19 di Dunia & ASEAN\\country_details.json"
df_countries = pd.read_json(countries_url)
print(df_countries.head())


# %%
#Merge Covid19 Data dan Countries
df_covid_denormalized = pd.merge(df_covid_worldwide.reset_index(), df_countries, on="geo_id").set_index("date")
print(df_covid_denormalized.head())


# %%
#menghitung fatility ratio
df_covid_denormalized["fatality_ratio"] = df_covid_denormalized["deaths"]/df_covid_denormalized["confirmed_cases"]
print(df_covid_denormalized.head())


# %%
#Negara-negara dengan Fatality Ratio Tertinggi
df_top_20_fatality_rate = df_covid_denormalized.sort_values("fatality_ratio", ascending=False).head(20)
print(df_top_20_fatality_rate[["geo_id","country_name","fatality_ratio"]])


# %%
#Kondisi Fatality ratio Tertinggi di Bulan Agustus 2020
df_covid_denormalized_august = df_covid_denormalized.loc["2020-08"].groupby("country_name").sum()

df_covid_denormalized_august["fatality_ratio"] = df_covid_denormalized_august["deaths"]/df_covid_denormalized_august["confirmed_cases"]

df_top_20_fatality_rate_on_august = df_covid_denormalized_august.sort_values(by="fatality_ratio", ascending=False).head(20)

print(df_top_20_fatality_rate_on_august["fatality_ratio"])


# %%
#Visualisasi Negara dengan Fatality Ratio Tertinggi di Bulan Agustus 2020
import matplotlib.pyplot as plt
plt.figure(figsize=(8,8))
df_top_20_fatality_rate_on_august["fatality_ratio"].sort_values().plot(kind="barh", color="coral")
plt.title("Top 20 Highest Fatality Rate Countries", fontsize=18, color="b")
plt.xlabel("Fatality Rate", fontsize=14)
plt.ylabel("Country Name", fontsize=14)
plt.grid(axis="x")
plt.tight_layout()
plt.show()


# %%
#Data Frame Kasus COVID-19 ASEAN
asean_country_id = ["ID", "MY", "SG", "TH", "VN"]
filter_list = [(df_covid_denormalized["geo_id"]==country_id).to_numpy() for country_id in asean_country_id]
filter_array = np.column_stack(filter_list).sum(axis=1, dtype="bool")
df_covid_denormalized_asean = df_covid_denormalized[filter_array].sort_index()

print("Cek nilai unik di kolom 'country_name':", df_covid_denormalized_asean["country_name"].unique())
print(df_covid_denormalized_asean.head())


# %%
#Kasus Pertama COVID-19 di ASEAN
print("The first case popped up in each of 5 ASEAN countries:")
for country_id in asean_country_id:
    asean_country = df_covid_denormalized_asean[df_covid_denormalized_asean["geo_id"]==country_id]
    first_case = asean_country[asean_country["confirmed_cases"]>0][["confirmed_cases","geo_id","country_name"]]
    print(first_case.head(1))


# %%
df_covid_denormalized_asean.info()


# %%
#Kasus Covid-19 di ASEAN mulai Bulan Maret 2020
df_covid_denormalized_asean_march_onward = df_covid_denormalized_asean[df_covid_denormalized_asean.index>="2020-03-01"]
print(df_covid_denormalized_asean_march_onward.head())


# %%
df_covid_denormalized_asean_march_onward.head()


# %%
df_covid_denormalized_asean_march_onward['date'] = df_covid_denormalized_asean_march_onward.index.date


# %%
df_covid_denormalized_asean_march_onward = df_covid_denormalized_asean_march_onward.reset_index(drop=True)
df_covid_denormalized_asean_march_onward.head()


# %%
#Visualisasi Kasus COVID-19 di ASEAN
import seaborn as sns
plt.figure(figsize=(16,6))
sns.lineplot(data=df_covid_denormalized_asean_march_onward, 
             x=df_covid_denormalized_asean_march_onward['date'], 
             y="confirmed_cases", 
             hue="country_name",
             linewidth=2)
plt.xlabel('Record Date', fontsize=14)
plt.ylabel('Total Cases', fontsize=14)
plt.title('Comparison of COVID19 Cases in 5 ASEAN Countries', color="b", fontsize=18)
plt.grid()
plt.tight_layout()
plt.show()


