
import pandas as pd
import boto3  
from botocore.config import Config
import awswrangler as wr

# Configurar la sesión de AWS
my_config = Config(
    region_name = 'us-east-1'
)

session = boto3.Session(profile_name='arquitectura',region_name="us-east-1")

# Transformar la base de datos
query = '''

WITH 
BURO AS (

SELECT CLIENTEID, MES, MES_INFORMACION,
date_add('month', 12, date_parse(CAST(MES_INFORMACION AS VARCHAR), '%Y%m')) AS MES_INFO_12M_AUX,
----------------------------------------------------------------------------------------------------------------------------------
B.Score_1,
----------------------------------------------------------------------------------------------------------------------------------
B.Number_of_trades,                                                           
B.Number_of_trades_opened_in_past_12_months ,                               
B.Number_of_trades_opened_in_past_24_months ,                                 
B.Months_since_oldest_account_opened  ,                                       
B.Months_since_most_recent_account_opened    ,                                
B.Number_of_trades_with_current_balance_balance_greater_than_0    ,           
-----------------------------------------------------------------------------------------------
B.Number_of_bankcard_accounts      ,                                        
B.Number_of_currently_active_bankcard_accounts   ,                            
B.Number_of_bankcard_accounts_opened_in_past_12_months  ,                     
B.Number_of_bankcard_accounts_opened_in_past_24_months  ,                   
B.Months_since_oldest_bankcard_account_opened         ,                       
B.Months_since_most_recent_bankcard_account_opened  ,                         
B.Number_of_bankcard_accounts_with_current_balance_balance_greater_than_0  , 
-----------------------------------------------------------------------------------
B.Number_of_bank_installment_accounts                        ,                
B.Number_of_bank_installment_accounts_opened_in_past_12_months        ,     
B.Number_of_bank_installment_accounts_opened_in_past_24_months       ,        
B.Months_since_oldest_bank_installment_account_opened       ,                 
-----------------------------------------------------------------------------------
B.Number_of_finance_installment_trades                ,                 
B.Number_of_finance_installment_trades_opened_in_past_12_months   ,         
B.Number_of_finance_installment_trades_opened_in_past_24_months   ,           
---------------------------------------------------------------------------------------------------------
B.Months_since_most_recent_activity          ,                                
B.Months_on_file                  ,                                           
---------------------------------------------------------------------------------------------------------
B.Number_of_installment_accounts   ,                                          
B.Number_of_currently_active_installment_trades,                           
B.Number_of_installment_accounts_opened_in_past_12_months ,                  
B.Number_of_installment_accounts_opened_in_past_24_months  ,                  
B.Months_since_oldest_installment_account_opened            ,                 
B.Months_since_most_recent_installment_accounts_opened       ,                
B.Number_of_installment_trades_with_balance_balance_greater_than_0,           
----------------------------------------------------------------------------------------
B.Number_of_mortgage_accounts              ,                                  
B.Number_of_currently_active_mortgage_accounts   ,                          
B.Number_of_mortgage_accounts_opened_in_past_12_months  ,                     
B.Number_of_mortgage_accounts_opened_in_past_24_months  ,                     
B.Months_since_oldest_mortgage_account_opened         ,                       
B.Months_since_most_recent_mortgage_account_opened      ,                    
B.Number_of_mortgage_accounts_with_current_balance_greater_than_0  ,        
------------------------------------------------------------------------------------------
B.Number_of_personal_finance_accounts                                        ,
B.Number_of_currently_active_personal_finance_accounts                       ,
B.Number_of_personal_finance_accounts_opened_in_past_12_months               ,
B.Number_of_personal_finance_accounts_opened_in_past_24_months               ,
B.Months_since_oldest_personal_finance_account_opened                        ,
B.Months_since_most_recent_personal_finance_account_opened                   ,
B.Number_of_personal_finance_trades_with_balance_balance_greater_than_0      ,
------------------------------------------------------------------------------------------
B.Number_of_revolving_accounts                                               ,
B.Number_of_currently_active_revolving_trades                                ,
B.Number_of_revolving_trades_opened_in_past_12_months                        ,
B.Number_of_revolving_trades_opened_in_past_24_months                        ,
B.Months_since_oldest_revolving_account_opened                               ,
B.Months_since_most_recent_revolving_account_opened                          ,
B.Number_of_revolving_trades_with_balance_balance_greater_than_0             ,
------------------------------------------------------------------------------------------
B.Number_of_retail_trades                                                    ,
B.Number_of_currently_active_retail_trades                                   ,
B.Number_of_retail_trades_opened_in_past_12_months                           ,
B.Number_of_retail_trades_opened_in_past_24_months                           ,
B.Months_since_oldest_retail_account_opened                                  ,
B.Months_since_most_recent_retail_account_opened                             ,
B.Number_of_retail_trades_with_current_balance_balance_greater_than_0        ,
---------------------------------------------------------------------------------------------------------
B.Number_of_open_trades                                                           ,
B.Number_of_open_revolving_trades                                                 ,
B.Number_of_accounts_opened_since_the_last_maximum_delinquency_of_60_day_past_due ,
B.Number_of_accounts_opened_since_the_last_charge_off                             ,
---------------------------------------------------------------------------------------------------------
B.Number_of_accounts_with_a_maximum_delinquency_of_60_days_past_due_since_opening_a_new_account_within_the_last_12_months       ,
B.Number_of_accounts_with_a_maximum_delinquency_of_90_days_plus_past_due_since_opening_a_new_account_within_the_last_12_months  ,
B.Number_of_accounts_Charged_Off_since_opening_a_new_account_within_the_last_12_months                                          ,
---------------------------------------------------------------------------------------------------------
B.Number_of_satisfactory_trades                                              ,
B.Number_of_satisfactory_bankcard_accounts                                   ,
B.Number_of_satisfactory_finance_installment_trades                          ,
B.Number_of_satisfactory_mortgage_accounts                                   ,
B.Number_of_satisfactory_revolving_accounts                                  ,
B.Number_of_satisfactory_bank_installment_accounts                           ,
B.Number_of_satisfactory_personal_finance_accounts                           ,
B.Number_of_satisfactory_retail_trades                                       ,
---------------------------------------------------------------------------------------------------------
B.Months_since_most_recent_delinquency                                       ,
B.Months_since_most_recent_bankcard_delinquency                              ,
B.Months_since_most_recent_derogatory_public_record                          ,
B.Months_since_most_recent_mortgage_account_delinquency                      ,
B.Months_since_most_recent_personal_finance_delinquency                      ,
B.Months_since_most_recent_revolving_delinquency                             ,
B.Months_since_most_recent_retail_delinquency                                ,
B.Months_since_most_recent_60_day_or_worse_rating                            ,
B.Months_since_most_recent_90_day_or_worse_rating                            ,
---------------------------------------------------------------------------------------------------------
B.Number_of_charge_offs_within_12_months_CHGOFF12                            ,
B.Highest_collection_amount_owed_in_12_months_COLAMT12                       ,
B.Number_of_collection_inquiries_COLINQ                                      ,
B.Number_of_collections_in_12_months_COLLEC12                                ,
B.Number_of_collections_in_12_months_excluding_medical_collections_COLXMD12  ,
---------------------------------------------------------------------------------------------------------
B.Number_of_30_day_ratings                                                   ,
B.Number_of_60_day_ratings                                                   ,
B.Number_of_90_day_ratings                                                   ,
B.Number_of_120_day_ratings                                                  ,
B.Number_of_30_and_60_day_ratings                                            ,
B.Number_of_30_day_or_worse_ratings                                          ,
B.Number_of_60_day_or_worse_ratings                                          ,
B.Number_of_90_day_or_worse_ratings                                          ,
---------------------------------------------------------------------------------------------------------
B.Number_of_trades_with_maximum_delinquency_02_in_last_3_months              ,
B.Number_of_trades_with_maximum_delinquency_02_in_last_6_months              ,
B.Number_of_trades_with_maximum_delinquency_02_in_last_12_months             ,
B.Number_of_trades_with_maximum_delinquency_02_in_last_24_months             ,
B.Number_of_trades_with_maximum_delinquency_03_in_last_3_months              ,
B.Number_of_trades_with_maximum_delinquency_03_in_last_6_months              ,
B.Number_of_trades_with_maximum_delinquency_03_in_last_12_months             ,
B.Number_of_trades_with_maximum_delinquency_03_in_last_24_months             ,
B.Number_of_trades_with_maximum_delinquency_04_in_last_3_months              ,
B.Number_of_trades_with_maximum_delinquency_04_in_last_6_months              ,
B.Number_of_trades_with_maximum_delinquency_04_in_last_12_months             ,
B.Number_of_trades_with_maximum_delinquency_04_in_last_24_months             ,
---------------------------------------------------------------------------------------------------------
B.Number_of_trades_ever_30_or_more_days_past_due                             ,
B.Number_of_trades_ever_60_or_more_days_past_due                             ,
B.Number_of_trades_ever_90_or_more_days_past_due                             ,
B.Number_of_trades_ever_120_or_more_days_past_due                            ,
---------------------------------------------------------------------------------------------------------
B.Number_of_trades_30_or_more_days_past_due_in_last_3_months                 ,
B.Number_of_trades_30_or_more_days_past_due_in_last_6_months                 ,
B.Number_of_trades_30_or_more_days_past_due_in_last_12_months                ,
B.Number_of_trades_30_or_more_days_past_due_in_last_24_months                ,
B.Number_of_trades_60_or_more_days_past_due_in_last_3_months                 ,
B.Number_of_trades_60_or_more_days_past_due_in_last_6_months                 ,
B.Number_of_trades_60_or_more_days_past_due_in_last_12_months                ,
B.Number_of_trades_60_or_more_days_past_due_in_last_24_months                ,
B.Number_of_trades_90_or_more_days_past_due_in_last_3_months                 ,
B.Number_of_trades_90_or_more_days_past_due_in_last_6_months                 ,
B.Number_of_trades_90_or_more_days_past_due_in_last_12_months                ,
B.Number_of_trades_90_or_more_days_past_due_in_last_24_months                ,
---------------------------------------------------------------------------------------------------------
B.Number_of_trades_currently_past_due_updated_in_past_2_months               ,
B.Number_of_trades_currently_30_days_past_due_updated_in_past_2_months       ,
B.Number_of_trades_currently_60_days_past_due_updated_in_past_2_months       ,
B.Number_of_trades_currently_90_days_past_due_updated_in_past_2_months       ,
B.Number_of_trades_currently_120_days_past_due_updated_in_past_2_months      ,
---------------------------------------------------------------------------------------------------------
B.Percent_of_trades_delinquent                                               ,
B.Total_amount_now_past_due                                                  ,
B.Number_of_derogatory_public_records                                        ,
B.Number_of_public_record_bankruptcies                                       ,
B.Number_of_public_record_and_account_line_derogatory_items_greater_than_100 ,
B.Total_public_record_amounts                                                ,
B.Total_collection_amounts_ever_owed                                         ,
B.Number_of_tax_liens                                                        ,
---------------------------------------------------------------------------------------------------------
B.Total_high_credit_credit_limit                                             ,
B.Total_bankcard_high_credit_credit_limit                                    ,
B.Total_installment_high_credit_credit_limit                                 ,
B.Total_mortgage_high_credit_credit_limit                                    ,
B.Total_personal_finance_high_credit_credit_limit                            ,
B.Total_revolving_high_credit_credit_limit                                   ,
B.Total_retail_high_credit_credit_limit                                      ,
-------------------------------------------------------------------------------------
B.Total_current_balance_of_all_trades                                        ,
B.Total_current_balance_of_all_trades_excluding_mortgage                     ,
B.Total_balance_of_all_bankcard_accounts                                     ,
B.Total_current_balance_of_all_installment_accounts                          ,
B.Total_current_balance_of_all_mortgage_accounts                             ,
B.Total_current_balance_of_all_personal_finance_accounts                     ,
B.Total_current_balance_of_all_revolving_accounts                            ,
B.Total_current_balance_of_all_retail_trades                                 ,
-------------------------------------------------------------------------------------
B.Average_current_balance_of_all_trades                                      ,
B.Average_current_balance_of_all_bankcard_accounts                           ,
B.Average_balance_of_all_installment_trades                                  ,
B.Average_current_balance_of_mortgage_accounts                               ,
B.Average_balance_of_all_personal_finance_trades                             ,
B.Average_current_balance_of_all_revolving_accounts                          ,
B.Average_current_balance_of_all_retail_trades                               ,
-------------------------------------------------------------------------------------
B.Maximum_balance_owed_on_all_bankcard_accounts                              ,
B.Maximum_balance_owed_on_all_finance_installment_trades                     ,
B.Maximum_current_balance_owed_on_all_mortgage_accounts                      ,
B.Maximum_balance_owed_on_all_personal_finance_trades                        ,
B.Maximum_current_balance_owed_on_all_revolving_accounts                     ,
B.Maximum_balance_owed_on_all_retail_trades                                  ,
-------------------------------------------------------------------------------------
B.Highest_retail_high_credit_credit_limit                                    ,
B.Number_of_non_installment_trades_50_of_limit                               ,
B.Total_open_to_buy_on_revolving_bankcards_includes_retail_and_gascards      ,
---------------------------------------------------------------------------------------------------------
B.Percent_of_active_trades_with_current_balance_balance_greater_than_0                         ,
B.Ratio_of_total_current_balance_to_high_credit_credit_limit_for_all_trades                    ,
B.Percentage_of_all_bankcard_accounts_50_of_limit                                              ,
B.Percentage_of_all_bankcard_accounts_75_of_limit                                              ,
B.Ratio_of_total_current_balance_to_high_credit_credit_limit_for_all_bankcard_accounts         ,
B.Ratio_of_total_balance_to_high_credit_credit_limit_for_all_bank_revolving_accounts           ,
B.Ratio_of_total_current_balance_to_high_credit_credit_limit_for_all_installment_accounts      ,
B.Ratio_of_current_balance_to_high_credit_credit_limit_on_mortgage_accounts                    ,
B.Ratio_of_total_current_balance_to_high_credit_credit_limit_for_all_personal_finance_accounts ,
B.Ratio_of_total_current_balance_to_high_credit_credit_limit_for_all_revolving_accounts        ,
B.Ratio_of_total_current_balance_to_high_credit_credit_limit_for_all_retail_trades             ,
---------------------------------------------------------------------------------------------------------
B.Number_of_inquiries                  ,
B.Number_or_inquiries_in_last_6_months ,
B.Months_since_most_recent_inquiry     

FROM analisis_buro.variables_buro B
WHERE MES_INFORMACION BETWEEN 202405 AND 202504
AND Number_of_trades > 0
),

BASE_EVER AS (
SELECT A.CLIENTEID, MES, MES_INFORMACION, 
year(MES_INFO_12M_AUX)*100 + month(MES_INFO_12M_AUX) AS MES_INFO_12, 
IF (SUM(P.OVER30) > 0,1,0) AS EVER30_12M
FROM BURO A
LEFT JOIN analisis_buro.performance  P
  ON A.CLIENTEID = P.CLIENTEID
  AND P.DESEMPENIO BETWEEN A.MES_INFORMACION AND year(MES_INFO_12M_AUX)*100 + month(MES_INFO_12M_AUX)
GROUP BY A.CLIENTEID, A.MES, A.MES_INFORMACION, A.MES_INFO_12M_AUX
)

 SELECT DISTINCT A.*, B.MES_INFO_12, B.EVER30_12M, C.DAYS_OFF
 FROM BURO A
 LEFT JOIN BASE_EVER B
 ON A.CLIENTEID = B.CLIENTEID AND A.MES_INFORMACION = B.MES_INFORMACION
 LEFT JOIN (SELECT CLIENTEID, DESEMPENIO, DAYS_OFF
            FROM analisis_buro.performance ) C
 ON A.CLIENTEID = C.CLIENTEID AND A.MES_INFORMACION = C.DESEMPENIO   
 WHERE C.DAYS_OFF <= 14      
 ORDER BY CLIENTEID, MES
'''

# Obtengo la base de datos transformada
df_buro_performance = wr.athena.read_sql_query(
    query, 
    database="analisis_buro", 
    ctas_approach=False,
    boto3_session=session
)

# Guardo la base de datos en local
df_buro_performance.to_csv("../data/df_buro_performance.csv", index=False)

