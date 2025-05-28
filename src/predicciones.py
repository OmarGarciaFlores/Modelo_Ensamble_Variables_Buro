
import pandas as pd
import joblib
import os

# === Cargar base y catálogos ===
df_buro = pd.read_csv('../data/df_buro_performance.csv')

catalogos = {
    "revolving": pd.read_csv('../data/revolving.csv'),
    "installment": pd.read_csv('../data/installment.csv'),
    "credit_activity": pd.read_csv('../data/credit_activity.csv'),
    "delinquency": pd.read_csv('../data/delinquency.csv'),
    "credit_utilization": pd.read_csv('../data/credit_utilization.csv')
}

# Crear datasets por categoría
dataframes = {
    nombre: df_buro[catalogo['Variable']]
    for nombre, catalogo in catalogos.items()
}

# Crear base de predicciones con columnas clave
df_predicciones = df_buro[["CLIENTEID", "MES_INFORMACION", "EVER30_12M"]].copy()

# Predicción por modelo
for nombre, df_vars in dataframes.items():
    modelo_path = os.path.join("..", "modelos", f"modelo_{nombre}.sav")
    modelo = joblib.load(modelo_path)

    X = df_vars.copy()
    X = X.reindex(columns=modelo.get_booster().feature_names)

    df_predicciones[f"pred_{nombre}"] = modelo.predict_proba(X)[:, 1]

# Ensamble
X_ensamble = df_predicciones[[col for col in df_predicciones.columns if col.startswith("pred_")]]
ensemble_model = joblib.load(os.path.join("..", "modelos", "modelo_ensamble.sav"))
df_predicciones["pred_ensamble"] = ensemble_model.predict_proba(X_ensamble)[:, 1]

# Crear ID_UNICO
df_predicciones["ID_UNICO"] = df_predicciones["CLIENTEID"].astype(str) + "_" + df_predicciones["MES_INFORMACION"].astype(str)

# Reordenar columnas
cols = ["ID_UNICO", "CLIENTEID", "MES_INFORMACION", "EVER30_12M"] + [col for col in df_predicciones.columns if col.startswith("pred_")]
df_predicciones = df_predicciones[cols]

# Exportar con el nuevo orden
df_predicciones.to_csv("../data/predicciones.csv", index=False)
