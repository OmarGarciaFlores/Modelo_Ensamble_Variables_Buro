
import pandas as pd
from pandas_gbq import to_gbq
from google.oauth2 import service_account

# Cargo la base de datos de atributos de cliente
df_atributos = pd.read_csv('../data/atributos_cliente.csv')

# Cargo la base de datos de predicciones
df_predicciones = pd.read_csv('../data/predicciones.csv')

# Reordeno las columnas de la base de predicciones
df_predicciones = df_predicciones[['ID_UNICO', 'CLIENTEID', 'MES_INFORMACION',  'pred_revolving', 'EVER30_12M', 'pred_installment', 'pred_credit_activity', 'pred_delinquency', 'pred_credit_utilization', 'pred_ensamble']]

df_predicciones.rename(columns={"pred_ensamble": "pred_ensemble"}, inplace=True)

# Seleccionar solo las columnas necesarias de df_atributos (para evitar duplicidad innecesaria)
cols_atributos = [
    "CLIENTEID", "DESEMPENIO",
    "TIPOCLIENTE", "VINTAGE", "SEGMENTO_RIESGO", "NOMBRE_SUCURSAL", "REGION"
]

# Hacemos el merge con left join
df_bq = df_predicciones.merge(
    df_atributos[cols_atributos],
    how="left",
    left_on=["CLIENTEID", "MES_INFORMACION"],   
    right_on=["CLIENTEID", "DESEMPENIO"]
)

df_bq.drop(columns=["DESEMPENIO"], inplace=True)



# Configura tu información
project_id = "gen-lang-client-0594597393"
dataset_table = "analisis_buro.predicciones_buro"
path_credenciales = "../credenciales.json"


# Autenticación
credenciales = service_account.Credentials.from_service_account_file(path_credenciales)


# Subir DataFrame
to_gbq(
    dataframe=df_bq,
    destination_table=dataset_table,
    project_id=project_id,
    credentials=credenciales,
    if_exists="append"  # opciones: 'fail', 'replace', 'append'
)


