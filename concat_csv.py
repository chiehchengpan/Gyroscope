import pandas as pd

f1name = 'data/2019-01-28_20_51_trans.csv'
f2name = 'data/2019-01-29_total.csv'

df = pd.read_csv(f1name, encoding='utf-8')
df1 = pd.read_csv(f2name, encoding='utf-8')

df = pd.concat([df, df1], axis=0, ignore_index=True)

df.to_csv('data/Total_training_data.csv', encoding='utf-8', index=False)
