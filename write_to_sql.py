from time import sleep

import pandas as pd
from sqlalchemy import create_engine, text

sleep(10)
engine = create_engine("postgresql://user:passwd@postgres:5432/testdb")


df1 = pd.read_csv('data1.csv')
df2 = pd.read_csv('data2.csv')
df3 = pd.read_csv('data3.csv')
df = pd.concat([df1, df2, df3])
df = df.drop('Unnamed: 0', axis=1)
df.to_sql('tmp', engine, if_exists='replace')

with engine.connect() as conn:
    res = conn.execute(text('SELECT * FROM tmp'))
    for row in res:
        print(row)