import pandas as pd
df =pd.read_csv("D:\\Project Data\\customer_shopping_behavior.csv")
df.info()
df.describe()
df.isnull().sum()
df['Review Rating']=df.groupby('Category')['Review Rating'].transform(lambda x: x.fillna(x.median()))
df.isnull().sum()
df.columns=df.columns.str.lower()
df.columns=df.columns.str.replace(' ','_')
df=df.rename(columns={'purchase_amount_(usd)':'purchase_amount'})
labels=['Young Adult','Adult','Middle-aged','Senior']
df['age_group']=pd.qcut(df['age'],q=4,labels=labels)
df[['age','age_group']].head()
frequency_mapping={
    'Fortnightly':14,
    'Weekly':7,
    'Monthly':30,
    'Quarterly':90,
    'Annually':365,
    'Bi-Weekly':14,
    'Every 3 Months':90
}
df['purchase_frequency_days']=df['frequency_of_purchases'].map(frequency_mapping)
df[['purchase_frequency_days','frequency_of_purchases']].head(10)
df[['discount_applied','promo_code_used']].head(10)
(df['discount_applied'] == df['promo_code_used']).all()
df=df.drop('promo_code_used',axis=1)

from sqlalchemy import create_engine
import psycopg2
#step 1: Connect to PostgreSql
#Replace placeholder with your actual details
username="postgres"
password="password"
host="localhost"
port="5432"
database="customer_behavior"
engine=create_engine(f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{database}")

#Step2 :Load DataFrame into PostfreSQL
table_name="customer" #choose any table name
df.to_sql(table_name,engine,if_exists='replace',index=False)
print(f"Data Sucessfully loaded into Table '{table_name}' in database '{database}'.")
