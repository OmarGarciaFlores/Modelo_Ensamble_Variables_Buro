
import pandas as pd
import boto3


# Abrir un cliente de S3
session = boto3.Session(profile_name='arquitectura',region_name="us-east-1")
s3 = session.client('s3')

# Nombre del bucket de S3
BUCKET_NAME = "itam-analytics-ogf"

# Cargar las bases de buro
df_buro_2022 = pd.read_csv("../data/BURO_2022.csv")
df_buro_2023 = pd.read_csv("../data/BURO_2023.csv")
df_buro_2024 = pd.read_csv("../data/BURO_2024.csv")
df_buro_2025 = pd.read_csv("../data/BURO_2025.csv")

# Juntar las bases de buro
df_buro = pd.concat([df_buro_2022, df_buro_2023, df_buro_2024, df_buro_2025])

# Guardar la base localmente
df_buro.to_csv("../data/BURO_COMPLETA.csv", index=False)


# Cargo los archivos a S3
s3.upload_file(Filename="../data/BURO_COMPLETA.csv", 
               Bucket=BUCKET_NAME, 
               Key="analisis_variables_buro/db_buro/BURO_COMPLETA.csv")

s3.upload_file(Filename="../data/PERFORMANCE.csv", 
               Bucket=BUCKET_NAME, 
               Key="analisis_variables_buro/db_performance/PERFORMANCE.csv")