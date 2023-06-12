import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd
import geopandas as gpd
import folium
from streamlit_folium import folium_static


# Page config
st.set_page_config(
    page_title='Real Estates Price in Paris',
    layout='wide',
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    })

# En tete
st.title(
    ':blue[_Real_ _Estates_ _Price_ _in_ _Paris_] :sunglasses:', anchor="custom-title1")
# Définir la taille de police spécifique pour le titre
st.markdown(
    "<style>.custom-title1{font-size: 40px;}</style>", unsafe_allow_html=True)
st.write('This dashboard was created for educational purposes only, and the data used is freely available at www.data-gouv.fr .')
st.write('The different visualizations present on this dashboard, are intended to demonstrate the potential of our data source, and give a first overview of the interest of the data set.')
st.write('Our analysis will focus on Real Estate sale between 2018 to 2022 in Paris.')

# Side bar
with st.sidebar:
    st.header("Informations sur l'auteur")
    st.markdown('**Mohamed AKHMOUCH**')
    st.write('Data Engineer chez CAFPI')
    st.write("""<div style="width:100%;text-align:center;"><a href="https://www.linkedin.com/in/mohamed-akhmouch-b77850199/" style="float:center"><img src="https://img.shields.io/badge/mohamed-akhmouch-b77850199?style=for-the-badge&logo=linkedin&logoColor=white&link=https://www.linkedin.com/in/mohamed-akhmouch-b77850199/%22" width="100%" height="50%"></img></a></div>""", unsafe_allow_html=True)

# Charger les données
data = pd.read_csv('./dataset/clean_data.csv')
data_vente_ile_de_france = pd.read_csv('./dataset/clean_data_vente_idf.csv')

# Définir l'option d'affichage pour afficher toutes les lignes, colonnes
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', None)


# Filter data for Île-de-France
data_ile_de_france = data.copy()

# Filter non-zero values for surface and value
data_ile_de_france = data_ile_de_france[data_ile_de_france['Surface reelle bati'] != 0]
data_ile_de_france = data_ile_de_france[data_ile_de_france['Valeur fonciere'] != 0]

# Calculate average price per square meter per year
average_price_per_m2_per_year = data_ile_de_france.groupby(['Année mutation', 'Type local'])['Valeur fonciere'].median(
) / data_ile_de_france.groupby(['Année mutation', 'Type local'])['Surface reelle bati'].median()

fig, ax = plt.subplots(figsize=(12, 6))

grouped_data = data_ile_de_france.groupby(['Type local', 'Année mutation'])[
    'Valeur fonciere'].median()
# Reset index to access 'Type local' and 'Année mutation' as columns
grouped_data = grouped_data.reset_index()

# Plot each curve
for type_local, group in grouped_data.groupby('Type local'):
    group.plot(x='Année mutation', y='Valeur fonciere',
               marker='o', label=type_local, ax=ax)

# Add labels
for _, row in grouped_data.iterrows():
    type_local = row['Type local']
    year = row['Année mutation']
    price = row['Valeur fonciere']
    label = f"{price:.2f} €"
    ax.annotate(label, (year, price), textcoords="offset points",
                xytext=(0, 10), ha='center')

# Modify x-axis labels
plt.xticks(grouped_data['Année mutation'])

plt.xlabel("Année")
plt.ylabel("Prix moyen au mètre carré")
# Définir la taille de police spécifique pour le titre
st.markdown(
    "<style>.custom-title{font-size: 15px;}</style>", unsafe_allow_html=True)
# Afficher le titre avec la classe personnalisée
st.title("Évolution du prix moyen au mètre carré en Île-de-France",
         anchor='custom-title')

# Show the plot
st.text("Explication du graphique 1 :")
st.markdown("""
Ce graphique montre l'évolution du prix moyen au mètre carré de l'immobilier en Île-de-France au fil des années. 
Chaque point représente le prix moyen par mètre carré pour une année spécifique. Les valeurs sont annotées à côté de chaque point.
""")
st.pyplot(fig)

data_ile_de_france = data[data["Nature mutation"] == "Vente"]

# Convert "Date mutation" to datetime
data_ile_de_france["Date mutation"] = pd.to_datetime(
    data_ile_de_france["Date mutation"])
print(data_ile_de_france["Type local"].unique())
# Define nature mutations
nature_mutations = ['Appartement', 'Maison',
                    'Local industriel. commercial ou assimilé']

# Create the plot
fig, ax = plt.subplots(figsize=(12, 10))

for nature in nature_mutations:
    nature_data = data_ile_de_france[data_ile_de_france["Type local"] == nature]
    nature_data = nature_data.set_index("Date mutation")
    grouped_data = nature_data.resample('A')["No disposition"].count()

    # Check if grouped_data contains at least one value
    if not grouped_data.empty:
        grouped_data.plot(marker='o', label=nature)

        for x, y in zip(grouped_data.index, grouped_data.values):
            label = f"{y}"
            ax.annotate(label, (x, y), textcoords="offset points",
                        xytext=(0, 10), ha='center')

plt.xlabel("Année")
plt.ylabel("Nombre de transactions")
st.title(
    "Évolution des transactions immobilières par nature de mutation en Île-de-France", anchor='custom-title')
st.text("Explication du graphique 2 :")
st.markdown("""
Ce graphique montre l'évolution du nombre de transactions immobilières par type de mutations en Île-de-France au fil des années. 
Chaque point représente le nombre de transaction pour une année spécifique. Les valeurs sont annotées à côté de chaque point.
""")
plt.legend()
plt.grid(True)

# Show the plot
st.pyplot(fig)


# Create the plot for monthly median prices
fig2, ax2 = plt.subplots(figsize=(12, 10))
data_vente_ile_de_france = data_ile_de_france.set_index("Date mutation")
monthly_median_prices = data_vente_ile_de_france.resample(
    'M')["Valeur fonciere"].median()
monthly_median_prices.plot(marker='o')

plt.xlabel("Mois")
plt.ylabel("Valeur foncière médiane")
st.title("Évolution des valeurs foncières médianes par mois en Île-de-France",
         anchor="custom-title")
st.text("Explication du graphique 3 :")
st.markdown("""
Ce graphique montre l'évolution du prix médian des valeurs foncières de l'immobilier en Île-de-France au fil des mois.
Chaque point représente le prix médian de vente pour un mois spécifique. Les valeurs sont annotées à côté de chaque point. 
On constate que le vente en l'état futur d'achèvement à bien diminué principalement pour 2 raisons l'augmentation progressive 
des taux qui prive les ménages d'un pouvoir d'achat conséquent, mais surtout la guerre en Ukraine ajouté à l'inflation qui augmente 
le coût de matières premières ce qui augmente les coûts de construction
""")
plt.grid(True)

# Show the plot for monthly median prices
st.pyplot(fig2)

# Calculate transaction percentages
transaction_counts = data.groupby('Type local')['No disposition'].count()
total_transactions = transaction_counts.sum()
transaction_percentages = transaction_counts / total_transactions * 100

# Filter categories with values greater than 0
filtered_transaction_percentages = transaction_percentages[transaction_percentages > 0]

# Create the bar plot with filtered values
fig, ax = plt.subplots(figsize=(12, 6))
filtered_transaction_percentages.plot(kind='bar')

# Add labels to the bars
for i, value in enumerate(filtered_transaction_percentages):
    ax.annotate(f"{value:.2f}%", (i, value),
                textcoords="offset points", xytext=(0, 10), ha='center')

plt.xlabel("Nature de mutation")
plt.ylabel("Pourcentage de transactions")
st.title(
    "Pourcentage de transactions par nature de mutation en Île-de-France", anchor='custom-title')
st.text("Explication du graphique 4 :")
st.markdown("""
Ce graphique représente la part de chque type de transactions en Île-de-France.
Chaque colonne représente le pourcentage du montant total de chaque type de mutations. Les valeurs sont annotées à côté de chaque point.
""")
plt.grid(True)

# Show the bar plot
st.pyplot(fig)

st.title("Carte des communes en Île-de-France", anchor='custom-title')
st.text("Explication du graphique 5 :")
st.markdown("""
Cette carte montre les communes en Île-de-France avec des marqueurs indiquant le prix médian par mètre carré pour chaque commune.
Les marqueurs sont positionnés sur la carte en fonction de la latitude et de la longitude de chaque commune, et le prix médian par mètre carré est affiché au survol.
""")

# Calculer le prix médian au mètre carré par commune
mediane_price_per_m2_per_department = data_vente_ile_de_france.groupby('Code commune')['Valeur fonciere'].median(
) / data_vente_ile_de_france.groupby('Code commune')['Surface reelle bati'].median()

# Conversion de la série en DataFrame
df_mediane_price_per_m2_per_department = pd.DataFrame({'Code commune': mediane_price_per_m2_per_department.index.astype(
    int), 'Prix median': mediane_price_per_m2_per_department.values})
df_mediane_price_per_m2_per_department['Prix median'] = df_mediane_price_per_m2_per_department['Prix median'].astype(
    int)

# Charger les données géographiques des départements
departements = gpd.read_file('./dataset/communes-departement-region.csv')
# Supprimer les lignes avec une valeur vide dans la colonne 'code_commune'
departements = departements.drop(
    departements[departements['code_commune'] == ''].index)
departements = departements.dropna(subset=['code_commune'])
departements = departements[departements["code_region"] == "11"]
departements['code_commune'] = departements['code_commune'].astype(int)

# Jointure des données des départements avec les prix moyens
departements = departements.merge(
    df_mediane_price_per_m2_per_department, left_on='code_commune', right_on='Code commune', how='right')
# Supprimer les colonnes vides
empty_cols = departements.columns[departements.isnull().all()]
departements.drop(empty_cols, axis=1, inplace=True)

departements = departements.drop(
    departements[departements['latitude'] == ''].index)
departements = departements.drop(
    departements[departements['longitude'] == ''].index)

# Créer une carte centrée sur l'Île-de-France
map_center = [48.8566, 2.3522]
m = folium.Map(location=map_center, zoom_start=13)

# Ajouter les marqueurs pour chaque commune
for _, row in departements.iterrows():
    commune = row['nom_commune_postal']
    prix_median = row['Prix median']
    latitude = float(row['latitude'])
    longitude = float(row['longitude'])

    # Créer une info-bulle avec le nom de la commune et le prix médian
    popup_text = f"Commune : {commune}<br>Prix médian m2 : {prix_median}"

    # Ajouter un marqueur à la carte
    folium.Marker(
        location=[latitude, longitude],
        popup=folium.Popup(popup_text, max_width=250),
        icon=folium.Icon(color='green', icon='tint', prefix='fa')
    ).add_to(m)

# Afficher la carte
folium_static(m)
