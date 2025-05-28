
# Análisis de Riesgo de Crédito con Variables de Buró

Este proyecto desarrolla una arquitectura integral para evaluar el **riesgo crediticio** a partir de variables de buró de crédito, utilizando técnicas de machine learning avanzadas como **XGBoost** y un modelo **ensamble**, todo desplegado en un ecosistema basado en **AWS** y **BigQuery**. El resultado es un sistema escalable que permite predicciones automatizadas y visualización continua del riesgo mediante **Looker Studio**.


## Objetivo del Proyecto

Anticipar el **riesgo de incumplimiento crediticio** mediante modelos predictivos construidos sobre más de 180 variables de buró y comportamiento histórico. Esto permitirá a la institución:

- Tomar mejores decisiones de originación.
- Optimizar estrategias de cobranza.
- Detectar tendencias de deterioro en el portafolio.
- Visualizar el riesgo de forma dinámica y granular.


# Estructura del Proyecto

.
├── credenciales.json
├── data
│   ├── catalogo.csv
│   ├── columnas_buro.csv
│   ├── credit_activity.csv
│   ├── credit_utilization.csv
│   ├── delinquency.csv
│   ├── installment.csv
│   ├── predicciones.csv
│   └── revolving.csv
├── modelos
│   ├── modelo_credit_activity.sav
│   ├── modelo_credit_utilization.sav
│   ├── modelo_delinquency.sav
│   ├── modelo_ensamble.sav
│   ├── modelo_installment.sav
│   └── modelo_revolving.sav
├── notebooks
│   └── elt.ipynb
├── Presentacion_v2.pdf
├── README.md
└── src
    ├── bigquery.py
    ├── cargar_bases.py
    ├── creacion_tbls_athena.py
    ├── glue.py
    ├── predicciones.py
    └── transformacion_athena.py

5 directories, 24 files


## Requisitos

```bash
pip install pandas boto3 scikit-learn xgboost joblib pandas-gbq google-auth
```


# Flujo del Proceso


## **Carga de datos en local**

La empresa inicialmente nos dio archivos csv que abarcan de enero 2022 a abril 2025.

Para la actualización de nuevos meses este archivo debe colocarse en la carpeta data y realizar los siguientes pasos.


## **Carga en AWS S3** 

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

## **Métrica de evaluación**: 

Se utiliza la variable binaria Ever30@12M: indica si un cliente se atrasó 30 días en los 12 meses posteriores a la fecha de evaluación.


## **Visualización de resultados**: 

Los resultados se integran en BigQuery y se visualizan en un dashboard interactivo en Looker Studio.


[🔗 Ver dashboard en Looker Studio](https://lookerstudio.google.com/u/0/reporting/5793b497-7407-4b84-b391-28ff9c770300/page/p_7e4glbdwsd/edit)


# Acciones Prácticas del Modelo Ensamble

1. Priorización de Originaciones de Crédito
Selecciona clientes con menor riesgo en renovaciones u ofertas nuevas.

2. Cobranza Diferenciada
Permite diseñar estrategias según el riesgo anticipado de mora.

3. Monitoreo del Portafolio
Detecta cosechas deterioradas o segmentos de mayor exposición.

4. Alertas Tempranas
Proporciona predicciones mensuales para decisiones proactivas.
