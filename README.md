
# Análisis de Riesgo de Crédito con Variables de Buró

Este proyecto implementa una arquitectura para analizar el riesgo crediticio utilizando información de buró, desde la recolección y transformación de datos hasta el entrenamiento y evaluación de modelos predictivos. El flujo está diseñado para integrarse con AWS (S3, Athena, Glue) y herramientas de visualización como Looker Studio.


# Estructura del Proyecto

├── data/ # Archivos CSV de entrada y salida local
├── modelos/ # Modelos entrenados guardados en formato .sav
├── notebooks/ # Notebooks para exploración, entrenamiento y validación
├── src/ # Scripts Python para ETL y automatización
└── README.md


# Flujo del Proceso


## **Carga de datos en local**

La empresa inicialmente nos dio archivos csv que abarcan de enero 2022 a abril 2025.

Para la actualización de nuevos meses este archivo debe colocarse en la carpeta data y realizar los siguientes pasos.


## **Carga en S3** 

Se utiliza el script `cargar_bases.py`

Antes de ejecutarlo considera lo siguiente:

1. Debes cambiar la configuración de tu sesión de S3
2. Debes cambiar el nombre de tu bucket
3. Debes cambiar el nombre de las bases que estas subiendo por el nombre que tenga tu csv

Ejecuta lo siguiente:

```bash
python cargar_bases.py
```

Los datos consolidados se cargan en un bucket S3 (`itam-analytics-ogf`).


## **Creación base de datos en Glue**

En caso de no tener una base de datos en Glue dedicada a este ejercicio se debe ejecutar lo siguiente:

```bash
python glue.py
```


## **Creación de tablas en Athena**

El siguiente script crea las tablas en athena para el siguiente mes

```bash
python creacion_tbls_athena.py
```


## **Transformación de datos**

Se transforma la información en Athena para pegarle el comportamiento a las bases de buro y de esta manera esten practicamente listas para calcular las predicciones.

**Importante** se debe cambiar los meses a evaluar en el query dentro del script `WHERE MES_INFORMACION BETWEEN 202405 AND 202504`

```bash
python transformacion_athena.py
```


## **Predicciones**

Se realizan las predicciones por categoría `installment`, `revolving`, `credit activity`, `credit utilization`, `delinquency` para posteriormente realizar el ensamble.

Ejecuta lo siguiente:

```bash
python predicciones.py
```



https://lookerstudio.google.com/u/0/reporting/5793b497-7407-4b84-b391-28ff9c770300/page/p_7e4glbdwsd/edit




## **Ensamble**: Se construye un modelo ensamble a partir de las predicciones individuales.




## **Evaluación y Visualización**: Los resultados se integran en BigQuery y se visualizan en Looker Studio.



## Requisitos

```bash
pip install pandas boto3 scikit-learn xgboost joblib pandas-gbq google-auth
```

