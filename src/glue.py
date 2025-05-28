import boto3
from botocore.config import Config

# Configurar la sesión de AWS
my_config = Config(
    region_name = 'us-east-1'
)

session = boto3.Session(profile_name='arquitectura',region_name="us-east-1")

glue = boto3.client('glue', config=my_config)

# Crear la base de datos
response = glue.create_database(
    DatabaseInput={
        'Name': 'analisis_buro',
        'Description': 'Variables de buro de credito e indicadores de performance',
    },
)
response

