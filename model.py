
from sklearn.linear_model import LassoCV
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import LabelEncoder
import pandas as pd

# Charger les données
data = pd.read_csv('./dataset/clean_data.csv')


def encodage_categorical_for_models(df):
    """
    Encodage des colonnes catégorielles d'un DataFrame pour le machine learning.

    Arguments:
    - df : DataFrame - Le DataFrame contenant les données à encoder.

    Retourne:
    - DataFrame - Le DataFrame avec les colonnes catégorielles encodées.
    """
    df_encodage = df.copy()  # Copie du DataFrame original
    label_encoder = LabelEncoder()  # Créer une instance du LabelEncoder

    # Parcourir toutes les colonnes du DataFrame
    for colonne in df_encodage.columns:
        # Vérifier si la colonne est de type objet
        if df_encodage[colonne].dtype == 'object':
            df_encodage[colonne] = label_encoder.fit_transform(
                df_encodage[colonne].astype(str))  # Encodage de la colonne
        # Vérifier si la colonne est de type float
        elif df_encodage[colonne].dtype == 'float64':
            df_encodage[colonne] = df_encodage[colonne].fillna(0).astype(
                int)  # Remplacer les valeurs nulles par 0 et convertir en int
        # Vérifier si la colonne est de type int
        elif df_encodage[colonne].dtype == 'int64':
            df_encodage[colonne] = df_encodage[colonne].fillna(0)
        else:
            df_encodage[colonne] = label_encoder.fit_transform(
                df_encodage[colonne].astype(str))
    return df_encodage


# colonnes non-necessaire ou en doublon
columns_to_delete = ['Type de voie', 'Code voie', 'Voie', 'Type local']

# on supprime les doublons
data.drop_duplicates(inplace=True)
data['Prix au m2'] = data['Valeur fonciere'] / data['Surface reelle bati']
# Supprimer les colonnes du DataFrame
data_copy_encoded = data.drop(columns=columns_to_delete)


# on recheck les caractéristiques de notre jeu de données
print(data_copy_encoded.info())
print(data_copy_encoded.isnull().sum())
print(data_copy_encoded.head())
print(data_copy_encoded.info())

# Nettoyage et encodage des données catégorielles
data_copy_encoded = encodage_categorical_for_models(data_copy_encoded)
colonnes_gardees = ['Prix au m2', 'Date mutation', 'Code postal', 'Code commune', 'Valeur fonciere',
                    'Année mutation', 'Surface reelle bati', 'Nombre pieces principales', 'Surface terrain']

data_copy_encoded = data_copy_encoded.loc[:, colonnes_gardees]
print(data_copy_encoded.info())


# Diviser les données en ensembles d'entraînement et de test
y = data_copy_encoded['Prix au m2']
X = data_copy_encoded.drop(columns=['Prix au m2'])
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33)

# Appliquer la mise à l'échelle MinMaxScaler sur les données d'entraînement
scaler = MinMaxScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Créer le modèle de régression linéaire
regression_model = LinearRegression()

# Obtention des scores de validation croisée sur les données d'entraînement
scores = cross_val_score(regression_model, X_train_scaled,
                         y_train, cv=5, scoring='neg_mean_squared_error')

# Conversion des scores en valeurs positives et calcul de la racine carrée de l'erreur quadratique moyenne (RMSE)
rmse_scores = np.sqrt(-scores)

# Entraîner le modèle sur les données d'entraînement
regression_model.fit(X_train_scaled, y_train)

# Calculer le coefficient de détermination (R²) sur les données de test
r2_score = regression_model.score(X_test_scaled, y_test)


# Affichage des scores
print("Scores de validation croisée (RMSE) : ", rmse_scores)
print("RMSE moyen : ", rmse_scores.mean())
print("Coefficient de détermination (R²) :", r2_score)


# Création d'un modèle de régression linéaire avec régularisation L1 (Lasso)
lasso_model = LassoCV(cv=5)

# Entraînement du modèle sur les données
lasso_model.fit(X, y)

# Obtention des caractéristiques les plus importantes
important_features = X.columns[lasso_model.coef_ != 0]

# Affichage des caractéristiques sélectionnées
print("Caractéristiques sélectionnées :", important_features)
