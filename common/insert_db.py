import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_CONFIG = {
    'user' : os.getenv('DATABASE_USER'),
    'password' : os.getenv('DATABASE_PASSWORD'),
    'host' : os.getenv('DATABASE_HOST'),
    'port' : os.getenv('DATABASE_PORT'),
    'database' : os.getenv('DATABASE_NAME')
}

df_faq = pd.read_csv("kia_faq_data.csv")
df_long = pd.read_excel("./data/src/자동차_등록_현황_edit.xlsx")
df_add_by_region =  pd.read_excel("./data/src/면적_당_전기차_증가량_db화.xlsx")
df_register_by_region =  pd.read_excel("./data/src/면적_당_등록수_db화.xlsx")
df_add_by_region["month"] = pd.to_datetime(df_add_by_region["month"] + "-01")

df_cal = pd.read_excel("./data/src/면적_당_연산_db.xlsx")
df_fire= pd.read_excel("./data/src/면적_당_화재발생_db.xlsx")
df_charge_db = pd.read_excel("./data/src/면적_당_전기차_충전소_db.xlsx")

df_population_db = pd.read_csv("./data/src/df_population_db.csv")
df_vehicle_db= pd.read_csv("./data/src/df_vehicle_db.csv")
df_total_db = pd.read_csv("./data/src/df_total_db.csv")
df_industry_db = pd.read_csv("./data/src/df_industry_db.csv")
df_income_db= pd.read_csv("./data/src/df_income_db.csv")



db_url = f"mysql+pymysql://{DATABASE_CONFIG['user']}:{DATABASE_CONFIG['password']}@{DATABASE_CONFIG['host']}:{DATABASE_CONFIG['port']}/{DATABASE_CONFIG['database']}?charset=utf8mb4"

con = create_engine(db_url, echo=False)

df_add_by_region.to_sql('add_electricity_car', con=con, if_exists='append', index=False)
df_register_by_region.to_sql('register_electricity_car', con=con, if_exists='append', index=False)
df_cal['cnt_popul'] = df_cal['cnt_popul'].round(2)


df_cal.to_sql('cal_by_region', con=con, if_exists='append', index=False)
df_fire.to_sql('fire_per', con=con, if_exists='append', index=False)
df_charge_db.to_sql('charge_by_region', con=con, if_exists='append', index=False)


df_population_db.to_sql('population_tb', con=con, if_exists='append', index=False)
df_vehicle_db.to_sql('vehicle_tb', con=con, if_exists='append', index=False)
df_total_db.to_sql('total_tb', con=con, if_exists='append', index=False)
df_industry_db.to_sql('industry_tb', con=con, if_exists='append', index=False)
df_income_db.to_sql('income_tb', con=con, if_exists='append', index=False)
